from datetime import date

MOCK_DATA = {
    "Costa Caribe": {
        "indicadores_macro": {
            "pib_construccion_yoy": 3.2,
            "licencias_vivienda_yoy": -5.1,
            "tasa_interes": 9.75,
            "inflacion": 5.8,
            "trm": 4180.5
        },
        "mercado_local": {
            "share_argos": 42,
            "share_competidor_1": 28,  # Cemex
            "share_competidor_2": 18,  # Holcim
            "share_otros": 12,
            "precio_promedio_argos": 38500,
            "precio_promedio_competencia": 37200,
            "diferencial_precio_pct": 3.5,
            "proyectos_pipeline": 145,
            "nuevas_licitaciones": 12,
            "competidores_activos": ["Cemex", "Holcim", "Corona"],
            "tendencia_precios_competencia": "estable"
        },
        "datos_internos": {
            "ventas_mtd": 125000,
            "ventas_ytd": 380000,
            "ventas_vs_budget": 0.95,
            "inventario_dias": 18,
            "cartera_vencida_pct": 4.2,
            "clientes_activos": 892,
            "top_5_concentracion_pct": 38,
            "costo_logistica_ton": 42000,
            "margen_bruto_pct": 31.5
        },
        "alertas": []
    },
    "Antioquia": {
        "indicadores_macro": {
            "pib_construccion_yoy": 4.1,
            "licencias_vivienda_yoy": 2.3,
            "tasa_interes": 9.75,
            "inflacion": 5.8,
            "trm": 4180.5
        },
        "mercado_local": {
            "share_argos": 55,
            "share_competidor_1": 25,  # Cemex
            "share_competidor_2": 12,  # Corona
            "share_otros": 8,
            "precio_promedio_argos": 41200,
            "precio_promedio_competencia": 39800,
            "diferencial_precio_pct": 3.5,
            "proyectos_pipeline": 203,
            "nuevas_licitaciones": 18,
            "competidores_activos": ["Cemex", "Corona"],
            "tendencia_precios_competencia": "bajando"  # Signal of price war
        },
        "datos_internos": {
            "ventas_mtd": 198000,
            "ventas_ytd": 590000,
            "ventas_vs_budget": 0.98,
            "inventario_dias": 22,  # Above optimal
            "cartera_vencida_pct": 6.8,  # High
            "clientes_activos": 1240,
            "top_5_concentracion_pct": 45,  # High concentration
            "costo_logistica_ton": 38000,
            "margen_bruto_pct": 29.8
        },
        "alertas": ["Cemex bajó precios 3% - posible guerra de precios", "2 clientes top con mora >60 días"]
    },
    "Centro": {
        "indicadores_macro": {
            "pib_construccion_yoy": 1.8,
            "licencias_vivienda_yoy": -8.2,
            "tasa_interes": 9.75,
            "inflacion": 5.8,
            "trm": 4180.5
        },
        "mercado_local": {
            "share_argos": 31,
            "share_competidor_1": 35,  # Holcim - leader
            "share_competidor_2": 22,  # Cemex
            "share_otros": 12,
            "precio_promedio_argos": 43500,
            "precio_promedio_competencia": 41800,
            "diferencial_precio_pct": 4.1,
            "proyectos_pipeline": 312,
            "nuevas_licitaciones": 45,
            "competidores_activos": ["Holcim", "Cemex", "Corona", "Ultracem"],
            "tendencia_precios_competencia": "estable"
        },
        "datos_internos": {
            "ventas_mtd": 285000,
            "ventas_ytd": 820000,
            "ventas_vs_budget": 0.88,  # Below budget
            "inventario_dias": 25,  # High
            "cartera_vencida_pct": 3.1,
            "clientes_activos": 2150,
            "top_5_concentracion_pct": 28,
            "costo_logistica_ton": 55000,  # High logistics cost
            "margen_bruto_pct": 27.2
        },
        "alertas": ["Ventas 12% bajo presupuesto", "Inventario elevado 25 días"]
    },
    "Sur": {
        "indicadores_macro": {
            "pib_construccion_yoy": 5.8,
            "licencias_vivienda_yoy": 7.2,
            "tasa_interes": 9.75,
            "inflacion": 5.8,
            "trm": 4180.5
        },
        "mercado_local": {
            "share_argos": 38,
            "share_competidor_1": 30,  # Holcim
            "share_competidor_2": 20,  # Cemex
            "share_otros": 12,
            "precio_promedio_argos": 40100,
            "precio_promedio_competencia": 39500,
            "diferencial_precio_pct": 1.5,
            "proyectos_pipeline": 178,
            "nuevas_licitaciones": 22,
            "competidores_activos": ["Holcim", "Cemex"],
            "tendencia_precios_competencia": "subiendo"
        },
        "datos_internos": {
            "ventas_mtd": 156000,
            "ventas_ytd": 445000,
            "ventas_vs_budget": 1.08,  # Above budget
            "inventario_dias": 14,  # Low - good
            "cartera_vencida_pct": 2.8,
            "clientes_activos": 985,
            "top_5_concentracion_pct": 32,
            "costo_logistica_ton": 45000,
            "margen_bruto_pct": 33.1
        },
        "alertas": []
    },
    "Eje Cafetero": {
        "indicadores_macro": {
            "pib_construccion_yoy": 2.9,
            "licencias_vivienda_yoy": 1.1,
            "tasa_interes": 9.75,
            "inflacion": 5.8,
            "trm": 4180.5
        },
        "mercado_local": {
            "share_argos": 48,
            "share_competidor_1": 32,  # Corona
            "share_competidor_2": 15,
            "share_otros": 5,
            "precio_promedio_argos": 39800,
            "precio_promedio_competencia": 38900,
            "diferencial_precio_pct": 2.3,
            "proyectos_pipeline": 89,
            "nuevas_licitaciones": 8,
            "competidores_activos": ["Corona", "Cemex"],
            "tendencia_precios_competencia": "estable"
        },
        "datos_internos": {
            "ventas_mtd": 72000,
            "ventas_ytd": 215000,
            "ventas_vs_budget": 1.02,
            "inventario_dias": 16,
            "cartera_vencida_pct": 3.5,
            "clientes_activos": 542,
            "top_5_concentracion_pct": 41,
            "costo_logistica_ton": 41000,
            "margen_bruto_pct": 30.8
        },
        "alertas": []
    },
    "Santanderes": {
        "indicadores_macro": {
            "pib_construccion_yoy": 3.7,
            "licencias_vivienda_yoy": 4.5,
            "tasa_interes": 9.75,
            "inflacion": 5.8,
            "trm": 4180.5
        },
        "mercado_local": {
            "share_argos": 35,
            "share_competidor_1": 40,  # Cemex - leader
            "share_competidor_2": 18,
            "share_otros": 7,
            "precio_promedio_argos": 40500,
            "precio_promedio_competencia": 40100,
            "diferencial_precio_pct": 1.0,
            "proyectos_pipeline": 112,
            "nuevas_licitaciones": 15,
            "competidores_activos": ["Cemex", "Holcim"],
            "tendencia_precios_competencia": "subiendo"
        },
        "datos_internos": {
            "ventas_mtd": 88000,
            "ventas_ytd": 262000,
            "ventas_vs_budget": 0.94,
            "inventario_dias": 19,
            "cartera_vencida_pct": 4.9,
            "clientes_activos": 678,
            "top_5_concentracion_pct": 36,
            "costo_logistica_ton": 48000,
            "margen_bruto_pct": 28.9
        },
        "alertas": ["Cemex lidera mercado local - oportunidad de ganar share"]
    },
    "Llanos": {
        "indicadores_macro": {
            "pib_construccion_yoy": 7.2,  # High growth - oil/mining activity
            "licencias_vivienda_yoy": 9.8,
            "tasa_interes": 9.75,
            "inflacion": 5.8,
            "trm": 4180.5
        },
        "mercado_local": {
            "share_argos": 52,
            "share_competidor_1": 28,
            "share_competidor_2": 15,
            "share_otros": 5,
            "precio_promedio_argos": 44200,
            "precio_promedio_competencia": 43100,
            "diferencial_precio_pct": 2.6,
            "proyectos_pipeline": 67,
            "nuevas_licitaciones": 9,
            "competidores_activos": ["Cemex"],
            "tendencia_precios_competencia": "subiendo"
        },
        "datos_internos": {
            "ventas_mtd": 45000,
            "ventas_ytd": 132000,
            "ventas_vs_budget": 1.15,  # Well above budget
            "inventario_dias": 12,  # Low - very good
            "cartera_vencida_pct": 2.1,
            "clientes_activos": 312,
            "top_5_concentracion_pct": 55,  # High concentration
            "costo_logistica_ton": 62000,  # High due to distance
            "margen_bruto_pct": 35.2
        },
        "alertas": ["Alta concentración en pocos clientes de oil & gas"]
    }
}


def get_zona_data(zona: str) -> dict:
    """Get mock data for a given zona.

    Args:
        zona: Zone name string.

    Returns:
        Dictionary with all zone indicators plus metadata.

    Raises:
        ValueError: If the zone is not found in mock data.
    """
    if zona not in MOCK_DATA:
        raise ValueError(
            f"Zona '{zona}' not found. Available zones: {list(MOCK_DATA.keys())}"
        )

    data = MOCK_DATA[zona].copy()
    data["zona"] = zona
    data["fecha_consulta"] = str(date.today())
    return data
