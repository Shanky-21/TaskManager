#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Run administrative tasks."""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')
        logger.info("Django settings module configured successfully")
        
        try:
            from django.core.management import execute_from_command_line
            logger.info("Django core management imported successfully")
        except ImportError as exc:
            logger.error(f"Failed to import Django: {exc}")
            logger.error("Please make sure Django is installed in your virtual environment")
            logger.error("You can install it using: python3 -m pip install django")
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed?"
            ) from exc
            
        logger.info("Starting Django command execution")
        execute_from_command_line(sys.argv)
        
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise

if __name__ == '__main__':
    main() 