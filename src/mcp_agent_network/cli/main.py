"""Command-line interface for the MCP Agent Network."""

import argparse
import sys
from typing import List, Optional

from mcp_agent_network import AgentNetwork


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments.
    
    Args:
        args: Command line arguments (defaults to sys.argv[1:])
        
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(description="MCP Agent Network CLI")
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Chat with an agent")
    chat_parser.add_argument("agent_id", help="ID of the agent to chat with")
    chat_parser.add_argument("message", help="Message to send to the agent")
    
    # Execute task command
    task_parser = subparsers.add_parser("task", help="Execute a task")
    task_parser.add_argument("description", help="Description of the task to execute")
    
    # Parse arguments
    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI.
    
    Args:
        args: Command line arguments (defaults to sys.argv[1:])
        
    Returns:
        Exit code
    """
    parsed_args = parse_args(args)
    
    # Initialize agent network
    network = AgentNetwork()
    
    # Connect to default servers
    network.connect_to_servers(["glama", "smithery"])
    
    # Execute requested command
    if parsed_args.command == "chat":
        response = network.chat_with_agent(parsed_args.agent_id, parsed_args.message)
        print(response)
    elif parsed_args.command == "task":
        result = network.execute_task(parsed_args.description)
        print(result)
    else:
        print("Please specify a command. Run with --help for more information.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 