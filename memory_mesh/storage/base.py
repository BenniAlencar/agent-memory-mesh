"""
Abstract Base Storage Interface for Memory Mesh.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from memory_mesh.core.models import MemoryNode, MemoryRelation, NodeType


class BaseMemoryStorage(ABC):
    """Abstract storage backend for memory graph nodes and relations."""

    @abstractmethod
    def save_node(self, node: MemoryNode) -> None:
        """Stores or updates a memory node."""
        pass

    @abstractmethod
    def get_node(self, node_id: str) -> Optional[MemoryNode]:
        """Retrieves a single node by its ID."""
        pass

    @abstractmethod
    def query_nodes(
        self,
        subject: Optional[str] = None,
        predicate: Optional[str] = None,
        node_type: Optional[NodeType] = None,
        as_of_valid_time: Optional[datetime] = None,
        include_superseded: bool = False,
    ) -> List[MemoryNode]:
        """Queries nodes matching temporal and property filters."""
        pass

    @abstractmethod
    def save_relation(self, relation: MemoryRelation) -> None:
        """Stores a directed edge relation."""
        pass

    @abstractmethod
    def get_relations(self, node_id: str) -> List[MemoryRelation]:
        """Retrieves all relations involving the node."""
        pass
