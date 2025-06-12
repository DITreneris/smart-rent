#!/usr/bin/env python3
"""
Script to run database migrations.
Provides a simple CLI for running database migrations:
- Create database if it doesn't exist
- Upgrade to latest version
- Downgrade to previous version
- Create new migration
"""

import os
import sys
import argparse
import logging
from typing import List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
MIGRATIONS_DIR = os.path.join("app", "migrations")

def run_alembic_command(command: str, args: Optional[List[str]] = None):
    """Run an Alembic command with optional arguments."""
    if args is None:
        args = []
    
    cmd = f"alembic -c {os.path.join(MIGRATIONS_DIR, 'alembic.ini')} {command} {' '.join(args)}"
    logger.info(f"Running: {cmd}")
    
    result = os.system(cmd)
    if result != 0:
        logger.error(f"Command failed with exit code: {result}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Database migration tool")
    parser.add_argument(
        "command",
        choices=["upgrade", "downgrade", "revision", "current", "history", "show"],
        help="Migration command to run"
    )
    parser.add_argument(
        "--revision",
        default="head",
        help="Revision identifier (default: head)"
    )
    parser.add_argument(
        "--message", "-m",
        help="Message for revision"
    )
    parser.add_argument(
        "--autogenerate",
        action="store_true",
        help="Autogenerate migration based on model changes"
    )
    
    args = parser.parse_args()
    
    if args.command == "revision":
        cmd_args = ["--rev-id", args.revision]
        if args.message:
            cmd_args.extend(["-m", args.message])
        if args.autogenerate:
            cmd_args.append("--autogenerate")
        run_alembic_command("revision", cmd_args)
    
    elif args.command in ["upgrade", "downgrade"]:
        run_alembic_command(args.command, [args.revision])
    
    else:  # current, history, show
        run_alembic_command(args.command)

if __name__ == "__main__":
    main() 