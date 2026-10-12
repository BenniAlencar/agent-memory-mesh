"""
Atomic Checkpoint and Snapshot Protocol.

Derived from Benni Master OS Skill 61:
Provides tamper-evident serialization, state hydration, and SHA-256 verification.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Union

from pydantic import BaseModel, Field

from memory_mesh.core.graph import MemoryGraph
from memory_mesh.core.models import MemoryNode, MemoryRelation


class CheckpointPayload(BaseModel):
    """Container for a sealed memory snapshot."""
    system: str = "Benni Master OS Memory Mesh v1.0.0"
    created_at: str
    node_count: int
    relation_count: int
    nodes: List[Dict[str, Any]]
    relations: List[Dict[str, Any]]
    checkpoint_hash: str


class AtomicCheckpoint:
    """
    Manages saving and restoring MemoryGraph states with cryptographic integrity.
    """

    @staticmethod
    def create_snapshot(graph: MemoryGraph) -> CheckpointPayload:
        """Serializes and seals the current state of a MemoryGraph."""
        nodes_data = [n.model_dump() for n in graph.nodes.values()]
        relations_data = [r.model_dump() for r in graph.relations]

        # Deterministic sorting for reproducible hash
        nodes_sorted = sorted(nodes_data, key=lambda x: str(x.get("id")))
        relations_sorted = sorted(relations_data, key=lambda x: (str(x.get("source_id")), str(x.get("target_id"))))

        now_str = datetime.now(timezone.utc).isoformat()
        digest_input = {
            "created_at": now_str,
            "nodes": nodes_sorted,
            "relations": relations_sorted,
        }
        encoded = json.dumps(digest_input, sort_keys=True, default=str).encode("utf-8")
        h = hashlib.sha256(encoded).hexdigest()

        return CheckpointPayload(
            created_at=now_str,
            node_count=len(nodes_sorted),
            relation_count=len(relations_sorted),
            nodes=nodes_sorted,
            relations=relations_sorted,
            checkpoint_hash=h,
        )

    @staticmethod
    def save_to_file(graph: MemoryGraph, filepath: Union[str, Path]) -> Path:
        """Saves sealed snapshot to a file."""
        p = Path(filepath)
        p.parent.mkdir(parents=True, exist_ok=True)
        snapshot = AtomicCheckpoint.create_snapshot(graph)
        with open(p, "w", encoding="utf-8") as f:
            f.write(snapshot.model_dump_json(indent=2))
        return p

    @staticmethod
    def restore_from_file(filepath: Union[str, Path]) -> MemoryGraph:
        """Loads and verifies a snapshot file, returning a hydrated MemoryGraph."""
        p = Path(filepath)
        if not p.is_file():
            raise FileNotFoundError(f"Checkpoint file not found: {p}")

        with open(p, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        payload = CheckpointPayload.model_validate(raw_data)

        # Verify integrity
        nodes_sorted = sorted(payload.nodes, key=lambda x: str(x.get("id")))
        relations_sorted = sorted(payload.relations, key=lambda x: (str(x.get("source_id")), str(x.get("target_id"))))
        digest_input = {
            "created_at": payload.created_at,
            "nodes": nodes_sorted,
            "relations": relations_sorted,
        }
        recomputed_hash = hashlib.sha256(json.dumps(digest_input, sort_keys=True, default=str).encode("utf-8")).hexdigest()

        if recomputed_hash != payload.checkpoint_hash:
            raise ValueError(
                f"[MEMORY-MESH INTEGRITY ERROR] Checkpoint digest mismatch! "
                f"Expected {payload.checkpoint_hash}, recomputed {recomputed_hash}. File may be tampered."
            )

        # Hydrate graph
        graph = MemoryGraph()
        for nd in payload.nodes:
            node = MemoryNode.model_validate(nd)
            graph.nodes[node.id] = node

        for rd in payload.relations:
            rel = MemoryRelation.model_validate(rd)
            graph.relations.append(rel)

        return graph
