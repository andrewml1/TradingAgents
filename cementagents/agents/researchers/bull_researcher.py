from langchain_core.messages import HumanMessage
from cementagents.agents.utils.agent_states import ZonaState
from cementagents.agents.utils.callbacks import set_active_node


def create_bull_researcher(llm, memory=None):
    """
    Create a bullish researcher node for cement zone analysis.

    Args:
        llm: LangChain LLM instance.
        memory: Optional ZonaMemory instance for historical context.

    Returns:
        A node function compatible with LangGraph.
    """

    def bull_node(state: ZonaState) -> dict:
        set_active_node("bull_researcher")
        zona = state["zona"]
        datos = state.get("datos_consolidados", "")
        argumentos_bearish = state.get("argumentos_bearish", [])
        rondas = state.get("rondas_debate", 0)

        # Get memory context if available
        memoria_str = ""
        if memory is not None:
            memoria_str = memory.get_memory(zona)

        # Build counter-argument context for cross-examination rounds
        ultimo_argumento_bearish = ""
        if argumentos_bearish:
            ultimo_argumento_bearish = argumentos_bearish[-1]

        cross_examination = ""
        if rondas > 0 and ultimo_argumento_bearish:
            cross_examination = f"""
RONDA DE CONTRAARGUMENTACIÓN (Ronda {rondas + 1}):
El analista bajista argumentó lo siguiente en la ronda anterior:
{ultimo_argumento_bearish}

Debes refutar ESPECÍFICAMENTE estos argumentos bajistas con datos concretos y razonamiento sólido.
"""

        prompt = f"""Eres el Investigador ALCISTA (Bull Researcher) del sistema de inteligencia comercial de cemento para Colombia - Zona: {zona}.

Tu rol es construir el caso más sólido posible para una perspectiva OPTIMISTA del mercado cementero en esta zona.

DATOS DEL ANALISTA:
{datos}

HISTORIAL DE DECISIONES PREVIAS:
{memoria_str}
{cross_examination}

ARGUMENTOS A CONSTRUIR - Enfócate en los factores más relevantes para el mercado cementero colombiano:

1. **Demanda y Construcción**: ¿El PIB construcción, licencias de vivienda y proyectos pipeline apuntan a crecimiento? ¿Hay mega-proyectos de infraestructura (vías 4G/5G, vivienda VIS, obras civiles)?

2. **Posicionamiento Competitivo**: ¿Tiene Argos ventajas en precio, marca, logística o relaciones comerciales en esta zona? ¿El diferencial de precio es justificable por calidad/servicio?

3. **Momentum de Ventas**: ¿Las ventas MTD/YTD muestran aceleración? ¿Se están ganando nuevas licitaciones? ¿El pipeline de proyectos es robusto?

4. **Condiciones de Mercado Favorables**: ¿La TRM alta favorece a producción local vs importaciones? ¿Los competidores muestran debilidad?

5. **Oportunidades de Crecimiento**: ¿Hay segmentos de clientes sin capturar? ¿Existe potencial de incremento de precios dado el diferencial actual?

Presenta un argumento PERSUASIVO, basado en los datos, que justifique una postura ALCISTA. Usa números específicos de los datos provistos. Sé directo y convincente."""

        response = llm.invoke([HumanMessage(content=prompt)])

        argumento = f"[Ronda {rondas + 1}] Bull Researcher - {zona}:\n{response.content}"

        from cementagents.agents.utils.callbacks import _get_buffer
        _get_buffer().complete_current_agent()
        return {
            "argumentos_bullish": [argumento],
        }

    return bull_node
