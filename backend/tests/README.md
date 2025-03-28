# Smart Rent Platform Tests

This directory contains tests for the Smart Rent Platform API, organized into several modules:

- `test_auth.py`: Tests for user authentication, registration, and profile management
- `test_properties.py`: Tests for property listing and management 
- `test_contracts.py`: Tests for rental contract creation and management
- `test_admin.py`: Tests for admin functionality (user/property approval, dashboard stats)
- `test_blockchain.py`: Tests for blockchain integration services
- `test_main.py`: Tests for application-wide functionality (CORS, error handling)

## Test Setup

The tests use pytest fixtures defined in `conftest.py` to:
- Create a test in-memory SQLite database
- Set up test clients
- Create test users (tenant, landlord, admin)
- Generate authentication tokens

## Running Tests

### On Windows:

```cmd
# From the project root
cd backend
run_tests.bat
```

### On Unix/Linux/Mac:

```bash
# From the project root
cd backend
chmod +x run_tests.sh
./run_tests.sh
```

### Running Specific Tests

To run specific test modules:

```bash
# Run only authentication tests
pytest tests/test_auth.py -v

# Run only property tests
pytest tests/test_properties.py -v

# Run only blockchain service tests
pytest tests/test_blockchain.py -v
```

To run specific test functions:

```bash
# Run a specific test function
pytest tests/test_auth.py::test_login_valid_credentials -v

# Run tests matching a pattern
pytest -xvs -k "admin" tests/
```

## Test Categories

Using markers, you can run specific categories of tests:

```bash
# Run only unit tests
pytest -m "unit" tests/

# Run only integration tests
pytest -m "integration" tests/

# Run all tests except slow ones
pytest -m "not slow" tests/
```

## Test Database

Tests use an in-memory SQLite database, which is created fresh for each test function.
This ensures test isolation and prevents tests from interfering with each other.

The database fixture (`db` in conftest.py) creates the database schema before each test
and tears it down afterward, ensuring a clean slate for every test.

## Mocking

External services (especially blockchain interactions) are mocked to avoid actual
network calls during testing. The `test_blockchain.py` file demonstrates how to
properly mock Web3 interactions using:

- `unittest.mock.patch` to mock modules and classes
- `unittest.mock.MagicMock` to create mock objects with specific behaviors
- Temporary files via `pytest`'s `tmp_path` fixture

## Test Coverage

After running tests with `run_tests.sh` or `run_tests.bat`, an HTML coverage report will be generated
in the `htmlcov` directory. Open `htmlcov/index.html` in a browser to see the
detailed coverage report.

Coverage metrics include:
- Line coverage: percentage of code lines executed during tests
- Branch coverage: percentage of code branches (if/else) tested
- Function coverage: percentage of functions called during tests

## Debugging Tests

To debug failing tests, you can increase verbosity and include print statements:

```bash
# Run with increased verbosity
pytest -vv tests/test_auth.py

# Show print statements in test output
pytest -v tests/test_auth.py -s

# Show locals in tracebacks
pytest --showlocals tests/test_auth.py
```

## CI Integration

These tests are designed to run in CI environments. The test configuration 
automatically handles database setup and teardown, and all external service 
calls are properly mocked. 