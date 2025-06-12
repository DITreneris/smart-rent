# Code Style Guidelines

This document outlines the coding standards and style guidelines for the SmartRent project. Following these guidelines helps ensure consistency across the codebase and makes collaboration easier.

## Python Code Style

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code with a few project-specific additions:

### Formatting

- Use 4 spaces for indentation (no tabs)
- Maximum line length is 100 characters
- Use blank lines to group related pieces of code
- Use implicit line continuation inside parentheses, brackets, and braces
- Avoid extraneous whitespace
- End files with a single newline

### Naming Conventions

- **Functions and Variables**: Use `snake_case` for function and variable names
- **Classes**: Use `PascalCase` for class names
- **Constants**: Use `UPPER_CASE_WITH_UNDERSCORES` for constants
- **Private Methods/Variables**: Prefix with a single underscore `_`
- **Protected Methods/Variables**: Prefix with double underscore `__`

### Comments and Docstrings

- Use docstrings for all public modules, functions, classes, and methods
- Follow the Google docstring format:
  ```python
  def function_with_pep8_style(param1, param2):
      """Example function with PEP 8 style docstrings.
      
      Args:
          param1: The first parameter.
          param2: The second parameter.
          
      Returns:
          The return value. True for success, False otherwise.
      
      Raises:
          ValueError: If param1 is None.
      """
      if param1 is None:
          raise ValueError("param1 cannot be None")
      return True
  ```
- Include type hints for function parameters and return values:
  ```python
  def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
      """Get user by ID.
      
      Args:
          user_id: The user ID.
          
      Returns:
          User dictionary or None if not found.
      """
      # Implementation
  ```

### Imports

- Group imports in the following order:
  1. Standard library imports
  2. Related third-party imports
  3. Local application/library-specific imports
- Separate each group with a blank line
- Use absolute imports for packages in the project
- Use relative imports for modules within the same package

## JavaScript/TypeScript Code Style

We use ESLint and Prettier for JavaScript/TypeScript code:

### Formatting

- Use 2 spaces for indentation
- Maximum line length is 100 characters
- Use semicolons at the end of statements
- Use single quotes for strings
- Always use trailing commas in multi-line arrays and objects
- Place opening braces on the same line as the statement

### Naming Conventions

- **Functions and Variables**: Use `camelCase` for function and variable names
- **Classes and Components**: Use `PascalCase` for class and component names
- **Constants**: Use `UPPER_CASE_WITH_UNDERSCORES` for constants
- **Private Methods/Variables**: Prefix with an underscore `_`
- **File Naming**: Use `kebab-case` for file names

### React Components

- Prefer functional components with hooks over class components
- Each component should be in its own file
- Use TypeScript interfaces for prop types
- Keep components focused on a single responsibility
- Extract complex logic into custom hooks

## Solidity Code Style

For Solidity smart contracts, we follow the [Solidity Style Guide](https://docs.soliditylang.org/en/latest/style-guide.html):

### Formatting

- Use 4 spaces for indentation
- Maximum line length is 120 characters
- Function declarations and other blocks should have opening braces on the same line

### Naming Conventions

- **Contracts**: Use `PascalCase` for contract names
- **Functions**: Use `camelCase` for function names
- **Local Variables**: Use `camelCase` for local variables
- **State Variables**: Use `camelCase` for state variables
- **Constants**: Use `UPPER_CASE_WITH_UNDERSCORES` for constants
- **Modifiers**: Use `camelCase` for modifiers
- **Events**: Use `PascalCase` for event names

### NatSpec Comments

- Use NatSpec comments for contracts, interfaces, and functions:
  ```solidity
  /// @title A title that describes the contract/interface
  /// @author The name of the author
  /// @notice Explain to an end user what this does
  /// @dev Explain to a developer any extra details
  contract SimpleToken {
      /// @notice Transfer tokens to a specified address
      /// @param to The address to transfer to
      /// @param amount The amount to be transferred
      /// @return success True if the transfer was successful
      function transfer(address to, uint256 amount) external returns (bool success) {
          // Implementation
      }
  }
  ```

## Testing Guidelines

- All code should have corresponding tests
- Unit tests should be independent and isolated
- Mock external dependencies
- Test both success and failure cases
- For Python, use pytest and aim for >90% code coverage
- For JavaScript/TypeScript, use Jest for unit tests and Cypress for end-to-end tests

## Git Commit Style

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types include:
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation changes
- **style**: Changes that do not affect the code's meaning (formatting)
- **refactor**: Code changes that neither fix a bug nor add a feature
- **test**: Adding or correcting tests
- **chore**: Changes to the build process or auxiliary tools

## Linting and Formatting

We use automated tools to enforce these guidelines:

- **Python**: Black for formatting, isort for imports, Flake8 for linting
- **JavaScript/TypeScript**: ESLint for linting, Prettier for formatting
- **Solidity**: Solhint for linting

Run these tools before committing your changes. 