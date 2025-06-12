"""
Feature extraction module for the ML quality prediction system.
Transforms raw data into features suitable for model training.
"""

import os
import re
import logging
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.impute import SimpleImputer
from scipy import stats

import sys
# Add parent directory to path to import config
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import CONFIG, DATA_DIR

# Set up logging
logging.basicConfig(
    level=getattr(logging, CONFIG["logging"]["level"]),
    format=CONFIG["logging"]["format"],
    handlers=[
        logging.FileHandler(CONFIG["logging"]["file"]),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("feature_extraction")


class FeatureExtractor:
    """Base class for feature extractors."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize with configuration."""
        self.config = config
        self.output_dir = Path(DATA_DIR) / "processed"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def extract(self, data: pd.DataFrame) -> pd.DataFrame:
        """Extract features from data."""
        raise NotImplementedError("Subclasses must implement extract()")
    
    def save_features(self, features: pd.DataFrame, name: str) -> Path:
        """Save extracted features to file."""
        output_path = self.output_dir / f"{name}_features.parquet"
        features.to_parquet(output_path, index=False)
        logger.info(f"Saved {len(features)} feature records to {output_path}")
        return output_path


class TextFeatureExtractor(FeatureExtractor):
    """Extract features from text data like issue titles, descriptions, etc."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize text feature extractor."""
        super().__init__(config)
        self.vectorizer_type = config["text_features"]["vectorizer"]
        self.max_features = config["text_features"]["max_features"]
        self.stopwords = config["text_features"]["stopwords"]
        self.ngram_range = config["text_features"]["ngram_range"]
        self._initialize_vectorizer()
    
    def _initialize_vectorizer(self):
        """Initialize the text vectorizer based on configuration."""
        if self.vectorizer_type == "tfidf":
            self.vectorizer = TfidfVectorizer(
                max_features=self.max_features,
                stop_words=self.stopwords,
                ngram_range=self.ngram_range,
                analyzer='word',
                min_df=2,
                max_df=0.9
            )
        elif self.vectorizer_type == "count":
            self.vectorizer = CountVectorizer(
                max_features=self.max_features,
                stop_words=self.stopwords,
                ngram_range=self.ngram_range,
                analyzer='word',
                min_df=2
            )
        # BERT embeddings would be handled differently - this implementation would use
        # a pre-trained model like sentence-transformers
        else:
            logger.warning(f"Unsupported vectorizer type: {self.vectorizer_type}. Using TF-IDF instead.")
            self.vectorizer = TfidfVectorizer(
                max_features=self.max_features,
                stop_words=self.stopwords,
                ngram_range=self.ngram_range
            )
    
    def extract(self, data: pd.DataFrame) -> pd.DataFrame:
        """Extract text features from data."""
        logger.info("Extracting text features...")
        
        if data.empty:
            logger.warning("Empty data provided for text feature extraction")
            return pd.DataFrame()
        
        # Combine text fields based on the data source
        if "title" in data.columns and "body" in data.columns:
            # GitHub issues
            data["text"] = data["title"] + " " + data.fillna({"body": ""})["body"]
        elif "failure_message" in data.columns:
            # Test results
            data["text"] = data.fillna({"failure_message": ""})["failure_message"]
        else:
            # Default case - try to use any text column available
            text_columns = [col for col in data.columns if data[col].dtype == 'object']
            if not text_columns:
                logger.warning("No text columns found in data")
                return pd.DataFrame()
            
            data["text"] = data[text_columns[0]].fillna("")
            for col in text_columns[1:]:
                data["text"] += " " + data[col].fillna("")
        
        # Clean text
        data["text"] = data["text"].apply(self._clean_text)
        
        # Filter out empty texts
        data = data[data["text"].str.strip() != ""]
        
        if data.empty:
            logger.warning("No valid text data after cleaning")
            return pd.DataFrame()
        
        # Extract text features
        try:
            text_features = self.vectorizer.fit_transform(data["text"])
            feature_names = self.vectorizer.get_feature_names_out()
            
            # Convert to DataFrame
            text_features_df = pd.DataFrame(
                text_features.toarray(),
                columns=[f"text_{feature}" for feature in feature_names]
            )
            
            # Add identifier columns back
            id_columns = ["id"] if "id" in data.columns else []
            if "repository" in data.columns:
                id_columns.append("repository")
            if "component" in data.columns:
                id_columns.append("component")
            
            # Reset index to have a common key for joining
            data = data.reset_index(drop=True)
            text_features_df = text_features_df.reset_index(drop=True)
            
            # Join with original data if ID columns exist
            if id_columns:
                result = pd.concat([data[id_columns], text_features_df], axis=1)
            else:
                # If no ID columns, just keep the features
                result = text_features_df
            
            logger.info(f"Extracted {len(feature_names)} text features from {len(data)} records")
            return result
            
        except Exception as e:
            logger.error(f"Error extracting text features: {e}")
            return pd.DataFrame()
    
    def _clean_text(self, text: str) -> str:
        """Clean text by removing special characters, URLs, etc."""
        if not isinstance(text, str):
            return ""
        
        # Remove URLs
        text = re.sub(r'http\S+', '', text)
        
        # Remove special characters
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text


class CodeMetricsExtractor(FeatureExtractor):
    """Extract features from code metrics data."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize code metrics extractor."""
        super().__init__(config)
        self.normalization = config["code_metrics"]["normalization"]
        self.handle_outliers = config["code_metrics"]["handle_outliers"]
        self.outlier_method = config["code_metrics"]["outlier_method"]
        self.outlier_threshold = config["code_metrics"]["outlier_threshold"]
        self._initialize_scalers()
    
    def _initialize_scalers(self):
        """Initialize scalers based on configuration."""
        if self.normalization == "standard":
            self.scaler = StandardScaler()
        elif self.normalization == "minmax":
            self.scaler = MinMaxScaler()
        elif self.normalization == "robust":
            self.scaler = RobustScaler()
        else:
            logger.warning(f"Unsupported normalization method: {self.normalization}. Using standard scaler.")
            self.scaler = StandardScaler()
        
        # Initialize imputer for missing values
        self.imputer = SimpleImputer(strategy="median")
    
    def extract(self, data: pd.DataFrame) -> pd.DataFrame:
        """Extract code metrics features."""
        logger.info("Extracting code metrics features...")
        
        if data.empty:
            logger.warning("Empty data provided for code metrics extraction")
            return pd.DataFrame()
        
        # Identify metric columns
        numeric_columns = data.select_dtypes(include=["int64", "float64"]).columns.tolist()
        id_columns = ["id"] if "id" in data.columns else []
        if "repository" in data.columns:
            id_columns.append("repository")
        if "file_path" in data.columns:
            id_columns.append("file_path")
        if "component" in data.columns:
            id_columns.append("component")
        
        # Exclude identifier columns from metrics
        metric_columns = [col for col in numeric_columns if col not in id_columns]
        
        if not metric_columns:
            logger.warning("No numeric metric columns found in data")
            return pd.DataFrame()
        
        # Create a copy to avoid modifying the original data
        metrics_df = data[id_columns + metric_columns].copy()
        
        # Handle outliers if enabled
        if self.handle_outliers:
            for col in metric_columns:
                metrics_df[col] = self._handle_outliers(metrics_df[col])
        
        # Impute missing values
        metrics_array = self.imputer.fit_transform(metrics_df[metric_columns])
        
        # Normalize metrics
        try:
            scaled_metrics = self.scaler.fit_transform(metrics_array)
            scaled_df = pd.DataFrame(
                scaled_metrics,
                columns=[f"scaled_{col}" for col in metric_columns]
            )
            
            # Add identifier columns back
            if id_columns:
                result = pd.concat([metrics_df[id_columns].reset_index(drop=True), 
                                    scaled_df.reset_index(drop=True)], axis=1)
            else:
                result = scaled_df
            
            logger.info(f"Extracted {len(metric_columns)} scaled metrics from {len(data)} records")
            return result
            
        except Exception as e:
            logger.error(f"Error scaling code metrics: {e}")
            return pd.DataFrame()
    
    def _handle_outliers(self, series: pd.Series) -> pd.Series:
        """Handle outliers in a series using the configured method."""
        if series.dtype not in ["int64", "float64"]:
            return series
        
        if self.outlier_method == "winsorize":
            return pd.Series(
                stats.mstats.winsorize(series, limits=[self.outlier_threshold, self.outlier_threshold])
            )
        elif self.outlier_method == "clip":
            q_low = series.quantile(self.outlier_threshold)
            q_high = series.quantile(1 - self.outlier_threshold)
            return series.clip(q_low, q_high)
        elif self.outlier_method == "remove":
            q_low = series.quantile(self.outlier_threshold)
            q_high = series.quantile(1 - self.outlier_threshold)
            return series.mask((series < q_low) | (series > q_high))
        else:
            logger.warning(f"Unsupported outlier method: {self.outlier_method}. Returning original data.")
            return series


class GitMetricsExtractor(FeatureExtractor):
    """Extract features from Git history data."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize Git metrics extractor."""
        super().__init__(config)
        self.aggregation = config["git_metrics"]["aggregation"]
        self.timeframes = config["git_metrics"]["timeframes"]
        self.normalization = config["git_metrics"]["normalization"]
        self._initialize_scaler()
    
    def _initialize_scaler(self):
        """Initialize scaler based on configuration."""
        if self.normalization == "standard":
            self.scaler = StandardScaler()
        elif self.normalization == "minmax":
            self.scaler = MinMaxScaler()
        elif self.normalization == "robust":
            self.scaler = RobustScaler()
        else:
            logger.warning(f"Unsupported normalization method: {self.normalization}. Using standard scaler.")
            self.scaler = StandardScaler()
    
    def extract(self, data: pd.DataFrame) -> pd.DataFrame:
        """Extract Git metrics features."""
        logger.info("Extracting Git metrics features...")
        
        if data.empty:
            logger.warning("Empty data provided for Git metrics extraction")
            return pd.DataFrame()
        
        # Identify Git metric columns
        git_metric_columns = [
            col for col in data.columns if any(
                metric in col for metric in [
                    "commit", "change", "churn", "contributor", "age"
                ]
            ) and data[col].dtype in ["int64", "float64"]
        ]
        
        id_columns = ["id"] if "id" in data.columns else []
        if "repository" in data.columns:
            id_columns.append("repository")
        if "file_path" in data.columns:
            id_columns.append("file_path")
        
        if not git_metric_columns:
            logger.warning("No Git metric columns found in data")
            return pd.DataFrame()
        
        # Group by repository and file path if available
        grouped_df = None
        
        if "repository" in data.columns and "file_path" in data.columns:
            # Group by repository and file path
            grouped = data.groupby(["repository", "file_path"])
            
            # Aggregate metrics by configured method
            if self.aggregation == "mean":
                grouped_df = grouped[git_metric_columns].mean()
            elif self.aggregation == "median":
                grouped_df = grouped[git_metric_columns].median()
            elif self.aggregation == "max":
                grouped_df = grouped[git_metric_columns].max()
            elif self.aggregation == "min":
                grouped_df = grouped[git_metric_columns].min()
            else:
                logger.warning(f"Unsupported aggregation method: {self.aggregation}. Using mean.")
                grouped_df = grouped[git_metric_columns].mean()
            
            # Reset index to convert back to columns
            grouped_df = grouped_df.reset_index()
        else:
            # Use the original data if grouping is not possible
            grouped_df = data[id_columns + git_metric_columns].copy()
        
        # Normalize Git metrics
        try:
            # Impute missing values
            imputer = SimpleImputer(strategy="median")
            metrics_array = imputer.fit_transform(grouped_df[git_metric_columns])
            
            # Scale metrics
            scaled_metrics = self.scaler.fit_transform(metrics_array)
            scaled_df = pd.DataFrame(
                scaled_metrics,
                columns=[f"scaled_{col}" for col in git_metric_columns]
            )
            
            # Add identifier columns back
            id_columns_in_grouped = [col for col in id_columns if col in grouped_df.columns]
            id_columns_in_grouped.extend(["repository", "file_path"] if "repository" in grouped_df.columns and "file_path" in grouped_df.columns else [])
            
            if id_columns_in_grouped:
                result = pd.concat([
                    grouped_df[id_columns_in_grouped].reset_index(drop=True),
                    scaled_df.reset_index(drop=True)
                ], axis=1)
            else:
                result = scaled_df
            
            logger.info(f"Extracted {len(git_metric_columns)} Git metrics from {len(grouped_df)} records")
            return result
            
        except Exception as e:
            logger.error(f"Error scaling Git metrics: {e}")
            return pd.DataFrame()


class CombinedFeatureExtractor:
    """Combine features from multiple extractors."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize combined feature extractor."""
        self.config = config
        self.output_dir = Path(DATA_DIR) / "features"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._initialize_extractors()
    
    def _initialize_extractors(self):
        """Initialize individual feature extractors."""
        self.extractors = {}
        
        if self.config["feature_extraction"]["text_features"]["enabled"]:
            self.extractors["text"] = TextFeatureExtractor(self.config)
        
        if self.config["feature_extraction"]["code_metrics"]["enabled"]:
            self.extractors["code_metrics"] = CodeMetricsExtractor(self.config)
        
        if self.config["feature_extraction"]["git_metrics"]["enabled"]:
            self.extractors["git_metrics"] = GitMetricsExtractor(self.config)
    
    def extract_all(self, data_sources: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """Extract features from all data sources."""
        logger.info("Starting feature extraction from all sources...")
        features = {}
        
        for source_name, data in data_sources.items():
            logger.info(f"Processing features from {source_name}...")
            
            if data.empty:
                logger.warning(f"Empty data for source: {source_name}")
                continue
            
            source_features = {}
            
            # Apply appropriate extractors based on data source
            if source_name == "github_issues":
                # Text features for GitHub issues
                if "text" in self.extractors:
                    source_features["text"] = self.extractors["text"].extract(data)
            
            elif source_name == "sonarqube_reports":
                # Code metrics for SonarQube data
                if "code_metrics" in self.extractors:
                    source_features["code_metrics"] = self.extractors["code_metrics"].extract(data)
            
            elif source_name == "git_history":
                # Git metrics for Git history data
                if "git_metrics" in self.extractors:
                    source_features["git_metrics"] = self.extractors["git_metrics"].extract(data)
                    
                # Also extract text features from commit messages if available
                if "text" in self.extractors and "message" in data.columns:
                    source_features["text"] = self.extractors["text"].extract(data[["message"]])
            
            elif source_name == "test_results":
                # Code metrics for test results
                if "code_metrics" in self.extractors:
                    source_features["code_metrics"] = self.extractors["code_metrics"].extract(data)
                
                # Text features for test failure messages
                if "text" in self.extractors and "failure_message" in data.columns:
                    source_features["text"] = self.extractors["text"].extract(data)
            
            features[source_name] = source_features
        
        # Save all features
        self._save_features(features)
        
        logger.info("Feature extraction completed")
        return features
    
    def _save_features(self, features: Dict[str, Dict[str, pd.DataFrame]]) -> None:
        """Save extracted features to files."""
        for source_name, source_features in features.items():
            for feature_type, feature_df in source_features.items():
                if feature_df.empty:
                    continue
                
                output_path = self.output_dir / f"{source_name}_{feature_type}_features.parquet"
                feature_df.to_parquet(output_path, index=False)
                logger.info(f"Saved {len(feature_df)} {feature_type} features for {source_name} to {output_path}")


def load_data(data_dir: Path) -> Dict[str, pd.DataFrame]:
    """Load data from parquet files in the raw data directory."""
    logger.info(f"Loading data from: {data_dir}")
    data_sources = {}
    
    if not data_dir.exists():
        logger.error(f"Data directory does not exist: {data_dir}")
        return data_sources
    
    # Get the most recent file for each source
    source_files = {}
    
    for file_path in data_dir.glob("*.parquet"):
        # Parse source name from filename (source_timestamp.parquet)
        parts = file_path.stem.split("_")
        if not parts:
            continue
        
        source_name = parts[0]
        
        # Keep track of the most recent file for each source
        if source_name not in source_files or file_path.stat().st_mtime > source_files[source_name][1]:
            source_files[source_name] = (file_path, file_path.stat().st_mtime)
    
    # Load data from the most recent files
    for source_name, (file_path, _) in source_files.items():
        try:
            data = pd.read_parquet(file_path)
            data_sources[source_name] = data
            logger.info(f"Loaded {len(data)} records from {file_path}")
        except Exception as e:
            logger.error(f"Error loading data from {file_path}: {e}")
    
    return data_sources


def main():
    """Main function to run feature extraction."""
    logger.info("Starting feature extraction process...")
    
    # Load raw data
    raw_data_dir = Path(CONFIG["data_collection"]["output_path"])
    data_sources = load_data(raw_data_dir)
    
    if not data_sources:
        logger.error("No data sources loaded. Exiting.")
        return
    
    # Initialize feature extractor
    feature_extractor = CombinedFeatureExtractor(CONFIG)
    
    # Extract features
    features = feature_extractor.extract_all(data_sources)
    
    logger.info(f"Extracted features from {len(features)} data sources")


if __name__ == "__main__":
    main() 