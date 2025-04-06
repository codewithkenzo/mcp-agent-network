# MCP Agent Network

An agent network built on top of MCP (Multi-agent Communication Protocol) technology, enabling intelligent agent communication, orchestration, and task execution through a unified interface.

## Features

- **MCP Protocol Integration**: Built on standardized agent communication protocols
- **Agent Orchestration**: Powered by Upsonic for workflows, memory, and knowledge management  
- **Browser Automation**: Integrated with Playwright/browseruse and browser-tools-mcp
- **Unified Interface**: Chat with all your agents through fast-agent.ai
- **Modular Architecture**: Easily extendable with new capabilities

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-agent-network.git
cd mcp-agent-network

# Set up using UV (recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

## Usage

```python
from mcp_agent_network import AgentNetwork

# Initialize the agent network
network = AgentNetwork()

# Connect to MCP servers
network.connect_to_servers(["glama", "smithery"])

# Start interacting with agents
response = network.execute_task("Research the latest AI developments")
print(response)
```

## Architecture

The MCP Agent Network follows a modular, layered architecture:

```
┌───────────────────────────────────────────────────────────┐
│                      User Interface                        │
│                    (Fast-agent.ai)                         │
└───────────────────────────┬───────────────────────────────┘
                            │
┌───────────────────────────▼───────────────────────────────┐
│                   Orchestration Layer                      │
│                       (Upsonic)                            │
└────────┬─────────────────┬────────────────────┬───────────┘
         │                 │                    │
┌────────▼─────────┐ ┌────▼────────────┐ ┌─────▼──────────┐
│    MCP Client    │ │ Browser Tools   │ │  Agent Tools   │
│  (Fast-agent.ai) │ │   (Playwright)  │ │   (Upsonic)    │
└────────┬─────────┘ └────┬────────────┘ └─────┬──────────┘
         │                │                    │
┌────────▼────────────────▼────────────────────▼──────────┐
│                     MCP Protocol                         │
└────────┬─────────────────┬────────────────────┬─────────┘
         │                 │                    │
┌────────▼─────────┐ ┌────▼────────────┐ ┌─────▼──────────┐
│   MCP Servers    │ │   MCP Servers   │ │  Other MCP     │
│     (Glama)      │ │   (Smithery)    │ │   Services     │
└──────────────────┘ └─────────────────┘ └────────────────┘
```

## Development

```bash
# Set up development environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"

# Run tests
pytest
```

## License

MIT 