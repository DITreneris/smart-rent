"""
API for ML-based code quality prediction system.
Provides endpoints for quality predictions, vulnerability detection, and performance assessments.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException, Depends, Query, Body, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
import uvicorn
from fastapi.security import APIKeyHeader

import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import CONFIG
from model.prediction import CombinedPredictor, QualityPredictor, VulnerabilityPredictor, PerformancePredictor

# Set up logging
logging.basicConfig(
    level=getattr(logging, CONFIG["logging"]["level"]),
    format=CONFIG["logging"]["format"],
    handlers=[
        logging.FileHandler(CONFIG["logging"]["file"]),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("api")

# Initialize FastAPI app
app = FastAPI(
    title="Code Quality Prediction API",
    description="API for predicting code quality, vulnerabilities, and performance",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CONFIG["api"]["cors_origins"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API security if enabled
if CONFIG["api"]["require_auth"]:
    API_KEY_NAME = "X-API-Key"
    api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
    
    async def get_api_key(api_key_header: str = Depends(api_key_header)):
        if api_key_header != CONFIG["api"]["api_key"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API Key",
            )
        return api_key_header
    
    # Add security dependency
    security_dependency = Depends(get_api_key)
else:
    # No security
    security_dependency = None


# Initialize predictors
combined_predictor = CombinedPredictor()


# Pydantic models for request and response validation
class CodeInput(BaseModel):
    """Code input for prediction."""
    code: str = Field(..., description="The source code to analyze")
    language: str = Field(..., description="Programming language of the code")
    file_path: Optional[str] = Field(None, description="Path of the file (optional)")
    repository: Optional[str] = Field(None, description="Repository name (optional)")
    
    @validator('language')
    def language_must_be_supported(cls, v):
        supported_languages = [
            "python", "javascript", "typescript", "java", "csharp", "cpp", 
            "go", "rust", "php", "ruby", "swift", "kotlin"
        ]
        if v.lower() not in supported_languages:
            raise ValueError(f"Language must be one of: {', '.join(supported_languages)}")
        return v.lower()


class FeatureInput(BaseModel):
    """Pre-extracted feature input for prediction."""
    features: Dict[str, float] = Field(..., description="Pre-extracted features for prediction")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class PredictionResponse(BaseModel):
    """Standard prediction response model."""
    timestamp: str = Field(..., description="Timestamp of the prediction")
    input_type: str = Field(..., description="Type of input provided (code or features)")
    predictions: Dict[str, Any] = Field(..., description="Prediction results from enabled models")
    request_id: str = Field(..., description="Unique identifier for the request")


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    models: Dict[str, bool] = Field(..., description="Status of each prediction model")
    timestamp: str = Field(..., description="Timestamp of the health check")


# Request ID middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Add request ID to each request for tracking."""
    request_id = datetime.now().strftime("%Y%m%d%H%M%S") + "-" + os.urandom(4).hex()
    request.state.request_id = request_id
    response = await call_next(request)
    return response


# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check the health of the prediction service."""
    logger.info("Health check requested")
    
    # Check which models are loaded
    models_status = {
        "quality_prediction": "quality" in combined_predictor.predictors,
        "vulnerability_detection": "vulnerability" in combined_predictor.predictors,
        "performance_prediction": "performance" in combined_predictor.predictors
    }
    
    return {
        "status": "healthy",
        "version": "1.0.0",
        "models": models_status,
        "timestamp": datetime.now().isoformat()
    }


# Code-based prediction endpoint
@app.post("/predict/code", response_model=PredictionResponse, dependencies=[security_dependency] if security_dependency else [])
async def predict_from_code(code_input: CodeInput, request: Request):
    """Make predictions based on source code."""
    logger.info(f"Code prediction requested for {code_input.language} file")
    
    # Extract features from code
    # This would typically call a feature extraction service or module
    # For now, we'll simulate with basic features
    try:
        features = _extract_features_from_code(code_input.code, code_input.language)
        
        # Create dataframe from features
        data = pd.DataFrame([features])
        
        # Make predictions
        predictions = combined_predictor.predict_all(data)
        
        # Format response
        response = {
            "timestamp": datetime.now().isoformat(),
            "input_type": "code",
            "predictions": predictions["predictions"],
            "request_id": request.state.request_id
        }
        
        return response
    except Exception as e:
        logger.error(f"Error in code prediction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


# Pre-extracted feature-based prediction endpoint
@app.post("/predict/features", response_model=PredictionResponse, dependencies=[security_dependency] if security_dependency else [])
async def predict_from_features(feature_input: FeatureInput, request: Request):
    """Make predictions based on pre-extracted features."""
    logger.info("Feature-based prediction requested")
    
    try:
        # Convert features to dataframe
        data = pd.DataFrame([feature_input.features])
        
        # Make predictions
        predictions = combined_predictor.predict_all(data)
        
        # Format response
        response = {
            "timestamp": datetime.now().isoformat(),
            "input_type": "features",
            "predictions": predictions["predictions"],
            "request_id": request.state.request_id
        }
        
        return response
    except Exception as e:
        logger.error(f"Error in feature prediction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


# Batch prediction endpoint
@app.post("/predict/batch", dependencies=[security_dependency] if security_dependency else [])
async def batch_predict(inputs: List[Union[CodeInput, FeatureInput]], request: Request):
    """Process batch prediction requests."""
    logger.info(f"Batch prediction requested with {len(inputs)} items")
    
    results = []
    errors = []
    
    for i, input_item in enumerate(inputs):
        try:
            # Determine input type
            if hasattr(input_item, "code") and hasattr(input_item, "language"):
                # Code input
                features = _extract_features_from_code(input_item.code, input_item.language)
                data = pd.DataFrame([features])
                input_type = "code"
            elif hasattr(input_item, "features"):
                # Feature input
                data = pd.DataFrame([input_item.features])
                input_type = "features"
            else:
                errors.append({"index": i, "error": "Unknown input type"})
                continue
            
            # Make predictions
            predictions = combined_predictor.predict_all(data)
            
            # Format result
            result = {
                "index": i,
                "timestamp": datetime.now().isoformat(),
                "input_type": input_type,
                "predictions": predictions["predictions"]
            }
            results.append(result)
            
        except Exception as e:
            logger.error(f"Error in batch item {i}: {e}")
            errors.append({"index": i, "error": str(e)})
    
    response = {
        "request_id": request.state.request_id,
        "results": results,
        "errors": errors,
        "total": len(inputs),
        "successful": len(results),
        "failed": len(errors)
    }
    
    return response


# Model-specific endpoints
@app.post("/predict/quality", dependencies=[security_dependency] if security_dependency else [])
async def predict_quality(code_input: CodeInput, request: Request):
    """Make quality predictions for code."""
    logger.info(f"Quality prediction requested for {code_input.language} file")
    
    if "quality" not in combined_predictor.predictors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quality prediction model not available"
        )
    
    try:
        # Extract features
        features = _extract_features_from_code(code_input.code, code_input.language)
        data = pd.DataFrame([features])
        
        # Make prediction
        predictor = combined_predictor.predictors["quality"]
        prediction = predictor.predict(data)
        
        response = {
            "timestamp": datetime.now().isoformat(),
            "quality_prediction": prediction,
            "request_id": request.state.request_id
        }
        
        return response
    except Exception as e:
        logger.error(f"Error in quality prediction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Quality prediction failed: {str(e)}"
        )


@app.post("/predict/vulnerability", dependencies=[security_dependency] if security_dependency else [])
async def predict_vulnerability(code_input: CodeInput, request: Request):
    """Detect vulnerabilities in code."""
    logger.info(f"Vulnerability prediction requested for {code_input.language} file")
    
    if "vulnerability" not in combined_predictor.predictors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vulnerability detection model not available"
        )
    
    try:
        # Extract features
        features = _extract_features_from_code(code_input.code, code_input.language)
        data = pd.DataFrame([features])
        
        # Make prediction
        predictor = combined_predictor.predictors["vulnerability"]
        prediction = predictor.predict(data)
        
        response = {
            "timestamp": datetime.now().isoformat(),
            "vulnerability_prediction": prediction,
            "request_id": request.state.request_id
        }
        
        return response
    except Exception as e:
        logger.error(f"Error in vulnerability prediction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Vulnerability prediction failed: {str(e)}"
        )


@app.post("/predict/performance", dependencies=[security_dependency] if security_dependency else [])
async def predict_performance(code_input: CodeInput, request: Request):
    """Predict performance characteristics of code."""
    logger.info(f"Performance prediction requested for {code_input.language} file")
    
    if "performance" not in combined_predictor.predictors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Performance prediction model not available"
        )
    
    try:
        # Extract features
        features = _extract_features_from_code(code_input.code, code_input.language)
        data = pd.DataFrame([features])
        
        # Make prediction
        predictor = combined_predictor.predictors["performance"]
        prediction = predictor.predict(data)
        
        response = {
            "timestamp": datetime.now().isoformat(),
            "performance_prediction": prediction,
            "request_id": request.state.request_id
        }
        
        return response
    except Exception as e:
        logger.error(f"Error in performance prediction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Performance prediction failed: {str(e)}"
        )


# Feature extraction utility function
def _extract_features_from_code(code: str, language: str) -> Dict[str, float]:
    """Extract features from code for prediction (placeholder implementation)."""
    # This is a placeholder implementation
    # In a real system, this would call a feature extraction module
    
    # Simple metrics that might correlate with quality/performance
    features = {
        # Code size metrics
        "code_length": len(code),
        "line_count": code.count("\n") + 1,
        "char_per_line": len(code) / (code.count("\n") + 1) if code.count("\n") + 1 > 0 else 0,
        
        # Potential indicators of complexity
        "comment_ratio": code.count("#") / len(code) if len(code) > 0 else 0,
        "function_count": code.count("def ") if language == "python" else code.count("function "),
        "class_count": code.count("class "),
        "loop_count": code.count("for ") + code.count("while "),
        "condition_count": code.count("if ") + code.count("else ") + code.count("elif "),
        "nested_count": code.count("    " + "if") + code.count("    " + "for") + code.count("    " + "while"),
        
        # Potential indicators of maintainability
        "max_line_length": max([len(line) for line in code.split("\n")]) if code.split("\n") else 0,
        "avg_name_length": _avg_identifier_length(code),
        
        # Language-specific features
        "language_" + language: 1.0
    }
    
    return features


def _avg_identifier_length(code: str) -> float:
    """Calculate average identifier length (simplistic implementation)."""
    words = code.split()
    identifier_lengths = [len(word) for word in words if word.isalnum() and not word.isdigit()]
    if identifier_lengths:
        return sum(identifier_lengths) / len(identifier_lengths)
    return 0


# Error handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "request_id": getattr(request.state, "request_id", "unknown")}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "request_id": getattr(request.state, "request_id", "unknown")
        }
    )


def start():
    """Start the API server."""
    host = CONFIG["api"]["host"]
    port = CONFIG["api"]["port"]
    debug = CONFIG["api"]["debug"]
    
    logger.info(f"Starting API server on {host}:{port}")
    uvicorn.run("app:app", host=host, port=port, reload=debug, log_level="info")


if __name__ == "__main__":
    start() 