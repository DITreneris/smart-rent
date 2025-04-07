"""
Background Tasks Manager

This module handles starting and stopping background tasks for the application.
"""

import asyncio
import logging
import time
from typing import List, Dict, Any

from app.middlewares.csrf import cleanup_expired_tokens

logger = logging.getLogger(__name__)


async def start_background_tasks() -> List[asyncio.Task]:
    """
    Start all background tasks for the application.
    
    Returns:
        List of running background tasks
    """
    tasks = []
    
    # Start token cleanup task
    tasks.append(asyncio.create_task(periodic_token_cleanup()))
    
    logger.info(f"Started {len(tasks)} background tasks")
    return tasks


async def stop_background_tasks() -> None:
    """
    Stop all running background tasks.
    """
    # With Python 3.7+, we can use asyncio.all_tasks() to get all tasks
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    
    for task in tasks:
        if not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
    
    logger.info(f"Stopped {len(tasks)} background tasks")


async def periodic_token_cleanup() -> None:
    """
    Periodically clean up expired CSRF tokens.
    Runs every 15 minutes.
    """
    while True:
        try:
            # Clean up expired tokens
            count = await cleanup_expired_tokens()
            if count > 0:
                logger.info(f"Cleaned up {count} expired CSRF tokens")
            
            # Sleep for 15 minutes
            await asyncio.sleep(15 * 60)
        except asyncio.CancelledError:
            # Task was cancelled, exit cleanly
            logger.info("Token cleanup task cancelled")
            break
        except Exception as e:
            # Log other exceptions but don't crash the task
            logger.error(f"Error in token cleanup task: {e}")
            
            # Sleep for a shorter period before retrying
            await asyncio.sleep(60) 