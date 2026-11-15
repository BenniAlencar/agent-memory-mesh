"""Tests for memory_mesh.tools and scripts/."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from click.testing import CliRunner

from memory_mesh.cli.main import cli
from memory_mesh.tools.bench_matrix import BenchMatrixRunner
from memory_mesh.tools.doctor import run_doctor

ROOT = Path(__file__).resolve().parent.parent


def test_doctor_healthy() -> None:
    report = run_doctor()
    assert report.healthy is True
    assert report.bitemporal_probe_ok is True
    assert report.sqlite_probe_ok is True
    assert report.checkpoint_probe_ok is True


def test_bench_matrix_runner() -> None:
    runner = BenchMatrixRunner(fact_counts=[10, 25], reps=1)
    data = runner.run_matrix()
    assert len(data["matrix_results"]) == 2
    md = BenchMatrixRunner.format_markdown_table(data)
    assert "| 10 |" in md
    assert "| 25 |" in md


def test_cli_doctor_and_matrix() -> None:
    runner = CliRunner()
    res_doc = runner.invoke(cli, ["doctor", "--json"])
    assert res_doc.exit_code == 0
    assert json.loads(res_doc.output)["healthy"] is True

    res_mat = runner.invoke(cli, ["matrix", "--facts", "10", "--reps", "1", "--json"])
    assert res_mat.exit_code == 0
    assert len(json.loads(res_mat.output)["matrix_results"]) == 1


def test_scripts_run_cleanly() -> None:
    bench = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "benchmark_compression_ratio.py"), "--facts", "10", "--reps", "1", "--json"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert len(json.loads(bench.stdout)["matrix_results"]) == 1

    gate = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "gate_bitemporal_integrity.py"), "--json"],
        capture_output=True,
        text=True,
        check=True,
    )
    gate_data = json.loads(gate.stdout)
    assert gate_data["approved"] is True
    assert all(c["passed"] for c in gate_data["checks"])
