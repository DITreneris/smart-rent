"""
Model training module for ML-based code quality prediction system.
"""

import os
import json
import logging
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime
import pickle
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, mean_squared_error, r2_score
)
import lightgbm as lgb
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

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
logger = logging.getLogger("model_training")


class ModelTrainer:
    """Base class for model training."""
    
    def __init__(self, config: Dict[str, Any], model_name: str):
        """Initialize model trainer with configuration."""
        self.config = config
        self.model_name = model_name
        self.model_config = config["model"][model_name]
        self.models_dir = Path(MODELS_DIR)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.model_dir = self.models_dir / model_name
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.metrics = {}
    
    def load_data(self) -> pd.DataFrame:
        """Load and combine preprocessed feature data."""
        logger.info(f"Loading data for {self.model_name} model training")
        features_dir = Path(self.config["feature_extraction"]["output_path"])
        
        if not features_dir.exists():
            logger.error(f"Features directory does not exist: {features_dir}")
            return pd.DataFrame()
        
        # Get all feature files
        feature_files = list(features_dir.glob("*.parquet"))
        if not feature_files:
            logger.error(f"No feature files found in: {features_dir}")
            return pd.DataFrame()
        
        # Load and combine features
        feature_dfs = []
        for file_path in feature_files:
            try:
                df = pd.read_parquet(file_path)
                feature_dfs.append(df)
                logger.info(f"Loaded {len(df)} records from {file_path}")
            except Exception as e:
                logger.error(f"Error loading features from {file_path}: {e}")
        
        if not feature_dfs:
            logger.error("No feature dataframes created")
            return pd.DataFrame()
        
        # Combine feature dataframes - this depends on the feature extraction design
        # For this implementation, we assume each dataframe has unique features that can be merged
        # In practice, you may need a more sophisticated merging strategy
        
        # Find common ID columns for merging
        id_columns = self._find_common_id_columns(feature_dfs)
        
        if not id_columns:
            logger.warning("No common ID columns found for merging. Concatenating instead.")
            return pd.concat(feature_dfs, axis=1)
        
        # Merge dataframes on common ID columns
        merged_df = feature_dfs[0]
        for df in feature_dfs[1:]:
            try:
                merged_df = pd.merge(merged_df, df, on=id_columns, how='outer')
            except Exception as e:
                logger.error(f"Error merging dataframes: {e}")
        
        logger.info(f"Combined features into dataframe with {len(merged_df)} rows and {len(merged_df.columns)} columns")
        return merged_df
    
    def _find_common_id_columns(self, dataframes: List[pd.DataFrame]) -> List[str]:
        """Find common columns that can be used as identifiers for merging."""
        if not dataframes:
            return []
        
        # Common columns across all dataframes
        common_columns = set(dataframes[0].columns)
        for df in dataframes[1:]:
            common_columns &= set(df.columns)
        
        # Potential ID columns
        id_cols = ["id", "repository", "file_path", "component", "issue_id"]
        
        # Filter to common ID columns
        common_id_columns = [col for col in id_cols if col in common_columns]
        
        return common_id_columns
    
    def prepare_data(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Prepare data for training including feature selection and splitting."""
        if data.empty:
            logger.error("Empty data provided for preparation")
            return np.array([]), np.array([]), np.array([]), np.array([])
        
        # Identify target column based on model type
        target_col = self.model_config.get("target_column")
        if not target_col or target_col not in data.columns:
            logger.error(f"Target column '{target_col}' not found in data")
            return np.array([]), np.array([]), np.array([]), np.array([])
        
        # Get the target values
        y = data[target_col].values
        
        # Remove the target column and any ID columns from features
        exclude_cols = [target_col]
        exclude_cols.extend(["id", "repository", "file_path", "component", "issue_id"])
        feature_cols = [col for col in data.columns if col not in exclude_cols]
        
        if not feature_cols:
            logger.error("No feature columns remaining after exclusions")
            return np.array([]), np.array([]), np.array([]), np.array([])
        
        # Extract features
        X = data[feature_cols].values
        
        # Handle missing values
        X = np.nan_to_num(X, nan=0)
        
        # Split data
        test_size = self.model_config.get("test_size", 0.2)
        random_state = self.config.get("random_seed", 42)
        
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state
            )
            logger.info(f"Data split: {X_train.shape[0]} training samples, {X_test.shape[0]} test samples")
            
            # Save feature columns for future inference
            self._save_feature_columns(feature_cols)
            
            return X_train, X_test, y_train, y_test
        except Exception as e:
            logger.error(f"Error splitting data: {e}")
            return np.array([]), np.array([]), np.array([]), np.array([])
    
    def _save_feature_columns(self, feature_columns: List[str]) -> None:
        """Save feature columns for future inference."""
        columns_path = self.model_dir / "feature_columns.json"
        try:
            with open(columns_path, 'w') as f:
                json.dump(feature_columns, f)
            logger.info(f"Saved {len(feature_columns)} feature columns to {columns_path}")
        except Exception as e:
            logger.error(f"Error saving feature columns: {e}")
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> Any:
        """Train model on the prepared data."""
        raise NotImplementedError("Subclasses must implement train()")
    
    def evaluate(self, model: Any, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """Evaluate the trained model."""
        raise NotImplementedError("Subclasses must implement evaluate()")
    
    def save_model(self, model: Any) -> Path:
        """Save the trained model to disk."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_path = self.model_dir / f"{self.model_name}_{timestamp}.pkl"
        
        try:
            with open(model_path, 'wb') as f:
                pickle.dump(model, f)
            logger.info(f"Saved model to {model_path}")
            
            # Save as latest model
            latest_path = self.model_dir / "latest.pkl"
            with open(latest_path, 'wb') as f:
                pickle.dump(model, f)
            
            # Save metrics
            self._save_metrics(timestamp)
            
            return model_path
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            return None
    
    def _save_metrics(self, timestamp: str) -> None:
        """Save evaluation metrics."""
        metrics_path = self.model_dir / f"metrics_{timestamp}.json"
        try:
            with open(metrics_path, 'w') as f:
                json.dump(self.metrics, f)
            
            # Save as latest metrics
            latest_metrics_path = self.model_dir / "latest_metrics.json"
            with open(latest_metrics_path, 'w') as f:
                json.dump(self.metrics, f)
            
            logger.info(f"Saved metrics to {metrics_path}")
        except Exception as e:
            logger.error(f"Error saving metrics: {e}")


class QualityPredictionTrainer(ModelTrainer):
    """Trainer for code quality prediction model."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize quality prediction model trainer."""
        super().__init__(config, "quality_prediction")
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> Any:
        """Train quality prediction model."""
        logger.info("Training quality prediction model...")
        
        algorithm = self.model_config.get("algorithm", "random_forest")
        
        if algorithm == "random_forest":
            model = self._train_random_forest(X_train, y_train)
        elif algorithm == "logistic_regression":
            model = self._train_logistic_regression(X_train, y_train)
        else:
            logger.warning(f"Unsupported algorithm: {algorithm}. Using random forest.")
            model = self._train_random_forest(X_train, y_train)
        
        return model
    
    def _train_random_forest(self, X_train: np.ndarray, y_train: np.ndarray) -> Any:
        """Train random forest model with hyperparameter tuning."""
        params = self.model_config.get("hyperparameters", {})
        
        # Define the model
        model = RandomForestClassifier(
            n_estimators=params.get("n_estimators", 100),
            max_depth=params.get("max_depth", None),
            min_samples_split=params.get("min_samples_split", 2),
            min_samples_leaf=params.get("min_samples_leaf", 1),
            random_state=self.config.get("random_seed", 42)
        )
        
        # Perform hyperparameter tuning if enabled
        if self.model_config.get("hyperparameter_tuning", {}).get("enabled", False):
            logger.info("Performing hyperparameter tuning for random forest...")
            
            tuning_config = self.model_config.get("hyperparameter_tuning", {})
            param_grid = tuning_config.get("param_grid", {
                "n_estimators": [50, 100, 200],
                "max_depth": [None, 10, 20, 30],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 4]
            })
            
            # Create the search
            if tuning_config.get("method", "grid") == "random":
                n_iter = tuning_config.get("n_iter", 10)
                search = RandomizedSearchCV(
                    model, param_grid, n_iter=n_iter, cv=5, 
                    scoring='f1', n_jobs=-1, random_state=self.config.get("random_seed", 42)
                )
            else:
                search = GridSearchCV(
                    model, param_grid, cv=5, scoring='f1', n_jobs=-1
                )
            
            # Perform the search
            search.fit(X_train, y_train)
            
            # Update model with best parameters
            model = search.best_estimator_
            logger.info(f"Best parameters: {search.best_params_}")
        
        # Train the final model
        model.fit(X_train, y_train)
        logger.info("Random forest model trained successfully")
        
        return model
    
    def _train_logistic_regression(self, X_train: np.ndarray, y_train: np.ndarray) -> Any:
        """Train logistic regression model."""
        params = self.model_config.get("hyperparameters", {})
        
        # Define the model
        model = LogisticRegression(
            C=params.get("C", 1.0),
            penalty=params.get("penalty", "l2"),
            solver=params.get("solver", "lbfgs"),
            max_iter=params.get("max_iter", 1000),
            random_state=self.config.get("random_seed", 42)
        )
        
        # Train the model
        model.fit(X_train, y_train)
        logger.info("Logistic regression model trained successfully")
        
        return model
    
    def evaluate(self, model: Any, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """Evaluate quality prediction model."""
        logger.info("Evaluating quality prediction model...")
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Get probability predictions (for ROC-AUC)
        try:
            y_prob = model.predict_proba(X_test)[:, 1]
        except:
            y_prob = None
        
        # Calculate metrics
        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, average='weighted'),
            "recall": recall_score(y_test, y_pred, average='weighted'),
            "f1": f1_score(y_test, y_pred, average='weighted')
        }
        
        # Add ROC-AUC if possible
        if y_prob is not None:
            try:
                metrics["roc_auc"] = roc_auc_score(y_test, y_prob)
            except:
                pass
        
        # Log metrics
        for metric_name, metric_value in metrics.items():
            logger.info(f"{metric_name}: {metric_value:.4f}")
        
        # Save metrics
        self.metrics = metrics
        
        return metrics


class VulnerabilityDetectionTrainer(ModelTrainer):
    """Trainer for vulnerability detection model."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize vulnerability detection model trainer."""
        super().__init__(config, "vulnerability_detection")
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> Any:
        """Train vulnerability detection model."""
        logger.info("Training vulnerability detection model...")
        
        algorithm = self.model_config.get("algorithm", "lightgbm")
        
        if algorithm == "lightgbm":
            model = self._train_lightgbm(X_train, y_train)
        elif algorithm == "random_forest":
            model = self._train_random_forest(X_train, y_train)
        else:
            logger.warning(f"Unsupported algorithm: {algorithm}. Using LightGBM.")
            model = self._train_lightgbm(X_train, y_train)
        
        return model
    
    def _train_lightgbm(self, X_train: np.ndarray, y_train: np.ndarray) -> Any:
        """Train LightGBM model."""
        params = self.model_config.get("hyperparameters", {})
        
        # Default hyperparameters
        lgb_params = {
            "objective": "binary",
            "metric": "binary_logloss",
            "boosting_type": "gbdt",
            "num_leaves": params.get("num_leaves", 31),
            "learning_rate": params.get("learning_rate", 0.05),
            "feature_fraction": params.get("feature_fraction", 0.9),
            "bagging_fraction": params.get("bagging_fraction", 0.8),
            "bagging_freq": params.get("bagging_freq", 5),
            "verbose": -1,
            "random_state": self.config.get("random_seed", 42)
        }
        
        # Create dataset
        lgb_train = lgb.Dataset(X_train, y_train)
        
        # Train model
        num_boost_round = params.get("num_boost_round", 100)
        model = lgb.train(lgb_params, lgb_train, num_boost_round=num_boost_round)
        
        logger.info("LightGBM model trained successfully")
        return model
    
    def _train_random_forest(self, X_train: np.ndarray, y_train: np.ndarray) -> Any:
        """Train random forest model for vulnerability detection."""
        params = self.model_config.get("hyperparameters", {})
        
        model = RandomForestClassifier(
            n_estimators=params.get("n_estimators", 100),
            max_depth=params.get("max_depth", None),
            min_samples_split=params.get("min_samples_split", 2),
            min_samples_leaf=params.get("min_samples_leaf", 1),
            class_weight="balanced",
            random_state=self.config.get("random_seed", 42)
        )
        
        model.fit(X_train, y_train)
        logger.info("Random forest model trained successfully")
        
        return model
    
    def evaluate(self, model: Any, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """Evaluate vulnerability detection model."""
        logger.info("Evaluating vulnerability detection model...")
        
        # Make predictions
        if isinstance(model, lgb.Booster):
            y_pred_proba = model.predict(X_test)
            y_pred = np.round(y_pred_proba)
        else:
            y_pred = model.predict(X_test)
            try:
                y_pred_proba = model.predict_proba(X_test)[:, 1]
            except:
                y_pred_proba = y_pred
        
        # Calculate metrics
        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, average='binary'),
            "recall": recall_score(y_test, y_pred, average='binary'),
            "f1": f1_score(y_test, y_pred, average='binary')
        }
        
        # Add ROC-AUC
        try:
            metrics["roc_auc"] = roc_auc_score(y_test, y_pred_proba)
        except:
            pass
        
        # Log metrics
        for metric_name, metric_value in metrics.items():
            logger.info(f"{metric_name}: {metric_value:.4f}")
        
        # Save metrics
        self.metrics = metrics
        
        return metrics


class PerformancePredictionTrainer(ModelTrainer):
    """Trainer for performance prediction model."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize performance prediction model trainer."""
        super().__init__(config, "performance_prediction")
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> Any:
        """Train performance prediction model."""
        logger.info("Training performance prediction model...")
        
        algorithm = self.model_config.get("algorithm", "random_forest")
        
        if algorithm == "random_forest":
            model = self._train_random_forest_regressor(X_train, y_train)
        elif algorithm == "linear_regression":
            model = self._train_linear_regression(X_train, y_train)
        else:
            logger.warning(f"Unsupported algorithm: {algorithm}. Using random forest regressor.")
            model = self._train_random_forest_regressor(X_train, y_train)
        
        return model
    
    def _train_random_forest_regressor(self, X_train: np.ndarray, y_train: np.ndarray) -> Any:
        """Train random forest regressor for performance prediction."""
        params = self.model_config.get("hyperparameters", {})
        
        model = RandomForestRegressor(
            n_estimators=params.get("n_estimators", 100),
            max_depth=params.get("max_depth", None),
            min_samples_split=params.get("min_samples_split", 2),
            min_samples_leaf=params.get("min_samples_leaf", 1),
            random_state=self.config.get("random_seed", 42)
        )
        
        model.fit(X_train, y_train)
        logger.info("Random forest regressor trained successfully")
        
        return model
    
    def _train_linear_regression(self, X_train: np.ndarray, y_train: np.ndarray) -> Any:
        """Train linear regression for performance prediction."""
        model = LinearRegression()
        model.fit(X_train, y_train)
        logger.info("Linear regression model trained successfully")
        
        return model
    
    def evaluate(self, model: Any, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """Evaluate performance prediction model."""
        logger.info("Evaluating performance prediction model...")
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        metrics = {
            "mse": mean_squared_error(y_test, y_pred),
            "rmse": np.sqrt(mean_squared_error(y_test, y_pred)),
            "r2": r2_score(y_test, y_pred)
        }
        
        # Log metrics
        for metric_name, metric_value in metrics.items():
            logger.info(f"{metric_name}: {metric_value:.4f}")
        
        # Save metrics
        self.metrics = metrics
        
        return metrics


def train_model(model_type: str, config: Dict[str, Any]) -> Optional[Path]:
    """Train a specific model type."""
    logger.info(f"Starting training for {model_type} model")
    
    # Initialize appropriate trainer
    if model_type == "quality_prediction":
        trainer = QualityPredictionTrainer(config)
    elif model_type == "vulnerability_detection":
        trainer = VulnerabilityDetectionTrainer(config)
    elif model_type == "performance_prediction":
        trainer = PerformancePredictionTrainer(config)
    else:
        logger.error(f"Unknown model type: {model_type}")
        return None
    
    # Load data
    data = trainer.load_data()
    if data.empty:
        logger.error("No data available for training")
        return None
    
    # Prepare data
    X_train, X_test, y_train, y_test = trainer.prepare_data(data)
    if len(X_train) == 0 or len(y_train) == 0:
        logger.error("Failed to prepare training data")
        return None
    
    # Train model
    model = trainer.train(X_train, y_train)
    
    # Evaluate model
    metrics = trainer.evaluate(model, X_test, y_test)
    
    # Save model
    model_path = trainer.save_model(model)
    
    logger.info(f"Completed training for {model_type} model")
    return model_path


def main():
    """Main function to train all enabled models."""
    logger.info("Starting model training process")
    
    # Check which models are enabled
    enabled_models = []
    for model_type in ["quality_prediction", "vulnerability_detection", "performance_prediction"]:
        if CONFIG["model"][model_type]["enabled"]:
            enabled_models.append(model_type)
    
    if not enabled_models:
        logger.warning("No models enabled for training")
        return
    
    logger.info(f"Will train the following models: {', '.join(enabled_models)}")
    
    # Train each enabled model
    for model_type in enabled_models:
        try:
            model_path = train_model(model_type, CONFIG)
            if model_path:
                logger.info(f"Successfully trained and saved {model_type} model to {model_path}")
            else:
                logger.error(f"Failed to train {model_type} model")
        except Exception as e:
            logger.error(f"Error training {model_type} model: {e}")
    
    logger.info("Model training process completed")


if __name__ == "__main__":
    main() 