"""
Alembic environment script for running migrations
"""

from logging.config import fileConfig
import os
import sys
from pathlib import Path

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Add parent directory to sys.path
parent_dir = Path(__file__).parent.parent.parent.absolute()
sys.path.append(str(parent_dir))

# Import database settings
from app.core.config import settings

# Import all models for Alembic to detect
from app.db.base import Base
from app.models.user import User
from app.models.property import Property
from app.models.transaction import Transaction

# Database URL modification for synchronous migrations
# Convert from aiomysql to pymysql for synchronous operations during migrations
sync_db_url = str(settings.DATABASE_URL).replace('aiomysql', 'pymysql')

# Load environment-specific configuration
config = context.config

# Set up database URL from environment with synchronous adapter
config.set_main_option("sqlalchemy.url", sync_db_url)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for autogenerate support
target_metadata = Base.metadata


def run_migrations_offline():
    """
    Run migrations in 'offline' mode.
    
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


def run_migrations_online():
    """
    Run migrations in 'online' mode.
    
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = sync_db_url
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    
    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            # Include schemas in autogenerate
            include_schemas=True,
            # Compare types when autogenerating
            compare_type=True,
            # Include foreign keys in migration
            render_item=render_item
        )
        
        with context.begin_transaction():
            context.run_migrations()


def render_item(type_, obj, autogen_context):
    """Custom rendering for migration items"""
    return autogen_context.imports.add("sqlalchemy"), False


# Run migrations based on the execution mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online() 