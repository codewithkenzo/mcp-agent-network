"""Tests for the MCP client."""

import pytest
from mcp_agent_network.mcp import MCPClient


def test_mcp_client_init():
    """Test MCPClient initialization."""
    client = MCPClient("test-server")
    assert client.server_name == "test-server"
    assert client.api_key is None
    assert not client.connected
    assert client.connection_info == {}
    
    client_with_key = MCPClient("test-server", "test-key")
    assert client_with_key.api_key == "test-key"


def test_mcp_client_connect():
    """Test MCPClient connect method."""
    client = MCPClient("test-server")
    success, info = client.connect()
    
    assert success is True
    assert client.connected is True
    assert "server_name" in info
    assert info["server_name"] == "test-server"
    assert "connection_latency" in info
    assert "protocol_version" in info
    assert "features" in info


def test_mcp_client_disconnect():
    """Test MCPClient disconnect method."""
    client = MCPClient("test-server")
    
    # Can't disconnect if not connected
    assert client.disconnect() is False
    
    # Connect and then disconnect
    client.connect()
    assert client.connected is True
    
    assert client.disconnect() is True
    assert client.connected is False
    assert client.connection_info == {}


def test_mcp_client_ping():
    """Test MCPClient ping method."""
    client = MCPClient("test-server")
    
    # Can't ping if not connected
    assert client.ping() == -1
    
    # Connect and then ping
    client.connect()
    latency = client.ping()
    
    assert latency >= 0  # Should be a non-negative number
    assert client.connection_latency == latency


def test_mcp_client_get_status():
    """Test MCPClient get_status method."""
    client = MCPClient("test-server")
    
    # Status when disconnected
    status = client.get_status()
    assert status["status"] == "disconnected"
    assert status["server_name"] == "test-server"
    
    # Status when connected
    client.connect()
    status = client.get_status()
    
    assert status["status"] == "connected"
    assert status["server_name"] == "test-server"
    assert "connection_latency" in status
    assert "time_since_ping" in status
    assert "features" in status


def test_mcp_client_send_message():
    """Test MCPClient send_message method."""
    client = MCPClient("test-server")
    
    # Can't send message if not connected
    response = client.send_message({"test": "message"})
    assert response["status"] == "failed"
    assert "error" in response
    
    # Connect and send message
    client.connect()
    response = client.send_message({"test": "message"})
    
    assert response["status"] == "delivered"
    assert response["server"] == "test-server"
    assert "timestamp" in response 