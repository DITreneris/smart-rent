#!/bin/bash

# Install test dependencies
pip install -r requirements-test.txt

# Run tests with coverage
pytest --cov=app tests/ --cov-report=term --cov-report=html

# Display test summary
echo "Test run complete. See htmlcov/index.html for detailed coverage report." 