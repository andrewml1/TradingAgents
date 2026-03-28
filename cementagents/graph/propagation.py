from cementagents.agents.utils.agent_states import ZonaState


class CementPropagator:
    """Extracts and formats final results from the graph state."""

    @staticmethod
    def extract_results(state: dict) -> dict:
        """Extract clean, serializable results from the final graph state.

        Args:
            state: Final ZonaState dictionary from graph invocation.

        Returns:
            Dictionary with key result fields.
        """
        return {
            "zona": state.get("zona", ""),
            "fecha_analisis": state.get("fecha_analisis", ""),
            "veredicto": state.get("veredicto", "NEUTRAL"),
            "confianza": state.get("confianza", 0.5),
            "propuesta_estratega": state.get("propuesta_estratega", ""),
            "propuesta_ajustada": state.get("propuesta_ajustada", ""),
            "scorecard_riesgo": state.get("scorecard_riesgo", ""),
            "decision_final": state.get("decision_final", ""),
            "acciones_autorizadas": state.get("acciones_autorizadas", ""),
            "justificacion": state.get("justificacion", ""),
            "datos_consolidados": state.get("datos_consolidados", ""),
            "argumentos_bullish": state.get("argumentos_bullish", []),
            "argumentos_bearish": state.get("argumentos_bearish", []),
            "historial_debate": state.get("historial_debate", []),
            "historial_riesgo": state.get("historial_riesgo", []),
        }

    @staticmethod
    def format_report(results: dict) -> str:
        """Format results as a readable text report.

        Args:
            results: Dictionary of results (from extract_results or analyze_zona).

        Returns:
            Formatted multi-section string report.
        """
        zona = results.get("zona", "Desconocida")
        fecha = results.get("fecha_analisis", "N/A")
        veredicto = results.get("veredicto", "NEUTRAL")
        confianza = results.get("confianza", 0.5)
        decision = results.get("decision_final", "N/A")
        justificacion = results.get("justificacion", "")
        scorecard = results.get("scorecard_riesgo", "")
        propuesta_ajustada = results.get("propuesta_ajustada", "")
        acciones = results.get("acciones_autorizadas", "")

        # Veredicto emoji/marker
        veredicto_marker = {
            "BULLISH": "[ALCISTA]",
            "BEARISH": "[BAJISTA]",
            "NEUTRAL": "[NEUTRAL]",
        }.get(veredicto, "[N/A]")

        decision_marker = {
            "EJECUTAR": "[EJECUTAR]",
            "MODIFICAR": "[MODIFICAR]",
            "RECHAZAR": "[RECHAZAR]",
        }.get(decision, "[N/A]")

        separator = "=" * 70

        lines = [
            separator,
            f"REPORTE DE INTELIGENCIA COMERCIAL - ARGOS COLOMBIA",
            separator,
            f"Zona:            {zona}",
            f"Fecha:           {fecha}",
            f"Veredicto:       {veredicto_marker} {veredicto}",
            f"Confianza:       {confianza:.0%}",
            f"Decision Final:  {decision_marker} {decision}",
            separator,
            "",
            "JUSTIFICACION DE LA DECISION",
            "-" * 40,
            justificacion if justificacion else "No disponible.",
            "",
            "SCORECARD DE RIESGO",
            "-" * 40,
            scorecard if scorecard else "No disponible.",
            "",
            "PROPUESTA ESTRATEGICA AJUSTADA",
            "-" * 40,
            propuesta_ajustada if propuesta_ajustada else "No disponible.",
            "",
            "ACCIONES AUTORIZADAS",
            "-" * 40,
            acciones if acciones else "No disponible.",
            "",
            separator,
        ]

        return "\n".join(lines)
