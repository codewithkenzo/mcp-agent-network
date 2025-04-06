# System Patterns

## System Architecture

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

## Key Technical Decisions

1. **Modular Design**: Each component is self-contained with clear interfaces
2. **Protocol-First Approach**: MCP protocol as the foundation for all agent communications
3. **Orchestration Centralization**: Upsonic serves as the central orchestration engine
4. **UI Separation**: Fast-agent.ai provides a clean interface layer separated from business logic
5. **Standardized Communication**: All agent interactions follow MCP standards

## Design Patterns in Use

1. **Facade Pattern**: Fast-agent.ai provides a simplified interface to the complex agent network
2. **Observer Pattern**: Agents can subscribe to events and notifications
3. **Command Pattern**: Tasks are encapsulated as commands that can be queued and executed
4. **Strategy Pattern**: Different agent behaviors can be swapped based on context
5. **Repository Pattern**: Consistent data access layer for agent knowledge and memory

## Component Relationships

1. **User → Fast-agent.ai**: Human interaction with the agent network
2. **Fast-agent.ai → Upsonic**: Translation of user intent into orchestrated workflows
3. **Upsonic → MCP Client**: Coordination of agent tasks through MCP
4. **MCP Client → MCP Servers**: Communication with external agent services
5. **Upsonic → Browser Tools**: Integration of web automation into agent workflows 