"""
Minimal Semantic Kernel Agents example for the Tailspin Shelter.

This agent uses a ChatCompletionAgent backed by Azure OpenAI or OpenAI to answer
questions about dogs in the shelter.  It exposes the shelter's REST API as
kernel functions so the model can call them as tools.

Prerequisites:
    pip install -r requirements.txt

Environment variables (at least one provider must be configured):

    Azure OpenAI:
        AZURE_OPENAI_ENDPOINT   – e.g. https://<resource>.openai.azure.com/
        AZURE_OPENAI_API_KEY    – your API key  (omit to use managed identity)
        AZURE_OPENAI_DEPLOYMENT – deployment / model name  (default: gpt-4o)

    OpenAI:
        OPENAI_API_KEY          – your API key
        OPENAI_MODEL            – model name  (default: gpt-4o-mini)

    Server URL (optional):
        SHELTER_API_URL         – base URL for the shelter API
                                  (default: http://localhost:5100/api)

Usage:
    python agent.py
"""

import asyncio
import os
from typing import Annotated

import httpx
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    OpenAIChatCompletion,
)
from semantic_kernel.functions import kernel_function

SHELTER_API_URL = os.environ.get("SHELTER_API_URL", "http://localhost:5100/api")


class DogShelterPlugin:
    """Kernel plugin that exposes the Tailspin Shelter REST API as tools."""

    def __init__(self) -> None:
        self._client = httpx.AsyncClient()

    @kernel_function(description="List all dogs currently in the shelter.")
    async def list_dogs(self) -> str:
        response = await self._client.get(f"{SHELTER_API_URL}/dogs")
        response.raise_for_status()
        return response.text

    @kernel_function(description="Get full details for a single dog by their numeric ID.")
    async def get_dog(
        self,
        dog_id: Annotated[int, "The numeric ID of the dog"],
    ) -> str:
        response = await self._client.get(f"{SHELTER_API_URL}/dogs/{dog_id}")
        if response.status_code == 404:
            return f"No dog found with ID {dog_id}."
        response.raise_for_status()
        return response.text


def _build_kernel() -> Kernel:
    """Create a Kernel and register the appropriate chat-completion service."""
    kernel = Kernel()

    if os.environ.get("AZURE_OPENAI_ENDPOINT"):
        kernel.add_service(
            AzureChatCompletion(
                deployment_name=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
                endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
                api_key=os.environ.get("AZURE_OPENAI_API_KEY"),  # None → managed identity
            )
        )
    else:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "Set AZURE_OPENAI_ENDPOINT (Azure OpenAI) or OPENAI_API_KEY (OpenAI)."
            )
        kernel.add_service(
            OpenAIChatCompletion(
                ai_model_id=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
                api_key=api_key,
            )
        )

    kernel.add_plugin(DogShelterPlugin(), plugin_name="DogShelter")
    return kernel


async def main() -> None:
    kernel = _build_kernel()

    agent = ChatCompletionAgent(
        kernel=kernel,
        name="PetAdoptionAssistant",
        instructions=(
            "You are a helpful assistant for Tailspin Shelter, a dog adoption centre. "
            "Use the provided tools to answer questions about the dogs in our care. "
            "Keep answers concise and friendly."
        ),
    )

    thread: ChatHistoryAgentThread | None = None

    print("🐾  Welcome to Tailspin Shelter!  Ask me about our dogs.")
    print("    Type 'quit' or 'exit' to leave.\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in {"quit", "exit", "q"}:
            print("Goodbye! 🐾")
            break

        async for response in agent.invoke(user_input, thread=thread):
            thread = response.thread
            print(f"Agent: {response.message.content}\n")


if __name__ == "__main__":
    asyncio.run(main())
