"""Tests for AtomicCheckpoint and snapshot integrity."""

from pathlib import Path
import pytest

from memory_mesh.core.checkpoint import AtomicCheckpoint
from memory_mesh.core.graph import MemoryGraph


def test_checkpoint_roundtrip(temp_dir: Path, sample_graph: MemoryGraph):
    snapshot_path = temp_dir / "snapshot.json"
    AtomicCheckpoint.save_to_file(sample_graph, snapshot_path)

    assert snapshot_path.exists()

    # Hydrate back
    hydrated = AtomicCheckpoint.restore_from_file(snapshot_path)
    assert len(hydrated.nodes) == len(sample_graph.nodes)
    assert len(hydrated.relations) == len(sample_graph.relations)

    # Check that Alice is still tech_lead in hydrated graph
    res = hydrated.query(subject="user:alice", predicate="role")
    assert len(res) == 1
    assert res[0].object_value == "tech_lead"


def test_checkpoint_tamper_detection(temp_dir: Path, sample_graph: MemoryGraph):
    snapshot_path = temp_dir / "tampered.json"
    AtomicCheckpoint.save_to_file(sample_graph, snapshot_path)

    # Tamper with file content manually
    raw = snapshot_path.read_text(encoding="utf-8")
    tampered_raw = raw.replace("postgresql_16", "insecure_sqlite")
    snapshot_path.write_text(tampered_raw, encoding="utf-8")

    with pytest.raises(ValueError) as exc_info:
        AtomicCheckpoint.restore_from_file(snapshot_path)

    assert "Checkpoint digest mismatch" in str(exc_info.value)
