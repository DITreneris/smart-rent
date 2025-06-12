# Testing Standards

## Overview

This document outlines the testing standards for the SmartRent project to ensure consistent, reliable, and maintainable tests across the codebase.

## Test Coverage Goals

- **Backend (Python)**: Minimum 80% code coverage
- **Frontend (React/TypeScript)**: Minimum 70% code coverage
- **Smart Contracts (Solidity)**: 100% code coverage

## Testing Levels

### Unit Tests

- Test individual functions and classes in isolation
- Mock external dependencies
- Should be fast and lightweight

### Integration Tests

- Test interactions between components
- Test database operations with test databases
- Test API endpoints with simulated requests

### End-to-End Tests

- Test complete user flows
- Simulate real user interactions
- Include frontend and backend integration

### Contract Tests

- Test smart contract functionality
- Verify correct behavior of contract methods
- Test edge cases and security concerns

## Test Structure

### Python (pytest)

```python
# tests/test_example.py
import pytest
from app.services.example import ExampleService

class TestExampleService:
    @pytest.fixture
    def service(self):
        """Setup fixture for the test class."""
        return ExampleService()
    
    def test_method_success_case(self, service):
        """Test the expected behavior when method succeeds."""
        # Arrange
        expected_result = "expected value"
        
        # Act
        result = service.method()
        
        # Assert
        assert result == expected_result
    
    def test_method_error_case(self, service):
        """Test error handling in the method."""
        # Arrange
        invalid_input = None
        
        # Act & Assert
        with pytest.raises(ValueError):
            service.method(invalid_input)
```

### JavaScript/TypeScript (Jest)

```typescript
// src/__tests__/example.test.ts
import { ExampleService } from '../services/example';

describe('ExampleService', () => {
  let service: ExampleService;
  
  beforeEach(() => {
    // Setup for each test
    service = new ExampleService();
  });
  
  test('method should return expected value on success', () => {
    // Arrange
    const expected = 'expected value';
    
    // Act
    const result = service.method();
    
    // Assert
    expect(result).toBe(expected);
  });
  
  test('method should throw error on invalid input', () => {
    // Arrange, Act & Assert
    expect(() => {
      service.method(null);
    }).toThrow(Error);
  });
});
```

### Solidity (Hardhat/Truffle)

```javascript
// test/ExampleContract.test.js
const { expect } = require('chai');
const { ethers } = require('hardhat');

describe('ExampleContract', function () {
  let exampleContract;
  let owner;
  let addr1;
  let addr2;
  
  beforeEach(async function () {
    // Deploy a new contract for each test
    const ExampleContract = await ethers.getContractFactory('ExampleContract');
    [owner, addr1, addr2] = await ethers.getSigners();
    exampleContract = await ExampleContract.deploy();
    await exampleContract.deployed();
  });
  
  describe('method', function () {
    it('Should return expected value on success', async function () {
      // Arrange
      const expected = 'expected value';
      
      // Act
      const result = await exampleContract.method();
      
      // Assert
      expect(result).to.equal(expected);
    });
    
    it('Should revert on invalid input', async function () {
      // Arrange, Act & Assert
      await expect(
        exampleContract.method(0)
      ).to.be.revertedWith('Invalid input');
    });
  });
});
```

## Naming Conventions

- Test files: `test_<module_name>.py` (Python), `<module_name>.test.ts` (TypeScript)
- Test classes: `Test<ClassUnderTest>` (Python)
- Test methods/functions: `test_<method_name>_<scenario>` (Python), `should <expected behavior>` (JavaScript/TypeScript)

## Best Practices

1. **Follow AAA pattern**: Arrange, Act, Assert
2. **One assertion per test**: Focus each test on a single behavior
3. **Use descriptive test names**: Name should describe what is being tested
4. **Isolate tests**: Tests should not depend on each other
5. **Avoid test logic**: Tests should be simple and straightforward
6. **Mock external dependencies**: Use mocking frameworks to isolate the code under test
7. **Test edge cases**: Include tests for boundary conditions and error cases
8. **Keep tests fast**: Slow tests discourage frequent testing
9. **Write tests first**: Consider Test-Driven Development (TDD) approach
10. **Maintain tests**: Update tests when code changes

## CI/CD Integration

- Tests run automatically on pull requests
- Pull requests cannot be merged if tests fail
- Code coverage reports are generated and stored
- Coverage thresholds are enforced

## Tools

- **Python**: pytest, pytest-cov
- **JavaScript/TypeScript**: Jest, React Testing Library
- **Solidity**: Hardhat, Chai, Waffle
- **CI/CD**: GitHub Actions 