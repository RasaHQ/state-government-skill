# State Government Services Bot — Rasa Pro & CALM

A self-contained [Rasa Pro](https://rasa.com/rasa-pro/) chatbot for state-level citizen services. Built with the LLM-native CALM approach: **flows, custom actions, and contextual response rephrasing** — no intents, stories, or rules required.

## Capabilities

- **Driver's license** — Status lookup, renewal info, and new application guidance
- **SNAP benefits** — Eligibility check (collects household size + income) and general program info
- **Knowledge search (RAG)** — FAQ-style answers about offices, required documents, timelines, etc. via `EnterpriseSearchPolicy`
- **Graceful boundaries** — Out-of-scope requests get a polite redirect; prompt injection resistance via untrusted-content tagging

## Quick Start

```bash
cp .env.example .env
# Add your RASA_PRO_LICENSE and OPENAI_API_KEY

uv sync
uv run rasa train
uv run rasa inspect
```

## Project Structure

```
├── config.yml                  # Pipeline: CompactLLMCommandGenerator + EnterpriseSearchPolicy
├── domain/
│   ├── domain.yml              # Slots and responses for license + SNAP flows
│   ├── chitchat.yml            # Greeting, goodbye, help responses
│   └── shared.yml              # Shared slots and refusal responses
├── data/flows/
│   ├── drivers_license.yml     # License status, renewal, and application flows
│   ├── snap_benefits.yml       # SNAP eligibility check and general info flows
│   ├── unsupported.yml         # Catch-all for out-of-scope requests
│   ├── chitchat.yml            # Greeting, goodbye, help, small talk flows
│   └── decline_behavior_modification.yml
├── actions/
│   ├── action_check_license_status.py   # Mock license status lookup
│   └── action_check_snap_eligibility.py # Mock SNAP eligibility check
├── prompt_templates/
│   ├── command_generator_prompt.jinja2
│   └── response-rephraser-template.jinja2
├── rephraser.py                # Custom rephraser with message truncation
├── docs/faq/georgia_services.txt  # Knowledge base for enterprise search
└── tests/                      # E2E test cases
```

## Key Patterns

1. **LLM-based routing** — `CompactLLMCommandGenerator` interprets user messages and selects the right flow from descriptions alone.
2. **Async custom actions** — `action_check_license_status` and `action_check_snap_eligibility` call mock APIs and set slots. In production, these would call real state agency APIs.
3. **Slot collection** — SNAP eligibility flow collects `household_size` and `monthly_income` before running the eligibility check.
4. **Conditional branching** — Flows branch on API results (eligible/not eligible, active/expired/suspended, error).
5. **Contextual rephrasing** — Responses are rephrased by an LLM to sound natural while staying within defined capabilities.

## Learn More

- [Rasa Pro Documentation](https://rasa.com/docs/rasa-pro/)
- [Building AI Assistants with CALM](https://rasa.com/docs/rasa-pro/calm)
- [Custom Actions Guide](https://rasa.com/docs/rasa-pro/concepts/custom-actions)
- [Enterprise Search (RAG)](https://rasa.com/docs/rasa-pro/concepts/policies/enterprise-search-policy)
