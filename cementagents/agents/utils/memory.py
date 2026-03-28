from langchain_core.messages import HumanMessage, AIMessage


class ZonaMemory:
    """Simple per-zona memory that keeps recent decisions and recommendations."""

    def __init__(self, llm, max_tokens: int = 1000):
        self.llm = llm
        self.max_tokens = max_tokens
        self.memories = {}

    def get_memory(self, zona: str) -> str:
        """Return stored memory for a zona, or a default message."""
        return self.memories.get(zona, "Sin historial previo.")

    def update_memory(self, zona: str, new_situation: str, new_recommendation: str):
        """Append a new decision entry to the zona's memory, keeping within max_tokens."""
        current = self.memories.get(zona, "")
        entry = (
            f"\n[Decisión previa] "
            f"Situación: {new_situation[:200]} "
            f"→ Recomendación: {new_recommendation[:200]}"
        )
        combined = current + entry
        # Trim to max_tokens by keeping the tail (most recent content)
        self.memories[zona] = combined[-self.max_tokens:]
