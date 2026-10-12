"""
Agent Memory Mesh CLI.

Provides command-line memory graph management, time-travel inspection,
and token compression metrics with Rich formatting.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional

# Ensure UTF-8 console output on Windows
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import click
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from memory_mesh.core.checkpoint import AtomicCheckpoint
from memory_mesh.core.compressor import LosslessGraphCompressor
from memory_mesh.core.graph import MemoryGraph
from memory_mesh.storage.sqlite import SqliteStorage
from memory_mesh.version import __author__, __doctrine__, __version__

console = Console(legacy_windows=False)


def _print_branding():
    banner = (
        f"[bold magenta]🧠 Agent Memory Mesh[/bold magenta] [bold white]v{__version__}[/bold white]\n"
        f"[dim]The Bi-Temporal State Graph & Lossless Context Compression Engine for AI Agents[/dim]\n"
        f"[dim cyan]Doctrine: {__doctrine__} • Maintained by {__author__}[/dim cyan]"
    )
    console.print(Panel(banner, border_style="magenta", expand=False))


@click.group()
@click.version_option(version=__version__, prog_name="memory-mesh")
def cli():
    """Agent Memory Mesh — Bi-temporal knowledge graph and context compression."""
    pass


@cli.command("info")
def info():
    """Displays system information, doctrine, and enterprise gateway links."""
    _print_branding()
    rprint("\n[bold]Core Principles:[/bold]")
    rprint("  1. [cyan]Bi-Temporal Ground-Truth[/cyan]: Valid Time (real world) vs Transaction Time (system assertion)")
    rprint("  2. [green]Automatic Superseding[/green]: Eliminates contradictory obsolete memory without losing history")
    rprint("  3. [yellow]Lossless Graph Compression[/yellow]: Replaces verbose chat logs with dense semantic triples\n")
    rprint("[bold]Community & Enterprise Gateway:[/bold]")
    rprint("  • GitHub: [blue]https://github.com/BenniAlencar/agent-memory-mesh[/blue]")
    rprint("  • Benni Master OS: [blue]https://bennios.dev[/blue]")
    rprint("  • Operator Hub: [blue]https://hub.bennios.dev[/blue]\n")


@cli.command("store")
@click.argument("subject")
@click.argument("predicate")
@click.argument("value")
@click.option("--db", default="memory_mesh.db", help="SQLite database path.")
@click.option("--provenance", default="cli_operator", help="Source provenance.")
def store(subject: str, predicate: str, value: str, db: str, provenance: str):
    """Stores a verified fact into the persistent memory mesh."""
    _print_branding()
    storage = SqliteStorage(db)
    graph = MemoryGraph()
    # Pre-populate with existing nodes from SQLite
    existing_nodes = storage.query_nodes(subject=subject, predicate=predicate, include_superseded=True)
    for n in existing_nodes:
        graph.nodes[n.id] = n

    new_node = graph.add_fact(
        subject=subject,
        predicate=predicate,
        object_value=value,
        provenance=provenance,
    )

    # Persist all modified/new nodes and relations
    for n in graph.nodes.values():
        storage.save_node(n)
    for r in graph.relations:
        storage.save_relation(r)

    console.print(f"[bold green]✔ Fact stored successfully![/bold green]")
    console.print(f"  • ID: [cyan]{new_node.id}[/cyan]")
    console.print(f"  • Triple: ([bold]{subject}[/bold]) -[{predicate}]-> [yellow]{value}[/yellow]")
    console.print(f"  • SHA-256 Digest: [dim]{new_node.digest[:16]}...[/dim]")


@cli.command("recall")
@click.option("--subject", default=None, help="Subject filter.")
@click.option("--predicate", default=None, help="Predicate filter.")
@click.option("--db", default="memory_mesh.db", help="SQLite database path.")
@click.option("--include-superseded", is_flag=True, default=False, help="Include historical superseded facts.")
def recall(subject: Optional[str], predicate: Optional[str], db: str, include_superseded: bool):
    """Queries active facts from the persistent database."""
    _print_branding()
    storage = SqliteStorage(db)
    nodes = storage.query_nodes(subject=subject, predicate=predicate, include_superseded=include_superseded)

    if not nodes:
        console.print("[yellow]No matching facts found in memory mesh.[/yellow]")
        return

    table = Table(title="Knowledge Graph Memory Query", border_style="magenta")
    table.add_column("Subject", style="cyan")
    table.add_column("Predicate", style="bold white")
    table.add_column("Value", style="green")
    table.add_column("Status", style="bold")
    table.add_column("Valid From", style="dim")

    for n in nodes:
        is_active = n.temporal.is_current()
        status_str = "[green]ACTIVE[/green]" if is_active else "[red]SUPERSEDED[/red]"
        val_str = str(n.object_value)[:40]
        table.add_row(n.subject, n.predicate, val_str, status_str, n.temporal.valid_from[:19])

    console.print(table)


@cli.command("compress")
@click.option("--db", default="memory_mesh.db", help="SQLite database path.")
def compress(db: str):
    """Compiles the active memory state into a minimal-token prompt injection block."""
    _print_branding()
    storage = SqliteStorage(db)
    nodes = storage.query_nodes(include_superseded=False)

    graph = MemoryGraph()
    for n in nodes:
        graph.nodes[n.id] = n

    compressor = LosslessGraphCompressor()
    compressed = compressor.compress(graph)

    console.print("[bold cyan]Compiled Lossless Context Prompt Block:[/bold cyan]")
    console.print(Panel(compressed, border_style="cyan"))

    tokens = compressor.estimate_token_count(compressed)
    console.print(f"[bold green]Estimated Prompt Overhead:[/bold green] ~{tokens} tokens for {len(nodes)} active ground-truth facts.")


@cli.command("snapshot")
@click.argument("output_path", default="memory_snapshot.json")
@click.option("--db", default="memory_mesh.db", help="SQLite database path.")
def snapshot(output_path: str, db: str):
    """Exports an atomic, SHA-256 sealed snapshot of the database."""
    _print_branding()
    storage = SqliteStorage(db)
    nodes = storage.query_nodes(include_superseded=True)

    graph = MemoryGraph()
    for n in nodes:
        graph.nodes[n.id] = n

    saved = AtomicCheckpoint.save_to_file(graph, output_path)
    console.print(f"[bold green]✔ Atomic snapshot created at:[/bold green] [cyan]{saved.resolve()}[/cyan]")


if __name__ == "__main__":
    cli()
