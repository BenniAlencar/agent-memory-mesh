"""Tests for BiTemporalInterval and MemoryNode models."""

from datetime import datetime, timezone

from memory_mesh.core.models import BiTemporalInterval, MemoryNode, NodeType


def test_bitemporal_validity():
    interval = BiTemporalInterval(
        valid_from="2026-01-01T00:00:00+00:00",
        valid_to="2026-06-01T00:00:00+00:00",
        transaction_time="2026-06-02T00:00:00+00:00",
    )

    # In March 2026 it was valid
    march_dt = datetime(2026, 3, 1, tzinfo=timezone.utc)
    assert interval.is_valid_at(march_dt) is True

    # In December 2025 it was not yet valid
    dec_dt = datetime(2025, 12, 1, tzinfo=timezone.utc)
    assert interval.is_valid_at(dec_dt) is False

    # In July 2026 it was already expired / superseded
    july_dt = datetime(2026, 7, 1, tzinfo=timezone.utc)
    assert interval.is_valid_at(july_dt) is False

    assert interval.is_current() is False


def test_node_sealing_and_tamper_detection():
    node = MemoryNode(
        node_type=NodeType.FACT,
        subject="cluster:prod",
        predicate="status",
        object_value="healthy",
    )

    assert node.digest is None
    assert node.is_tampered() is True

    node.seal()
    assert node.digest is not None
    assert node.is_tampered() is False

    # Tampering with object_value
    node.object_value = "degraded"
    assert node.is_tampered() is True
