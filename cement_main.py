#!/usr/bin/env python3
"""Cement Sales Intelligence System - Main Entry Point"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

load_dotenv(Path(__file__).parent / ".env")

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import date

from cementagents import CementAgentsGraph
from cementagents.default_config import DEFAULT_CONFIG
from cementagents.graph.propagation import CementPropagator

app = typer.Typer(name="cement-agents", help="Cement Sales Intelligence — Argos Colombia")
console = Console()

VEREDICTO_COLORS = {"BULLISH": "green", "BEARISH": "red",    "NEUTRAL": "yellow"}
DECISION_COLORS  = {"EJECUTAR": "green","MODIFICAR": "yellow","RECHAZAR": "red"}
AGENTES          = ["analista", "bullish", "bearish", "debate", "estratega", "riesgos", "manager"]


def _validate_key(config):
    key_map = {"anthropic": "ANTHROPIC_API_KEY", "openai": "OPENAI_API_KEY"}
    env_var = key_map.get(config.get("llm_provider", "anthropic"))
    if env_var and not os.environ.get(env_var):
        console.print(f"[red]Falta [bold]{env_var}[/bold] en el archivo .env[/red]")
        raise typer.Exit(1)


def _run(graph, zona, perfil_riesgo, analysis_date, verbose):
    if verbose:
        from cementagents.ui.dashboard import CementLiveDashboard
        with CementLiveDashboard(zona) as db:
            result = graph.analyze_zona(zona, perfil_riesgo=perfil_riesgo, fecha=analysis_date)
            db.refresh()
    else:
        with console.status(f"[yellow]Analizando [bold]{zona}[/bold]...[/yellow]"):
            result = graph.analyze_zona(zona, perfil_riesgo=perfil_riesgo, fecha=analysis_date)
    return result


@app.command()
def main(
    zona: str = typer.Option(None, "--zona", "-z", help="Zona a analizar"),
    all_zonas: bool = typer.Option(False, "--all", "-a", help="Analizar todas las zonas"),
    perfil_riesgo: str = typer.Option("Neutral", "--perfil", "-p", help="Agresivo | Neutral | Conservador"),
    provider: str = typer.Option(None, "--provider", help="anthropic | openai"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Dashboard en tiempo real"),
    agente: str = typer.Option(None, "--agente",
                               help=f"Ver detalle de agente: {' | '.join(AGENTES)}"),
    fecha: str = typer.Option(None, "--fecha", "-f", help="Fecha YYYY-MM-DD (default: hoy)"),
):
    """Ejecutar análisis de mercado de cemento por zona."""

    if not zona and not all_zonas:
        console.print("[red]Especifica --zona NOMBRE o --all[/red]")
        console.print("Zonas: " + ", ".join(DEFAULT_CONFIG["zonas"]))
        raise typer.Exit(1)

    analysis_date = fecha or str(date.today())
    config = DEFAULT_CONFIG.copy()
    config["risk_profile"] = perfil_riesgo
    if provider:
        config["llm_provider"] = provider
        config["deep_think_llm"] = None
        config["quick_think_llm"] = None

    _validate_key(config)
    active_provider = config.get("llm_provider", "anthropic")

    console.print(Panel.fit(
        f"[bold blue]Cement Sales Intelligence System[/bold blue]\n"
        f"Fecha: {analysis_date} | Perfil: [bold]{perfil_riesgo}[/bold] | Provider: [bold]{active_provider}[/bold]",
        border_style="blue",
    ))

    graph = CementAgentsGraph(config=config, verbose=verbose)

    # ── Una zona ──────────────────────────────────────────────────────────────
    if zona:
        if zona not in config["zonas"]:
            console.print(f"[red]Zona '{zona}' no encontrada.[/red]")
            console.print("Disponibles: " + ", ".join(config["zonas"]))
            raise typer.Exit(1)

        result = _run(graph, zona, perfil_riesgo, analysis_date, verbose)
        console.print(CementPropagator.format_report(result))

        if agente:
            console.print(CementPropagator.format_agent_detail(result, agente))
        else:
            console.print(
                f"\n[dim]Tip: agrega [bold]--agente NOMBRE[/bold] para ver el análisis de un agente específico.[/dim]\n"
                f"[dim]Opciones: {', '.join(AGENTES)}[/dim]"
            )

    # ── Todas las zonas ───────────────────────────────────────────────────────
    elif all_zonas:
        results = {}
        for z in config["zonas"]:
            results[z] = _run(graph, z, perfil_riesgo, analysis_date, verbose)

        table = Table(
            title=f"Resumen — Todas las Zonas | {analysis_date}",
            header_style="bold magenta",
        )
        table.add_column("Zona",          style="cyan",  min_width=15)
        table.add_column("Veredicto",     justify="center", min_width=12)
        table.add_column("Confianza",     justify="center", min_width=10)
        table.add_column("Decision",      justify="center", min_width=12)
        table.add_column("Perfil Riesgo", justify="center", min_width=14)

        for z, r in results.items():
            v, d = r.get("veredicto", "N/A"), r.get("decision_final", "N/A")
            table.add_row(
                z,
                f"[{VEREDICTO_COLORS.get(v,'white')}]{v}[/]",
                f"{r.get('confianza', 0):.0%}",
                f"[{DECISION_COLORS.get(d,'white')}]{d}[/]",
                perfil_riesgo,
            )
        console.print(table)


if __name__ == "__main__":
    app()
