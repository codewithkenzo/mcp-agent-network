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
    
    # Connect command
    connect_parser = subparsers.add_parser("connect", help="Connect to MCP servers")
    connect_parser.add_argument("--servers", nargs="+", help="List of server names to connect to")
    connect_parser.add_argument("--no-progress", action="store_true", help="Disable progress bar")
    
    # Status command
    subparsers.add_parser("status", help="Show MCP server connection status")
    
    # Disconnect command
    subparsers.add_parser("disconnect", help="Disconnect from MCP servers")
    
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
    
    # Execute requested command
    if parsed_args.command == "connect":
        server_names = parsed_args.servers or ["glama", "smithery"]
        show_progress = not parsed_args.no_progress
        
        print(f"Connecting to MCP servers: {', '.join(server_names)}...")
        success = network.connect_to_servers(server_names, show_progress=show_progress)
        
        if success:
            print("✅ Successfully connected to all MCP servers")
        else:
            print("⚠️ Failed to connect to some MCP servers")
            return 1
    
    elif parsed_args.command == "status":
        statuses = network.get_server_status()
        
        if not statuses:
            print("No MCP server connections configured")
            return 0
        
        print("MCP Server Status:")
        for server_name, status in statuses.items():
            print(f"  • {server_name}: {status['status']}")
            
            if status['status'] == 'connected':
                print(f"    - Latency: {status['connection_latency']}")
                print(f"    - Last ping: {status['time_since_ping']} ago")
                if 'features' in status:
                    print(f"    - Features: {', '.join(status['features'])}")
    
    elif parsed_args.command == "disconnect":
        print("Disconnecting from MCP servers...")
        success = network.disconnect_from_servers()
        
        if success:
            print("✅ Successfully disconnected from all MCP servers")
        else:
            print("⚠️ Failed to disconnect from some MCP servers")
            return 1
    
    elif parsed_args.command == "chat":
        # First check if we're connected to any servers
        statuses = network.get_server_status()
        connected = any(status.get('status') == 'connected' for status in statuses.values())
        
        if not connected:
            print("⚠️ Not connected to any MCP servers. Connect first with 'connect' command.")
            return 1
        
        print(f"Sending message to agent {parsed_args.agent_id}...")
        response = network.chat_with_agent(parsed_args.agent_id, parsed_args.message)
        print(f"Response: {response}")
    
    elif parsed_args.command == "task":
        # First check if we're connected to any servers
        statuses = network.get_server_status()
        connected = any(status.get('status') == 'connected' for status in statuses.values())
        
        if not connected:
            print("⚠️ Not connected to any MCP servers. Connect first with 'connect' command.")
            return 1
        
        print(f"Executing task: {parsed_args.description}")
        result = network.execute_task(parsed_args.description)
        print(f"Task submitted with status: {result.get('status', 'unknown')}")
        print(f"Servers responded: {', '.join(result.get('servers_responded', []))}")
    
    else:
        print("Please specify a command. Run with --help for more information.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 