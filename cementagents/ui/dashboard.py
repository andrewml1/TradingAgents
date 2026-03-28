"""
Dashboard TUI para Cement Sales Intelligence System.
Replica el estilo de TradingAgents: progreso de agentes a la izquierda,
mensajes/razonamiento a la derecha, reporte actual abajo.
"""

import time
import threading
from collections import deque
from datetime import datetime

from rich import box
from rich.layout import Layout
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.spinner import Spinner
from rich.table import Table
from rich.text import Text


# ─── Estructura de equipos ────────────────────────────────────────────────────

TEAMS = {
    "Equipo Analista":     ["Analista de Datos"],
    "Equipo Investigador": ["Investigador Bullish", "Investigador Bearish"],
    "Moderación":          ["Moderador de Debate"],
    "Equipo Estratega":    ["Estratega Comercial"],
    "Equipo de Riesgos":   ["Analista de Riesgos"],
    "Gestión":             ["Manager"],
}

NODE_TO_AGENT = {
    "analyst":          "Analista de Datos",
    "bull_researcher":  "Investigador Bullish",
    "bear_researcher":  "Investigador Bearish",
    "debate_moderator": "Moderador de Debate",
    "strategist":       "Estratega Comercial",
    "risk_analyst":     "Analista de Riesgos",
    "manager":          "Manager",
}

TYPE_COLORS = {
    "Razonamiento": "green",
    "Herramienta":  "cyan",
    "Veredicto":    "yellow",
    "Decision":     "magenta",
    "Error":        "red",
    "Sistema":      "blue",
}


# ─── Buffer de estado ─────────────────────────────────────────────────────────

class CementMessageBuffer:
    def __init__(self, max_messages: int = 200):
        self.messages: deque = deque(maxlen=max_messages)
        self.current_report: str = ""
        self.current_token_buffer: str = ""
        self.agent_status: dict = {}
        self.current_agent: str = ""
        self.llm_calls: int = 0
        self.tokens_out: int = 0
        self.zona: str = ""
        self.start_time: float = time.time()
        self._lock = threading.Lock()
        self._init_agents()

    def _init_agents(self):
        for agents in TEAMS.values():
            for agent in agents:
                self.agent_status[agent] = "pendiente"

    def set_zona(self, zona: str):
        with self._lock:
            self.zona = zona
            self.start_time = time.time()
            # Reset estado para nueva zona
            self._init_agents()
            self.messages.clear()
            self.current_report = ""
            self.current_token_buffer = ""
            self.llm_calls = 0
            self.tokens_out = 0

    def set_agent_active(self, node_name: str):
        agent = NODE_TO_AGENT.get(node_name, node_name)
        with self._lock:
            # Marcar agente anterior como completado
            if self.current_agent and self.agent_status.get(self.current_agent) == "en proceso":
                self.agent_status[self.current_agent] = "completado"
                # Flush tokens del agente anterior
                if self.current_token_buffer.strip():
                    ts = datetime.now().strftime("%H:%M:%S")
                    self.messages.appendleft((ts, "Razonamiento", self.current_token_buffer.strip()))
                    self.current_report = self.current_token_buffer.strip()
                    self.current_token_buffer = ""

            self.current_agent = agent
            self.agent_status[agent] = "en proceso"
            ts = datetime.now().strftime("%H:%M:%S")
            self.messages.appendleft((ts, "Sistema", f"▶ Iniciando: {agent}"))

    def add_token(self, token: str):
        with self._lock:
            self.current_token_buffer += token
            self.tokens_out += 1

    def flush_tokens(self):
        with self._lock:
            if self.current_token_buffer.strip():
                ts = datetime.now().strftime("%H:%M:%S")
                content = self.current_token_buffer.strip()
                self.messages.appendleft((ts, "Razonamiento", content))
                self.current_report = content
                self.current_token_buffer = ""
            self.llm_calls += 1

    def complete_current_agent(self):
        """Marcar el agente actual como completado y flush del buffer de tokens."""
        with self._lock:
            if self.current_agent and self.agent_status.get(self.current_agent) == "en proceso":
                self.agent_status[self.current_agent] = "completado"
            if self.current_token_buffer.strip():
                ts = datetime.now().strftime("%H:%M:%S")
                self.messages.appendleft((ts, "Razonamiento", self.current_token_buffer.strip()))
                self.current_report = self.current_token_buffer.strip()
                self.current_token_buffer = ""

    def add_message(self, msg_type: str, content: str):
        ts = datetime.now().strftime("%H:%M:%S")
        with self._lock:
            self.messages.appendleft((ts, msg_type, content))

    def mark_all_complete(self):
        with self._lock:
            for agent in self.agent_status:
                self.agent_status[agent] = "completado"
            self.current_token_buffer = ""


# Singleton global
message_buffer = CementMessageBuffer()


# ─── Layout y render ──────────────────────────────────────────────────────────

def create_layout() -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main"),
        Layout(name="footer", size=3),
    )
    layout["main"].split_column(
        Layout(name="upper", ratio=3),
        Layout(name="reporte", ratio=5),
    )
    layout["upper"].split_row(
        Layout(name="progreso", ratio=2),
        Layout(name="mensajes", ratio=3),
    )
    return layout


def _elapsed(start: float) -> str:
    s = int(time.time() - start)
    return f"{s // 60:02d}:{s % 60:02d}"


def update_display(layout: Layout):
    """Renderiza el estado actual del buffer en el layout."""

    with message_buffer._lock:
        zona        = message_buffer.zona
        agent_st    = dict(message_buffer.agent_status)
        cur_agent   = message_buffer.current_agent
        messages    = list(message_buffer.messages)
        token_buf   = message_buffer.current_token_buffer
        cur_report  = message_buffer.current_report
        llm_calls   = message_buffer.llm_calls
        tokens_out  = message_buffer.tokens_out
        start_time  = message_buffer.start_time

    # ── Header ────────────────────────────────────────────────────────────────
    zona_label = f" | Zona: [bold yellow]{zona}[/bold yellow]" if zona else ""
    layout["header"].update(Panel(
        f"[bold green]Sistema de Inteligencia Comercial — Argos Colombia[/bold green]{zona_label}",
        title="[bold]Cement Sales Intelligence[/bold]",
        border_style="green",
        padding=(0, 2),
    ))

    # ── Progreso ──────────────────────────────────────────────────────────────
    progress_table = Table(
        show_header=True,
        header_style="bold magenta",
        box=box.SIMPLE_HEAD,
        padding=(0, 2),
        expand=True,
    )
    progress_table.add_column("Equipo",  style="cyan",  justify="center", width=22)
    progress_table.add_column("Agente",  style="green", justify="center", width=22)
    progress_table.add_column("Estado",                 justify="center", width=14)

    for team, agents in TEAMS.items():
        first = True
        for agent in agents:
            status    = agent_st.get(agent, "pendiente")
            team_cell = team if first else ""
            first = False

            if status == "en proceso":
                status_cell = Spinner("dots", text="[bold cyan]en proceso[/]")
            elif status == "completado":
                status_cell = "[bold green]✓ completado[/bold green]"
            else:
                status_cell = "[dim yellow]pendiente[/dim yellow]"

            progress_table.add_row(team_cell, agent, status_cell)
        progress_table.add_row("─" * 18, "─" * 18, "─" * 12, style="dim")

    layout["progreso"].update(Panel(
        progress_table,
        title="[bold]Progreso[/bold]",
        border_style="cyan",
        padding=(1, 1),
    ))

    # ── Mensajes ──────────────────────────────────────────────────────────────
    msg_table = Table(
        show_header=True,
        header_style="bold magenta",
        box=box.MINIMAL,
        show_lines=True,
        padding=(0, 1),
        expand=True,
    )
    msg_table.add_column("Hora",      style="cyan",  width=9,  justify="center")
    msg_table.add_column("Tipo",                     width=13, justify="center")
    msg_table.add_column("Contenido", no_wrap=False, ratio=1)

    visible = list(messages)[:13]

    # Primera fila: tokens en streaming si hay buffer activo
    if token_buf.strip():
        ts = datetime.now().strftime("%H:%M:%S")
        preview = token_buf[-400:] + "▌"
        visible.insert(0, (ts, "Razonamiento", preview))
        visible = visible[:13]

    for ts, msg_type, content in visible:
        color     = TYPE_COLORS.get(msg_type, "white")
        type_cell = f"[{color}]{msg_type}[/{color}]"
        display   = content[:280] + ("…" if len(content) > 280 else "")
        msg_table.add_row(ts, type_cell, Text(display, overflow="fold"))

    layout["mensajes"].update(Panel(
        msg_table,
        title="[bold]Mensajes & Razonamiento[/bold]",
        border_style="blue",
        padding=(1, 1),
    ))

    # ── Reporte actual ────────────────────────────────────────────────────────
    if token_buf.strip():
        # Mostrar tokens en streaming
        title   = f"[bold]Generando — {cur_agent}[/bold]"
        content = Markdown(token_buf)
    elif cur_report:
        title   = f"[bold]Último reporte — {cur_agent}[/bold]"
        content = Markdown(cur_report)
    else:
        title   = "[bold]Reporte Actual[/bold]"
        content = Text("Esperando análisis...", style="italic dim")

    layout["reporte"].update(Panel(
        content,
        title=title,
        border_style="green",
        padding=(1, 2),
    ))

    # ── Footer ────────────────────────────────────────────────────────────────
    completed = sum(1 for s in agent_st.values() if s == "completado")
    total     = len(agent_st)

    parts = [
        f"Agentes: {completed}/{total}",
        f"LLM Calls: {llm_calls}",
        f"Tokens: {tokens_out:,}",
        f"⏱ {_elapsed(start_time)}",
    ]
    if cur_agent and agent_st.get(cur_agent) == "en proceso":
        parts.append(f"Activo: [bold cyan]{cur_agent}[/bold cyan]")

    stats_table = Table(show_header=False, box=None, padding=(0, 2), expand=True)
    stats_table.add_column("s", justify="center")
    stats_table.add_row(" | ".join(parts))

    layout["footer"].update(Panel(stats_table, border_style="grey50"))


# ─── Context manager ──────────────────────────────────────────────────────────

class CementLiveDashboard:
    """
    Context manager que ejecuta el dashboard TUI en un hilo de refresco
    mientras el grafo de agentes corre en el hilo principal.
    """

    def __init__(self, zona: str, refresh_per_second: int = 4):
        message_buffer.set_zona(zona)
        self.layout = create_layout()
        self.live   = Live(self.layout, screen=True, refresh_per_second=refresh_per_second)
        self._stop  = threading.Event()
        self._thread: threading.Thread | None = None

    def _refresh_loop(self):
        while not self._stop.is_set():
            update_display(self.layout)
            self.live.refresh()
            time.sleep(0.25)

    def __enter__(self):
        update_display(self.layout)
        self.live.__enter__()
        self._thread = threading.Thread(target=self._refresh_loop, daemon=True)
        self._thread.start()
        return self

    def refresh(self):
        update_display(self.layout)
        self.live.refresh()

    def __exit__(self, *args):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=2)
        message_buffer.mark_all_complete()
        update_display(self.layout)
        self.live.refresh()
        self.live.__exit__(*args)
