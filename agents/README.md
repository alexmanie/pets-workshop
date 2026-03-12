# Semantic Kernel Agents — Tailspin Shelter example

A minimal Python example that shows how to build a conversational AI agent with
[Semantic Kernel 1.x](https://github.com/microsoft/semantic-kernel) against the
Tailspin Shelter backend.  The agent exposes the shelter's REST API as
*kernel functions* (tools), allowing the model to look up dog and breed data on
demand.

## How it works

```
┌─────────────┐     natural language      ┌───────────────────────┐
│    User     │ ─────────────────────────► │  ChatCompletionAgent  │
│  (terminal) │ ◄───────────────────────── │  (Semantic Kernel)    │
└─────────────┘     friendly response      └───────────┬───────────┘
                                                        │ tool calls
                                           ┌────────────▼────────────┐
                                           │    DogShelterPlugin     │
                                           │  list_dogs / get_dog    │
                                           └────────────┬────────────┘
                                                        │ HTTP
                                           ┌────────────▼────────────┐
                                           │  Tailspin Shelter API   │
                                           │  (Flask, port 5100)     │
                                           └─────────────────────────┘
```

## Prerequisites

- Python 3.11+
- The shelter server running on `http://localhost:5100` (see `../server/`)
- An **Azure OpenAI** or **OpenAI** API key

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2a. Azure OpenAI
export AZURE_OPENAI_ENDPOINT="https://<resource>.openai.azure.com/"
export AZURE_OPENAI_API_KEY="<key>"          # omit to use managed identity
export AZURE_OPENAI_DEPLOYMENT="gpt-4o"      # optional, default: gpt-4o

# 2b. OpenAI (if not using Azure)
export OPENAI_API_KEY="<key>"
export OPENAI_MODEL="gpt-4o-mini"            # optional, default: gpt-4o-mini

# 3. Optional: override the default shelter API URL
export SHELTER_API_URL="http://localhost:5100/api"

# 4. Run
python agent.py
```

## Example session

```
🐾  Welcome to Tailspin Shelter!  Ask me about our dogs.
    Type 'quit' or 'exit' to leave.

You: How many dogs do you have?
Agent: We currently have 12 dogs in our care!

You: Show me the available Labradors
Agent: Here are the available Labradors:
  • Buddy (ID 3) — male, age 2, available for adoption
  • Daisy (ID 7) — female, age 4, available for adoption

You: Tell me more about Buddy
Agent: Buddy is a 2-year-old male Labrador Retriever. He's friendly and loves to play fetch…

You: quit
Goodbye! 🐾
```

## Key concepts

| Concept | Where |
|---|---|
| `@kernel_function` | `DogShelterPlugin` methods — each one becomes a tool the model can call |
| `ChatCompletionAgent` | Wraps the kernel + instructions; drives the conversation |
| `ChatHistoryAgentThread` | Persists the conversation across turns |
| Azure OpenAI / OpenAI | Swappable via environment variables, no code change needed |
