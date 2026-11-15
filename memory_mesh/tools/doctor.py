"""Memory Mesh Doctor — Environment, bi-temporal graph, SQLite, and checkpoint diagnostics.

Inspects Python runtime, SQLite3 version, optional adapters, and executes an
end-to-end bi-temporal supersede + lossless compression + SHA-256 checkpoint probe.
"""

from __future__ import annotations

import argparse
import gc
import importlib.util
import json
import platform
import sqlite3
import tempfile
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from memory_mesh.core.checkpoint import AtomicCheckpoint
from memory_mesh.core.compressor import LosslessGraphCompressor
from memory_mesh.core.graph import MemoryGraph
from memory_mesh.storage.sqlite import SqliteStorage
from memory_mesh.version import __doctrine__, __version__


@dataclass(frozen=True)
class DoctorReport:
    """Structured diagnostic report for Agent Memory Mesh."""

    version: str
    doctrine: str
    python_version: str
    platform: str
    sqlite_version: str
    dependencies: dict[str, bool]
    bitemporal_probe_ok: bool
    sqlite_probe_ok: bool
    checkpoint_probe_ok: bool
    probe_latency_ms: float
    healthy: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def probe_dependencies() -> dict[str, bool]:
    """Check availability of core and optional runtime dependencies."""
    packages = ("pydantic", "click", "rich", "mcp", "langchain_core", "pytest")
    return {pkg: importlib.util.find_spec(pkg) is not None for pkg in packages}


def run_doctor() -> DoctorReport:
    """Execute environment and bi-temporal memory self-checks."""
    deps = probe_dependencies()
    t0 = time.perf_counter()

    # 1. Bi-temporal supersede + compression probe
    graph = MemoryGraph()
    graph.add_fact("customer:probe", "plan", "free", valid_from="2026-01-01T00:00:00+00:00")
    graph.add_fact("customer:probe", "plan", "enterprise", valid_from="2026-06-01T00:00:00+00:00")
    active = graph.query(subject="customer:probe", predicate="plan")
    compressed = LosslessGraphCompressor().compress(graph)
    bitemporal_ok = len(active) == 1 and active[0].object_value == "enterprise" and "enterprise" in compressed

    # 2. SQLite + SHA-256 AtomicCheckpoint probe
    sqlite_ok = False
    checkpoint_ok = False
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        db_path = Path(tmp) / "doctor_mesh.db"
        storage = SqliteStorage(str(db_path))
        for n in graph.nodes.values():
            storage.save_node(n)
        for r in graph.relations:
            storage.save_relation(r)
        queried = storage.query_nodes(subject="customer:probe", include_superseded=False)
        sqlite_ok = len(queried) == 1 and queried[0].object_value == "enterprise"

        cp_path = Path(tmp) / "doctor_cp.json"
        AtomicCheckpoint.save_to_file(graph, cp_path)
        restored = AtomicCheckpoint.restore_from_file(cp_path)
        checkpoint_ok = len(restored.nodes) == len(graph.nodes)
        del storage
        gc.collect()

    latency_ms = round((time.perf_counter() - t0) * 1000.0, 2)
    healthy = (
        bitemporal_ok
        and sqlite_ok
        and checkpoint_ok
        and all(deps[k] for k in ("pydantic", "click", "rich"))
    )

    return DoctorReport(
        version=__version__,
        doctrine=__doctrine__,
        python_version=platform.python_version(),
        platform=f"{platform.system()} {platform.release()}",
        sqlite_version=sqlite3.sqlite_version,
        dependencies=deps,
        bitemporal_probe_ok=bitemporal_ok,
        sqlite_probe_ok=sqlite_ok,
        checkpoint_probe_ok=checkpoint_ok,
        probe_latency_ms=latency_ms,
        healthy=healthy,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Agent Memory Mesh environment diagnostics.")
    parser.add_argument("--json", action="store_true", help="Emit JSON report.")
    args = parser.parse_args(argv)

    report = run_doctor()
    if args.json:
        print(json.dumps(report.to_dict(), indent=2))
    else:
        status = "HEALTHY" if report.healthy else "DEGRADED"
        print(f"Agent Memory Mesh Doctor v{report.version} [{status}]")
        print(f"Python: {report.python_version} | SQLite: {report.sqlite_version} | OS: {report.platform}")
        print(
            f"Bi-Temporal: {'OK' if report.bitemporal_probe_ok else 'FAIL'} | "
            f"SQLite: {'OK' if report.sqlite_probe_ok else 'FAIL'} | "
            f"Checkpoint: {'OK' if report.checkpoint_probe_ok else 'FAIL'} ({report.probe_latency_ms} ms)"
        )
    return 0 if report.healthy else 1


if __name__ == "__main__":
    raise SystemExit(main())
