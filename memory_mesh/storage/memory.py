"""
In-Memory Storage Implementation for Memory Mesh.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List, Optional

from memory_mesh.core.models import MemoryNode, MemoryRelation, NodeType
from memory_mesh.storage.base import BaseMemoryStorage


class InMemoryStorage(BaseMemoryStorage):
    """Fast, volatile in-memory storage backend."""

    def __init__(self):
        self._nodes: Dict[str, MemoryNode] = {}
        self._relations: List[MemoryRelation] = []

    def save_node(self, node: MemoryNode) -> None:
        self._nodes[node.id] = node

    def get_node(self, node_id: str) -> Optional[MemoryNode]:
        return self._nodes.get(node_id)

    def query_nodes(
        self,
        subject: Optional[str] = None,
        predicate: Optional[str] = None,
        node_type: Optional[NodeType] = None,
        as_of_valid_time: Optional[datetime] = None,
        include_superseded: bool = False,
    ) -> List[MemoryNode]:
        results: List[MemoryNode] = []
        target_time = as_of_valid_time or datetime.now(timezone.utc)

        for node in self._nodes.values():
            if subject and node.subject != subject:
                continue
            if predicate and node.predicate != predicate:
                continue
            if node_type and node.node_type != node_type:
                continue
            if not include_superseded and not node.temporal.is_valid_at(target_time):
                continue
            results.append(node)

        return results

    def save_relation(self, relation: MemoryRelation) -> None:
        self._relations.append(relation)

    def get_relations(self, node_id: str) -> List[MemoryRelation]:
        return [r for r in self._relations if r.source_id == node_id or r.target_id == node_id]
