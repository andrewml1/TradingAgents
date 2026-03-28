<p align="center">
  <img src="assets/TauricResearch.png" style="width: 60%; height: auto;">
</p>

<div align="center" style="line-height: 1;">
  <a href="https://arxiv.org/abs/2412.20138" target="_blank"><img alt="arXiv" src="https://img.shields.io/badge/arXiv-2412.20138-B31B1B?logo=arxiv"/></a>
  <a href="https://discord.com/invite/hk9PGKShPK" target="_blank"><img alt="Discord" src="https://img.shields.io/badge/Discord-TradingResearch-7289da?logo=discord&logoColor=white&color=7289da"/></a>
  <a href="./assets/wechat.png" target="_blank"><img alt="WeChat" src="https://img.shields.io/badge/WeChat-TauricResearch-brightgreen?logo=wechat&logoColor=white"/></a>
  <a href="https://x.com/TauricResearch" target="_blank"><img alt="X Follow" src="https://img.shields.io/badge/X-TauricResearch-white?logo=x&logoColor=white"/></a>
  <br>
  <a href="https://github.com/TauricResearch/" target="_blank"><img alt="Community" src="https://img.shields.io/badge/Join_GitHub_Community-TauricResearch-14C290?logo=discourse"/></a>
</div>

<div align="center">
  <!-- Keep these links. Translations will automatically update with the README. -->
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=de">Deutsch</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=es">Español</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=fr">français</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ja">日本語</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ko">한국어</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=pt">Português</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ru">Русский</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=zh">中文</a>
</div>

---

# TradingAgents: Multi-Agents LLM Financial Trading Framework

> **Este repositorio también incluye [Cement Sales Intelligence](#cement-sales-intelligence-sistema-de-inteligencia-comercial-de-cemento), un sistema multi-agente especializado para análisis del mercado de cemento en Colombia.**

## News
- [2026-03] **TradingAgents v0.2.2** released with GPT-5.4/Gemini 3.1/Claude 4.6 model coverage, five-tier rating scale, OpenAI Responses API, Anthropic effort control, and cross-platform stability.
- [2026-02] **TradingAgents v0.2.0** released with multi-provider LLM support (GPT-5.x, Gemini 3.x, Claude 4.x, Grok 4.x) and improved system architecture.
- [2026-01] **Trading-R1** [Technical Report](https://arxiv.org/abs/2509.11420) released, with [Terminal](https://github.com/TauricResearch/Trading-R1) expected to land soon.

<div align="center">
<a href="https://www.star-history.com/#TauricResearch/TradingAgents&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date" />
   <img alt="TradingAgents Star History" src="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date" style="width: 80%; height: auto;" />
 </picture>
</a>
</div>

> 🎉 **TradingAgents** officially released! We have received numerous inquiries about the work, and we would like to express our thanks for the enthusiasm in our community.
>
> So we decided to fully open-source the framework. Looking forward to building impactful projects with you!

<div align="center">

🚀 [TradingAgents](#tradingagents-framework) | ⚡ [Installation & CLI](#installation-and-cli) | 🎬 [Demo](https://www.youtube.com/watch?v=90gr5lwjIho) | 📦 [Package Usage](#tradingagents-package) | 🤝 [Contributing](#contributing) | 📄 [Citation](#citation)

</div>

## TradingAgents Framework

TradingAgents is a multi-agent trading framework that mirrors the dynamics of real-world trading firms. By deploying specialized LLM-powered agents: from fundamental analysts, sentiment experts, and technical analysts, to trader, risk management team, the platform collaboratively evaluates market conditions and informs trading decisions. Moreover, these agents engage in dynamic discussions to pinpoint the optimal strategy.

<p align="center">
  <img src="assets/schema.png" style="width: 100%; height: auto;">
</p>

> TradingAgents framework is designed for research purposes. Trading performance may vary based on many factors, including the chosen backbone language models, model temperature, trading periods, the quality of data, and other non-deterministic factors. [It is not intended as financial, investment, or trading advice.](https://tauric.ai/disclaimer/)

Our framework decomposes complex trading tasks into specialized roles. This ensures the system achieves a robust, scalable approach to market analysis and decision-making.

### Analyst Team
- Fundamentals Analyst: Evaluates company financials and performance metrics, identifying intrinsic values and potential red flags.
- Sentiment Analyst: Analyzes social media and public sentiment using sentiment scoring algorithms to gauge short-term market mood.
- News Analyst: Monitors global news and macroeconomic indicators, interpreting the impact of events on market conditions.
- Technical Analyst: Utilizes technical indicators (like MACD and RSI) to detect trading patterns and forecast price movements.

<p align="center">
  <img src="assets/analyst.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

### Researcher Team
- Comprises both bullish and bearish researchers who critically assess the insights provided by the Analyst Team. Through structured debates, they balance potential gains against inherent risks.

<p align="center">
  <img src="assets/researcher.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

### Trader Agent
- Composes reports from the analysts and researchers to make informed trading decisions. It determines the timing and magnitude of trades based on comprehensive market insights.

<p align="center">
  <img src="assets/trader.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

### Risk Management and Portfolio Manager
- Continuously evaluates portfolio risk by assessing market volatility, liquidity, and other risk factors. The risk management team evaluates and adjusts trading strategies, providing assessment reports to the Portfolio Manager for final decision.
- The Portfolio Manager approves/rejects the transaction proposal. If approved, the order will be sent to the simulated exchange and executed.

<p align="center">
  <img src="assets/risk.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

## Installation and CLI

### Installation

Clone TradingAgents:
```bash
git clone https://github.com/TauricResearch/TradingAgents.git
cd TradingAgents
```

Create a virtual environment in any of your favorite environment managers:
```bash
conda create -n tradingagents python=3.13
conda activate tradingagents
```

Install the package and its dependencies:
```bash
pip install .
```

### Required APIs

TradingAgents supports multiple LLM providers. Set the API key for your chosen provider:

```bash
export OPENAI_API_KEY=...          # OpenAI (GPT)
export GOOGLE_API_KEY=...          # Google (Gemini)
export ANTHROPIC_API_KEY=...       # Anthropic (Claude)
export XAI_API_KEY=...             # xAI (Grok)
export OPENROUTER_API_KEY=...      # OpenRouter
export ALPHA_VANTAGE_API_KEY=...   # Alpha Vantage
```

For local models, configure Ollama with `llm_provider: "ollama"` in your config.

Alternatively, copy `.env.example` to `.env` and fill in your keys:
```bash
cp .env.example .env
```

### CLI Usage

Launch the interactive CLI:
```bash
tradingagents          # installed command
python -m cli.main     # alternative: run directly from source
```
You will see a screen where you can select your desired tickers, analysis date, LLM provider, research depth, and more.

<p align="center">
  <img src="assets/cli/cli_init.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

An interface will appear showing results as they load, letting you track the agent's progress as it runs.

<p align="center">
  <img src="assets/cli/cli_news.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

<p align="center">
  <img src="assets/cli/cli_transaction.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

## TradingAgents Package

### Implementation Details

We built TradingAgents with LangGraph to ensure flexibility and modularity. The framework supports multiple LLM providers: OpenAI, Google, Anthropic, xAI, OpenRouter, and Ollama.

### Python Usage

To use TradingAgents inside your code, you can import the `tradingagents` module and initialize a `TradingAgentsGraph()` object. The `.propagate()` function will return a decision. You can run `main.py`, here's also a quick example:

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())

# forward propagate
_, decision = ta.propagate("NVDA", "2026-01-15")
print(decision)
```

You can also adjust the default configuration to set your own choice of LLMs, debate rounds, etc.

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "openai"        # openai, google, anthropic, xai, openrouter, ollama
config["deep_think_llm"] = "gpt-5.2"     # Model for complex reasoning
config["quick_think_llm"] = "gpt-5-mini" # Model for quick tasks
config["max_debate_rounds"] = 2

ta = TradingAgentsGraph(debug=True, config=config)
_, decision = ta.propagate("NVDA", "2026-01-15")
print(decision)
```

See `tradingagents/default_config.py` for all configuration options.

---

# Cement Sales Intelligence: Sistema de Inteligencia Comercial de Cemento

Sistema multi-agente construido sobre la misma arquitectura de TradingAgents, adaptado para el análisis estratégico del mercado de cemento en Colombia. Genera recomendaciones de pricing, mix de productos e inversión comercial por zona geográfica, con análisis de riesgos integrado.

<p align="center">
  <img src="assets/schema.png" style="width: 100%; height: auto;">
</p>

## Arquitectura de Agentes

El sistema replica el flujo Analista → Investigadores → Debate → Estratega → Riesgos → Manager, adaptado al dominio de cemento:

| Agente | Equivalente TradingAgents | Función |
|--------|--------------------------|---------|
| **Analista de Datos** | Analyst Team | Consolida DANE, SAP/ERP, precios competencia |
| **Investigador Bullish** | Bull Researcher | Construye el caso optimista por zona |
| **Investigador Bearish** | Bear Researcher | Construye el caso pesimista por zona |
| **Moderador de Debate** | Invest Judge | Produce veredicto BULLISH / BEARISH / NEUTRAL |
| **Estratega** | Trader | Traduce el veredicto en estrategia comercial |
| **Analista de Riesgos** | Risk Management | Scorecard de riesgos en 6 dimensiones |
| **Manager** | Portfolio Manager | Decisión final: EJECUTAR / MODIFICAR / RECHAZAR |

### Flujo del Grafo

```
analyst → [bull_researcher ‖ bear_researcher] → debate_moderator
       ↺ (hasta 2 rondas de debate)
       → strategist → risk_analyst → manager → END
```

### Zonas Comerciales

1. Costa Caribe (Barranquilla, Cartagena, Santa Marta)
2. Antioquia (Medellín, Valle de Aburrá)
3. Centro (Bogotá, Cundinamarca)
4. Sur (Cali, Valle del Cauca, Cauca)
5. Eje Cafetero (Pereira, Manizales, Armenia)
6. Santanderes (Bucaramanga, Cúcuta)
7. Llanos (Villavicencio, Meta)

## Instalación y Uso

### Dependencias adicionales

```bash
pip install langchain-anthropic langgraph
```

### API Key requerida

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

### CLI

```bash
# Analizar una zona específica
python cement_main.py --zona "Sur" --perfil Agresivo

# Analizar una zona con perfil conservador
python cement_main.py --zona "Antioquia" --perfil Conservador

# Analizar todas las zonas (tabla resumen)
python cement_main.py --all --perfil Neutral
```

**Perfiles de riesgo disponibles:** `Agresivo` | `Neutral` | `Conservador`

### Uso como módulo Python

```python
from cementagents import CementAgentsGraph
from cementagents.graph.propagation import CementPropagator

graph = CementAgentsGraph()

# Analizar una zona
result = graph.analyze_zona("Sur", perfil_riesgo="Agresivo")
print(f"Veredicto: {result['veredicto']} ({result['confianza']:.0%})")
print(f"Decisión:  {result['decision_final']}")
print(CementPropagator.format_report(result))

# Analizar todas las zonas
resultados = graph.analyze_all_zonas(perfil_riesgo="Neutral")
for zona, r in resultados.items():
    print(f"{zona}: {r['veredicto']} → {r['decision_final']}")
```

### Configuración

```python
from cementagents import CementAgentsGraph
from cementagents.default_config import DEFAULT_CONFIG

config = DEFAULT_CONFIG.copy()
config["max_debate_rounds"] = 3          # Rondas de debate por zona
config["max_risk_discuss_rounds"] = 2    # Rondas de análisis de riesgo
config["risk_profile"] = "Conservador"  # Perfil de riesgo global
config["use_mock_data"] = True           # False para conectar a datos reales

graph = CementAgentsGraph(config=config)
```

Ver [`cementagents/default_config.py`](cementagents/default_config.py) para todas las opciones.

### Ejemplo de output

```
┌─────────────────────────────────────────────────┐
│ ZONA: Sur | Fecha: 2026-03-28 | Perfil: Agresivo│
├─────────────────────────────────────────────────┤
│ VEREDICTO:  BULLISH (confianza: 82%)            │
│ DECISIÓN:   EJECUTAR                            │
├─────────────────────────────────────────────────┤
│ Propuesta Estratega:                            │
│   Pricing:  Incrementar 3.5%                   │
│   Volumen:  Push clientes tier 1               │
│   Mix:      Priorizar cemento gris premium     │
├─────────────────────────────────────────────────┤
│ Scorecard de Riesgos:                           │
│   Concentración clientes:  BAJO  (3/10)        │
│   Guerra de precios:       BAJO  (2/10)        │
│   Inventario:              BAJO  (2/10)        │
│   Cartera:                 BAJO  (2/10)        │
│   RIESGO GLOBAL:           BAJO                │
└─────────────────────────────────────────────────┘
```

### Estructura del Proyecto

```
cementagents/
├── agents/
│   ├── analysts/data_analyst.py       # Agente consolidador de datos
│   ├── researchers/
│   │   ├── bull_researcher.py         # Investigador bullish
│   │   └── bear_researcher.py         # Investigador bearish
│   ├── debate/debate_moderator.py     # Moderador y árbitro
│   ├── strategist/strategist.py       # Estratega comercial
│   ├── risk_mgmt/risk_analyst.py      # Analista de riesgos
│   ├── managers/manager.py            # Manager decisor
│   └── utils/
│       ├── agent_states.py            # ZonaState TypedDict
│       └── memory.py                  # Memoria por zona
├── dataflows/
│   └── mock_data.py                   # Datos simulados 2026 (7 zonas)
├── graph/
│   ├── cement_graph.py                # Orquestador principal
│   ├── setup.py                       # Construcción del grafo LangGraph
│   ├── conditional_logic.py           # Condiciones de routing
│   └── propagation.py                 # Extracción y formato de resultados
├── schemas/zona_schema.py             # Modelos Pydantic
└── default_config.py                  # Configuración por defecto
cement_main.py                         # CLI entry point
```

---

## Contributing

We welcome contributions from the community! Whether it's fixing a bug, improving documentation, or suggesting a new feature, your input helps make this project better. If you are interested in this line of research, please consider joining our open-source financial AI research community [Tauric Research](https://tauric.ai/).

## Citation

Please reference our work if you find *TradingAgents* provides you with some help :)

```
@misc{xiao2025tradingagentsmultiagentsllmfinancial,
      title={TradingAgents: Multi-Agents LLM Financial Trading Framework}, 
      author={Yijia Xiao and Edward Sun and Di Luo and Wei Wang},
      year={2025},
      eprint={2412.20138},
      archivePrefix={arXiv},
      primaryClass={q-fin.TR},
      url={https://arxiv.org/abs/2412.20138}, 
}
```
