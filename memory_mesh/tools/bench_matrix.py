"""Matrix Benchmark Suite for Agent Memory Mesh.

Sweeps fact counts to measure bi-temporal graph insertion throughput, active-fact
query latency, LosslessGraphCompressor token reduction ratio, and SHA-256
AtomicCheckpoint serialization speed.
"""

from __future__ import annotations

import argparse
import json
import statistics
import tempfile
import time
from pathlib import Path
from typing import Any

from memory_mesh.core.checkpoint import AtomicCheckpoint
from memory_mesh.core.compressor import LosslessGraphCompressor
from memory_mesh.core.graph import MemoryGraph


class BenchMatrixRunner:
    """Executes a multi-scale benchmark matrix on MemoryGraph & LosslessGraphCompressor."""

    def __init__(self, fact_counts: list[int] | None = None, reps: int = 2) -> None:
        self.fact_counts = fact_counts or [25, 100, 250]
        self.reps = reps

    def _run_once(self, n_facts: int) -> dict[str, float]:
        graph = MemoryGraph()
        raw_transcript_chars = 0

        t0 = time.perf_counter()
        for i in range(n_facts):
            subj = f"entity:{i % max(1, n_facts // 2)}"
            pred = f"attr_{i % 5}"
            val = f"value_{i}"
            graph.add_fact(subj, pred, val)
            raw_transcript_chars += len(
                f"Assistant turn {i}: Based on our prior discussion, I am updating {subj} "
                f"so that {pred} is now set to {val}. Please confirm this change.\n"
            )
        insert_ms = max(1e-3, (time.perf_counter() - t0) * 1000.0)

        t_q = time.perf_counter()
        active = graph.query(include_superseded=False)
        query_ms = max(1e-3, (time.perf_counter() - t_q) * 1000.0)

        compressor = LosslessGraphCompressor()
        compressed = compressor.compress(graph)
        raw_tokens = max(1, raw_transcript_chars // 4)
        compressed_tokens = max(1, compressor.estimate_token_count(compressed))
        savings_pct = max(0.0, (1.0 - (compressed_tokens / raw_tokens)) * 100.0)

        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            t_cp = time.perf_counter()
            AtomicCheckpoint.save_to_file(graph, Path(tmp) / "bench_cp.json")
            cp_ms = (time.perf_counter() - t_cp) * 1000.0

        return {
            "insert_ms": insert_ms,
            "query_ms": query_ms,
            "cp_ms": cp_ms,
            "active_facts": float(len(active)),
            "savings_pct": savings_pct,
        }

    def run_matrix(self) -> dict[str, Any]:
        """Run the benchmark sweep across all configured fact counts."""
        rows: list[dict[str, Any]] = []
        for n_facts in self.fact_counts:
            samples = [self._run_once(n_facts) for _ in range(self.reps)]
            mean_insert_ms = statistics.mean(s["insert_ms"] for s in samples)
            rows.append(
                {
                    "facts": n_facts,
                    "active_facts": int(samples[0]["active_facts"]),
                    "insert_ms": round(mean_insert_ms, 2),
                    "facts_per_sec": round(n_facts / (mean_insert_ms / 1000.0), 1),
                    "query_ms": round(statistics.mean(s["query_ms"] for s in samples), 3),
                    "token_savings_pct": round(statistics.mean(s["savings_pct"] for s in samples), 1),
                    "checkpoint_ms": round(statistics.mean(s["cp_ms"] for s in samples), 2),
                }
            )
        return {
            "fact_counts": self.fact_counts,
            "reps": self.reps,
            "matrix_results": rows,
            "timestamp": int(time.time()),
        }

    @staticmethod
    def format_markdown_table(data: dict[str, Any]) -> str:
        """Render a Markdown summary table from benchmark matrix results."""
        lines = [
            "# Agent Memory Mesh Benchmark Matrix",
            "",
            "| Facts | Active | Insert (ms) | Throughput (facts/s) | Query (ms) | Token Savings | Checkpoint (ms) |",
            "|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for row in data.get("matrix_results", []):
            lines.append(
                f"| {row['facts']} | {row['active_facts']} | {row['insert_ms']} | "
                f"{row['facts_per_sec']} | {row['query_ms']} | {row['token_savings_pct']}% | {row['checkpoint_ms']} |"
            )
        return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Agent Memory Mesh benchmark matrix.")
    parser.add_argument("--facts", type=int, nargs="+", default=[25, 100, 250], help="Fact counts to sweep.")
    parser.add_argument("--reps", type=int, default=2, help="Repetitions per cell.")
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    args = parser.parse_args(argv)

    runner = BenchMatrixRunner(fact_counts=args.facts, reps=args.reps)
    data = runner.run_matrix()
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(runner.format_markdown_table(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
