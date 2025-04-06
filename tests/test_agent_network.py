"""Tests for the AgentNetwork class."""

import pytest
from mcp_agent_network import AgentNetwork


def test_agent_network_init():
    """Test that the AgentNetwork initializes correctly."""
    network = AgentNetwork()
    assert network.config == {}
    assert network.mcp_clients == {}
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
    result = network.connect_to_servers(["glama", "smithery"])
    assert result is True


def test_execute_task():
    """Test executing a task."""
    network = AgentNetwork()
    task = "Test task"
    result = network.execute_task(task)
    assert result == f"Executed task: {task}"


def test_chat_with_agent():
    """Test chatting with an agent."""
    network = AgentNetwork()
    agent_id = "test-agent"
    message = "Hello"
    response = network.chat_with_agent(agent_id, message)
    assert response == f"Agent {agent_id} response to '{message}'" 