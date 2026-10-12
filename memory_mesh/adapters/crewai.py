"""
CrewAI Memory Adapter for Memory Mesh.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from memory_mesh.core.compressor import LosslessGraphCompressor
from memory_mesh.core.graph import MemoryGraph


class MemoryMeshCrewAIAdapter:
    """
    CrewAI-compatible memory handler providing bi-temporal context retrieval.
    """

    def __init__(self, graph: Optional[MemoryGraph] = None):
        self.graph = graph or MemoryGraph()
        self.compressor = LosslessGraphCompressor()

    def save(self, value: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Saves memory item parsed as fact or unstructured episode."""
        meta = metadata or {}
        subject = meta.get("subject", "agent_observation")
        predicate = meta.get("predicate", "recorded")
        self.graph.add_fact(
            subject=subject,
            predicate=predicate,
            object_value=value,
            provenance="crewai_agent",
            metadata=meta,
        )

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Returns matching active facts for the agent."""
        matching = self.graph.query(include_superseded=False)
        # Simple subject/predicate substring matching
        q = query.lower()
        filtered = [
            n for n in matching
            if q in n.subject.lower() or q in n.predicate.lower() or q in str(n.object_value).lower()
        ]
        return [
            {
                "id": n.id,
                "subject": n.subject,
                "predicate": n.predicate,
                "value": n.object_value,
                "confidence": n.confidence,
            }
            for n in filtered[:limit]
        ]
