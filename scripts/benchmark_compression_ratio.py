#!/usr/bin/env python3
"""Bi-Temporal Graph Compression & Throughput Benchmark.

Measures token savings achieved by LosslessGraphCompressor compared to raw
multi-turn conversational transcripts, alongside insert/query/checkpoint latency.

Usage:
    python scripts/benchmark_compression_ratio.py
    python scripts/benchmark_compression_ratio.py --facts 25 100 250 --reps 2
    python scripts/benchmark_compression_ratio.py --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from memory_mesh.tools.bench_matrix import BenchMatrixRunner


def run_benchmark(facts: list[int] | None = None, reps: int = 2) -> dict[str, Any]:
    """Execute the memory compression matrix benchmark."""
    runner = BenchMatrixRunner(fact_counts=facts or [25, 100, 250], reps=reps)
    return runner.run_matrix()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Benchmark Agent Memory Mesh compression & throughput.")
    parser.add_argument("--facts", type=int, nargs="+", default=[25, 100, 250], help="Fact counts to sweep.")
    parser.add_argument("--reps", type=int, default=2, help="Repetitions per cell.")
    parser.add_argument("--json", action="store_true", help="Emit JSON report.")
    args = parser.parse_args(argv)

    data = run_benchmark(facts=args.facts, reps=args.reps)
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(BenchMatrixRunner.format_markdown_table(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
