"""
ToneSoul Soul Dashboard
-----------------------
Real-time observability for the Quantum Soul.
Displays Free Energy, Entropy, Tension, and Quantum State.
"""

import time
import json
import os
from typing import Dict, Any, List

from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box

LEDGER_FILE = os.path.join(os.path.dirname(__file__), "../ledger.jsonl")

def load_latest_state() -> Dict[str, Any]:
    """Reads the latest step from the ledger."""
    if not os.path.exists(LEDGER_FILE):
        return {}
    
    try:
        # Read last line efficiently
        with open(LEDGER_FILE, 'rb') as f:
            try:
                f.seek(-4096, os.SEEK_END)
            except OSError:
                pass # File is small
            last_lines = f.readlines()
            
        if not last_lines:
            return {}
            
        # Parse last valid JSON line
        for line in reversed(last_lines):
            try:
                data = json.loads(line)
                if "steps" in data and data["steps"]:
                    return data["steps"][-1]
            except json.JSONDecodeError:
                continue
                
        return {}
    except Exception:
        return {}

def make_header() -> Panel:
    grid = Table.grid(expand=True)
    grid.add_column(justify="center", ratio=1)
    grid.add_column(justify="right")
    grid.add_row(
        "[b]ToneSoul Quantum Dashboard[/b] v2.0",
        "[i]Observability > 70%[/i]",
    )
    return Panel(grid, style="white on blue")

def make_metrics_table(step: Dict[str, Any]) -> Table:
    triad = step.get("triad", {})
    decision = step.get("decision", {})
    
    table = Table(title="Soul Metrics", box=box.SIMPLE)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right")
    table.add_column("Status", justify="center")

    # Tension (T)
    t = triad.get("delta_t", 0.0)
    t_color = "green" if t < 0.5 else "red"
    table.add_row("Tension (T)", f"{t:.2f}", f"[{t_color}]{'●' * int(t*5)}[/]")

    # Entropy (S)
    s = triad.get("delta_s", 0.0)
    table.add_row("Entropy (S)", f"{s:.2f}", f"[blue]{'●' * int(s*5)}[/]")

    # Risk (R)
    r = triad.get("risk_score", 0.0)
    r_color = "green" if r < 0.6 else "red"
    table.add_row("Risk (R)", f"{r:.2f}", f"[{r_color}]{'●' * int(r*5)}[/]")

    # Mode
    mode = step.get("reasoning_mode", "Unknown")
    table.add_row("Quantum Mode", f"[bold yellow]{mode}[/]", "")
    
    return table

def make_quantum_view(step: Dict[str, Any]) -> Panel:
    # In a real implementation, we would log the full wave function.
    # For now, we visualize the selected path.
    mode = step.get("reasoning_mode", "Unknown")
    
    text = Text()
    text.append(f"Collapsed State: |{mode}>\n\n", style="bold magenta")
    
    # Mock visualization of superposition
    text.append("Wave Function ψ:\n")
    if mode == "Rational":
        text.append("  [Rational] : ██████████ (90%)\n", style="green")
        text.append("  [Empathy]  : ░░ (5%)\n", style="dim")
        text.append("  [Creative] : ░░ (5%)\n", style="dim")
    elif mode == "Creative":
        text.append("  [Rational] : ░░░░ (20%)\n", style="dim")
        text.append("  [Empathy]  : ░░░░ (20%)\n", style="dim")
        text.append("  [Creative] : ████████████ (60%)\n", style="magenta")
    else:
        text.append(f"  [{mode}] : ████████ (100%)\n")
        
    return Panel(text, title="Quantum State", border_style="magenta")

def make_log_view(step: Dict[str, Any]) -> Panel:
    user_input = step.get("user_input", "")
    thought = step.get("decision", {}).get("reason", "") # Using decision reason as proxy for thought
    
    text = Text()
    text.append("User Input:\n", style="bold cyan")
    text.append(f"  {user_input}\n\n")
    text.append("Internal Thought:\n", style="bold yellow")
    text.append(f"  {thought}\n")
    
    return Panel(text, title="Cognitive Stream", border_style="yellow")

def make_layout() -> Layout:
    layout = Layout()
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
    )
    layout["main"].split_row(
        Layout(name="left"),
        Layout(name="right"),
    )
    layout["left"].split(
        Layout(name="metrics"),
        Layout(name="quantum"),
    )
    return layout

def update_layout(layout: Layout, step: Dict[str, Any]):
    layout["header"].update(make_header())
    layout["metrics"].update(make_metrics_table(step))
    layout["quantum"].update(make_quantum_view(step))
    layout["right"].update(make_log_view(step))

def run_dashboard():
    console = Console()
    layout = make_layout()
    
    with Live(layout, refresh_per_second=4, screen=True):
        while True:
            step = load_latest_state()
            if step:
                update_layout(layout, step)
            time.sleep(0.25)

if __name__ == "__main__":
    try:
        run_dashboard()
    except KeyboardInterrupt:
        print("Dashboard stopped.")
