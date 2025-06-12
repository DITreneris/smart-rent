# ML-Based Code Quality Prediction System

This system uses machine learning to predict code quality, detect vulnerabilities, and assess performance characteristics based on code metrics, git history, and development patterns.

## Overview

The ML Quality Prediction System analyzes code and development metrics to provide predictive insights about:

1. **Code Quality** - Predicting overall code quality scores
2. **Vulnerability Detection** - Identifying potential security vulnerabilities  
3. **Performance Prediction** - Estimating performance characteristics

## System Architecture

The system consists of the following components:

### Data Collection

Collects raw data from various sources:
- GitHub issues and pull requests
- SonarQube static analysis reports
- Git repository history
- Test results and coverage

### Feature Extraction

Processes raw data to generate relevant features:
- Text features using TF-IDF or Count vectorization
- Code metrics with normalization and outlier handling
- Git metrics aggregated across time periods

### Model Training

Trains machine learning models for prediction:
- Quality prediction using Random Forest
- Vulnerability detection using LightGBM
- Performance prediction using Random Forest Regression

### Prediction

Makes predictions using trained models:
- Batch prediction support
- Real-time prediction via API
- Classification of quality levels and vulnerability risk

### API

Exposes prediction capabilities through REST endpoints:
- Code-based predictions
- Feature-based predictions
- Batch prediction support
- Model-specific endpoints

## Setup and Usage

### Prerequisites

- Python 3.8+
- Required packages: pandas, scikit-learn, lightgbm, fastapi, uvicorn

### Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up the system:
   ```
   python cli.py setup
   ```

### Configuration

The system configuration is defined in `config.py`. Key settings include:
- Data collection sources and parameters
- Feature extraction methods
- Model hyperparameters
- API configuration

### Basic Usage

The system provides a command-line interface for all operations:

```bash
# Run data collection
python cli.py collect

# Extract features
python cli.py extract

# Train models
python cli.py train --model quality  # or vulnerability, performance, all

# Make predictions
python cli.py predict

# Start the API server
python cli.py api

# Run the complete pipeline
python cli.py run-all

# View system information
python cli.py info
```

### API Usage

The prediction API provides several endpoints:

```
GET /health                     - Health check
POST /predict/code              - Predictions from source code
POST /predict/features          - Predictions from pre-extracted features
POST /predict/batch             - Batch predictions
POST /predict/quality           - Quality-specific prediction
POST /predict/vulnerability     - Vulnerability-specific prediction
POST /predict/performance       - Performance-specific prediction
```

Example request:

```json
POST /predict/code
{
  "code": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)",
  "language": "python",
  "file_path": "math_utils.py",
  "repository": "example-repo"
}
```

## Features

- **Multi-source data collection**: Integrates data from multiple sources
- **Customizable feature extraction**: Configurable preprocessing options
- **Modular design**: Easy to extend with new models or data sources
- **Comprehensive API**: REST interface for integration with other systems
- **Batch processing**: Support for processing multiple files
- **Detailed metrics**: Performance evaluation for all prediction types

## Development

### Directory Structure

```
quality_prediction/
├── config.py                  # System configuration
├── cli.py                     # Command-line interface
├── README.md                  # This file
├── api/                       # API module
│   └── app.py                 # FastAPI application
├── preprocessing/             # Data processing modules
│   ├── data_collection.py     # Data collection
│   └── feature_extraction.py  # Feature generation
└── model/                     # Model modules
    ├── training.py            # Model training
    └── prediction.py          # Prediction using trained models
```

### Adding New Models

To add a new model type:
1. Add configuration to `config.py`
2. Create a new trainer class in `model/training.py`
3. Create a new predictor class in `model/prediction.py`
4. Update the CLI in `cli.py` to include the new model

### Adding New Data Sources

To add a new data source:
1. Add configuration to `config.py`
2. Create a new collector class in `preprocessing/data_collection.py`
3. Update feature extraction to handle the new data source

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 