import argparse
import sys
from .org_mover.cli import org_mover_command

def main():
    """Main entry point for the hf-hub-utils command."""
    parser = argparse.ArgumentParser(
        description='Hugging Face Hub Utilities - A collection of tools for managing HF Hub resources'
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add org-mover command
    org_mover_parser = subparsers.add_parser(
        'org-mover',
        help='Move repositories between organizations'
    )
    # Add org-mover specific arguments
    org_mover_parser.add_argument('--source', '-s', required=True,
                               help='Source organization name')
    org_mover_parser.add_argument('--target', '-t', required=True,
                               help='Target organization name')
    org_mover_parser.add_argument('--token', 
                               help='Hugging Face API token (if not provided, will use HF_TOKEN from environment)')
    org_mover_parser.add_argument('--exceptions', '-e',
                               help='Path to exceptions file (optional)',
                               default='exceptions.txt')
    org_mover_parser.add_argument('--debug', '-d', action='store_true',
                               help='Enable debug logging')
    
    # If no command is provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()
    
    # Route to appropriate command
    if args.command == 'org-mover':
        from .org_mover.cli import org_mover_command
        org_mover_command(args)
    elif args.command is None:
        parser.print_help()
        sys.exit(1)
    else:
        parser.error(f"Unknown command: {args.command}")

if __name__ == '__main__':
    main()