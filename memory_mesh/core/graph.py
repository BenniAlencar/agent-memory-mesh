"""
Bi-Temporal Memory Graph Engine.

Manages nodes, superseding edges, and time-travel queries.
Prevents catastrophic contradictions by automatically invalidating superseded facts.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from memory_mesh.core.models import (
    BiTemporalInterval,
    MemoryNode,
    MemoryRelation,
    NodeType,
    _iso_now,
    _parse_dt,
)


class MemoryGraph:
    """
    In-memory graph implementation with bi-temporal indexing and causality traversal.
    """

    def __init__(self):
        self.nodes: Dict[str, MemoryNode] = {}
        self.relations: List[MemoryRelation] = []

    def add_fact(
        self,
        subject: str,
        predicate: str,
        object_value: Any,
        valid_from: Optional[str] = None,
        provenance: str = "direct_observation",
        confidence: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> MemoryNode:
        """
        Adds a new fact. If an active fact with identical (subject, predicate) exists,
        it is automatically marked as superseded (valid_to closed) and linked via an edge.
        """
        now_str = _iso_now()
        v_from = valid_from or now_str

        # 1. Supersede any currently active facts with matching subject and predicate
        for existing in self.nodes.values():
            if (
                existing.subject == subject
                and existing.predicate == predicate
                and existing.temporal.is_current()
            ):
                existing.temporal.valid_to = v_from
                existing.seal()
                # Create superseding relationship
                relation = MemoryRelation(
                    source_id="",  # will populate after creating new node
                    target_id=existing.id,
                    relation_type="supersedes",
                )
                self.relations.append(relation)

        # 2. Create and seal the new node
        new_node = MemoryNode(
            node_type=NodeType.FACT,
            subject=subject,
            predicate=predicate,
            object_value=object_value,
            confidence=confidence,
            provenance=provenance,
            temporal=BiTemporalInterval(valid_from=v_from, transaction_time=now_str),
            metadata=metadata or {},
        )
        new_node.seal()
        self.nodes[new_node.id] = new_node

        # Fix relationship source_id for superseding relations created above
        for rel in self.relations:
            if rel.source_id == "":
                rel.source_id = new_node.id

        return new_node

    def add_decision(
        self,
        subject: str,
        chosen_option: Any,
        rationale: str,
        alternatives: Optional[List[Any]] = None,
        provenance: str = "operator_or_agent",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> MemoryNode:
        """Records an architectural, operational, or business decision."""
        meta = metadata or {}
        meta["rationale"] = rationale
        meta["alternatives"] = alternatives or []

        node = MemoryNode(
            node_type=NodeType.DECISION,
            subject=subject,
            predicate="chosen_option",
            object_value=chosen_option,
            provenance=provenance,
            metadata=meta,
        )
        node.seal()
        self.nodes[node.id] = node
        return node

    def query(
        self,
        subject: Optional[str] = None,
        predicate: Optional[str] = None,
        node_type: Optional[NodeType] = None,
        as_of_valid_time: Optional[datetime] = None,
        include_superseded: bool = False,
    ) -> List[MemoryNode]:
        """
        Queries the graph with optional filters and bi-temporal time-travel coordinates.
        """
        results: List[MemoryNode] = []
        target_time = as_of_valid_time or datetime.now(timezone.utc)

        for node in self.nodes.values():
            if subject and node.subject != subject:
                continue
            if predicate and node.predicate != predicate:
                continue
            if node_type and node.node_type != node_type:
                continue

            if not include_superseded:
                if not node.temporal.is_valid_at(target_time):
                    continue

            results.append(node)

        return results

    def get_timeline(self, subject: str) -> List[MemoryNode]:
        """Returns the full chronological history of all facts relating to a subject."""
        matching = [n for n in self.nodes.values() if n.subject == subject]
        return sorted(matching, key=lambda n: _parse_dt(n.temporal.valid_from))

    def get_relations_for(self, node_id: str) -> List[MemoryRelation]:
        """Returns all relations where node_id is source or target."""
        return [r for r in self.relations if r.source_id == node_id or r.target_id == node_id]

    def count_active_facts(self) -> int:
        """Returns count of non-superseded facts."""
        return sum(1 for n in self.nodes.values() if n.temporal.is_current())
