#!/usr/bin/env python3
"""Cement Sales Intelligence System - Main Entry Point"""

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint
from datetime import date

from cementagents import CementAgentsGraph
from cementagents.default_config import DEFAULT_CONFIG
from cementagents.graph.propagation import CementPropagator

app = typer.Typer(
    name="cement-agents",
    help="Cement Sales Intelligence Multi-Agent System for Argos Colombia",
)
console = Console()


@app.command()
def analyze(
    zona: str = typer.Option(
        None, "--zona", "-z", help="Specific zona to analyze"
    ),
    perfil_riesgo: str = typer.Option(
        "Neutral",
        "--perfil",
        "-p",
        help="Risk profile: Agresivo | Neutral | Conservador",
    ),
    all_zonas: bool = typer.Option(
        False, "--all", "-a", help="Analyze all configured zonas"
    ),
    debug: bool = typer.Option(
        False, "--debug", "-d", help="Show additional debug output"
    ),
    fecha: str = typer.Option(
        None,
        "--fecha",
        "-f",
        help="Analysis date (YYYY-MM-DD). Defaults to today.",
    ),
):
    """Run cement market analysis for one or all zonas."""

    if not zona and not all_zonas:
        console.print(
            "[red]Error: Debes especificar --zona ZONA o --all para analizar todas.[/red]"
        )
        console.print(
            "\nZonas disponibles: "
            + ", ".join(DEFAULT_CONFIG["zonas"])
        )
        raise typer.Exit(1)

    analysis_date = fecha or str(date.today())

    config = DEFAULT_CONFIG.copy()
    config["risk_profile"] = perfil_riesgo

    console.print(
        Panel.fit(
            f"[bold blue]Cement Sales Intelligence System[/bold blue]\n"
            f"Argos Colombia | Fecha: {analysis_date} | "
            f"Perfil de Riesgo: [bold]{perfil_riesgo}[/bold]",
            border_style="blue",
        )
    )

    graph = CementAgentsGraph(config=config)

    if zona:
        # Validate zona name
        available = config["zonas"]
        if zona not in available:
            console.print(
                f"[red]Error: Zona '{zona}' no encontrada.[/red]\n"
                f"Zonas disponibles: {', '.join(available)}"
            )
            raise typer.Exit(1)

        with console.status(
            f"[yellow]Analizando zona [bold]{zona}[/bold]...[/yellow]"
        ):
            result = graph.analyze_zona(
                zona, perfil_riesgo=perfil_riesgo, fecha=analysis_date
            )

        report = CementPropagator.format_report(result)
        console.print(report)

        if debug:
            console.print("\n[dim]--- DEBUG: Argumentos Alcistas ---[/dim]")
            for i, arg in enumerate(result.get("argumentos_bullish", []), 1):
                console.print(f"[dim]{i}. {arg[:300]}...[/dim]")

            console.print("\n[dim]--- DEBUG: Argumentos Bajistas ---[/dim]")
            for i, arg in enumerate(result.get("argumentos_bearish", []), 1):
                console.print(f"[dim]{i}. {arg[:300]}...[/dim]")

    elif all_zonas:
        results = {}
        zonas_list = config["zonas"]

        for z in zonas_list:
            with console.status(
                f"[yellow]Analizando [bold]{z}[/bold] "
                f"({zonas_list.index(z) + 1}/{len(zonas_list)})...[/yellow]"
            ):
                results[z] = graph.analyze_zona(
                    z, perfil_riesgo=perfil_riesgo, fecha=analysis_date
                )

        # Summary table
        table = Table(
            title=f"Resumen de Analisis - Todas las Zonas | {analysis_date}",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Zona", style="cyan", min_width=15)
        table.add_column("Veredicto", style="bold", justify="center", min_width=12)
        table.add_column("Confianza", justify="center", min_width=10)
        table.add_column("Decision", style="bold", justify="center", min_width=12)
        table.add_column("Perfil Riesgo", justify="center", min_width=14)

        colors = {
            "BULLISH": "green",
            "BEARISH": "red",
            "NEUTRAL": "yellow",
        }
        decision_colors = {
            "EJECUTAR": "green",
            "MODIFICAR": "yellow",
            "RECHAZAR": "red",
        }

        for z, r in results.items():
            v = r.get("veredicto", "N/A")
            d = r.get("decision_final", "N/A")
            conf = r.get("confianza", 0.0)
            table.add_row(
                z,
                f"[{colors.get(v, 'white')}]{v}[/]",
                f"{conf:.0%}",
                f"[{decision_colors.get(d, 'white')}]{d}[/]",
                perfil_riesgo,
            )

        console.print(table)

        # Print detailed reports if debug mode
        if debug:
            for z, r in results.items():
                console.print(f"\n[bold cyan]--- Detalle: {z} ---[/bold cyan]")
                console.print(CementPropagator.format_report(r))


if __name__ == "__main__":
    app()
