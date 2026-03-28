import json
from langchain_core.messages import HumanMessage
from cementagents.agents.utils.agent_states import ZonaState
from cementagents.agents.utils.callbacks import set_active_node


def create_data_analyst(llm, dataflow_fn):
    """
    Create a data analyst node.

    Args:
        llm: LangChain LLM instance.
        dataflow_fn: callable(zona: str) -> dict with all raw indicators.

    Returns:
        A node function compatible with LangGraph.
    """

    def analyst_node(state: ZonaState) -> dict:
        set_active_node("analyst")
        zona = state["zona"]
        fecha = state["fecha_analisis"]

        # Get raw data from the dataflow function
        raw_data = dataflow_fn(zona)

        prompt = f"""Eres el Analista de Datos del sistema de inteligencia comercial de cemento para Colombia.

Zona: {zona}
Fecha: {fecha}
Datos recopilados:
{json.dumps(raw_data, ensure_ascii=False, indent=2)}

Tu tarea es consolidar y normalizar estos datos en un reporte estructurado que incluya:

1. **Resumen de Indicadores Macro**: Interpreta el PIB construcción, licencias de vivienda, tasa de interés, inflación y TRM en relación con el ciclo del mercado cementero.

2. **Situación del Mercado Local**: Analiza participaciones de mercado, brechas de precio frente a la competencia, proyectos en pipeline y tendencias competitivas. Identifica si Argos está ganando o perdiendo share.

3. **Estado de las Operaciones Internas**: Evalúa ventas MTD/YTD vs presupuesto, nivel de inventario (óptimo: 15-18 días), cartera vencida (alerta >5%), concentración de clientes (riesgo si top-5 >40%), y eficiencia logística.

4. **Señales de Alerta Tempranas**: Identifica explícitamente cualquier indicador fuera de rango óptimo con etiqueta [ALERTA], [RIESGO] o [OPORTUNIDAD].

5. **Contexto Competitivo**: Describe el panorama competitivo local, acciones recientes de competidores y posicionamiento relativo de Argos.

Usa los números exactos de los datos. Sé preciso y analítico. No agregues información que no esté en los datos provistos."""

        response = llm.invoke([HumanMessage(content=prompt)])

        from cementagents.agents.utils.callbacks import _get_buffer
        _get_buffer().complete_current_agent()
        return {
            "datos_consolidados": response.content,
        }

    return analyst_node
