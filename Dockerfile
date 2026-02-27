# syntax=docker/dockerfile:1.10.0

FROM rasa/rasa-pro:3.15.8

USER root

# Install uv for faster dependency management
RUN pip install uv

# Copy project files
COPY pyproject.toml pyproject.toml
COPY actions actions
COPY configs/config.yml configs/config.yml
COPY data data
COPY domain domain
COPY docs docs
COPY rephraser.py rephraser.py
COPY prompt_templates prompt_templates
COPY endpoints.yml endpoints.yml

# Install dependencies with uv
RUN uv sync

# Train the model
RUN --mount=type=secret,id=RASA_PRO_LICENSE,env=RASA_PRO_LICENSE \
    --mount=type=secret,id=OPENAI_API_KEY,env=OPENAI_API_KEY \
    uv run rasa train -c configs/config.yml -d domain
