"""Tests for the MCP connection manager."""

import pytest
from mcp_agent_network.mcp import MCPConnectionManager, MCPClient


def test_connection_manager_init():
    """Test MCPConnectionManager initialization."""
    manager = MCPConnectionManager()
    assert manager.clients == {}
    assert manager.connection_statuses == {}
    assert manager.default_servers == ["glama", "smithery"]


def test_add_server():
    """Test adding servers to the manager."""
    manager = MCPConnectionManager()
    
    # Add a server
    assert manager.add_server("test-server") is True
    assert "test-server" in manager.clients
    assert isinstance(manager.clients["test-server"], MCPClient)
    
    # Add a server with API key
    assert manager.add_server("test-server-2", "test-key") is True
    assert manager.clients["test-server-2"].api_key == "test-key"
    
    # Try to add a server that already exists
    assert manager.add_server("test-server") is False


def test_remove_server():
    """Test removing servers from the manager."""
    manager = MCPConnectionManager()
    
    # Try to remove a server that doesn't exist
    assert manager.remove_server("nonexistent-server") is False
    
    # Add and then remove a server
    manager.add_server("test-server")
    assert "test-server" in manager.clients
    
    assert manager.remove_server("test-server") is True
    assert "test-server" not in manager.clients


def test_connect_to_servers():
    """Test connecting to servers."""
    manager = MCPConnectionManager()
    
    # Connect to servers that haven't been added yet
    results = manager.connect_to_servers(["test-server", "test-server-2"], show_progress=False)
    
    assert len(results) == 2
    assert all(result["success"] for result in results.values())
    
    # Check that servers were added automatically
    assert "test-server" in manager.clients
    assert "test-server-2" in manager.clients
    
    # Check that all clients are connected
    assert all(client.connected for client in manager.clients.values())


def test_disconnect_from_all():
    """Test disconnecting from all servers."""
    manager = MCPConnectionManager()
    
    # Add and connect to servers
    manager.add_server("test-server")
    manager.add_server("test-server-2")
    manager.connect_to_servers(show_progress=False)
    
    # Disconnect from all
    results = manager.disconnect_from_all()
    
    assert len(results) == 2
    assert all(results.values())
    
    # Check that all clients are disconnected
    assert all(not client.connected for client in manager.clients.values())


def test_update_all_statuses():
    """Test updating status information for all servers."""
    manager = MCPConnectionManager()
    
    # Add servers
    manager.add_server("test-server")
    manager.add_server("test-server-2")
    
    # Update statuses before connecting
    statuses = manager.update_all_statuses()
    
    assert len(statuses) == 2
    assert all(status["status"] == "disconnected" for status in statuses.values())
    
    # Connect and update statuses
    manager.connect_to_servers(show_progress=False)
    statuses = manager.update_all_statuses()
    
    assert all(status["status"] == "connected" for status in statuses.values())


def test_get_connected_servers():
    """Test getting list of connected servers."""
    manager = MCPConnectionManager()
    
    # Add servers but don't connect
    manager.add_server("test-server")
    manager.add_server("test-server-2")
    
    # Check that no servers are connected
    assert manager.get_connected_servers() == []
    
    # Connect and check again
    manager.connect_to_servers(show_progress=False)
    connected = manager.get_connected_servers()
    
    assert len(connected) == 2
    assert "test-server" in connected
    assert "test-server-2" in connected


def test_get_client():
    """Test getting a specific client."""
    manager = MCPConnectionManager()
    
    # Try to get a client that doesn't exist
    assert manager.get_client("nonexistent-server") is None
    
    # Add a server and get the client
    manager.add_server("test-server")
    client = manager.get_client("test-server")
    
    assert client is not None
    assert isinstance(client, MCPClient)
    assert client.server_name == "test-server"


def test_broadcast_message():
    """Test broadcasting a message to all connected servers."""
    manager = MCPConnectionManager()
    
    # Add and connect to servers
    manager.add_server("test-server")
    manager.add_server("test-server-2")
    manager.connect_to_servers(show_progress=False)
    
    # Broadcast a message
    message = {"test": "message"}
    responses = manager.broadcast_message(message)
    
    assert len(responses) == 2
    assert all(response["status"] == "delivered" for response in responses.values()) 