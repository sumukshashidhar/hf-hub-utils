import argparse
from dotenv import load_dotenv
import os
import sys
from loguru import logger
from ..common.logging import setup_logger
from .mover import move_repos_between_orgs

def org_mover_command(args):
    """Command-line interface for the organization mover tool."""
    load_dotenv()
    
    # Configure logger
    setup_logger(args.debug)
    
    # Get token from args or environment
    token = args.token or os.getenv("HF_TOKEN")
    if not token:
        logger.error("No token provided. Either use --token or set HF_TOKEN environment variable")
        sys.exit(1)
    
    try:
        # Run the move operation
        move_repos_between_orgs(
            source_org=args.source,
            target_org=args.target,
            token=token,
            exceptions_file=args.exceptions,
            debug=args.debug
        )
    except Exception as e:
        logger.error("Failed to complete operation: {}", str(e))
        sys.exit(1)