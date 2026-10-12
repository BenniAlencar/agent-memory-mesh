"""
Bi-Temporal Knowledge Graph & Memory Node Models.

Implements the Benni Master OS Skill 60 & 61 doctrines:
- Bi-temporal intervals: separates valid_time (real world) from transaction_time (system assertion).
- Immutable, SHA-256 verifiable knowledge triples.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_dt(iso_str: Any) -> datetime:
    """Parses ISO-8601 strings into timezone-aware UTC datetime across Python 3.10+."""
    if isinstance(iso_str, datetime):
        if iso_str.tzinfo is None:
            return iso_str.replace(tzinfo=timezone.utc)
        return iso_str

    clean = str(iso_str).strip()
    if clean.endswith("Z") or clean.endswith("z"):
        clean = clean[:-1] + "+00:00"

    try:
        dt = datetime.fromisoformat(clean)
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return datetime.now(timezone.utc)



class NodeType(str, Enum):
    """Categorical classification of memory nodes."""
    FACT = "fact"
    DECISION = "decision"
    ENTITY = "entity"
    PREFERENCE = "preference"
    TASK = "task"
    EPISODE = "episode"


class BiTemporalInterval(BaseModel):
    """
    Bi-temporal timeline coordinates:
    - valid_time: When the fact was/is true in the real world.
    - transaction_time: When the AI agent learned or stored the fact.
    """
    valid_from: str = Field(default_factory=_iso_now)
    valid_to: Optional[str] = None  # None indicates currently active fact
    transaction_time: str = Field(default_factory=_iso_now)

    def is_valid_at(self, target_time: Optional[datetime] = None) -> bool:
        """Evaluates whether the fact was active at a given valid_time."""
        t = target_time or datetime.now(timezone.utc)
        v_from = _parse_dt(self.valid_from)
        if t < v_from:
            return False
        if self.valid_to:
            v_to = _parse_dt(self.valid_to)
            if t >= v_to:
                return False
        return True

    def is_current(self) -> bool:
        """Returns True if the fact has not been superseded or expired."""
        return self.valid_to is None


class MemoryNode(BaseModel):
    """
    A discrete node in the agent's knowledge graph.
    Structured as a semantic triple: (subject) -[predicate]-> (object_value).
    """
    id: str = Field(default_factory=lambda: f"node_{uuid.uuid4().hex[:12]}")
    node_type: NodeType = NodeType.FACT
    subject: str
    predicate: str
    object_value: Any
    confidence: float = 1.0
    provenance: str = "direct_observation"
    temporal: BiTemporalInterval = Field(default_factory=BiTemporalInterval)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    digest: Optional[str] = None

    def seal(self) -> MemoryNode:
        """Computes deterministic SHA-256 digest of node content."""
        data_to_hash = {
            "id": self.id,
            "node_type": self.node_type.value,
            "subject": self.subject,
            "predicate": self.predicate,
            "object_value": self.object_value,
            "provenance": self.provenance,
            "valid_from": self.temporal.valid_from,
            "valid_to": self.temporal.valid_to,
            "transaction_time": self.temporal.transaction_time,
        }
        encoded = json.dumps(data_to_hash, sort_keys=True, default=str).encode("utf-8")
        self.digest = hashlib.sha256(encoded).hexdigest()
        return self

    def is_tampered(self) -> bool:
        """Checks if content has been modified post-sealing."""
        if not self.digest:
            return True
        orig_digest = self.digest
        self.seal()
        tampered = self.digest != orig_digest
        self.digest = orig_digest
        return tampered


class MemoryRelation(BaseModel):
    """
    A causal or semantic directed edge linking two memory nodes.
    """
    source_id: str
    target_id: str
    relation_type: str = "supersedes"  # "supersedes", "caused_by", "depends_on", "references"
    created_at: str = Field(default_factory=_iso_now)
    metadata: Dict[str, Any] = Field(default_factory=dict)
