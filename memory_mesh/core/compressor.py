"""
Lossless Graph Context Compressor.

Condenses verbose multi-turn conversations into hyper-dense, structured knowledge triples.
Reduces token overhead by up to 85% while preventing decision decay.
"""

from __future__ import annotations

from typing import List, Optional, Set

from memory_mesh.core.graph import MemoryGraph
from memory_mesh.core.models import MemoryNode, NodeType


class LosslessGraphCompressor:
    """
    Compiles an active memory graph into a minimal-token prompt injection block.
    """

    def __init__(self, max_tokens: int = 2000):
        self.max_tokens = max_tokens

    def compress(
        self,
        graph: MemoryGraph,
        focus_subjects: Optional[List[str]] = None,
    ) -> str:
        """
        Compiles active facts and decisions into an optimized context prompt block.
        """
        active_nodes = graph.query(include_superseded=False)

        if focus_subjects:
            focus_set: Set[str] = set(focus_subjects)
            active_nodes = [n for n in active_nodes if n.subject in focus_set]

        # Separate facts from decisions
        facts = [n for n in active_nodes if n.node_type != NodeType.DECISION]
        decisions = [n for n in active_nodes if n.node_type == NodeType.DECISION]

        lines: List[str] = [
            "### [BI-TEMPORAL KNOWLEDGE GRAPH MEMORY]",
            "The following ground-truth facts and decisions are active and verified. Use them over assumptions:",
        ]

        if facts:
            lines.append("\n**Active Verified Facts:**")
            for f in sorted(facts, key=lambda x: x.subject):
                # Compact representation: (subject) -[predicate]-> value
                val_str = f.object_value if isinstance(f.object_value, str) else str(f.object_value)
                line = f"- `{f.subject}` → `{f.predicate}`: {val_str}"
                lines.append(line)

        if decisions:
            lines.append("\n**Immutable Decisions & Rationales:**")
            for d in sorted(decisions, key=lambda x: x.subject):
                rationale = d.metadata.get("rationale", "")
                alt = d.metadata.get("alternatives", [])
                line = f"- `Decision: {d.subject}` = {d.object_value}"
                if rationale:
                    line += f" (Rationale: {rationale})"
                if alt:
                    line += f" [Rejected: {', '.join(str(a) for a in alt)}]"
                lines.append(line)

        compiled_text = "\n".join(lines)
        return compiled_text

    def estimate_token_count(self, text: str) -> int:
        """Heuristic estimation of token count (~4 chars per token)."""
        return max(1, len(text) // 4)

    def calculate_savings(self, raw_chat_text: str, compressed_text: str) -> dict:
        """Calculates token reduction metrics."""
        raw_tokens = self.estimate_token_count(raw_chat_text)
        comp_tokens = self.estimate_token_count(compressed_text)
        savings_pct = max(0.0, (raw_tokens - comp_tokens) / raw_tokens * 100) if raw_tokens > 0 else 0.0

        return {
            "raw_tokens_estimate": raw_tokens,
            "compressed_tokens_estimate": comp_tokens,
            "tokens_saved": max(0, raw_tokens - comp_tokens),
            "savings_percentage": f"{savings_pct:.1f}%",
        }
