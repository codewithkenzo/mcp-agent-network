"""MCP connection manager for handling multiple server connections."""

import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Any, Tuple

from mcp_agent_network.mcp.client import MCPClient
from mcp_agent_network.mcp.progress import ProgressBar

# Configure logging
logger = logging.getLogger(__name__)


class MCPConnectionManager:
    """Manages connections to multiple MCP servers.
    
    Provides a unified interface for connecting to and communicating with
    different MCP servers like glama and smithery.
    """
    
    def __init__(self):
        """Initialize the connection manager."""
        self.clients: Dict[str, MCPClient] = {}
        self.connection_statuses: Dict[str, Dict[str, Any]] = {}
        self.default_servers = ["glama", "smithery"]
        
    def add_server(self, server_name: str, api_key: Optional[str] = None) -> bool:
        """Add a server to the manager.
        
        Args:
            server_name: Name of the server to add
            api_key: Optional API key for authentication
            
        Returns:
            Success status
        """
        if server_name in self.clients:
            logger.warning(f"Server {server_name} already exists")
            return False
        
        logger.info(f"Adding server: {server_name}")
        self.clients[server_name] = MCPClient(server_name, api_key)
        return True
    
    def remove_server(self, server_name: str) -> bool:
        """Remove a server from the manager.
        
        Args:
            server_name: Name of the server to remove
            
        Returns:
            Success status
        """
        if server_name not in self.clients:
            logger.warning(f"Server {server_name} not found")
            return False
        
        # Disconnect first if connected
        if self.clients[server_name].connected:
            self.clients[server_name].disconnect()
        
        logger.info(f"Removing server: {server_name}")
        del self.clients[server_name]
        if server_name in self.connection_statuses:
            del self.connection_statuses[server_name]
        return True
    
    def connect_to_servers(self, server_names: Optional[List[str]] = None, 
                           show_progress: bool = True) -> Dict[str, Dict[str, Any]]:
        """Connect to specified servers.
        
        Args:
            server_names: List of server names to connect to, or None for all
            show_progress: Whether to show a progress bar
            
        Returns:
            Dictionary of server names to connection results
        """
        server_names = server_names or list(self.clients.keys())
        if not server_names:
            # Add default servers if none specified and none added
            for server in self.default_servers:
                self.add_server(server)
            server_names = self.default_servers
        
        # Make sure all servers are in the client list
        for server in server_names:
            if server not in self.clients:
                self.add_server(server)
        
        total_servers = len(server_names)
        logger.info(f"Connecting to {total_servers} MCP servers: {', '.join(server_names)}")
        
        results = {}
        progress = ProgressBar(total_servers, "Connecting to MCP servers") if show_progress else None
        
        # Use ThreadPoolExecutor for parallel connections
        with ThreadPoolExecutor(max_workers=min(total_servers, 5)) as executor:
            # Submit connection tasks
            future_to_server = {
                executor.submit(self.clients[server].connect): server
                for server in server_names
            }
            
            # Process results as they complete
            for i, future in enumerate(as_completed(future_to_server)):
                server = future_to_server[future]
                try:
                    success, info = future.result()
                    results[server] = {
                        "success": success,
                        "info": info
                    }
                    if progress:
                        progress.update(i + 1, f"Connected to {server}")
                except Exception as e:
                    logger.error(f"Error connecting to {server}: {e}")
                    results[server] = {
                        "success": False,
                        "error": str(e)
                    }
                    if progress:
                        progress.update(i + 1, f"Failed to connect to {server}")
        
        if progress:
            progress.finish()
        
        # Update status cache
        self.update_all_statuses()
        
        return results
    
    def disconnect_from_all(self) -> Dict[str, bool]:
        """Disconnect from all servers.
        
        Returns:
            Dictionary of server names to disconnection results
        """
        results = {}
        for server_name, client in self.clients.items():
            results[server_name] = client.disconnect()
        
        # Update status cache
        self.update_all_statuses()
        
        return results
    
    def update_all_statuses(self) -> Dict[str, Dict[str, Any]]:
        """Update status information for all servers.
        
        Returns:
            Dictionary of server names to status information
        """
        for server_name, client in self.clients.items():
            self.connection_statuses[server_name] = client.get_status()
        return self.connection_statuses
    
    def get_connected_servers(self) -> List[str]:
        """Get a list of connected server names.
        
        Returns:
            List of server names that are currently connected
        """
        return [
            server_name for server_name, client in self.clients.items()
            if client.connected
        ]
    
    def get_client(self, server_name: str) -> Optional[MCPClient]:
        """Get the client for a specific server.
        
        Args:
            server_name: Name of the server
            
        Returns:
            MCPClient instance or None if not found
        """
        return self.clients.get(server_name)
    
    def broadcast_message(self, message: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Broadcast a message to all connected servers.
        
        Args:
            message: Message to broadcast
            
        Returns:
            Dictionary of server names to response information
        """
        responses = {}
        for server_name, client in self.clients.items():
            if client.connected:
                responses[server_name] = client.send_message(message)
        return responses 