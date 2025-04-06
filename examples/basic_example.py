"""Basic example of using the MCP Agent Network."""

from mcp_agent_network import AgentNetwork


def main():
    """Run the basic example."""
    # Initialize the agent network
    network = AgentNetwork()
    
    # Connect to MCP servers
    success = network.connect_to_servers(["glama", "smithery"])
    if not success:
        print("Failed to connect to MCP servers")
        return
    
    print("Connected to MCP servers successfully")
    
    # Execute a task
    result = network.execute_task("Summarize the latest tech news")
    print(f"Task result: {result}")
    
    # Chat with an agent
    agent_id = "research-agent"
    message = "What are the latest developments in AI?"
    response = network.chat_with_agent(agent_id, message)
    print(f"Agent response: {response}")


if __name__ == "__main__":
    main() 