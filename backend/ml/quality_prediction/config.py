"""
Configuration for the ML-based code quality prediction system.
"""

import os
from pathlib import Path
from typing import Dict, List, Any

# Base directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# Data collection settings
DATA_COLLECTION_CONFIG = {
    "sources": [
        {
            "name": "github_issues",
            "enabled": True,
            "params": {
                "repositories": [
                    "backend",
                    "frontend"
                ],
                "issue_types": [
                    "bug",
                    "performance",
                    "security",
                    "maintenance"
                ],
                "max_issues": 1000,
                "include_closed": True
            }
        },
        {
            "name": "sonarqube_reports",
            "enabled": True,
            "params": {
                "url": os.environ.get("SONARQUBE_URL", "http://localhost:9000"),
                "token": os.environ.get("SONARQUBE_TOKEN", ""),
                "projects": ["smartrent-backend", "smartrent-frontend"],
                "metrics": [
                    "bugs", "vulnerabilities", "code_smells", 
                    "duplicated_lines_density", "coverage",
                    "cognitive_complexity", "security_rating"
                ]
            }
        },
        {
            "name": "git_history",
            "enabled": True,
            "params": {
                "repositories": ["backend", "frontend"],
                "metrics": [
                    "commit_frequency",
                    "file_change_frequency",
                    "code_churn",
                    "contributor_count",
                    "file_age"
                ],
                "timeframe_days": 180
            }
        },
        {
            "name": "test_results",
            "enabled": True,
            "params": {
                "include_unit_tests": True,
                "include_integration_tests": True,
                "include_e2e_tests": True,
                "metrics": [
                    "failure_rate",
                    "test_duration",
                    "flakiness_score",
                    "test_coverage"
                ]
            }
        }
    ],
    "output_format": "parquet",
    "output_path": DATA_DIR / "raw",
    "collection_frequency": "daily"  # Options: hourly, daily, weekly
}

# Feature extraction settings
FEATURE_EXTRACTION_CONFIG = {
    "text_features": {
        "enabled": True,
        "vectorizer": "tfidf",  # Options: tfidf, count, bert
        "max_features": 1000,
        "stopwords": "english",
        "ngram_range": (1, 3)
    },
    "code_metrics": {
        "enabled": True,
        "normalization": "standard",  # Options: standard, minmax, robust
        "handle_outliers": True,
        "outlier_method": "winsorize",  # Options: winsorize, clip, remove
        "outlier_threshold": 0.05
    },
    "git_metrics": {
        "enabled": True,
        "aggregation": "mean",  # Options: mean, median, max, min
        "timeframes": ["1w", "1m", "3m", "6m"],
        "normalization": "standard"
    }
}

# Model configuration
MODEL_CONFIG = {
    "quality_prediction": {
        "algorithm": "random_forest",  # Options: random_forest, xgboost, lightgbm, neural_network
        "hyperparameters": {
            "random_forest": {
                "n_estimators": 100,
                "max_depth": 10,
                "min_samples_split": 2,
                "min_samples_leaf": 1,
                "random_state": 42
            },
            "xgboost": {
                "n_estimators": 100,
                "learning_rate": 0.1,
                "max_depth": 5,
                "subsample": 0.8,
                "colsample_bytree": 0.8,
                "random_state": 42
            }
        },
        "feature_selection": {
            "method": "rfe",  # Options: rfe, chi2, mutual_info, lasso
            "n_features": 50
        },
        "validation": {
            "method": "cross_validation",  # Options: cross_validation, holdout
            "k_folds": 5,
            "test_size": 0.2,
            "random_state": 42
        }
    },
    "vulnerability_detection": {
        "algorithm": "lightgbm",
        "hyperparameters": {
            "lightgbm": {
                "n_estimators": 100,
                "learning_rate": 0.05,
                "num_leaves": 31,
                "feature_fraction": 0.9,
                "bagging_fraction": 0.8,
                "random_state": 42
            }
        },
        "class_weight": "balanced",  # Handle imbalanced data
        "validation": {
            "method": "stratified_cross_validation",
            "k_folds": 5,
            "metrics": ["precision", "recall", "f1", "roc_auc"]
        }
    },
    "performance_prediction": {
        "algorithm": "neural_network",
        "architecture": {
            "hidden_layers": [64, 32],
            "activation": "relu",
            "dropout_rate": 0.3
        },
        "training": {
            "batch_size": 32,
            "epochs": 100,
            "early_stopping": True,
            "patience": 10,
            "validation_split": 0.2
        }
    }
}

# API configuration
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 8080,
    "debug": False,
    "log_level": "info",
    "enable_swagger": True,
    "cors_origins": ["*"],
    "auth_required": True,
    "rate_limit": {
        "enabled": True,
        "limit": 100,
        "timeframe": 60  # seconds
    }
}

# Logging configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": BASE_DIR / "logs" / "quality_prediction.log",
    "rotation": "10 MB"
}

# Notification settings
NOTIFICATION_CONFIG = {
    "enabled": True,
    "channels": {
        "slack": {
            "enabled": True,
            "webhook_url": os.environ.get("SLACK_WEBHOOK_URL", ""),
            "channel": "#quality-alerts"
        },
        "email": {
            "enabled": False,
            "smtp_server": "smtp.example.com",
            "smtp_port": 587,
            "sender": "quality-alerts@smartrent.com",
            "recipients": ["dev-team@smartrent.com"]
        }
    },
    "alert_thresholds": {
        "quality_score": 0.7,  # Alert if below this threshold
        "vulnerability_probability": 0.6,  # Alert if above this threshold
        "performance_degradation": 20  # Percentage degradation to trigger alert
    }
}

# Schedule settings
SCHEDULE_CONFIG = {
    "data_collection": "0 0 * * *",  # Daily at midnight (cron format)
    "model_training": "0 2 * * 0",   # Weekly on Sunday at 2 AM
    "prediction_generation": "0 4 * * *",  # Daily at 4 AM
    "dashboard_update": "0 6 * * *"  # Daily at 6 AM
}

# Export all configs
CONFIG = {
    "base_dir": BASE_DIR,
    "data_dir": DATA_DIR,
    "models_dir": MODELS_DIR,
    "data_collection": DATA_COLLECTION_CONFIG,
    "feature_extraction": FEATURE_EXTRACTION_CONFIG,
    "model": MODEL_CONFIG,
    "api": API_CONFIG,
    "logging": LOGGING_CONFIG,
    "notification": NOTIFICATION_CONFIG,
    "schedule": SCHEDULE_CONFIG
} 