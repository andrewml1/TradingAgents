from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import date


class IndicadoresMacro(BaseModel):
    """Macroeconomic indicators relevant to the cement market."""
    pib_construccion_yoy: float = Field(..., description="GDP construction growth year-over-year (%)")
    licencias_vivienda_yoy: float = Field(..., description="Housing permits growth year-over-year (%)")
    tasa_interes: float = Field(..., description="Reference interest rate (%)")
    inflacion: float = Field(..., description="Inflation rate (%)")
    trm: float = Field(..., description="Exchange rate COP/USD")


class MercadoLocal(BaseModel):
    """Local market share and competitive data."""
    share_argos: float = Field(..., description="Argos market share (%)")
    share_competidor_1: float = Field(..., description="Main competitor market share (%)")
    precio_promedio_argos: float = Field(..., description="Average price Argos (COP/ton)")
    precio_promedio_competencia: float = Field(..., description="Average price competition (COP/ton)")
    diferencial_precio_pct: float = Field(..., description="Price differential vs competition (%)")
    proyectos_pipeline: int = Field(..., description="Number of construction projects in pipeline")
    nuevas_licitaciones: int = Field(..., description="Number of new tenders opened")


class DatosInternos(BaseModel):
    """Internal operations data."""
    ventas_mtd: float = Field(..., description="Sales month-to-date (tons)")
    ventas_ytd: float = Field(..., description="Sales year-to-date (tons)")
    ventas_vs_budget: float = Field(..., description="Sales vs budget ratio (1.0 = 100%)")
    inventario_dias: float = Field(..., description="Inventory in days")
    cartera_vencida_pct: float = Field(..., description="Overdue portfolio as % of total")
    clientes_activos: int = Field(..., description="Number of active clients")
    top_5_concentracion_pct: float = Field(..., description="Top 5 clients concentration (%)")
    costo_logistica_ton: float = Field(..., description="Logistics cost per ton (COP)")


class RiesgosIdentificados(BaseModel):
    """Identified risk with severity and type."""
    descripcion: str = Field(..., description="Risk description")
    severidad: Literal["Alta", "Media", "Baja"] = Field(..., description="Risk severity")
    tipo: str = Field(..., description="Risk type (e.g., Competitivo, Financiero, Operacional)")


class EstrategiaRecomendada(BaseModel):
    """Recommended commercial strategy."""
    accion_pricing: str = Field(..., description="Pricing action to take")
    variacion_precio_pct: float = Field(..., description="Recommended price variation (%)")
    accion_volumen: str = Field(..., description="Volume action to take")
    accion_mix: str = Field(..., description="Product mix action")
    perfil_riesgo: str = Field(..., description="Risk profile applied")
    inversion_comercial: str = Field(..., description="Commercial investment recommendation")


class ZonaAnalysis(BaseModel):
    """Complete zone analysis output."""
    zona: str = Field(..., description="Zone name")
    fecha_analisis: str = Field(..., description="Analysis date")
    indicadores_macro: IndicadoresMacro = Field(..., description="Macroeconomic indicators")
    mercado_local: MercadoLocal = Field(..., description="Local market data")
    datos_internos: DatosInternos = Field(..., description="Internal operations data")
    veredicto: Optional[Literal["BULLISH", "BEARISH", "NEUTRAL"]] = Field(
        None, description="Market verdict"
    )
    confianza: Optional[float] = Field(
        None, description="Confidence level (0.0-1.0)", ge=0.0, le=1.0
    )
    estrategia_recomendada: Optional[EstrategiaRecomendada] = Field(
        None, description="Recommended strategy"
    )
    riesgos_identificados: List[RiesgosIdentificados] = Field(
        default_factory=list, description="List of identified risks"
    )
    decision_manager: Optional[Literal["EJECUTAR", "MODIFICAR", "RECHAZAR"]] = Field(
        None, description="Manager final decision"
    )
    justificacion_decision: Optional[str] = Field(
        None, description="Justification for the manager's decision"
    )
