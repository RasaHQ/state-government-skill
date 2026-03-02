# State Government Services Bot — Rasa Pro CALM + MCP Sub-Agents

A [Rasa Pro](https://rasa.com/rasa-pro/) chatbot demonstrating SNAP benefits eligibility checking and DFCS appointment scheduling. Built with the LLM-native CALM approach and MCP sub-agent architecture — **no intents, stories, rules, or custom Python actions**.

## Capabilities

- **SNAP eligibility check** — Collects household size and income, calls an MCP tool via sub-agent, and returns eligibility results
- **DFCS appointment scheduling** — Sub-agent queries available slots, user confirms, and a direct MCP tool call books the appointment
- **General SNAP info** — Program overview with links to apply online
- **Graceful boundaries** — Out-of-scope requests (license, taxes, Medicaid, etc.) get a polite redirect

## Quick Start

```bash
cp .env.example .env
# Add your RASA_PRO_LICENSE and OPENAI_API_KEY

uv sync
uv run rasa train

# Start the MCP server (separate terminal)
uv run mcp_server/server.py

# Launch the inspector
uv run rasa inspect
```

## Architecture

```
User → Rasa (CompactLLMCommandGenerator + FlowPolicy) → Flow
  → snap_agent (sub-agent)            → mcp_server → check_snap_eligibility
  → appointment_selector (sub-agent)   → mcp_server → query_available_appointments
  → book_appointment (direct MCP call) → mcp_server → book_appointment
```

All service logic lives in the MCP server. Sub-agents are config-only (no custom Python). The bot uses Rasa's built-in response rephraser so templated responses sound natural.

## Project Structure

```
├── config.yml                     # Pipeline: CompactLLMCommandGenerator + FlowPolicy
├── endpoints.yml                  # MCP server connection, rephraser config, model groups
├── domain/
│   ├── domain.yml                 # Slots and responses for SNAP + appointments
│   ├── chitchat.yml               # Greeting, goodbye, help responses
│   └── shared.yml                 # Shared slots and refusal responses
├── data/flows/
│   ├── snap_benefits.yml          # SNAP eligibility check + general info flows
│   ├── schedule_snap_appointment.yml  # Appointment query, confirm, and book flow
│   ├── unsupported.yml            # Catch-all for out-of-scope requests
│   └── chitchat.yml               # Greeting, goodbye, help, small talk flows
├── mcp_server/
│   └── server.py                  # FastMCP server with 3 tools (mock data)
├── sub_agents/
│   ├── snap_agent/config.yml      # MCPOpenAgent → check_snap_eligibility
│   └── appointment_selector/config.yml  # MCPOpenAgent → query_available_appointments
└── tests/                         # E2E test cases
```

## Key Patterns

1. **LLM-based routing** — `CompactLLMCommandGenerator` reads flow descriptions and selects the right flow. No NLU training data needed.
2. **MCP sub-agents** — Config-only `MCPOpenAgent` definitions that call MCP tools and set slots. No custom Python classes or prompt templates.
3. **Direct MCP tool calls** — The appointment booking step calls `book_appointment` directly from a flow using `call:` + `mcp_server:` + `mapping:` syntax, bypassing the need for agent reasoning.
4. **Slot collection** — Flows collect user input (`from_llm` slots) before calling sub-agents. The MCP server handles type casting.
5. **Response rephrasing** — Rasa's built-in `rephrase` NLG rewrites templated responses via GPT-4o so they sound natural and contextual.

## Testing

```bash
# Run all E2E tests
uv run rasa test e2e tests/

# Run a single test file
uv run rasa test e2e tests/test_out_of_scope.yml
```

## Learn More

- [Rasa Pro Documentation](https://rasa.com/docs/rasa-pro/)
- [Building AI Assistants with CALM](https://rasa.com/docs/rasa-pro/calm)
- [MCP Sub-Agents](https://rasa.com/docs/rasa-pro/concepts/sub-agents)
