"""
PCOIS2-48: Set up LLM API access and basic call.

Implements the provider choice from PCOIS2-32: Ollama running Qwen3
locally. Ollama exposes an HTTP API on localhost, so there is no API key,
no account, and no request leaving the machine - which is the whole point
of the choice for a university policy corpus.

This module is plumbing only. It knows how to send text to the model and
return the generated text. It knows nothing about policies, retrieval,
chunks, or the response schema - that separation is deliberate, so
swapping providers later means rewriting only this file.

Config via environment variables (defaults suit a standard local install):
    OLLAMA_HOST    default http://localhost:11434
    OLLAMA_MODEL   default qwen3
    OLLAMA_TIMEOUT default 120 (seconds; local inference on CPU is slow)

Usage:
    from ollama_client import OllamaClient
    client = OllamaClient()
    text = client.generate(system="You are terse.", user="Say hello.")

CLI smoke test (proves the connection works - the PCOIS2-48 acceptance
criterion):
    python ollama_client.py
    python ollama_client.py "What is 2 + 2?"
"""
import os
import re
import sys

import requests

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen3")
OLLAMA_TIMEOUT = int(os.environ.get("OLLAMA_TIMEOUT", "120"))

# Qwen3 is a hybrid-reasoning model: it can emit an internal reasoning
# trace wrapped in <think>...</think> before its actual answer. We ask
# Ollama to disable it (think=False), but older Ollama builds ignore that
# flag, so the tags are also stripped defensively. Leaving them in would
# put the model's private reasoning in front of a user asking about
# university policy.
THINK_BLOCK_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)


class OllamaError(RuntimeError):
    """Raised when Ollama is unreachable or returns an error."""


def strip_reasoning(text: str) -> str:
    """Remove any <think> block and surrounding whitespace."""
    return THINK_BLOCK_RE.sub("", text).strip()


class OllamaClient:
    """Thin wrapper over Ollama's /api/chat endpoint."""

    def __init__(self, host: str = OLLAMA_HOST, model: str = OLLAMA_MODEL,
                 timeout: int = OLLAMA_TIMEOUT):
        self.host = host.rstrip("/")
        self.model = model
        self.timeout = timeout

    def is_available(self) -> bool:
        """True if Ollama is running and reachable. Cheap pre-flight check
        so the backend can fail with a clear message rather than a stack
        trace when someone forgets to start Ollama."""
        try:
            resp = requests.get(f"{self.host}/api/tags", timeout=5)
            return resp.ok
        except requests.RequestException:
            return False

    def installed_models(self) -> list[str]:
        """Names of models Ollama has pulled locally."""
        try:
            resp = requests.get(f"{self.host}/api/tags", timeout=5)
            resp.raise_for_status()
        except requests.RequestException as e:
            raise OllamaError(f"Could not reach Ollama at {self.host}: {e}") from e
        return [m.get("name", "") for m in resp.json().get("models", [])]

    def generate(self, system: str, user: str, temperature: float = 0.0) -> str:
        """Send one system + user turn, return the model's text.

        temperature defaults to 0.0: for policy answers we want the most
        deterministic output the model will give, not creative variation.
        The same question should produce the same answer.
        """
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "stream": False,          # one complete response, not tokens
            "think": False,           # suppress Qwen3's reasoning trace
            "options": {"temperature": temperature},
        }

        try:
            resp = requests.post(
                f"{self.host}/api/chat", json=payload, timeout=self.timeout
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            raise OllamaError(
                f"Ollama request failed ({self.host}, model={self.model}): {e}"
            ) from e

        data = resp.json()
        content = data.get("message", {}).get("content", "")
        return strip_reasoning(content)


def main():
    """Smoke test: proves the connection works end to end."""
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Reply with exactly: connection ok"

    client = OllamaClient()
    print(f"Host:  {client.host}")
    print(f"Model: {client.model}")

    if not client.is_available():
        print("\nOllama is not reachable. Start it with:  ollama serve", file=sys.stderr)
        sys.exit(1)

    models = client.installed_models()
    print(f"Installed models: {', '.join(models) or '(none)'}")
    if not any(m.split(":")[0] == client.model.split(":")[0] for m in models):
        print(f"\nModel '{client.model}' not pulled. Run:  ollama pull {client.model}",
              file=sys.stderr)
        sys.exit(1)

    print(f"\nPrompt: {prompt}")
    answer = client.generate(system="You are a concise assistant.", user=prompt)
    print(f"Reply:  {answer}")


if __name__ == "__main__":
    main()
