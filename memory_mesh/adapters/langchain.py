"""
LangChain & LangGraph Adapter for Memory Mesh.

Provides graph-backed bi-temporal memory storage for LangChain agents.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from memory_mesh.core.compressor import LosslessGraphCompressor
from memory_mesh.core.graph import MemoryGraph


class MemoryMeshLangChainAdapter:
    """
    Integrates MemoryGraph with LangChain agent memory cycles.
    """

    def __init__(self, graph: Optional[MemoryGraph] = None):
        self.graph = graph or MemoryGraph()
        self.compressor = LosslessGraphCompressor()

    def store_fact(
        self,
        subject: str,
        predicate: str,
        object_value: Any,
        provenance: str = "langchain_agent",
    ) -> str:
        """Stores a ground-truth fact extracted during conversation."""
        node = self.graph.add_fact(
            subject=subject,
            predicate=predicate,
            object_value=object_value,
            provenance=provenance,
        )
        return node.id

    def store_decision(
        self,
        subject: str,
        chosen_option: Any,
        rationale: str,
        alternatives: Optional[List[Any]] = None,
    ) -> str:
        """Records an agent or user decision."""
        node = self.graph.add_decision(
            subject=subject,
            chosen_option=chosen_option,
            rationale=rationale,
            alternatives=alternatives,
            provenance="langchain_agent",
        )
        return node.id

    def get_prompt_context(self, focus_subjects: Optional[List[str]] = None) -> str:
        """Generates condensed token-efficient context for agent prompt."""
        return self.compressor.compress(self.graph, focus_subjects=focus_subjects)

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, str]:
        """LangChain-compatible memory variable loader."""
        return {"knowledge_graph_memory": self.get_prompt_context()}
