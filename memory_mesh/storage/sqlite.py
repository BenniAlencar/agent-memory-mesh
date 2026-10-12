"""
SQLite Durable Storage Backend for Memory Mesh.

Features WAL mode, indexed bi-temporal coordinates, and zero external DB dependencies.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Union

from memory_mesh.core.models import (
    BiTemporalInterval,
    MemoryNode,
    MemoryRelation,
    NodeType,
)
from memory_mesh.storage.base import BaseMemoryStorage


class SqliteStorage(BaseMemoryStorage):
    """Local SQLite backend with bi-temporal indexing and ACID durability."""

    def __init__(self, db_path: Union[str, Path] = "memory_mesh.db"):
        self.db_path = str(Path(db_path).resolve())
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        return conn

    def _init_db(self) -> None:
        with self._get_conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS nodes (
                    id TEXT PRIMARY KEY,
                    node_type TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    predicate TEXT NOT NULL,
                    object_value TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    provenance TEXT NOT NULL,
                    valid_from TEXT NOT NULL,
                    valid_to TEXT,
                    transaction_time TEXT NOT NULL,
                    metadata TEXT NOT NULL,
                    digest TEXT
                );

                CREATE INDEX IF NOT EXISTS idx_nodes_subject ON nodes(subject);
                CREATE INDEX IF NOT EXISTS idx_nodes_predicate ON nodes(predicate);
                CREATE INDEX IF NOT EXISTS idx_nodes_temporal ON nodes(valid_from, valid_to);

                CREATE TABLE IF NOT EXISTS relations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_id TEXT NOT NULL,
                    target_id TEXT NOT NULL,
                    relation_type TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    metadata TEXT NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_rel_source ON relations(source_id);
                CREATE INDEX IF NOT EXISTS idx_rel_target ON relations(target_id);
            """)

    def save_node(self, node: MemoryNode) -> None:
        with self._get_conn() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO nodes (
                    id, node_type, subject, predicate, object_value,
                    confidence, provenance, valid_from, valid_to,
                    transaction_time, metadata, digest
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    node.id,
                    node.node_type.value,
                    node.subject,
                    node.predicate,
                    json.dumps(node.object_value, default=str),
                    node.confidence,
                    node.provenance,
                    node.temporal.valid_from,
                    node.temporal.valid_to,
                    node.temporal.transaction_time,
                    json.dumps(node.metadata, default=str),
                    node.digest,
                ),
            )

    def get_node(self, node_id: str) -> Optional[MemoryNode]:
        with self._get_conn() as conn:
            row = conn.execute("SELECT * FROM nodes WHERE id = ?", (node_id,)).fetchone()
            if not row:
                return None
            return self._row_to_node(row)

    def query_nodes(
        self,
        subject: Optional[str] = None,
        predicate: Optional[str] = None,
        node_type: Optional[NodeType] = None,
        as_of_valid_time: Optional[datetime] = None,
        include_superseded: bool = False,
    ) -> List[MemoryNode]:
        query = "SELECT * FROM nodes WHERE 1=1"
        params: List[Any] = []

        if subject:
            query += " AND subject = ?"
            params.append(subject)
        if predicate:
            query += " AND predicate = ?"
            params.append(predicate)
        if node_type:
            query += " AND node_type = ?"
            params.append(node_type.value)

        with self._get_conn() as conn:
            rows = conn.execute(query, params).fetchall()

        nodes = [self._row_to_node(r) for r in rows]
        target_time = as_of_valid_time or datetime.now(timezone.utc)

        if not include_superseded:
            nodes = [n for n in nodes if n.temporal.is_valid_at(target_time)]

        return nodes

    def save_relation(self, relation: MemoryRelation) -> None:
        with self._get_conn() as conn:
            conn.execute(
                """
                INSERT INTO relations (source_id, target_id, relation_type, created_at, metadata)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    relation.source_id,
                    relation.target_id,
                    relation.relation_type,
                    relation.created_at,
                    json.dumps(relation.metadata, default=str),
                ),
            )

    def get_relations(self, node_id: str) -> List[MemoryRelation]:
        with self._get_conn() as conn:
            rows = conn.execute(
                "SELECT * FROM relations WHERE source_id = ? OR target_id = ?",
                (node_id, node_id),
            ).fetchall()
        return [
            MemoryRelation(
                source_id=r["source_id"],
                target_id=r["target_id"],
                relation_type=r["relation_type"],
                created_at=r["created_at"],
                metadata=json.loads(r["metadata"]),
            )
            for r in rows
        ]

    def _row_to_node(self, row: sqlite3.Row) -> MemoryNode:
        return MemoryNode(
            id=row["id"],
            node_type=NodeType(row["node_type"]),
            subject=row["subject"],
            predicate=row["predicate"],
            object_value=json.loads(row["object_value"]),
            confidence=row["confidence"],
            provenance=row["provenance"],
            temporal=BiTemporalInterval(
                valid_from=row["valid_from"],
                valid_to=row["valid_to"],
                transaction_time=row["transaction_time"],
            ),
            metadata=json.loads(row["metadata"]),
            digest=row["digest"],
        )
