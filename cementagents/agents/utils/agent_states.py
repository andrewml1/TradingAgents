from typing import TypedDict, Annotated, Optional
import operator


class ZonaState(TypedDict):
    """State for a single zona analysis cycle."""
    zona: str
    fecha_analisis: str
    # Raw data from Analyst
    datos_consolidados: str  # JSON string with all indicators
    # Researcher outputs
    argumentos_bullish: Annotated[list, operator.add]
    argumentos_bearish: Annotated[list, operator.add]
    # Debate
    historial_debate: Annotated[list, operator.add]
    veredicto: str  # BULLISH | BEARISH | NEUTRAL
    confianza: float
    rondas_debate: int
    # Strategist
    propuesta_estratega: str
    # Risk
    historial_riesgo: Annotated[list, operator.add]
    propuesta_ajustada: str
    scorecard_riesgo: str
    rondas_riesgo: int
    # Manager
    decision_final: str  # EJECUTAR | MODIFICAR | RECHAZAR
    acciones_autorizadas: str
    justificacion: str
    # Config
    perfil_riesgo_zona: str  # Agresivo | Neutral | Conservador
