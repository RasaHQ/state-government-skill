# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Ask GeorgiaGov is a Rasa Pro chatbot built with the LLM-native CALM approach and MCP sub-agent architecture. It provides SNAP benefits services (eligibility checking and DFCS appointment scheduling) using flows instead of intents/stories/rules. Routing is handled by an LLM (`CompactLLMCommandGenerator`) that selects flows from their descriptions alone. Service lookups and appointment booking are performed by MCP sub-agents and direct MCP tool calls via a FastMCP server.

## Commands

```bash
uv sync                    # Install dependencies
uv run rasa train          # Train the model
uv run rasa inspect        # Launch interactive inspector UI
uv run rasa test e2e tests/  # Run all E2E test files
uv run rasa test e2e tests/test_snap_flows.yml  # Run a single test file
```

Starting the MCP server (required before running the bot):
```bash
uv run mcp_server/server.py
```

Manual smoke testing via REST API (requires running server on port 5005):
```bash
bash test_conversations.sh
```

## Architecture

```
User → Rasa (CompactLLMCommandGenerator + FlowPolicy) → Flow
  → snap_agent (MCPOpenAgent, no custom code) → georgia_mcp_server → check_snap_eligibility
  → appointment_selector (MCPOpenAgent, no custom code) → georgia_mcp_server → query_available_appointments
  → book_appointment (direct MCP tool call from flow) → georgia_mcp_server → book_appointment
```

**CALM (no intents/stories):** User messages are interpreted by `CompactLLMCommandGenerator` (GPT-4o) which reads flow descriptions and selects the appropriate flow. No NLU training data needed.

**Flows** (`data/flows/`): Define conversation logic as YAML step sequences with slot collection, sub-agent calls, and conditional branching. Key flows: `snap_benefits.yml` (2 flows), `schedule_snap_appointment.yml` (1 flow), `chitchat.yml`, `unsupported.yml`.

**Domain** (`domain/`): Split across 3 files — `domain.yml` (slots + responses for SNAP/appointments), `chitchat.yml` (greetings/help), `shared.yml` (shared responses + refusal).

**MCP Server** (`mcp_server/server.py`): Single FastMCP server on port 8090 exposing three tools — `check_snap_eligibility`, `query_available_appointments`, and `book_appointment` — with mock data inline.

**Sub-Agents** (`sub_agents/`): Two simple MCPOpenAgent configs (no custom Python code):
- `snap_agent` — calls `check_snap_eligibility` tool
- `appointment_selector` — calls `query_available_appointments` tool

Each sub-agent has only a `config.yml` connecting it to the MCP server.

**Direct MCP Tool Calls:** The appointment booking flow calls `book_appointment` directly from a flow step using `mcp_server:` + `mapping:` syntax, without a sub-agent.

**Prompt Templates** (`prompt_templates/`): Jinja2 template for the command generator controlling LLM routing behavior.

## Configuration

- `config.yml` — Pipeline (CompactLLMCommandGenerator) and policies (FlowPolicy)
- `endpoints.yml` — MCP server connection, model groups
- `credentials.yml` — Channel config (REST, SocketIO); gitignored, copy from example
- `.env` — Requires `RASA_PRO_LICENSE` and `OPENAI_API_KEY`

## Conventions

- Sub-agents use the simplified pattern: just a `config.yml` with agent name, protocol, description, and MCP server connection. No custom Python classes or prompt templates.
- Direct MCP tool calls from flows use `call:` + `mcp_server:` + `mapping:` syntax for tools that don't need agent reasoning (e.g., booking confirmation).
- Flow descriptions are human-readable text that the LLM uses for routing decisions — keep them clear and distinct
- Slots collected from users use `from_llm` mapping; slots set by sub-agents or MCP calls use `controlled` mapping
- SNAP income limits use 130% of federal poverty guidelines (mock data for demo)
- Python 3.10-3.11 required; dependencies managed with `uv` and locked via `uv.lock`
