"""
Model Context Protocol (MCP) Memory Server Interface.

Exposes native MCP tools for Claude Desktop, Cursor, and Antigravity agents:
- memory_store
- memory_decision
- memory_recall
- memory_timeline
- memory_compress
- memory_snapshot
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from memory_mesh.core.checkpoint import AtomicCheckpoint
from memory_mesh.core.compressor import LosslessGraphCompressor
from memory_mesh.core.graph import MemoryGraph


class McpMemoryServer:
    """
    Exposes MemoryGraph capabilities as Model Context Protocol (MCP) tool endpoints.
    """

    def __init__(self, graph: Optional[MemoryGraph] = None):
        self.graph = graph or MemoryGraph()
        self.compressor = LosslessGraphCompressor()

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Returns standard MCP tool schemas."""
        return [
            {
                "name": "memory_store",
                "description": "Store a ground-truth fact into the bi-temporal knowledge graph.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "subject": {"type": "string"},
                        "predicate": {"type": "string"},
                        "object_value": {"description": "Value or structured data"},
                        "provenance": {"type": "string", "default": "mcp_client"},
                    },
                    "required": ["subject", "predicate", "object_value"],
                },
            },
            {
                "name": "memory_decision",
                "description": "Store an immutable architectural or business decision with rationale.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "subject": {"type": "string"},
                        "chosen_option": {"description": "The selected choice"},
                        "rationale": {"type": "string"},
                        "alternatives": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["subject", "chosen_option", "rationale"],
                },
            },
            {
                "name": "memory_recall",
                "description": "Query verified active facts from the knowledge graph without obsolete noise.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "subject": {"type": "string"},
                        "predicate": {"type": "string"},
                        "include_superseded": {"type": "boolean", "default": False},
                    },
                },
            },
            {
                "name": "memory_timeline",
                "description": "View the chronological history and evolution of a subject across time.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "subject": {"type": "string"},
                    },
                    "required": ["subject"],
                },
            },
            {
                "name": "memory_compress",
                "description": "Compile the current active knowledge graph into a compact, token-dense prompt block.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "focus_subjects": {"type": "array", "items": {"type": "string"}},
                    },
                },
            },
            {
                "name": "memory_snapshot",
                "description": "Create a SHA-256 sealed atomic snapshot file of the entire memory graph.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "filepath": {"type": "string"},
                    },
                    "required": ["filepath"],
                },
            },
        ]

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatches tool execution according to MCP specification."""
        try:
            if name == "memory_store":
                node = self.graph.add_fact(
                    subject=arguments["subject"],
                    predicate=arguments["predicate"],
                    object_value=arguments["object_value"],
                    provenance=arguments.get("provenance", "mcp_client"),
                )
                return {
                    "content": [{"type": "text", "text": f"Stored fact {node.id}: ({node.subject}) -[{node.predicate}]-> {node.object_value}"}],
                    "isError": False,
                }

            elif name == "memory_decision":
                node = self.graph.add_decision(
                    subject=arguments["subject"],
                    chosen_option=arguments["chosen_option"],
                    rationale=arguments["rationale"],
                    alternatives=arguments.get("alternatives"),
                    provenance="mcp_client",
                )
                return {
                    "content": [{"type": "text", "text": f"Recorded decision {node.id}: {node.subject} = {node.object_value}"}],
                    "isError": False,
                }

            elif name == "memory_recall":
                nodes = self.graph.query(
                    subject=arguments.get("subject"),
                    predicate=arguments.get("predicate"),
                    include_superseded=arguments.get("include_superseded", False),
                )
                serialized = [n.model_dump() for n in nodes]
                return {
                    "content": [{"type": "text", "text": json.dumps(serialized, indent=2, default=str)}],
                    "isError": False,
                }

            elif name == "memory_timeline":
                timeline = self.graph.get_timeline(arguments["subject"])
                serialized = [n.model_dump() for n in timeline]
                return {
                    "content": [{"type": "text", "text": json.dumps(serialized, indent=2, default=str)}],
                    "isError": False,
                }

            elif name == "memory_compress":
                compressed = self.compressor.compress(self.graph, focus_subjects=arguments.get("focus_subjects"))
                return {
                    "content": [{"type": "text", "text": compressed}],
                    "isError": False,
                }

            elif name == "memory_snapshot":
                saved_path = AtomicCheckpoint.save_to_file(self.graph, arguments["filepath"])
                return {
                    "content": [{"type": "text", "text": f"Created atomic snapshot at: {saved_path}"}],
                    "isError": False,
                }

            else:
                return {
                    "content": [{"type": "text", "text": f"Unknown tool: {name}"}],
                    "isError": True,
                }

        except Exception as exc:
            return {
                "content": [{"type": "text", "text": f"[MCP MEMORY ERROR] {exc}"}],
                "isError": True,
            }
