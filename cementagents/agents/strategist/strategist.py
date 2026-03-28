from langchain_core.messages import HumanMessage
from cementagents.agents.utils.agent_states import ZonaState


def create_strategist(llm, memory=None):
    """
    Create the strategist (commercial strategy) node.

    The strategist translates the debate verdict into actionable commercial
    recommendations for the cement zone.

    Args:
        llm: LangChain LLM instance.
        memory: Optional ZonaMemory instance for historical context.

    Returns:
        A node function compatible with LangGraph.
    """

    def strategist_node(state: ZonaState) -> dict:
        zona = state["zona"]
        veredicto = state.get("veredicto", "NEUTRAL")
        confianza = state.get("confianza", 0.5)
        datos = state.get("datos_consolidados", "")
        historial_debate = state.get("historial_debate", [])
        perfil_riesgo = state.get("perfil_riesgo_zona", "Neutral")

        # Get memory context
        memoria_str = ""
        if memory is not None:
            memoria_str = memory.get_memory(zona)

        # Build debate summary
        debate_resumen = "\n\n".join(historial_debate[-2:]) if historial_debate else "Sin historial de debate."

        # Direction-specific guidance
        if veredicto == "BULLISH":
            orientacion = """
ORIENTACIÓN ALCISTA - El mercado presenta oportunidades. Propón estrategias ofensivas:
- Incremento de precios: Evalúa el espacio para subir precios dado el diferencial actual vs competencia
- Captura de share: Identifica segmentos de clientes y proyectos donde ganar participación
- Mix premium: Promociona productos de mayor valor agregado (concretos especiales, sacos premium)
- Expansión comercial: Nuevos clientes, nuevas licitaciones, incremento de cuota por cliente
- Inversión en servicio: Refuerza propuesta de valor para justificar precio premium"""
        elif veredicto == "BEARISH":
            orientacion = """
ORIENTACIÓN BAJISTA - El mercado presenta riesgos. Propón estrategias defensivas:
- Defensa de precio: Define el piso mínimo de precio para no destruir valor, evitar guerra de precios
- Optimización de costos: Reduce costo logístico, optimiza rutas, revisa eficiencia operacional
- Gestión de cartera: Prioriza clientes con menor riesgo crediticio, reduce exposición a morosos
- Reducción de inventario: Acciones para bajar días de stock al rango óptimo (15-18 días)
- Retención de clientes clave: Enfoca recursos en los clientes más importantes para evitar pérdidas"""
        else:  # NEUTRAL
            orientacion = """
ORIENTACIÓN NEUTRAL - Mercado en equilibrio. Propón estrategias de consolidación y monitoreo:
- Mantener precios: Sin variaciones agresivas hasta mayor claridad del mercado
- Eficiencia operacional: Mejoras incrementales en logística e inventario
- Vigilancia competitiva: Monitoreo estrecho de movimientos de Cemex, Holcim y otros
- Desarrollo de pipeline: Asegurar proyectos en la cartera para suavizar demanda futura
- Gestión proactiva de cartera: Cobro preventivo antes de que la situación se deteriore"""

        prompt = f"""Eres el Estratega Comercial del sistema de inteligencia de cemento para Colombia - Zona: {zona}.

Has recibido el análisis del mercado y el veredicto del debate. Tu tarea es traducir este veredicto en una PROPUESTA ESTRATÉGICA COMERCIAL concreta y accionable para el equipo de ventas y la gerencia de zona.

VEREDICTO DEL DEBATE: {veredicto} (Confianza: {confianza:.0%})
PERFIL DE RIESGO DE LA ZONA: {perfil_riesgo}

DATOS DEL MERCADO:
{datos}

SÍNTESIS DEL DEBATE:
{debate_resumen}

HISTORIAL DE ESTRATEGIAS PREVIAS:
{memoria_str}

{orientacion}

Tu PROPUESTA ESTRATÉGICA debe incluir:

1. **DIAGNÓSTICO EJECUTIVO** (2-3 oraciones): Situación actual de la zona en términos de mercado, competencia y operaciones.

2. **ESTRATEGIA DE PRICING**:
   - Precio recomendado o rango (COP/ton)
   - Variación propuesta vs precio actual (%)
   - Justificación basada en diferencial competitivo y elasticidad de demanda

3. **ESTRATEGIA DE VOLUMEN**:
   - Meta de ventas ajustada (tons)
   - Segmentos/clientes prioritarios
   - Proyectos o licitaciones clave a ganar

4. **ESTRATEGIA DE MIX DE PRODUCTOS**:
   - Productos a impulsar (granel, saco, concreto especial)
   - Razón estratégica

5. **GESTIÓN OPERACIONAL**:
   - Acción sobre inventario (si está fuera de rango 15-18 días)
   - Acción sobre cartera vencida (si >5%)
   - Eficiencia logística

6. **INVERSIÓN COMERCIAL RECOMENDADA**:
   - Descuentos, bonificaciones o inversión en servicio
   - Criterios de focalización

7. **KPIs A MONITOREAR** (mínimo 4):
   - Métricas específicas con umbrales de alerta

8. **RIESGOS DE LA ESTRATEGIA** (2-3 riesgos principales con mitigación)

Sé específico, usa los números del análisis y propón acciones que el equipo comercial pueda implementar en las próximas 4 semanas."""

        response = llm.invoke([HumanMessage(content=prompt)])

        return {
            "propuesta_estratega": response.content,
        }

    return strategist_node
