import re
from langchain_core.messages import HumanMessage
from cementagents.agents.utils.agent_states import ZonaState


def create_manager(llm, memory=None):
    """
    Create the zone manager (final decision maker) node.

    The manager synthesizes all prior analysis and makes the final commercial
    decision: EJECUTAR, MODIFICAR, or RECHAZAR.

    Args:
        llm: LangChain LLM instance.
        memory: Optional ZonaMemory instance for historical context.

    Returns:
        A node function compatible with LangGraph.
    """

    def manager_node(state: ZonaState) -> dict:
        zona = state["zona"]
        fecha = state.get("fecha_analisis", "")
        veredicto = state.get("veredicto", "NEUTRAL")
        confianza = state.get("confianza", 0.5)
        datos = state.get("datos_consolidados", "")
        propuesta_ajustada = state.get("propuesta_ajustada", "")
        scorecard_riesgo = state.get("scorecard_riesgo", "")
        historial_debate = state.get("historial_debate", [])
        perfil_riesgo = state.get("perfil_riesgo_zona", "Neutral")
        argumentos_bullish = state.get("argumentos_bullish", [])
        argumentos_bearish = state.get("argumentos_bearish", [])

        # Get memory context
        memoria_str = ""
        if memory is not None:
            memoria_str = memory.get_memory(zona)

        # Build context summaries
        debate_resumen = "\n".join(historial_debate[-1:]) if historial_debate else "Sin historial."
        bull_resumen = argumentos_bullish[-1] if argumentos_bullish else "Sin argumentos alcistas."
        bear_resumen = argumentos_bearish[-1] if argumentos_bearish else "Sin argumentos bajistas."

        prompt = f"""Eres el Gerente Regional de Ventas de Argos Colombia para la Zona: {zona}.

Tienes la autoridad y responsabilidad de tomar la DECISIÓN FINAL sobre la estrategia comercial para esta zona. Has recibido el análisis completo del equipo: analista de datos, investigadores alcista/bajista, moderador del debate, estratega comercial y analista de riesgos.

FECHA: {fecha}
ZONA: {zona}
VEREDICTO DEL MERCADO: {veredicto} (Confianza: {confianza:.0%})
PERFIL DE RIESGO: {perfil_riesgo}

DATOS CLAVE DEL MERCADO:
{datos}

SCORECARD DE RIESGO:
{scorecard_riesgo}

PROPUESTA ESTRATÉGICA AJUSTADA POR RIESGOS:
{propuesta_ajustada}

SÍNTESIS DEL DEBATE:
{debate_resumen}

ARGUMENTO ALCISTA FINAL:
{bull_resumen}

ARGUMENTO BAJISTA FINAL:
{bear_resumen}

DECISIONES PREVIAS EN ESTA ZONA:
{memoria_str}

CRITERIOS PARA TU DECISIÓN:

EJECUTAR: Cuando la estrategia propuesta es sólida, los riesgos son manejables y las acciones están bien calibradas para el perfil de riesgo. El mercado apoya la dirección estratégica.

MODIFICAR: Cuando la estrategia tiene la orientación correcta pero requiere ajustes específicos antes de implementar (ej: precio demasiado agresivo, se necesitan más garantías de cartera, ajustar metas de volumen).

RECHAZAR: Cuando los riesgos son demasiado altos, la estrategia no está bien calibrada, o las condiciones de mercado hacen que la propuesta sea inviable o contraproducente.

CONSIDERACIONES SEGÚN PERFIL {perfil_riesgo}:
{"- Conservador: Prioriza protección de márgenes y base de clientes sobre crecimiento. Rechaza estrategias agresivas con riesgo ALTO." if perfil_riesgo == "Conservador" else ""}
{"- Neutral: Busca equilibrio entre crecimiento y protección. Acepta riesgo MEDIO si hay potencial de upside claro." if perfil_riesgo == "Neutral" else ""}
{"- Agresivo: Prioriza captura de oportunidades. Acepta riesgo ALTO si el mercado lo justifica y hay plan de contingencia." if perfil_riesgo == "Agresivo" else ""}

FORMATO DE RESPUESTA OBLIGATORIO:

DECISION: [EJECUTAR|MODIFICAR|RECHAZAR]

JUSTIFICACION:
[3-5 párrafos explicando tu razonamiento. Incluye:
- Por qué tomaste esta decisión específica
- Los 2-3 factores más determinantes
- Cómo se alinea con el perfil de riesgo {perfil_riesgo}
- Cualquier condición o prerequisito para la implementación]

ACCIONES:
[Lista numerada de acciones concretas autorizadas, con responsable y plazo:
1. [Acción] - Responsable: [rol] - Plazo: [días/semanas]
2. [Acción] - Responsable: [rol] - Plazo: [días/semanas]
... (mínimo 5 acciones)]

KPIS_SEGUIMIENTO:
[Lista de KPIs con umbrales de alerta que el equipo debe monitorear semanalmente:
- [KPI]: Meta [valor] | Alerta si [condición]
... (mínimo 4 KPIs)]

CONDICIONES_REVISION:
[Circunstancias que triggearían una revisión urgente de la estrategia]"""

        response = llm.invoke([HumanMessage(content=prompt)])
        content = response.content

        # Parse decision
        decision_final = "MODIFICAR"  # Default to safe option
        decision_match = re.search(r"DECISION:\s*(EJECUTAR|MODIFICAR|RECHAZAR)", content, re.IGNORECASE)
        if decision_match:
            decision_final = decision_match.group(1).upper()

        # Parse justification
        justificacion = content
        justificacion_match = re.search(
            r"JUSTIFICACION:(.*?)(?:ACCIONES:|$)",
            content,
            re.IGNORECASE | re.DOTALL
        )
        if justificacion_match:
            justificacion = justificacion_match.group(1).strip()

        # Parse authorized actions
        acciones_autorizadas = ""
        acciones_match = re.search(
            r"ACCIONES:(.*?)(?:KPIS_SEGUIMIENTO:|CONDICIONES_REVISION:|$)",
            content,
            re.IGNORECASE | re.DOTALL
        )
        if acciones_match:
            acciones_autorizadas = acciones_match.group(1).strip()

        # If acciones not found separately, use full content
        if not acciones_autorizadas:
            acciones_autorizadas = content

        # Update memory if available
        if memory is not None:
            situacion_resumen = f"Zona {zona}: {veredicto} ({confianza:.0%} confianza), Riesgo: {scorecard_riesgo[:100]}"
            memory.update_memory(zona, situacion_resumen, f"Decisión: {decision_final}")

        return {
            "decision_final": decision_final,
            "acciones_autorizadas": acciones_autorizadas,
            "justificacion": justificacion,
        }

    return manager_node
