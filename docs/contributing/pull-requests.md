# Pull Request Guidelines

This document outlines the process for submitting pull requests to the SmartRent project. Following these guidelines helps ensure that your contributions can be quickly reviewed and merged.

## Before Creating a Pull Request

1. **Check Existing Issues and PRs**
   - Search through existing issues and pull requests to avoid duplicating work
   - If you're fixing a bug, check if an issue exists and reference it in your PR
   - If no issue exists for a bug fix, create one first

2. **Create a Feature Branch**
   - Don't work directly on `main` or `develop` branches
   - Create a feature branch with a descriptive name:
     ```bash
     git checkout -b feature/add-wallet-integration
     # or
     git checkout -b fix/login-error
     ```

3. **Follow Code Style Guidelines**
   - Ensure your code follows our [code style guidelines](code-style.md)
   - Run linters and formatters before committing

4. **Write Tests**
   - Add tests for new features
   - Fix or add tests for bug fixes
   - Make sure all tests pass locally

## Creating a Pull Request

1. **Push Your Branch**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create the Pull Request**
   - Go to the SmartRent repository on GitHub
   - Click "New Pull Request"
   - Select your branch and the target branch (usually `develop`)
   - Fill out the PR template with all required information

3. **PR Title Format**
   Follow the [conventional commits](https://www.conventionalcommits.org/) format:
   ```
   feat: add wallet integration
   fix: resolve login error on mobile devices
   docs: update API documentation
   ```

4. **PR Description**
   Include the following in your PR description:
   - Summary of changes
   - Issue number(s) being fixed (e.g., "Fixes #123")
   - Screenshots or GIFs for UI changes
   - Any specific review feedback you're looking for
   - Any potential concerns or areas needing extra attention

5. **PR Size**
   - Keep PRs small and focused on a single task
   - Large changes should be broken into smaller, logical PRs when possible
   - Consider creating a draft PR for work in progress

## PR Template

```markdown
## Description
[Provide a brief description of your changes]

## Related Issue(s)
- Fixes #[issue number]

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code cleanup or refactor

## Testing
- [ ] New tests added to cover changes
- [ ] All new and existing tests passing

## Screenshots (if appropriate)
[Add screenshots here]

## Checklist
- [ ] My code follows the project's code style
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings or errors
- [ ] I have updated tests for my changes
```

## After Submitting a PR

1. **CI/CD Checks**
   - GitHub Actions will run tests and linting on your PR
   - Fix any issues that arise from these checks

2. **Code Review**
   - A project maintainer will review your PR
   - Be open to feedback and make requested changes
   - Respond to all comments and questions

3. **Address Review Feedback**
   - Make necessary changes based on review feedback
   - Push additional commits to your branch
   - Use clear commit messages for your changes
   - Avoid force-pushing unless absolutely necessary

4. **PR Approval and Merge**
   - PRs require approval from at least one maintainer
   - Once approved, a maintainer will merge your PR
   - In some cases, you might be asked to rebase your branch before merging

## Review Process

The review process typically includes:

1. **Automated Checks**
   - Linting and code style verification
   - Test coverage and passing tests
   - Build verification

2. **Code Review**
   - Functionality review
   - Code quality and maintainability
   - Security considerations
   - Performance implications

3. **Final Verification**
   - Documentation completeness
   - Integration with existing systems
   - Adherence to project standards

## After Your PR is Merged

1. **Delete Your Branch**
   ```bash
   git branch -d feature/your-feature-name
   ```

2. **Update Your Fork**
   ```bash
   git checkout main
   git pull upstream main
   git push origin main
   ```

3. **Celebrate Your Contribution!** 🎉
   - Your contribution is now part of SmartRent
   - Thank you for making the project better!

## Need Help?

If you need help with the PR process:
- Ask in the related issue
- Join our community chat
- Contact a project maintainer directly

Thank you for contributing to SmartRent! 