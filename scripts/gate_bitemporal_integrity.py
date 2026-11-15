#!/usr/bin/env python3
"""Bi-Temporal Integrity Gate Runner — fail-closed verification of Skill 60 & 61 invariants.

Verifies:
  1. Automatic superseding closes prior (subject, predicate) facts on write.
  2. Time-travel queries (as_of_valid_time) return accurate historical state.
  3. Present queries return zero superseded noise.
  4. Immutable decisions preserve rationale & rejected alternatives.
  5. SHA-256 AtomicCheckpoint rejects tampered snapshot files.

Usage:
    python scripts/gate_bitemporal_integrity.py
    python scripts/gate_bitemporal_integrity.py --json
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from memory_mesh.core.checkpoint import AtomicCheckpoint
from memory_mesh.core.compressor import LosslessGraphCompressor
from memory_mesh.core.graph import MemoryGraph


@dataclass(frozen=True)
class GateCheck:
    name: str
    passed: bool
    detail: str


def run_gate() -> dict[str, Any]:
    """Run all fail-closed bi-temporal and checkpoint integrity gates."""
    checks: list[GateCheck] = []
    graph = MemoryGraph()

    # 1 & 2 & 3. Supersede & time-travel
    graph.add_fact("customer:acme", "plan", "free_tier", valid_from="2026-01-01T00:00:00+00:00")
    graph.add_fact("customer:acme", "plan", "enterprise", valid_from="2026-06-01T00:00:00+00:00")

    present = graph.query(subject="customer:acme", predicate="plan")
    checks.append(
        GateCheck(
            "automatic_superseding",
            len(present) == 1 and present[0].object_value == "enterprise",
            "Present query returns only active enterprise fact",
        )
    )

    historical = graph.query(
        subject="customer:acme",
        predicate="plan",
        as_of_valid_time=datetime(2026, 3, 15, tzinfo=timezone.utc),
    )
    checks.append(
        GateCheck(
            "bitemporal_time_travel",
            len(historical) == 1 and historical[0].object_value == "free_tier",
            "Time-travel as-of March returns free_tier",
        )
    )

    # 4. Immutable decisions + lossless compression
    graph.add_decision(
        subject="db_engine",
        chosen_option="sqlite_wal",
        rationale="Zero-ops local ACID",
        alternatives=["redis", "in_memory_only"],
    )
    compressed = LosslessGraphCompressor().compress(graph)
    checks.append(
        GateCheck(
            "immutable_decision_compression",
            "sqlite_wal" in compressed and "Zero-ops local ACID" in compressed,
            "Decision rationale & choice preserved in compressed block",
        )
    )

    # 5. Atomic checkpoint tamper rejection
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        cp_path = Path(tmp) / "gate_mesh_cp.json"
        AtomicCheckpoint.save_to_file(graph, cp_path)
        restored = AtomicCheckpoint.restore_from_file(cp_path)
        roundtrip_ok = len(restored.nodes) == len(graph.nodes)
        checks.append(GateCheck("checkpoint_roundtrip", roundtrip_ok, "SHA-256 checkpoint roundtrip succeeded"))

        payload = json.loads(cp_path.read_text(encoding="utf-8"))
        payload["nodes"][0]["object_value"] = "tampered_value"
        cp_path.write_text(json.dumps(payload), encoding="utf-8")
        tamper_rejected = False
        try:
            AtomicCheckpoint.restore_from_file(cp_path)
        except ValueError:
            tamper_rejected = True
        checks.append(GateCheck("checkpoint_tamper_rejection", tamper_rejected, "Tampered SHA-256 checkpoint rejected"))

    approved = all(c.passed for c in checks)
    return {
        "status": "approved" if approved else "rejected",
        "approved": approved,
        "checks": [asdict(c) for c in checks],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Agent Memory Mesh fail-closed integrity gate.")
    parser.add_argument("--json", action="store_true", help="Emit JSON report.")
    args = parser.parse_args(argv)

    result = run_gate()
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Gate Status: {result['status'].upper()}")
        for c in result["checks"]:
            mark = "PASS" if c["passed"] else "FAIL"
            print(f"  [{mark}] {c['name']}: {c['detail']}")
    return 0 if result["approved"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
