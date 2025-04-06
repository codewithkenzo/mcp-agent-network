"""Tests for the AgentNetwork class."""

import pytest
from mcp_agent_network import AgentNetwork
from mcp_agent_network.mcp import MCPConnectionManager


def test_agent_network_init():
    """Test that the AgentNetwork initializes correctly."""
    network = AgentNetwork()
    assert network.config == {}
    assert isinstance(network.mcp_connection_manager, MCPConnectionManager)
    assert network.orchestrator is None
    assert network.browser_tools is None


def test_agent_network_with_config():
    """Test that the AgentNetwork initializes with a config."""
    config = {"server": "test-server", "api_key": "test-key"}
    network = AgentNetwork(config)
    assert network.config == config


def test_connect_to_servers():
    """Test connecting to servers."""
    network = AgentNetwork()
    result = network.connect_to_servers(["glama", "smithery"], show_progress=False)
    assert result is True


def test_execute_task():
    """Test executing a task."""
    network = AgentNetwork()
    
    # Connect to servers first
    network.connect_to_servers(["test-server"], show_progress=False)
    
    task = "Test task"
    result = network.execute_task(task)
    
    assert isinstance(result, dict)
    assert result["task"] == task
    assert result["status"] == "submitted"
    assert "servers_responded" in result
    assert "test-server" in result["servers_responded"]


def test_chat_with_agent():
    """Test chatting with an agent."""
    network = AgentNetwork()
    
    # Connect to servers first
    network.connect_to_servers(["test-server"], show_progress=False)
    
    agent_id = "test-agent"
    message = "Hello"
    response = network.chat_with_agent(agent_id, message)
    
    assert "Message sent to agent" in response
    assert agent_id in response 