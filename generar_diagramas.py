import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

def make_diagram(title, blocks, filename, bg="#0d1117", title_color="#58a6ff"):
    """Render a list of (label, text, color) blocks as a vertical diagram image."""
    fig_height = sum(len(b[1].split('\n')) * 0.22 + 0.7 for b in blocks) + 1.5
    fig, ax = plt.subplots(figsize=(18, max(fig_height, 8)))
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)
    ax.axis('off')

    ax.text(0.5, 1.0, title, transform=ax.transAxes,
            fontsize=15, fontweight='bold', color=title_color,
            ha='center', va='top', fontfamily='monospace',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#161b22', edgecolor=title_color, linewidth=1.5))

    total_lines = sum(len(b[1].split('\n')) + 3 for b in blocks)
    y = 0.96
    margin = 0.025
    width = 1 - 2 * margin

    for (label, text, color) in blocks:
        lines = text.split('\n')
        block_height = (len(lines) + 2) / (total_lines + 4)

        fancy = FancyBboxPatch((margin, y - block_height), width, block_height,
                               boxstyle="round,pad=0.005",
                               facecolor='#161b22', edgecolor=color, linewidth=1.8,
                               transform=ax.transAxes, clip_on=False)
        ax.add_patch(fancy)

        ax.text(margin + 0.012, y - 0.012, label,
                transform=ax.transAxes,
                fontsize=8, fontweight='bold', color=color,
                ha='left', va='top', fontfamily='monospace')

        body = '\n'.join(lines)
        ax.text(margin + 0.012, y - 0.042, body,
                transform=ax.transAxes,
                fontsize=6.8, color='#c9d1d9',
                ha='left', va='top', fontfamily='monospace',
                linespacing=1.4)

        # Arrow between blocks
        if (label, text, color) != blocks[-1]:
            ax.annotate('', xy=(0.5, y - block_height - 0.003),
                       xytext=(0.5, y - block_height),
                       xycoords='axes fraction', textcoords='axes fraction',
                       arrowprops=dict(arrowstyle='->', color='#484f58', lw=1.5))

        y -= block_height + 0.018

    plt.tight_layout(pad=0.2)
    plt.savefig(filename, dpi=180, bbox_inches='tight',
                facecolor=bg, edgecolor='none')
    plt.close()
    print(f"Saved: {filename}")


# ─────────────────────────────────────────────────────────────
# TRADING AGENTS — 3 imágenes
# ─────────────────────────────────────────────────────────────

trading_p1 = [
    ("ENTRADA  •  main.py / cli/main.py", 
     "Usuario ingresa:  ticker (ej. AAPL)  +  trade_date (ej. 2025-03-25)",
     "#58a6ff"),

    ("ORQUESTADOR  •  tradingagents/graph/setup.py  —  TradingAgentsGraph",
     "• Construye nodos LangGraph y vincula herramientas (bind_tools) a cada LLM\n"
     "• Registra rutas condicionales (conditional_logic.py)\n"
     "• Estado compartido: AgentState TypedDict\n"
     "  company_of_interest | trade_date | market_report | sentiment_report\n"
     "  news_report | fundamentals_report | investment_debate_state\n"
     "  investment_plan | trader_investment_plan | risk_debate_state | final_trade_decision",
     "#3fb950"),

    ("CAPA DE DATOS  •  tradingagents/dataflows/",
     "interface.py — route_to_vendor()\n"
     "  Prioridad 1: tool_vendors[método]       →  override por herramienta específica\n"
     "  Prioridad 2: data_vendors[categoría]    →  default por categoría\n"
     "  Fallback: solo en AlphaVantageRateLimitError → intenta siguiente vendor\n\n"
     "  FUENTE PRINCIPAL (default)              FUENTE ALTERNATIVA\n"
     "  Yahoo Finance — yfinance                Alpha Vantage\n"
     "  • Precios OHLCV  (ticker.history)       • TIME_SERIES_DAILY_ADJUSTED\n"
     "  • Fundamentales  (yfinance)             • NEWS_SENTIMENT\n"
     "  • Noticias       (get_news)             • BALANCE_SHEET / CASH_FLOW\n"
     "  • 15 años de historia                  • INCOME_STATEMENT\n"
     "  • Retry backoff: 2s → 4s → 8s          • Requiere ALPHA_VANTAGE_API_KEY\n\n"
     "  PROCESAMIENTO  •  y_finance.py + stockstats_utils.py\n"
     "  get_YFin_data_online():                 _clean_dataframe():\n"
     "  • Elimina timezone del índice           • Parsea fechas a datetime\n"
     "  • Redondea OHLC a 2 decimales           • Elimina filas con fecha inválida\n"
     "  • Convierte a CSV string                • Convierte columnas a numérico\n"
     "                                          • Elimina filas sin Close\n"
     "  get_stock_stats_indicators_window():    • Rellena huecos: ffill() + bfill()\n"
     "  • Valida indicador en best_ind_params   stockstats.wrap(df)\n"
     "  • _get_stock_stats_bulk()               df[indicator]  →  cálculo lazy\n"
     "  • Cache CSV en data_cache/\n\n"
     "  Indicadores soportados (13):\n"
     "  close_50_sma  close_200_sma  close_10_ema  macd  macds  macdh\n"
     "  rsi  boll  boll_ub  boll_lb  atr  vwma  mfi",
     "#e3b341"),
]

trading_p2 = [
    ("ETAPA 1 — ANALISTAS  •  agents/analysts/  •  quick_think_llm: gpt-5-mini  •  corren en paralelo",
     "market_analyst.py                         fundamentals_analyst.py\n"
     "  Herramientas:                             Herramientas:\n"
     "  • get_stock_data                          • get_fundamentals\n"
     "  • get_indicators                          • get_balance_sheet\n"
     "  El LLM elige hasta 8 indicadores          • get_cashflow\n"
     "  relevantes de 13 disponibles              • get_income_stmt\n"
     "  → market_report                           → fundamentals_report\n\n"
     "news_analyst.py                           social_media_analyst.py\n"
     "  Herramientas:                             Herramientas:\n"
     "  • get_news                                • get_news  (foco sentimiento)\n"
     "  • get_global_news                         → sentiment_report\n"
     "  → news_report",
     "#3fb950"),

    ("ETAPA 2 — DEBATE DE INVESTIGACIÓN  •  agents/researchers/  •  deep_think_llm: gpt-5.2  •  max_debate_rounds=1",
     "bull_researcher.py                        bear_researcher.py\n"
     "  Lee los 4 reportes del AgentState         Lee los 4 reportes del AgentState\n"
     "  Construye tesis:                          Construye tesis:\n"
     "  • Por qué COMPRAR la acción               • Por qué NO comprar / VENDER\n"
     "  • Contraargumenta al bear                 • Contraargumenta al bull\n\n"
     "                       research_manager.py\n"
     "                         Evalúa el debate completo\n"
     "                         Emite: investment_plan",
     "#f0883e"),

    ("ETAPA 3 — TRADER  •  agents/trader/trader.py  •  deep_think_llm",
     "Lee: investment_plan del research_manager\n"
     "Genera: trader_investment_plan  (cuánto, cuándo, en qué condiciones operar)",
     "#3fb950"),
]

trading_p3 = [
    ("ETAPA 4 — DEBATE DE RIESGO  •  agents/risk_mgmt/  •  deep_think_llm  •  max_risk_discuss_rounds=1",
     "risk_aggressive               risk_neutral               risk_conservative\n"
     "  Maximizar retorno             Equilibrar riesgo/rtno     Proteger capital\n\n"
     "                       portfolio_manager.py\n"
     "                         Consolida todos los puntos de vista\n"
     "                         Toma la decisión final",
     "#f85149"),

    ("ETAPA 5 — EXTRACCIÓN DE SEÑAL  •  graph/signal_processing.py  —  SignalProcessor",
     "Recibe el reporte completo del portfolio_manager\n"
     "Extrae una sola palabra usando quick_thinking_llm:\n"
     "BUY   |   OVERWEIGHT   |   HOLD   |   UNDERWEIGHT   |   SELL",
     "#8957e5"),

    ("SALIDA  •  final_trade_decision  +  reporte completo",
     "Decisión final:   BUY  /  OVERWEIGHT  /  HOLD  /  UNDERWEIGHT  /  SELL\n"
     "Guardado en:      results/  (configurable vía TRADINGAGENTS_RESULTS_DIR)\n\n"
     "Config activa (default_config.py):\n"
     "  llm_provider: openai      deep_think_llm: gpt-5.2      quick_think_llm: gpt-5-mini\n"
     "  max_debate_rounds: 1      max_risk_discuss_rounds: 1   max_recur_limit: 100\n"
     "  data_vendors: yfinance (todas las categorías por defecto)",
     "#58a6ff"),
]

make_diagram("TRADING AGENTS — Arquitectura (1/3): Entrada · Datos",
             trading_p1, "/home/user/TradingAgents/trading_diagrama_1.jpg")

make_diagram("TRADING AGENTS — Arquitectura (2/3): Analistas · Debate · Trader",
             trading_p2, "/home/user/TradingAgents/trading_diagrama_2.jpg")

make_diagram("TRADING AGENTS — Arquitectura (3/3): Riesgo · Señal · Salida",
             trading_p3, "/home/user/TradingAgents/trading_diagrama_3.jpg")


# ─────────────────────────────────────────────────────────────
# CEMENT AGENTS — 2 imágenes
# ─────────────────────────────────────────────────────────────

cement_p1 = [
    ("ENTRADA  •  cement_main.py / cementagents_main.py",
     "Usuario selecciona:\n"
     "  • Zona:   Costa Caribe | Antioquia | Centro | Sur | Eje Cafetero | Santanderes | Llanos\n"
     "  • Fecha de análisis\n"
     "  • Perfil de riesgo:   Agresivo | Neutral | Conservador",
     "#58a6ff"),

    ("ORQUESTADOR  •  cementagents/graph/setup.py  —  CementGraphSetup",
     "• Construye StateGraph de LangGraph con 7 nodos de agentes\n"
     "• Registra rutas condicionales (conditional_logic.py)\n"
     "• Estado compartido: ZonaState TypedDict\n"
     "  zona | fecha_analisis | datos_consolidados | argumentos_bullish | argumentos_bearish\n"
     "  historial_debate | veredicto | confianza | rondas_debate | propuesta_estratega\n"
     "  historial_riesgo | propuesta_ajustada | scorecard_riesgo | rondas_riesgo\n"
     "  decision_final | acciones_autorizadas | justificacion | perfil_riesgo_zona\n\n"
     "Config (default_config.py):\n"
     "  llm_provider: anthropic        deep_think_llm: claude-sonnet-4-6\n"
     "  quick_think_llm: claude-sonnet-4-6      max_debate_rounds: 2\n"
     "  max_risk_discuss_rounds: 1             use_mock_data: True",
     "#3fb950"),

    ("CAPA DE DATOS  •  cementagents/dataflows/mock_data.py  —  get_zona_data(zona)",
     "⚠  ACTUALMENTE USA DATOS SIMULADOS  (use_mock_data: True en default_config.py)\n\n"
     "Devuelve dict completo por zona con 3 bloques:\n\n"
     "indicadores_macro:                mercado_local:\n"
     "  pib_construccion_yoy              share_argos / share_competidor_1 / _2\n"
     "  licencias_vivienda_yoy            precio_promedio_argos\n"
     "  tasa_interes                      precio_promedio_competencia\n"
     "  inflacion                         diferencial_precio_pct\n"
     "  trm                               proyectos_pipeline\n"
     "                                    nuevas_licitaciones\n"
     "datos_internos:                     competidores_activos []\n"
     "  ventas_mtd / ytd                  tendencia_precios_competencia\n"
     "  ventas_vs_budget\n"
     "  inventario_dias     alertas: []   ← alertas pre-identificadas por zona\n"
     "  cartera_vencida_pct\n"
     "  clientes_activos\n"
     "  top_5_concentracion_pct\n"
     "  costo_logistica_ton\n"
     "  margen_bruto_pct",
     "#e3b341"),

    ("ETAPA 1 — ANALISTA DE DATOS  •  agents/analysts/data_analyst.py  •  claude-sonnet-4-6",
     "A diferencia de TradingAgents, NO usa tool calls.\n"
     "Recibe TODOS los datos como JSON directamente en el prompt.\n\n"
     "Consolida y analiza:\n"
     "  1. Indicadores macro      →  PIB, licencias, tasas, inflación, TRM\n"
     "  2. Mercado local          →  share, gaps de precio, pipeline, tendencias\n"
     "  3. Operaciones internas   →  ventas vs budget, inventario, cartera, logística\n"
     "  4. Alertas tempranas      →  etiqueta [ALERTA]  [RIESGO]  [OPORTUNIDAD]\n"
     "  5. Contexto competitivo   →  posicionamiento Argos vs Cemex/Holcim/Corona\n\n"
     "→ datos_consolidados  (guardado en ZonaState)",
     "#3fb950"),
]

cement_p2 = [
    ("ETAPA 2 — DEBATE DE INVESTIGACIÓN  •  agents/researchers/  •  claude-sonnet-4-6  •  max_debate_rounds=2",
     "bull_researcher.py                        bear_researcher.py\n"
     "  Lee: datos_consolidados                   Lee: datos_consolidados\n"
     "       + memoria histórica de la zona            + memoria histórica de la zona\n"
     "  Construye caso BULLISH:                   Construye caso BEARISH:\n"
     "  • Subir precios                           • No subir / bajar precios\n"
     "  • Ampliar distribución                    • Reducir exposición\n"
     "  • Ganar share                             • Proteger margen\n"
     "  • Invertir en zona                        • Esperar mejores condiciones\n"
     "  En ronda 2 contraargumenta al bear        En ronda 2 contraargumenta al bull\n\n"
     "                       debate_moderator.py\n"
     "                         Evalúa argumentos de ambos lados\n"
     "                         Emite:  veredicto (BULLISH | BEARISH | NEUTRAL)\n"
     "                                 confianza (0.0 — 1.0)\n"
     "                         ¿Más rondas?  SÍ → vuelve al debate  |  NO → estratega",
     "#f0883e"),

    ("ETAPA 3 — ESTRATEGA COMERCIAL  •  agents/strategist/strategist.py  •  claude-sonnet-4-6",
     "Lee: veredicto + confianza + datos_consolidados + historial_debate\n"
     "     + perfil_riesgo_zona + memoria histórica\n\n"
     "Orientación según veredicto:\n"
     "  BULLISH  →  ofensiva: subir precios, ganar share, invertir\n"
     "  BEARISH  →  defensiva: proteger margen, reducir exposición\n"
     "  NEUTRAL  →  mantenimiento: estabilizar y monitorear\n\n"
     "Produce propuesta_estratega:\n"
     "  • Precio recomendado por producto y zona\n"
     "  • Mix de productos y canal\n"
     "  • Acciones sobre clientes clave\n"
     "  • Metas de volumen (toneladas)",
     "#3fb950"),

    ("ETAPA 4 — ANALISTA DE RIESGO  •  agents/risk_mgmt/risk_analyst.py  •  max_risk_discuss_rounds=1",
     "Lee: propuesta_estratega + datos_consolidados + perfil_riesgo_zona\n\n"
     "Evalúa 6 dimensiones de riesgo:\n"
     "  1. Riesgo de precio        →  guerra de precios, elasticidad de demanda\n"
     "  2. Riesgo de demanda       →  caída en licencias, ciclo de construcción\n"
     "  3. Riesgo competitivo      →  acciones de Cemex, Holcim, Corona\n"
     "  4. Riesgo financiero       →  cartera vencida, concentración de clientes\n"
     "  5. Riesgo operacional      →  inventario, logística, capacidad instalada\n"
     "  6. Riesgo macroeconómico   →  tasas de interés, inflación, TRM\n\n"
     "Produce:\n"
     "  • propuesta_ajustada   (estrategia con mitigaciones de riesgo)\n"
     "  • scorecard_riesgo     (puntuación 1-10 por dimensión)",
     "#f85149"),

    ("ETAPA 5 — GERENTE  •  agents/managers/manager.py  •  claude-sonnet-4-6",
     "Lee TODO el ZonaState:\n"
     "  veredicto + confianza + datos_consolidados + propuesta_ajustada\n"
     "  scorecard_riesgo + historial_debate + argumentos_bullish/bearish\n"
     "  perfil_riesgo_zona + memoria histórica de la zona\n\n"
     "Toma la decisión final:\n"
     "  EJECUTAR   →  aprueba la estrategia propuesta\n"
     "  MODIFICAR  →  aprueba con cambios específicos\n"
     "  RECHAZAR   →  descarta y justifica\n\n"
     "Genera:\n"
     "  • decision_final\n"
     "  • acciones_autorizadas  (lista concreta de acciones a ejecutar)\n"
     "  • justificacion         (razonamiento completo del gerente)",
     "#8957e5"),

    ("SALIDA  •  Por cada zona analizada",
     "  Decisión:    EJECUTAR  /  MODIFICAR  /  RECHAZAR\n"
     "  Acciones:    Lista concreta de acciones autorizadas\n"
     "  Scorecard:   Puntuación 1-10 en 6 dimensiones de riesgo\n"
     "  Justific.:   Razonamiento completo del gerente\n\n"
     "Componentes de soporte:\n"
     "  agents/utils/memory.py       →  Memoria histórica por zona\n"
     "  agents/utils/callbacks.py    →  Rastreo de nodo activo\n"
     "  graph/propagation.py         →  Extracción y formateo del resultado\n"
     "  graph/conditional_logic.py   →  Rutas condicionales (¿más debate? ¿más riesgo?)\n"
     "  schemas/zona_schema.py       →  Modelos Pydantic para validación\n"
     "  ui/dashboard.py              →  Dashboard visual en terminal (Rich)",
     "#58a6ff"),
]

make_diagram("CEMENT AGENTS — Arquitectura (1/2): Entrada · Datos · Analista · Debate",
             cement_p1, "/home/user/TradingAgents/cement_diagrama_1.jpg")

make_diagram("CEMENT AGENTS — Arquitectura (2/2): Debate · Estrategia · Riesgo · Decisión · Salida",
             cement_p2, "/home/user/TradingAgents/cement_diagrama_2.jpg")

print("\nListo. Archivos generados:")
print("  trading_diagrama_1.jpg  —  Entrada, Datos")
print("  trading_diagrama_2.jpg  —  Analistas, Debate, Trader")
print("  trading_diagrama_3.jpg  —  Riesgo, Señal, Salida")
print("  cement_diagrama_1.jpg   —  Entrada, Datos, Analista")
print("  cement_diagrama_2.jpg   —  Debate, Estrategia, Riesgo, Decisión, Salida")
