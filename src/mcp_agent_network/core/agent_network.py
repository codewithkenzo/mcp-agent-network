"""Main AgentNetwork class for managing the agent network."""

import logging
from typing import Dict, List, Optional, Any

from mcp_agent_network.mcp.connection_manager import MCPConnectionManager

# Configure logging
logger = logging.getLogger(__name__)


class AgentNetwork:
    """Main agent network orchestration class.
    
    This is the primary interface for interacting with the MCP Agent Network.
    It handles coordination between MCP clients, Upsonic orchestration,
    and browser automation tools.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the agent network.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.mcp_connection_manager = MCPConnectionManager()
        self.orchestrator = None
        self.browser_tools = None
        
        # Apply configuration settings
        self._apply_config()
        
    def _apply_config(self) -> None:
        """Apply configuration settings."""
        # Configure MCP servers from config
        if "mcp_servers" in self.config:
            for server_name, server_config in self.config["mcp_servers"].items():
                api_key = server_config.get("api_key")
                self.mcp_connection_manager.add_server(server_name, api_key)
        
    def connect_to_servers(self, server_names: List[str], show_progress: bool = True) -> bool:
        """Connect to MCP servers.
        
        Args:
            server_names: List of server names to connect to (e.g., "glama", "smithery")
            show_progress: Whether to show connection progress
            
        Returns:
            bool: True if all connections successful, False otherwise
        """
        results = self.mcp_connection_manager.connect_to_servers(server_names, show_progress)
        
        # Check if all connections were successful
        all_successful = all(result.get("success", False) for result in results.values())
        
        if all_successful:
            logger.info(f"Successfully connected to all servers: {', '.join(server_names)}")
        else:
            failed_servers = [
                server for server, result in results.items() 
                if not result.get("success", False)
            ]
            logger.warning(f"Failed to connect to some servers: {', '.join(failed_servers)}")
        
        return all_successful
        
    def disconnect_from_servers(self) -> bool:
        """Disconnect from all connected MCP servers.
        
        Returns:
            bool: True if all disconnections successful, False otherwise
        """
        results = self.mcp_connection_manager.disconnect_from_all()
        return all(results.values())
        
    def get_server_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all MCP server connections.
        
        Returns:
            Dictionary of server names to status information
        """
        return self.mcp_connection_manager.update_all_statuses()
        
    def execute_task(self, task_description: str) -> Any:
        """Execute a task using the agent network.
        
        Args:
            task_description: Description of the task to execute
            
        Returns:
            Any: Result of the task execution
        """
        # Check if we're connected to any servers
        connected_servers = self.mcp_connection_manager.get_connected_servers()
        if not connected_servers:
            logger.error("Cannot execute task: not connected to any MCP servers")
            return {"error": "Not connected to any MCP servers"}
        
        logger.info(f"Executing task: {task_description}")
        
        # Create task message
        task_message = {
            "type": "task",
            "content": task_description,
            "timestamp": None,  # Will be filled by send_message
        }
        
        # Broadcast to all connected servers
        responses = self.mcp_connection_manager.broadcast_message(task_message)
        
        # Process responses
        # In a real implementation, we would coordinate responses and return results
        logger.info(f"Received responses from {len(responses)} servers")
        
        return {
            "task": task_description,
            "servers_responded": list(responses.keys()),
            "status": "submitted",
        }
        
    def chat_with_agent(self, agent_id: str, message: str) -> str:
        """Chat with a specific agent.
        
        Args:
            agent_id: ID of the agent to chat with
            message: Message to send to the agent
            
        Returns:
            str: Response from the agent
        """
        # Check if we're connected to any servers
        connected_servers = self.mcp_connection_manager.get_connected_servers()
        if not connected_servers:
            logger.error(f"Cannot chat with agent {agent_id}: not connected to any MCP servers")
            return f"Error: Not connected to any MCP servers"
        
        logger.info(f"Sending message to agent {agent_id}: {message}")
        
        # Create chat message
        chat_message = {
            "type": "chat",
            "agent_id": agent_id,
            "content": message,
            "timestamp": None,  # Will be filled by send_message
        }
        
        # Broadcast to all connected servers
        responses = self.mcp_connection_manager.broadcast_message(chat_message)
        
        # Process responses
        # In a real implementation, we would find the response from the right server
        logger.info(f"Received responses from {len(responses)} servers")
        
        return f"Message sent to agent {agent_id} via {len(responses)} servers" 