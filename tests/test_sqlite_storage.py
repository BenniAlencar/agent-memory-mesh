"""Tests for SqliteStorage durable persistence."""

from memory_mesh.core.models import MemoryNode, MemoryRelation, NodeType
from memory_mesh.storage.sqlite import SqliteStorage


def test_sqlite_storage_roundtrip(sqlite_storage: SqliteStorage):
    node = MemoryNode(
        node_type=NodeType.FACT,
        subject="server:web",
        predicate="ip",
        object_value="192.168.1.50",
    ).seal()

    sqlite_storage.save_node(node)

    retrieved = sqlite_storage.get_node(node.id)
    assert retrieved is not None
    assert retrieved.subject == "server:web"
    assert retrieved.predicate == "ip"
    assert retrieved.object_value == "192.168.1.50"

    # Query active
    active_nodes = sqlite_storage.query_nodes(subject="server:web")
    assert len(active_nodes) == 1


def test_sqlite_relations(sqlite_storage: SqliteStorage):
    rel = MemoryRelation(
        source_id="node_a",
        target_id="node_b",
        relation_type="depends_on",
    )
    sqlite_storage.save_relation(rel)

    results = sqlite_storage.get_relations("node_a")
    assert len(results) == 1
    assert results[0].relation_type == "depends_on"
