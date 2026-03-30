import json
from datetime import datetime
from pathlib import Path

from cementagents.agents.utils.agent_states import ZonaState

REPORTS_DIR = Path(__file__).parent.parent.parent / "reports"


class CementPropagator:
    """Extrae, formatea y persiste los resultados del grafo."""

    @staticmethod
    def extract_results(state: dict) -> dict:
        return {
            "zona":               state.get("zona", ""),
            "fecha_analisis":     state.get("fecha_analisis", ""),
            "veredicto":          state.get("veredicto", "NEUTRAL"),
            "confianza":          state.get("confianza", 0.5),
            # Por agente
            "datos_consolidados": state.get("datos_consolidados", ""),
            "argumentos_bullish": state.get("argumentos_bullish", []),
            "argumentos_bearish": state.get("argumentos_bearish", []),
            "historial_debate":   state.get("historial_debate", []),
            "propuesta_estratega":state.get("propuesta_estratega", ""),
            "scorecard_riesgo":   state.get("scorecard_riesgo", ""),
            "propuesta_ajustada": state.get("propuesta_ajustada", ""),
            "historial_riesgo":   state.get("historial_riesgo", []),
            "decision_final":     state.get("decision_final", ""),
            "acciones_autorizadas":state.get("acciones_autorizadas", ""),
            "justificacion":      state.get("justificacion", ""),
        }

    @staticmethod
    def save_report(result: dict) -> Path:
        """Guarda el resultado completo en reports/ZONA_FECHA_HORA.json."""
        REPORTS_DIR.mkdir(exist_ok=True)
        zona_slug = result["zona"].replace(" ", "_")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = REPORTS_DIR / f"{zona_slug}_{ts}.json"
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    @staticmethod
    def load_report(path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def list_reports() -> list[Path]:
        if not REPORTS_DIR.exists():
            return []
        return sorted(REPORTS_DIR.glob("*.json"), reverse=True)

    @staticmethod
    def format_report(results: dict) -> str:
        zona      = results.get("zona", "Desconocida")
        fecha     = results.get("fecha_analisis", "N/A")
        veredicto = results.get("veredicto", "NEUTRAL")
        confianza = results.get("confianza", 0.5)
        decision  = results.get("decision_final", "N/A")

        veredicto_marker = {"BULLISH": "[ALCISTA]", "BEARISH": "[BAJISTA]", "NEUTRAL": "[NEUTRAL]"}.get(veredicto, "")
        decision_marker  = {"EJECUTAR": "[EJECUTAR]", "MODIFICAR": "[MODIFICAR]", "RECHAZAR": "[RECHAZAR]"}.get(decision, "")
        sep = "=" * 70

        lines = [
            sep,
            "REPORTE DE INTELIGENCIA COMERCIAL - ARGOS COLOMBIA",
            sep,
            f"Zona:            {zona}",
            f"Fecha:           {fecha}",
            f"Veredicto:       {veredicto_marker} {veredicto}",
            f"Confianza:       {confianza:.0%}",
            f"Decision Final:  {decision_marker} {decision}",
            sep, "",
            "JUSTIFICACION DE LA DECISION", "-" * 40,
            results.get("justificacion", "No disponible."), "",
            "SCORECARD DE RIESGO", "-" * 40,
            results.get("scorecard_riesgo", "No disponible."), "",
            "PROPUESTA ESTRATEGICA AJUSTADA", "-" * 40,
            results.get("propuesta_ajustada", "No disponible."), "",
            "ACCIONES AUTORIZADAS", "-" * 40,
            results.get("acciones_autorizadas", "No disponible."), "",
            sep,
        ]
        return "\n".join(lines)

    @staticmethod
    def format_agent_detail(result: dict, agente: str) -> str:
        """Devuelve el análisis detallado de un agente específico."""
        sep = "─" * 70
        agente_lower = agente.lower()

        if "analista" in agente_lower or "datos" in agente_lower:
            titulo  = "ANALISTA DE DATOS"
            content = result.get("datos_consolidados", "Sin datos.")

        elif "bullish" in agente_lower or "alcista" in agente_lower:
            titulo  = "INVESTIGADOR BULLISH"
            partes  = result.get("argumentos_bullish", [])
            content = "\n\n".join(f"[Ronda {i+1}]\n{p}" for i, p in enumerate(partes)) or "Sin argumentos."

        elif "bearish" in agente_lower or "bajista" in agente_lower:
            titulo  = "INVESTIGADOR BEARISH"
            partes  = result.get("argumentos_bearish", [])
            content = "\n\n".join(f"[Ronda {i+1}]\n{p}" for i, p in enumerate(partes)) or "Sin argumentos."

        elif "debate" in agente_lower or "moderador" in agente_lower:
            titulo  = "MODERADOR DE DEBATE"
            partes  = result.get("historial_debate", [])
            content = "\n\n".join(f"[Ronda {i+1}]\n{p}" for i, p in enumerate(partes)) or "Sin historial."

        elif "estratega" in agente_lower:
            titulo  = "ESTRATEGA COMERCIAL"
            content = result.get("propuesta_estratega", "Sin propuesta.")

        elif "riesgo" in agente_lower:
            titulo  = "ANALISTA DE RIESGOS"
            sc      = result.get("scorecard_riesgo", "")
            prop    = result.get("propuesta_ajustada", "")
            content = f"SCORECARD:\n{sc}\n\nPROPUESTA AJUSTADA:\n{prop}" if sc or prop else "Sin análisis."

        elif "manager" in agente_lower:
            titulo  = "MANAGER"
            decision = result.get("decision_final", "N/A")
            just     = result.get("justificacion", "")
            acciones = result.get("acciones_autorizadas", "")
            content  = f"DECISION: {decision}\n\nJUSTIFICACION:\n{just}\n\nACCIONES:\n{acciones}"

        else:
            return f"Agente '{agente}' no reconocido. Opciones: analista, bullish, bearish, debate, estratega, riesgos, manager"

        return f"\n{'=' * 70}\n{titulo} — {result.get('zona','')}\n{sep}\n{content}\n{'=' * 70}"
