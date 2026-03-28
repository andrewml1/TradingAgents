from langchain_core.messages import HumanMessage
from cementagents.agents.utils.agent_states import ZonaState


def create_bear_researcher(llm, memory=None):
    """
    Create a bearish researcher node for cement zone analysis.

    Args:
        llm: LangChain LLM instance.
        memory: Optional ZonaMemory instance for historical context.

    Returns:
        A node function compatible with LangGraph.
    """

    def bear_node(state: ZonaState) -> dict:
        zona = state["zona"]
        datos = state.get("datos_consolidados", "")
        argumentos_bullish = state.get("argumentos_bullish", [])
        rondas = state.get("rondas_debate", 0)

        # Get memory context if available
        memoria_str = ""
        if memory is not None:
            memoria_str = memory.get_memory(zona)

        # Build counter-argument context for cross-examination rounds
        ultimo_argumento_bullish = ""
        if argumentos_bullish:
            ultimo_argumento_bullish = argumentos_bullish[-1]

        cross_examination = ""
        if rondas > 0 and ultimo_argumento_bullish:
            cross_examination = f"""
RONDA DE CONTRAARGUMENTACIÓN (Ronda {rondas + 1}):
El analista alcista argumentó lo siguiente en la ronda anterior:
{ultimo_argumento_bullish}

Debes refutar ESPECÍFICAMENTE estos argumentos alcistas, exponiendo sus debilidades y suposiciones excesivamente optimistas con datos concretos.
"""

        prompt = f"""Eres el Investigador BAJISTA (Bear Researcher) del sistema de inteligencia comercial de cemento para Colombia - Zona: {zona}.

Tu rol es construir el caso más sólido posible para una perspectiva PESIMISTA o de PRECAUCIÓN del mercado cementero en esta zona.

DATOS DEL ANALISTA:
{datos}

HISTORIAL DE DECISIONES PREVIAS:
{memoria_str}
{cross_examination}

ARGUMENTOS A CONSTRUIR - Enfócate en los riesgos más relevantes para el mercado cementero colombiano:

1. **Riesgos de Demanda**: ¿Las licencias de vivienda están cayendo? ¿La alta tasa de interés (9.75%) está frenando la construcción privada? ¿El pipeline de proyectos es insuficiente?

2. **Presión Competitiva**: ¿Los competidores están bajando precios (señal de guerra de precios)? ¿El diferencial de precio de Argos es insostenible? ¿Se está perdiendo market share?

3. **Problemas Operacionales**: ¿El inventario está por encima del óptimo (>18 días)? ¿La cartera vencida es elevada (>5%)? ¿Las ventas están por debajo del presupuesto?

4. **Riesgos Financieros**: ¿La alta concentración en pocos clientes genera riesgo? ¿Los costos logísticos son insostenibles? ¿El margen bruto está deteriorándose?

5. **Factores Macroeconómicos Adversos**: ¿La inflación está erosionando márgenes? ¿La TRM alta encarece insumos importados? ¿Hay riesgo político o regulatorio en la zona?

Presenta un argumento CONVINCENTE y basado en datos que justifique una postura BAJISTA o de ALTA PRECAUCIÓN. Usa números específicos de los datos provistos. Sé riguroso y no suavices los riesgos."""

        response = llm.invoke([HumanMessage(content=prompt)])

        argumento = f"[Ronda {rondas + 1}] Bear Researcher - {zona}:\n{response.content}"

        return {
            "argumentos_bearish": [argumento],
        }

    return bear_node
