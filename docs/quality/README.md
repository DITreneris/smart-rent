# Quality Assurance System

## Overview

This directory contains documentation related to the SmartRent Quality Assurance System. The goal of this system is to ensure code quality, security, and reliability throughout the development lifecycle.

## Documentation Structure

- [QA Process](./process.md) - Defines the overall QA workflow and responsibilities
- [Testing Standards](./testing-standards.md) - Standards for writing tests and maintaining test coverage
- [Code Review Guidelines](./code-review.md) - Guidelines for conducting effective code reviews
- [Quality Metrics](./metrics.md) - Definitions of quality metrics tracked in the project

## Quality Assurance Tools

The SmartRent project uses the following code quality tools:

### Python
- **Flake8**: Style guide enforcement
- **Black**: Code formatting
- **isort**: Import sorting
- **mypy**: Static type checking
- **pylint**: Static code analysis

### JavaScript/TypeScript
- **ESLint**: Style guide and code quality enforcement
- **Prettier**: Code formatting
- **TypeScript Compiler**: Static type checking

### General
- **SonarCloud**: Comprehensive code quality and security analysis
- **pre-commit**: Git hooks for code quality checks
- **GitHub Actions**: CI/CD for automated quality checks

## Setup Instructions

### Local Development Setup

1. Install pre-commit hooks:
   ```bash
   pip install pre-commit
   pre-commit install
   ```

2. Install Python quality tools:
   ```bash
   pip install flake8 black isort mypy pylint
   ```

3. Install JavaScript/TypeScript quality tools:
   ```bash
   cd frontend
   npm install --save-dev eslint prettier @typescript-eslint/eslint-plugin @typescript-eslint/parser eslint-plugin-react eslint-plugin-react-hooks eslint-config-prettier eslint-plugin-prettier
   ```

### CI/CD Integration

Quality checks are automatically run on:
- Push to main and develop branches
- Pull requests to main and develop branches

See the GitHub Actions workflow configuration in `.github/workflows/quality-checks.yml` for details. 