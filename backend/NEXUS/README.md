# NEXUS AI

**Neural Expert eXchange & Unified Specialization System**

## Overview
NEXUS AI is a modular, multi-agent AI system designed for expert-level query handling, intelligent routing, and efficient inter-agent communication using the AICL (AI Communication Language) protocol.

- **Core Engine:** Central coordination (NEXUS Core)
- **Router:** Smart query distribution (NEXUS Router)
- **Specialists:** Domain-specific expert agents (e.g., Builder, Coder, Gardener)
- **Protocol:** JSON-based AICL for all inter-agent messages

## Key Files
- `nexus-core.py`: Main system engine
- `nexus-router.py`: Query routing
- `nexus-specialist-template.py`: Specialist agent base class
- `specialist_builder.py`, `specialist_coder.py`, `specialist_gardener.py`: Example domain agents
- `nexus-protocol.json`: AICL message format/schema
- `nexus-config.yaml`: System configuration
- `agent_registry.py`, `intent_classifier.py`, `context_manager.py`, `smart_router.py`: Core infrastructure

## Architecture
- **AICL Protocol:** Standardized JSON for all agent communication
- **Agent Registry:** Manages agent capabilities and selection
- **Intent Classifier:** Classifies user queries into domains
- **Context Manager:** Enhances and manages user/session context
- **Smart Router:** Routes queries to best-fit agents

## Quickstart
1. Clone the repo and install Python 3.8+
2. Review `nexus-config.yaml` for system settings
3. Run or import modules as needed for development

## Example Specialist Agent
See `specialist_builder.py` for a construction domain agent template.

## LLM Integration (OpenAI & Anthropic)

NEXUS can use either OpenAI or Anthropic as its LLM backend. You can select the provider and model in `nexus-config.yaml`.

### 1. Get API Keys
- **OpenAI:** Sign up at https://platform.openai.com/ and create an API key.
- **Anthropic:** Sign up at https://console.anthropic.com/ and create an API key.

### 2. Set Environment Variables
Set the appropriate environment variable in your shell or `.env` file:
- For OpenAI: `export OPENAI_API_KEY=your_openai_key`
- For Anthropic: `export ANTHROPIC_API_KEY=your_anthropic_key`

### 3. Configure Provider
Edit `nexus-config.yaml`:
```
llm:
  provider: openai  # or 'anthropic'
  model: gpt-3.5-turbo  # or 'claude-3-opus-20240229' for Anthropic
  temperature: 0.7
  max_tokens: 512
```

### 4. Install Dependencies
```
pip install -r requirements.txt
```

### 5. Run the System
Start the backend as usual. The Guardian will use the selected LLM for query handling.

## License
Proprietary. All rights reserved. 