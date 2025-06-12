"""
Alembic environment script for running migrations
"""

import asyncio
from logging.config import fileConfig
import os
import sys
from pathlib import Path

# from sqlalchemy import engine_from_config # Removed, using create_async_engine
from sqlalchemy.ext.asyncio import create_async_engine # Added
from sqlalchemy import pool
from alembic import context

# Add parent directory to sys.path
parent_dir = Path(__file__).parent.parent.parent.absolute()
sys.path.append(str(parent_dir))

# Import database settings
from app.core.config import settings

# Import all models for Alembic to detect
from app.db.base import Base
# Ensure all your SQLAlchemy models are imported here directly or indirectly
# For example:
from app.models.user import User
from app.models.property import Property
# from app.models.transaction import Transaction # Make sure Transaction uses Base if needed for Alembic

# --- Removed sync_db_url logic ---
# sync_db_url = str(settings.DATABASE_URL).replace('aiomysql', 'pymysql')

# Load environment-specific configuration
config = context.config

# --- Use actual DATABASE_URL from settings ---
# config.set_main_option("sqlalchemy.url", sync_db_url) # Removed
# Set database url using settings (Alembic will use this if not overridden)
if settings.DATABASE_URL:
    config.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for autogenerate support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable here as well.
    By skipping the Engine creation we don't even need a DBAPI to be available.
    
    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    """Helper function to run migrations within a transaction."""
    context.configure(
        connection=connection, 
        target_metadata=target_metadata,
        # include_schemas=True, # Consider if using multiple schemas
        compare_type=True, # Compare types when autogenerating
        # render_item=render_item # Uncomment if custom rendering is needed
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode using an async engine."""
    
    # Create async engine directly from settings
    connectable = create_async_engine(
        str(settings.DATABASE_URL), # Use the actual async URL
        poolclass=pool.NullPool,
        future=True, # Ensure SQLAlchemy 2.0 style is used
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    # Dispose the engine after use
    await connectable.dispose()

# --- Removed custom render_item, uncomment if needed ---
# def render_item(type_, obj, autogen_context):
#     """Custom rendering for migration items"""
#     # Example: Add import for sqlalchemy types if needed
#     # if type_ == 'type' and isinstance(obj, YourCustomType):
#     #     autogen_context.imports.add("import sqlalchemy")
#     #     return "sqlalchemy.YourCustomType()"
#     return False


# Run migrations based on the execution mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online()) 