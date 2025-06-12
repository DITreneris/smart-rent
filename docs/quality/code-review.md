# Code Review Guidelines

## Overview

Code reviews are a critical part of our development process. They help ensure code quality, knowledge sharing, and consistency across the codebase. This document outlines the code review process and guidelines for the SmartRent project.

## Code Review Process

1. **Create a Pull Request**
   - Create a branch for your feature or bugfix
   - Write your code and tests
   - Create a pull request to the appropriate branch (usually `develop`)
   - Fill out the pull request template with all required information

2. **Automated Checks**
   - Wait for CI/CD pipeline to complete
   - Address any issues identified by automated checks

3. **Code Review**
   - Assign at least one reviewer from your team
   - The reviewer will review the code and provide feedback
   - Address all feedback and make necessary changes
   - Request a re-review if significant changes are made

4. **Approval and Merge**
   - Once approved, merge the pull request
   - Delete the feature branch after merging

## Reviewer Guidelines

### Code Quality

- **Functionality**: Does the code work as intended?
- **Simplicity**: Is the code as simple as possible?
- **Readability**: Is the code easy to understand?
- **Maintainability**: Will the code be easy to maintain?
- **Security**: Are there any security concerns?
- **Performance**: Are there any obvious performance issues?
- **Error Handling**: Is error handling appropriate and consistent?

### Standards Compliance

- **Style Guide**: Does the code follow the project's style guide?
- **Documentation**: Is the code properly documented?
- **Testing**: Are there sufficient tests? Do they cover edge cases?
- **Design Patterns**: Does the code follow appropriate design patterns?

### Best Practices

- **Focus on the code, not the author**
- **Be constructive, not critical**
- **Explain why, not just what**
- **Prioritize feedback (critical vs. nitpick)**
- **Ask questions rather than make demands**
- **Respond to all comments**
- **Acknowledge good practices**

## Author Guidelines

### Preparing for Review

- **Self-review** your code before submitting
- **Keep PRs small and focused** (ideally < 400 lines of code)
- **Provide context** in the PR description
- **Include tests** for your changes
- **Update documentation** if necessary

### Responding to Feedback

- **Be open to feedback**, not defensive
- **Address all comments** (fix, explain, or discuss)
- **Thank reviewers** for their feedback
- **Learn from the feedback** for future PRs

## Code Review Checklist

### General

- [ ] Does the code work as intended?
- [ ] Is the code easy to understand?
- [ ] Is there appropriate documentation?
- [ ] Are there sufficient tests?
- [ ] Does the code follow the style guide?

### Security

- [ ] Is user input validated and sanitized?
- [ ] Are there any potential SQL injection vulnerabilities?
- [ ] Are authentication and authorization handled properly?
- [ ] Are sensitive data (API keys, credentials) handled securely?
- [ ] Are potential race conditions addressed?

### Blockchain-Specific

- [ ] Are smart contract functions protected against reentrancy attacks?
- [ ] Is proper access control implemented?
- [ ] Are gas costs optimized?
- [ ] Is error handling appropriate?
- [ ] Has the contract been tested thoroughly?

### Frontend-Specific

- [ ] Is the UI responsive and accessible?
- [ ] Are components reusable where appropriate?
- [ ] Is state management implemented effectively?
- [ ] Are API calls properly handled with loading and error states?
- [ ] Is the UI consistent with the design system?

### Backend-Specific

- [ ] Are database queries optimized?
- [ ] Is the API design consistent and RESTful?
- [ ] Is proper error handling and logging implemented?
- [ ] Are transactions used where appropriate?
- [ ] Is the code properly structured and modular?

## Example Comments

### Constructive

```
The validation logic in this function is duplicated from the one in `user_service.py`. Consider extracting it to a shared utility function to avoid duplication and ensure consistent validation.
```

### Non-Constructive

```
This code is messy and needs to be rewritten.
```

## Time Expectations

- Reviewers should aim to respond within 24 hours
- For complex PRs, communicate expected review timeline
- If a PR is urgent, clearly indicate in the description and notify reviewers directly 