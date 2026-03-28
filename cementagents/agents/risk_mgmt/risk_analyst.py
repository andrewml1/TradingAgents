import re
from langchain_core.messages import HumanMessage
from cementagents.agents.utils.agent_states import ZonaState
from cementagents.agents.utils.callbacks import set_active_node


def create_risk_analyst(llm):
    """
    Create the risk analyst node.

    Evaluates the strategist's proposal against multiple risk dimensions and
    produces a risk-adjusted proposal and a structured scorecard.

    Args:
        llm: LangChain LLM instance.

    Returns:
        A node function compatible with LangGraph.
    """

    def risk_node(state: ZonaState) -> dict:
        set_active_node("risk_analyst")
        zona = state["zona"]
        propuesta = state.get("propuesta_estratega", "")
        datos = state.get("datos_consolidados", "")
        perfil_riesgo = state.get("perfil_riesgo_zona", "Neutral")
        veredicto = state.get("veredicto", "NEUTRAL")
        rondas = state.get("rondas_riesgo", 0)
        historial_riesgo = state.get("historial_riesgo", [])

        # Include previous risk feedback if this is a revision round
        contexto_previo = ""
        if rondas > 0 and historial_riesgo:
            contexto_previo = f"""
ANÁLISIS DE RIESGO PREVIO (Ronda {rondas}):
{historial_riesgo[-1]}

En esta ronda, profundiza en los riesgos marcados como ALTO y verifica si la propuesta los mitiga adecuadamente.
"""

        prompt = f"""Eres el Analista de Riesgos del sistema de inteligencia comercial de cemento para Colombia - Zona: {zona}.

Tu tarea es evaluar la propuesta estratégica del Estratega Comercial desde una perspectiva de gestión de riesgos y producir:
1. Un SCORECARD DE RIESGO estructurado
2. Una PROPUESTA AJUSTADA que incorpore las mitigaciones necesarias

PERFIL DE RIESGO DE LA ZONA: {perfil_riesgo}
VEREDICTO DEL MERCADO: {veredicto}
RONDA DE ANÁLISIS: {rondas + 1}

DATOS DEL MERCADO:
{datos}

PROPUESTA ESTRATÉGICA A EVALUAR:
{propuesta}
{contexto_previo}

DIMENSIONES DE RIESGO A EVALUAR:

1. **Riesgo de Concentración de Clientes**
   - Umbral de alerta: Top-5 clientes >40% de ventas
   - Evalúa la exposición si se pierden clientes clave

2. **Riesgo de Guerra de Precios**
   - Analiza si la estrategia de pricing es defensible ante movimientos competitivos
   - Considera la tendencia de precios de competencia

3. **Riesgo de Inventario**
   - Óptimo: 15-18 días. Evalúa si inventario está fuera de rango
   - Considera el capital inmovilizado y riesgo de obsolescencia

4. **Riesgo de Cartera / Crédito**
   - Umbral de alerta: Cartera vencida >5%
   - Evalúa exposición por cliente y sector

5. **Riesgo Macroeconómico**
   - Sensibilidad de la demanda a tasas de interés altas (9.75%)
   - Impacto de licencias de vivienda negativas o estancadas
   - Exposición a volatilidad del peso colombiano

6. **Riesgo Operacional / Logístico**
   - Evalúa si el costo logístico es competitivo
   - Riesgo de abastecimiento o disrupciones

PERFIL DE RIESGO Y CALIBRACIÓN:
- Si perfil es CONSERVADOR: Sé más estricto, recomienda márgenes de seguridad más altos
- Si perfil es NEUTRAL: Balance entre oportunidad y prudencia
- Si perfil es AGRESIVO: Acepta más riesgo si el retorno potencial lo justifica

Ajustes según perfil {perfil_riesgo}:
{"- Reduce exposición a clientes concentrados. Limita variaciones de precio >3%. Exige garantías en cartera." if perfil_riesgo == "Conservador" else ""}
{"- Acepta riesgo moderado. Variaciones de precio hasta 5%. Gestión activa de cartera." if perfil_riesgo == "Neutral" else ""}
{"- Toma posiciones ofensivas. Variaciones de precio hasta 8%. Inversión en captura de share." if perfil_riesgo == "Agresivo" else ""}

FORMATO DE RESPUESTA OBLIGATORIO:

SCORECARD DE RIESGO - {zona}
========================================
Riesgo Concentración Clientes: [BAJO|MEDIO|ALTO] (score: X/10)
Análisis: [1-2 oraciones]

Riesgo Guerra de Precios: [BAJO|MEDIO|ALTO] (score: X/10)
Análisis: [1-2 oraciones]

Riesgo Inventario: [BAJO|MEDIO|ALTO] (score: X/10)
Análisis: [1-2 oraciones]

Riesgo Cartera/Crédito: [BAJO|MEDIO|ALTO] (score: X/10)
Análisis: [1-2 oraciones]

Riesgo Macroeconómico: [BAJO|MEDIO|ALTO] (score: X/10)
Análisis: [1-2 oraciones]

Riesgo Operacional/Logístico: [BAJO|MEDIO|ALTO] (score: X/10)
Análisis: [1-2 oraciones]

RIESGO GLOBAL: [BAJO|MEDIO|MEDIO-ALTO|ALTO]
SCORE GLOBAL: X/10

PROPUESTA AJUSTADA:
[La propuesta del estratega con modificaciones específicas para mitigar los riesgos identificados.
Incluye: ajustes de precio, límites de exposición por cliente, acciones de cartera, y palancas de mitigación.
Mantén la orientación estratégica pero con guardarraíles de riesgo apropiados para el perfil {perfil_riesgo}.]"""

        response = llm.invoke([HumanMessage(content=prompt)])
        content = response.content

        # Extract scorecard (everything before PROPUESTA AJUSTADA)
        scorecard = content
        propuesta_ajustada = content

        # Try to split into scorecard and adjusted proposal
        split_marker = re.search(r"PROPUESTA AJUSTADA:", content, re.IGNORECASE)
        if split_marker:
            scorecard = content[:split_marker.start()].strip()
            propuesta_ajustada = content[split_marker.start():].strip()

        entrada_riesgo = (
            f"[Analista de Riesgo - Ronda {rondas + 1}]\n"
            f"Perfil: {perfil_riesgo}\n"
            f"{content}"
        )

        from cementagents.agents.utils.callbacks import _get_buffer
        _get_buffer().complete_current_agent()
        return {
            "historial_riesgo": [entrada_riesgo],
            "propuesta_ajustada": propuesta_ajustada,
            "scorecard_riesgo": scorecard,
            "rondas_riesgo": rondas + 1,
        }

    return risk_node
