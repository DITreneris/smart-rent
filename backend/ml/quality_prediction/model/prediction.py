"""
Prediction module for ML-based code quality prediction system.
"""

import os
import json
import logging
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple
import pickle
from datetime import datetime
import joblib

import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import CONFIG, MODELS_DIR

# Set up logging
logging.basicConfig(
    level=getattr(logging, CONFIG["logging"]["level"]),
    format=CONFIG["logging"]["format"],
    handlers=[
        logging.FileHandler(CONFIG["logging"]["file"]),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("prediction")


class Predictor:
    """Base class for model prediction."""
    
    def __init__(self, model_name: str):
        """Initialize predictor with model name."""
        self.model_name = model_name
        self.model_dir = Path(MODELS_DIR) / model_name
        self.model = None
        self.feature_columns = []
        self._load_model()
        self._load_feature_columns()
    
    def _load_model(self) -> None:
        """Load the latest trained model."""
        model_path = self.model_dir / "latest.pkl"
        
        if not model_path.exists():
            logger.error(f"Model file not found: {model_path}")
            return
        
        try:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            logger.info(f"Loaded model from {model_path}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
    
    def _load_feature_columns(self) -> None:
        """Load the feature columns used for training."""
        columns_path = self.model_dir / "feature_columns.json"
        
        if not columns_path.exists():
            logger.error(f"Feature columns file not found: {columns_path}")
            return
        
        try:
            with open(columns_path, 'r') as f:
                self.feature_columns = json.load(f)
            logger.info(f"Loaded {len(self.feature_columns)} feature columns")
        except Exception as e:
            logger.error(f"Error loading feature columns: {e}")
    
    def prepare_input(self, data: pd.DataFrame) -> np.ndarray:
        """Prepare input data for prediction."""
        if data.empty:
            logger.error("Empty data provided for prediction")
            return np.array([])
        
        if not self.feature_columns:
            logger.error("No feature columns available")
            return np.array([])
        
        # Extract only the columns used during training
        available_columns = [col for col in self.feature_columns if col in data.columns]
        missing_columns = [col for col in self.feature_columns if col not in data.columns]
        
        if missing_columns:
            logger.warning(f"Missing {len(missing_columns)} columns in input data: {missing_columns[:5]}...")
        
        if not available_columns:
            logger.error("No valid feature columns in input data")
            return np.array([])
        
        # Use available columns and fill missing ones with zeros
        X = data[available_columns].copy()
        
        # Add missing columns as zero-filled
        for col in missing_columns:
            X[col] = 0
        
        # Ensure columns are in the same order as during training
        X = X[self.feature_columns]
        
        # Convert to numpy array
        return X.values
    
    def predict(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Make predictions on input data."""
        if self.model is None:
            logger.error("No model loaded for prediction")
            return {"error": "Model not loaded"}
        
        # Prepare input
        X = self.prepare_input(data)
        if len(X) == 0:
            logger.error("Failed to prepare input data for prediction")
            return {"error": "Failed to prepare input data"}
        
        # Make prediction
        try:
            prediction = self._predict(X)
            return prediction
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            return {"error": str(e)}
    
    def _predict(self, X: np.ndarray) -> Dict[str, Any]:
        """Make model-specific predictions."""
        raise NotImplementedError("Subclasses must implement _predict()")


class QualityPredictor(Predictor):
    """Predictor for code quality model."""
    
    def __init__(self):
        """Initialize quality predictor."""
        super().__init__("quality_prediction")
        self.quality_thresholds = CONFIG["model"]["quality_prediction"].get("thresholds", {
            "high": 0.8,
            "medium": 0.5,
            "low": 0.2
        })
    
    def _predict(self, X: np.ndarray) -> Dict[str, Any]:
        """Make quality predictions."""
        logger.info(f"Making quality predictions for {len(X)} samples")
        
        # Get raw predictions
        try:
            # Get probability predictions if available
            if hasattr(self.model, 'predict_proba'):
                y_prob = self.model.predict_proba(X)
                # Assume binary classification for now (0: low quality, 1: high quality)
                quality_scores = y_prob[:, 1]
            else:
                # Fall back to regular prediction (likely 0 or 1 for classification)
                y_pred = self.model.predict(X)
                quality_scores = y_pred
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            return {"error": str(e)}
        
        # Determine quality levels
        quality_levels = []
        for score in quality_scores:
            if score >= self.quality_thresholds["high"]:
                quality_levels.append("high")
            elif score >= self.quality_thresholds["medium"]:
                quality_levels.append("medium")
            elif score >= self.quality_thresholds["low"]:
                quality_levels.append("low")
            else:
                quality_levels.append("very low")
        
        # Create result object
        results = {
            "quality_scores": quality_scores.tolist(),
            "quality_levels": quality_levels,
            "timestamp": datetime.now().isoformat()
        }
        
        return results


class VulnerabilityPredictor(Predictor):
    """Predictor for vulnerability detection model."""
    
    def __init__(self):
        """Initialize vulnerability predictor."""
        super().__init__("vulnerability_detection")
        self.vulnerability_thresholds = CONFIG["model"]["vulnerability_detection"].get("thresholds", {
            "high": 0.7,
            "medium": 0.4,
            "low": 0.2
        })
    
    def _predict(self, X: np.ndarray) -> Dict[str, Any]:
        """Make vulnerability predictions."""
        logger.info(f"Making vulnerability predictions for {len(X)} samples")
        
        # Get raw predictions
        try:
            # Check if this is a LightGBM Booster
            if hasattr(self.model, 'predict'):
                # LightGBM booster
                y_prob = self.model.predict(X)
            elif hasattr(self.model, 'predict_proba'):
                # Scikit-learn classifier with predict_proba
                y_prob = self.model.predict_proba(X)[:, 1]
            else:
                # Fall back to regular prediction
                y_pred = self.model.predict(X)
                y_prob = y_pred
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            return {"error": str(e)}
        
        # Determine vulnerability levels
        vulnerability_levels = []
        for prob in y_prob:
            if prob >= self.vulnerability_thresholds["high"]:
                vulnerability_levels.append("high")
            elif prob >= self.vulnerability_thresholds["medium"]:
                vulnerability_levels.append("medium")
            elif prob >= self.vulnerability_thresholds["low"]:
                vulnerability_levels.append("low")
            else:
                vulnerability_levels.append("very low")
        
        # Create result object
        results = {
            "vulnerability_probabilities": y_prob.tolist() if isinstance(y_prob, np.ndarray) else y_prob,
            "vulnerability_levels": vulnerability_levels,
            "timestamp": datetime.now().isoformat()
        }
        
        return results


class PerformancePredictor(Predictor):
    """Predictor for performance prediction model."""
    
    def __init__(self):
        """Initialize performance predictor."""
        super().__init__("performance_prediction")
        self.performance_thresholds = CONFIG["model"]["performance_prediction"].get("thresholds", {
            "excellent": 90,
            "good": 70,
            "moderate": 50,
            "poor": 30
        })
    
    def _predict(self, X: np.ndarray) -> Dict[str, Any]:
        """Make performance predictions."""
        logger.info(f"Making performance predictions for {len(X)} samples")
        
        # Get raw predictions
        try:
            performance_values = self.model.predict(X)
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            return {"error": str(e)}
        
        # Determine performance levels
        performance_levels = []
        for value in performance_values:
            if value >= self.performance_thresholds["excellent"]:
                performance_levels.append("excellent")
            elif value >= self.performance_thresholds["good"]:
                performance_levels.append("good")
            elif value >= self.performance_thresholds["moderate"]:
                performance_levels.append("moderate")
            elif value >= self.performance_thresholds["poor"]:
                performance_levels.append("poor")
            else:
                performance_levels.append("very poor")
        
        # Create result object
        results = {
            "performance_values": performance_values.tolist() if isinstance(performance_values, np.ndarray) else performance_values,
            "performance_levels": performance_levels,
            "timestamp": datetime.now().isoformat()
        }
        
        return results


class CombinedPredictor:
    """Combined predictor for all models."""
    
    def __init__(self):
        """Initialize all available predictors based on configuration."""
        self.predictors = {}
        
        # Load quality prediction model if enabled
        if CONFIG["model"]["quality_prediction"]["enabled"]:
            try:
                self.predictors["quality"] = QualityPredictor()
                logger.info("Quality predictor initialized")
            except Exception as e:
                logger.error(f"Error initializing quality predictor: {e}")
        
        # Load vulnerability detection model if enabled
        if CONFIG["model"]["vulnerability_detection"]["enabled"]:
            try:
                self.predictors["vulnerability"] = VulnerabilityPredictor()
                logger.info("Vulnerability predictor initialized")
            except Exception as e:
                logger.error(f"Error initializing vulnerability predictor: {e}")
        
        # Load performance prediction model if enabled
        if CONFIG["model"]["performance_prediction"]["enabled"]:
            try:
                self.predictors["performance"] = PerformancePredictor()
                logger.info("Performance predictor initialized")
            except Exception as e:
                logger.error(f"Error initializing performance predictor: {e}")
    
    def predict_all(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Make predictions using all available models."""
        logger.info(f"Making predictions with all models for {len(data)} samples")
        
        if data.empty:
            logger.error("Empty data provided for prediction")
            return {"error": "Empty input data"}
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "input_size": len(data),
            "predictions": {}
        }
        
        # Make predictions with each available model
        for model_type, predictor in self.predictors.items():
            try:
                model_results = predictor.predict(data)
                results["predictions"][model_type] = model_results
            except Exception as e:
                logger.error(f"Error in {model_type} prediction: {e}")
                results["predictions"][model_type] = {"error": str(e)}
        
        return results


def load_prediction_data(file_path: str) -> pd.DataFrame:
    """Load data for prediction from a file."""
    path = Path(file_path)
    
    if not path.exists():
        logger.error(f"Data file does not exist: {path}")
        return pd.DataFrame()
    
    try:
        # Determine file type and load accordingly
        if path.suffix == '.parquet':
            data = pd.read_parquet(path)
        elif path.suffix == '.csv':
            data = pd.read_csv(path)
        elif path.suffix == '.json':
            data = pd.read_json(path)
        else:
            logger.error(f"Unsupported file format: {path.suffix}")
            return pd.DataFrame()
        
        logger.info(f"Loaded {len(data)} records from {path}")
        return data
    except Exception as e:
        logger.error(f"Error loading data from {path}: {e}")
        return pd.DataFrame()


def save_prediction_results(results: Dict[str, Any], output_path: str) -> bool:
    """Save prediction results to a file."""
    path = Path(output_path)
    
    # Create directory if it doesn't exist
    path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(path, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"Saved prediction results to {path}")
        return True
    except Exception as e:
        logger.error(f"Error saving prediction results: {e}")
        return False


def main():
    """Main function for making predictions."""
    logger.info("Starting prediction process")
    
    # Get input and output paths from config
    input_path = CONFIG["prediction"].get("input_path", "data/features/latest.parquet")
    output_path = CONFIG["prediction"].get("output_path", "data/predictions/latest.json")
    
    # Load data
    data = load_prediction_data(input_path)
    if data.empty:
        logger.error("No data available for prediction")
        return
    
    # Initialize predictor
    predictor = CombinedPredictor()
    
    # Make predictions
    results = predictor.predict_all(data)
    
    # Save results
    save_prediction_results(results, output_path)
    
    logger.info("Prediction process completed")


if __name__ == "__main__":
    main() 