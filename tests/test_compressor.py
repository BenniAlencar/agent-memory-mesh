"""Tests for LosslessGraphCompressor."""

from memory_mesh.core.compressor import LosslessGraphCompressor
from memory_mesh.core.graph import MemoryGraph


def test_compression_output(sample_graph: MemoryGraph):
    compressor = LosslessGraphCompressor()
    compressed = compressor.compress(sample_graph)

    assert "BI-TEMPORAL KNOWLEDGE GRAPH MEMORY" in compressed
    assert "user:alice" in compressed
    assert "tech_lead" in compressed
    # Software engineer should NOT be present because it was superseded!
    assert "software_engineer" not in compressed
    assert "`Decision: database_choice` = postgresql_16" in compressed


def test_savings_calculation(sample_graph: MemoryGraph):
    compressor = LosslessGraphCompressor()
    compressed = compressor.compress(sample_graph)

    # Simulated verbose conversation transcript
    raw_chat = (
        "User: Hey, who is Alice?\n"
        "Agent: Alice was a software engineer back in January, but then in June she got promoted to tech lead.\n"
        "User: Cool, what database did we decide on?\n"
        "Agent: We evaluated MongoDB and MySQL 8, but decided on PostgreSQL 16 because of JSONB and bi-temporal features."
    ) * 10

    metrics = compressor.calculate_savings(raw_chat, compressed)
    assert metrics["tokens_saved"] > 0
    assert float(metrics["savings_percentage"].replace("%", "")) > 0.0
