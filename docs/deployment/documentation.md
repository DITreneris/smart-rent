# Documentation Deployment

This document outlines how the SmartRent documentation is built, tested, and deployed.

## Documentation Infrastructure

SmartRent documentation uses the following technology stack:

- **MkDocs**: Documentation static site generator
- **Material for MkDocs**: Theme and extended functionality
- **GitHub Actions**: CI/CD pipeline for testing and deployment
- **GitHub Pages**: Staging environment for documentation
- **AWS S3 + CloudFront**: Production hosting environment

## Documentation Workflow

The documentation follows a structured workflow:

1. **Development**: Documentation is written in Markdown in the `docs/` directory
2. **Testing**: Automated checks validate the documentation quality
3. **Staging**: Documentation is deployed to GitHub Pages for review
4. **Production**: After review, documentation is deployed to the production environment

## CI/CD Pipeline

### Documentation Testing

Every time changes are made to the documentation (either directly or via a pull request), the documentation testing workflow runs automatically. This workflow is defined in `.github/workflows/docs-test.yml`.

The testing process includes:

- **Build validation**: Ensuring the documentation builds successfully with `mkdocs build --strict`
- **Link checking**: Validating all internal and external links
- **Spell checking**: Checking for spelling errors with a custom dictionary
- **Markdown syntax validation**: Ensuring consistent formatting
- **Mermaid diagram validation**: Testing that all diagrams are correctly formatted

For pull requests, a preview of the documentation is deployed for review.

### Documentation Deployment

When documentation changes are merged to the `main` branch, the deployment workflow (`.github/workflows/docs-deploy.yml`) automatically:

1. Builds the documentation
2. Deploys it to GitHub Pages as a staging environment
3. If the changes are on the `main` branch, also deploys to the production environment (AWS S3 + CloudFront)

The production deployment includes:

- Syncing the built documentation to an S3 bucket
- Invalidating the CloudFront cache to ensure users see the latest version

## Manual Deployment

Documentation can also be manually deployed using the "workflow_dispatch" trigger on the GitHub Actions workflow.

To manually trigger a deployment:

1. Go to the GitHub repository
2. Navigate to Actions → Documentation Deployment
3. Click "Run workflow"
4. Select the branch and click "Run workflow"

## Local Development

To work on the documentation locally:

1. Install the required dependencies:
   ```bash
   pip install mkdocs-material mkdocs-minify-plugin mkdocs-git-revision-date-localized-plugin mkdocs-social pymdown-extensions
   ```

2. Run the local development server:
   ```bash
   mkdocs serve
   ```

3. View the documentation at `http://localhost:8000`

## Adding New Documentation

When adding new documentation:

1. Add the Markdown file to the appropriate directory under `docs/`
2. Update the navigation in `mkdocs.yml` if needed
3. Ensure all links are relative and work correctly
4. Add any new technical terms to `.github/wordlist.txt`

## Best Practices

- **Use relative links** between documentation pages
- **Include diagrams** where they add clarity (using Mermaid)
- **Add code examples** with proper syntax highlighting
- **Keep the documentation up-to-date** with code changes
- **Follow the established structure** and formatting conventions 