"""Example of using the MCP connection functionality with progress indicators."""

import time
from mcp_agent_network import AgentNetwork
from mcp_agent_network.mcp.progress import SpinnerIndicator


def main():
    """Run the MCP connection example."""
    print("\n=== MCP Agent Network Connection Example ===\n")
    
    # Initialize the agent network
    network = AgentNetwork()
    
    # Connect to MCP servers with progress bar
    print("Connecting to MCP servers...")
    servers = ["glama", "smithery"]
    success = network.connect_to_servers(servers, show_progress=True)
    
    if not success:
        print("❌ Failed to connect to all MCP servers")
        return
    
    print("✅ Connected to all MCP servers successfully\n")
    
    # Get and display server status
    print("Server connection status:")
    statuses = network.get_server_status()
    
    for server_name, status in statuses.items():
        print(f"  • {server_name}: {status['status']} (latency: {status['connection_latency']})")
        if status['status'] == 'connected':
            print(f"    - Protocol: {status.get('protocol_version', 'unknown')}")
            print(f"    - Features: {', '.join(status.get('features', []))}")
    
    print("\nExecuting a task...")
    spinner = SpinnerIndicator("Processing task")
    spinner.start("Sending task to MCP servers")
    
    # Execute a task
    task_result = network.execute_task("Query the latest data from connected services")
    
    # Simulate processing time
    for i in range(3):
        time.sleep(0.5)
        spinner.update(f"Processing task data ({i+1}/3)")
    
    spinner.stop()
    print("\n✅ Task execution complete\n")
    print(f"Task status: {task_result['status']}")
    print(f"Servers that responded: {', '.join(task_result['servers_responded'])}")
    
    # Chat with an agent
    print("\nSending chat message to an agent...")
    agent_id = "research-agent"
    message = "What's the latest progress on our project?"
    
    spinner = SpinnerIndicator("Sending message")
    spinner.start(f"Communicating with agent {agent_id}")
    response = network.chat_with_agent(agent_id, message)
    
    # Simulate processing time
    time.sleep(1)
    spinner.update("Waiting for agent response")
    time.sleep(0.5)
    
    spinner.stop()
    print(f"\n✅ Message sent successfully\n")
    print(f"Response: {response}")
    
    # Disconnect from servers
    print("\nDisconnecting from MCP servers...")
    network.disconnect_from_servers()
    print("✅ Disconnected from all MCP servers\n")


if __name__ == "__main__":
    main() 