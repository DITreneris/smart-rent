#!/usr/bin/env python
"""
Command-line interface for the ML-based code quality prediction system.
Allows users to run data collection, feature extraction, model training, and predictions.
"""

import os
import sys
import logging
import argparse
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add the parent directory to the path
sys.path.append(str(Path(__file__).resolve().parent))
from config import CONFIG, DATA_DIR, MODELS_DIR
from preprocessing.data_collection import main as run_data_collection
from preprocessing.feature_extraction import main as run_feature_extraction
from model.training import main as run_model_training
from model.prediction import main as run_prediction
from api.app import start as start_api

# Set up logging
logging.basicConfig(
    level=getattr(logging, CONFIG["logging"]["level"]),
    format=CONFIG["logging"]["format"],
    handlers=[
        logging.FileHandler(CONFIG["logging"]["file"]),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("cli")


def setup_argparse() -> argparse.ArgumentParser:
    """Set up command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="ML-based code quality prediction system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py collect                   # Run data collection
  python cli.py extract                   # Run feature extraction
  python cli.py train --model quality     # Train quality prediction model
  python cli.py predict                   # Run predictions
  python cli.py api                       # Start the API server
  python cli.py run-all                   # Run all steps in sequence
  python cli.py info                      # Show system information
  python cli.py setup                     # Setup the system (create directories)
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Data collection command
    collect_parser = subparsers.add_parser("collect", help="Run data collection")
    collect_parser.add_argument(
        "--source", 
        choices=["github", "sonarqube", "git", "tests", "all"], 
        default="all",
        help="Data source to collect from (default: all)"
    )
    
    # Feature extraction command
    extract_parser = subparsers.add_parser("extract", help="Run feature extraction")
    extract_parser.add_argument(
        "--input", 
        type=str, 
        help="Input directory with raw data (default: from config)"
    )
    extract_parser.add_argument(
        "--output", 
        type=str, 
        help="Output directory for features (default: from config)"
    )
    
    # Model training command
    train_parser = subparsers.add_parser("train", help="Train prediction models")
    train_parser.add_argument(
        "--model", 
        choices=["quality", "vulnerability", "performance", "all"], 
        default="all",
        help="Model type to train (default: all)"
    )
    
    # Prediction command
    predict_parser = subparsers.add_parser("predict", help="Run predictions")
    predict_parser.add_argument(
        "--input", 
        type=str, 
        help="Input file with features (default: from config)"
    )
    predict_parser.add_argument(
        "--output", 
        type=str, 
        help="Output file for predictions (default: from config)"
    )
    predict_parser.add_argument(
        "--model", 
        choices=["quality", "vulnerability", "performance", "all"], 
        default="all",
        help="Model to use for prediction (default: all)"
    )
    
    # API command
    api_parser = subparsers.add_parser("api", help="Start the API server")
    api_parser.add_argument(
        "--host", 
        type=str, 
        help="API host (default: from config)"
    )
    api_parser.add_argument(
        "--port", 
        type=int, 
        help="API port (default: from config)"
    )
    
    # Run all command
    subparsers.add_parser("run-all", help="Run all steps in sequence")
    
    # Info command
    subparsers.add_parser("info", help="Show system information")
    
    # Setup command
    subparsers.add_parser("setup", help="Setup the system (create directories)")
    
    return parser


def run_collect(args):
    """Run data collection step."""
    logger.info("Starting data collection process")
    
    # In a real implementation, we'd filter sources here based on args.source
    # For now, we just call the main data collection function
    run_data_collection()
    
    logger.info("Data collection completed")


def run_extract(args):
    """Run feature extraction step."""
    logger.info("Starting feature extraction process")
    
    # Update config with command-line arguments if provided
    if args.input:
        CONFIG["data_collection"]["output_path"] = args.input
    if args.output:
        CONFIG["feature_extraction"]["output_path"] = args.output
    
    run_feature_extraction()
    
    logger.info("Feature extraction completed")


def run_train(args):
    """Run model training step."""
    logger.info("Starting model training process")
    
    # Update config based on model selection
    if args.model != "all":
        # Disable all models first
        for model_type in ["quality_prediction", "vulnerability_detection", "performance_prediction"]:
            CONFIG["model"][model_type]["enabled"] = False
        
        # Enable only the selected model
        if args.model == "quality":
            CONFIG["model"]["quality_prediction"]["enabled"] = True
        elif args.model == "vulnerability":
            CONFIG["model"]["vulnerability_detection"]["enabled"] = True
        elif args.model == "performance":
            CONFIG["model"]["performance_prediction"]["enabled"] = True
    
    run_model_training()
    
    logger.info("Model training completed")


def run_predict(args):
    """Run prediction step."""
    logger.info("Starting prediction process")
    
    # Update config with command-line arguments if provided
    if args.input:
        CONFIG["prediction"]["input_path"] = args.input
    if args.output:
        CONFIG["prediction"]["output_path"] = args.output
    
    # Update config based on model selection
    if args.model != "all":
        # Disable all models first
        for model_type in ["quality_prediction", "vulnerability_detection", "performance_prediction"]:
            CONFIG["model"][model_type]["enabled"] = False
        
        # Enable only the selected model
        if args.model == "quality":
            CONFIG["model"]["quality_prediction"]["enabled"] = True
        elif args.model == "vulnerability":
            CONFIG["model"]["vulnerability_detection"]["enabled"] = True
        elif args.model == "performance":
            CONFIG["model"]["performance_prediction"]["enabled"] = True
    
    run_prediction()
    
    logger.info("Prediction process completed")


def run_api(args):
    """Start the API server."""
    logger.info("Starting API server")
    
    # Update config with command-line arguments if provided
    if args.host:
        CONFIG["api"]["host"] = args.host
    if args.port:
        CONFIG["api"]["port"] = args.port
    
    start_api()


def run_all(args):
    """Run all steps in sequence."""
    logger.info("Running all steps in sequence")
    
    logger.info("Step 1: Data collection")
    run_data_collection()
    
    logger.info("Step 2: Feature extraction")
    run_feature_extraction()
    
    logger.info("Step 3: Model training")
    run_model_training()
    
    logger.info("Step 4: Prediction")
    run_prediction()
    
    logger.info("All steps completed")


def show_info(args):
    """Show system information."""
    logger.info("Displaying system information")
    
    # Collect information
    info = {
        "system": {
            "timestamp": datetime.now().isoformat(),
            "config_file": str(Path(__file__).resolve().parent / "config.py"),
            "data_directory": str(DATA_DIR),
            "models_directory": str(MODELS_DIR)
        },
        "models": {}
    }
    
    # Check for trained models
    models_dir = Path(MODELS_DIR)
    for model_type in ["quality_prediction", "vulnerability_detection", "performance_prediction"]:
        model_dir = models_dir / model_type
        latest_model = model_dir / "latest.pkl"
        latest_metrics = model_dir / "latest_metrics.json"
        
        model_info = {
            "directory": str(model_dir),
            "trained": latest_model.exists(),
            "metrics_available": latest_metrics.exists(),
            "metrics": None
        }
        
        if latest_metrics.exists():
            try:
                with open(latest_metrics, 'r') as f:
                    model_info["metrics"] = json.load(f)
            except Exception as e:
                logger.error(f"Error loading metrics for {model_type}: {e}")
        
        info["models"][model_type] = model_info
    
    # Display information
    print("\n===== ML Code Quality Prediction System Information =====")
    print(f"Timestamp: {info['system']['timestamp']}")
    print(f"Config: {info['system']['config_file']}")
    print(f"Data Directory: {info['system']['data_directory']}")
    print(f"Models Directory: {info['system']['models_directory']}")
    print("\nModel Status:")
    
    for model_type, model_info in info["models"].items():
        status = "Trained" if model_info["trained"] else "Not trained"
        print(f"  - {model_type}: {status}")
        
        if model_info["metrics"]:
            print("    Metrics:")
            for metric, value in model_info["metrics"].items():
                if isinstance(value, float):
                    print(f"      {metric}: {value:.4f}")
                else:
                    print(f"      {metric}: {value}")
    
    print("\n===== Configuration Summary =====")
    for section in ["data_collection", "feature_extraction", "model", "prediction", "api"]:
        if section in CONFIG:
            print(f"{section.upper()}:")
            for key, value in CONFIG[section].items():
                if isinstance(value, dict):
                    print(f"  {key}: {...}")
                else:
                    print(f"  {key}: {value}")
    
    print("\n===== End of Information =====")


def setup_system(args):
    """Setup the system by creating necessary directories."""
    logger.info("Setting up system directories")
    
    directories = [
        DATA_DIR,
        MODELS_DIR,
        DATA_DIR / "raw",
        DATA_DIR / "processed",
        DATA_DIR / "features",
        DATA_DIR / "predictions",
        MODELS_DIR / "quality_prediction",
        MODELS_DIR / "vulnerability_detection",
        MODELS_DIR / "performance_prediction"
    ]
    
    for directory in directories:
        try:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")
        except Exception as e:
            logger.error(f"Error creating directory {directory}: {e}")
    
    logger.info("System setup completed")


def main():
    """Main CLI entry point."""
    parser = setup_argparse()
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return
    
    # Route to appropriate function based on command
    if args.command == "collect":
        run_collect(args)
    elif args.command == "extract":
        run_extract(args)
    elif args.command == "train":
        run_train(args)
    elif args.command == "predict":
        run_predict(args)
    elif args.command == "api":
        run_api(args)
    elif args.command == "run-all":
        run_all(args)
    elif args.command == "info":
        show_info(args)
    elif args.command == "setup":
        setup_system(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main() 