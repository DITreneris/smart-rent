#!/usr/bin/env python3
"""
Build script for SmartRent documentation.
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path

# Set up paths
ROOT_DIR = Path(__file__).parent.parent
DOCS_DIR = ROOT_DIR / "docs"
SITE_DIR = ROOT_DIR / "site"

def install_dependencies():
    """Install documentation dependencies."""
    requirements_file = DOCS_DIR / "requirements.txt"
    print(f"Installing documentation dependencies from {requirements_file}...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
        check=True
    )
    print("Dependencies installed successfully.")

def build_docs():
    """Build the documentation site."""
    print("Building documentation...")
    subprocess.run(
        ["mkdocs", "build", "--clean"],
        check=True,
        cwd=ROOT_DIR
    )
    print(f"Documentation built successfully in {SITE_DIR}")

def serve_docs():
    """Serve the documentation site locally."""
    print("Starting documentation server...")
    subprocess.run(
        ["mkdocs", "serve"],
        check=True,
        cwd=ROOT_DIR
    )

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Build and serve SmartRent documentation")
    parser.add_argument("--install", action="store_true", help="Install dependencies")
    parser.add_argument("--build", action="store_true", help="Build documentation")
    parser.add_argument("--serve", action="store_true", help="Serve documentation locally")
    args = parser.parse_args()

    # Default behavior: install and serve
    if not (args.install or args.build or args.serve):
        args.install = True
        args.serve = True

    if args.install:
        install_dependencies()
    
    if args.build:
        build_docs()
    
    if args.serve:
        serve_docs()

if __name__ == "__main__":
    main() 