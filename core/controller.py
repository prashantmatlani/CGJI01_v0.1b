
# core/controller.py

from rich.console import Console
from rich.panel import Panel
from dream_engine.interpreter import interpret_dream
from core.agent_orchestrator import run_agents
from agents.jung_unified_agent import jung_unified_chat
from core.intent_detector import detect_intent

import time


console = Console()


def run_terminal():
    console.print(Panel.fit(
        "[bold cyan]CGJI01 — Jungian Intelligence v0.1[/bold cyan]\n"
        "Local Analytical Psychology System",
        border_style="cyan"
    ))

    while True:
        console.print("\n[bold yellow]Select Mode:[/bold yellow]")
        console.print("1. Dream Analysis")
        console.print("2. Psychological Material Analysis")
        console.print("3. JU01")
        console.print("4. Exit")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            print("Dream Analysis")
            handle_dream_mode()

        elif choice == "2":
            print("Psychological Material Analysis")
            handle_general_analysis()

        #elif choice == "3":
        #    jung_unified_chat()

        elif choice == "3":
            print("JU")
            from agents.jung_unified_agent import jung_unified_chat
            jung_unified_chat()

        elif choice == "4":
            console.print("\n[bold green]Exiting JI01.[/bold green]")
            break

        else:
            console.print("[bold red]Invalid choice. Try again.[/bold red]")


# ---------------------------
# DREAM MODE
# ---------------------------

def handle_dream_mode():
    console.print("\n[bold cyan]Enter dream content:[/bold cyan]")
    text = input("> ")

    intent = detect_intent(text)

    if intent in ["diagnostic", "minimal"]:
        console.print("\n[bold green]System Status:[/bold green]")
        console.print("✓ Dream engine operational")
        return

    # Step 1 — Symbol Extraction
    dream_data = interpret_dream(text)

    console.print("\n[bold magenta]Symbolic Extraction:[/bold magenta]")
    console.print(dream_data)

    # Step 2 — Multi-Agent Jung Analysis
    console.print("\n[bold cyan]Running Jungian Multi-Agent Analysis...[/bold cyan]")

    total_start = time.perf_counter()
    analysis = run_agents(text)
    total_end = time.perf_counter()

    console.print("\n[bold green]Multi-Agent Synthesis/Faciliated Output:[/bold green]")
    console.print(analysis)

    console.print(
        f"\n[bold green]Total Execution Time: {(total_end - total_start)/60:.2f} minutes ({total_end - total_start:.2f} seconds)[/bold green]"
    )


# ---------------------------
# GENERAL PSYCHOLOGICAL MODE
# ---------------------------

def handle_general_analysis():
    console.print("\n[bold cyan]Enter psychological material:[/bold cyan]")
    text = input("> ")

    intent = detect_intent(text)

    if intent in ["diagnostic", "minimal"]:
        console.print("\n[bold green]System Status:[/bold green]")
        console.print("✓ JI01 operational")
        return

    console.print("\n[bold cyan]Running Jungian Multi-Agent Analysis...[/bold cyan]")

    total_start = time.perf_counter()
    #print("DEBUG: run_agents called")
    analysis = run_agents(text)
    total_end = time.perf_counter()

    console.print("\n[bold green]Multi-Agent Synthesis/Facilitated Output:[/bold green]")
    console.print(analysis)

    console.print(
        #f"\n[bold green]Total Execution Time: {total_end - total_start:.2f} seconds[/bold green]"
        f"\n[bold green]Total Execution Time: {(total_end - total_start)/60:.2f} minutes[/bold green]"
    )





"""
from rich.console import Console
from rich.panel import Panel
from dream_engine.interpreter import interpret_dream
from core.agent_orchestrator import run_agents


console = Console()


def run_terminal():
    console.print(Panel.fit(
        "[bold cyan]JI01 — Jungian Intelligence v0.1[/bold cyan]\n"
        "Local Analytical Psychology System",
        border_style="cyan"
    ))

    while True:
        console.print("\n[bold yellow]Select Mode:[/bold yellow]")
        console.print("1. Dream Analysis")
        console.print("2. Psychological Material Analysis")
        console.print("3. Exit")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            handle_dream_mode()

        elif choice == "2":
            handle_general_analysis()

        elif choice == "3":
            console.print("\n[bold green]Exiting JI01.[/bold green]")
            break

        else:
            console.print("[bold red]Invalid choice. Try again.[/bold red]")


# ---------------------------
# DREAM MODE
# ---------------------------

def handle_dream_mode():
    console.print("\n[bold cyan]Enter dream content:[/bold cyan]")
    text = input("> ")

    # Step 1 — Symbol Extraction
    dream_data = interpret_dream(text)

    console.print("\n[bold magenta]Symbolic Extraction:[/bold magenta]")
    console.print(dream_data)

    # Step 2 — Multi-Agent Jung Analysis
    console.print("\n[bold cyan]Running Jungian Multi-Agent Analysis...[/bold cyan]")
    analysis = run_agents(text)

    console.print("\n[bold green]Multi-Agent Synthesis:[/bold green]")
    console.print(analysis)


# ---------------------------
# GENERAL PSYCHOLOGICAL MODE
# ---------------------------

def handle_general_analysis():
    console.print("\n[bold cyan]Enter psychological material:[/bold cyan]")
    text = input("> ")

    console.print("\n[bold cyan]Running Jungian Multi-Agent Analysis...[/bold cyan]")
    analysis = run_agents(text)

    console.print("\n[bold green]Multi-Agent Synthesis:[/bold green]")
    console.print(analysis)
"""

