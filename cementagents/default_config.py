DEFAULT_CONFIG = {
    "project_dir": ".",
    "llm_provider": "anthropic",       # anthropic | openai
    "deep_think_llm": "claude-sonnet-4-6",
    "quick_think_llm": "claude-sonnet-4-6",
    "max_debate_rounds": 2,
    "max_risk_discuss_rounds": 1,
    "zonas": [
        "Costa Caribe",
        "Antioquia",
        "Centro",
        "Sur",
        "Eje Cafetero",
        "Santanderes",
        "Llanos"
    ],
    "risk_profile": "Neutral",         # Agresivo | Neutral | Conservador
    "backend_url": "http://localhost:8000",
    "use_mock_data": True,
}

# Model defaults per provider
PROVIDER_DEFAULTS = {
    "anthropic": {
        "deep_think_llm": "claude-sonnet-4-6",
        "quick_think_llm": "claude-sonnet-4-6",
    },
    "openai": {
        "deep_think_llm": "gpt-4o",
        "quick_think_llm": "gpt-4o-mini",
    },
}
