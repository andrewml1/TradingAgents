import re
from langchain_core.messages import HumanMessage
from cementagents.agents.utils.agent_states import ZonaState
from cementagents.agents.utils.callbacks import set_active_node


def create_debate_moderator(llm):
    """
    Create a debate moderator node.

    The moderator evaluates the bull and bear arguments, synthesizes them,
    and produces a verdict (BULLISH/BEARISH/NEUTRAL) with a confidence score.

    Args:
        llm: LangChain LLM instance.

    Returns:
        A node function compatible with LangGraph.
    """

    def moderator_node(state: ZonaState) -> dict:
        set_active_node("debate_moderator")
        zona = state["zona"]
        argumentos_bullish = state.get("argumentos_bullish", [])
        argumentos_bearish = state.get("argumentos_bearish", [])
        rondas = state.get("rondas_debate", 0)
        datos = state.get("datos_consolidados", "")

        # Build debate summary
        bull_text = "\n\n".join(argumentos_bullish) if argumentos_bullish else "Sin argumentos alcistas aún."
        bear_text = "\n\n".join(argumentos_bearish) if argumentos_bearish else "Sin argumentos bajistas aún."

        prompt = f"""Eres el Moderador del Debate del sistema de inteligencia comercial de cemento para Colombia - Zona: {zona}.

Has supervisado el debate entre el Investigador Alcista y el Investigador Bajista. Tu tarea es evaluar imparcialmente los argumentos de ambos lados y emitir un VEREDICTO definitivo sobre las perspectivas comerciales de esta zona.

DATOS BASE DEL ANALISTA:
{datos}

ARGUMENTOS ALCISTAS (Bull Researcher):
{bull_text}

ARGUMENTOS BAJISTAS (Bear Researcher):
{bear_text}

RONDA ACTUAL: {rondas + 1}

Tu análisis debe:
1. Identificar los 3 argumentos más sólidos de cada lado
2. Determinar qué perspectiva está mejor sustentada en los datos concretos
3. Emitir un veredicto con nivel de confianza

Criterios para el veredicto:
- BULLISH: Si los indicadores de demanda, competitividad y operaciones apuntan mayoritariamente a crecimiento y oportunidad
- BEARISH: Si los riesgos, presiones competitivas y debilidades operacionales predominan
- NEUTRAL: Si hay un equilibrio genuino entre oportunidades y riesgos, o incertidumbre significativa

La confianza refleja qué tan claro es el panorama (0.5 = muy incierto, 0.9 = muy claro).

RESPONDE EXACTAMENTE EN ESTE FORMATO:
VEREDICTO: [BULLISH|BEARISH|NEUTRAL]
CONFIANZA: [número entre 0.0 y 1.0]
SINTESIS: [Tu síntesis del debate en 3-5 párrafos, incluyendo los argumentos más convincentes de cada lado y la justificación del veredicto]
FACTORES_CLAVE: [Lista de 3-5 factores determinantes separados por punto y coma]"""

        response = llm.invoke([HumanMessage(content=prompt)])
        content = response.content

        # Parse veredicto
        veredicto = "NEUTRAL"
        veredicto_match = re.search(r"VEREDICTO:\s*(BULLISH|BEARISH|NEUTRAL)", content, re.IGNORECASE)
        if veredicto_match:
            veredicto = veredicto_match.group(1).upper()

        # Parse confianza
        confianza = 0.6
        confianza_match = re.search(r"CONFIANZA:\s*([0-9]*\.?[0-9]+)", content)
        if confianza_match:
            try:
                val = float(confianza_match.group(1))
                confianza = max(0.0, min(1.0, val))
            except ValueError:
                confianza = 0.6

        entrada_debate = (
            f"[Moderador - Ronda {rondas + 1}]\n"
            f"Veredicto: {veredicto} (Confianza: {confianza:.0%})\n"
            f"{content}"
        )

        from cementagents.agents.utils.callbacks import _get_buffer
        _get_buffer().complete_current_agent()
        return {
            "historial_debate": [entrada_debate],
            "veredicto": veredicto,
            "confianza": confianza,
            "rondas_debate": rondas + 1,
        }

    return moderator_node
