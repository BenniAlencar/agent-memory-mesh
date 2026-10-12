"""
Example 03: Atomic Checkpoint & Tamper-Evident Restore.

Derived from Benni Master OS Skill 61:
Preserves complete agent memory with cryptographic SHA-256 sealing.
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from memory_mesh import AtomicCheckpoint, MemoryGraph

if __name__ == "__main__":
    print("--- [MEMORY-MESH] Atomic Checkpoint & Restore ---")
    graph = MemoryGraph()

    graph.add_fact("agent:code_writer", "status", "idle")
    graph.add_fact("cluster:k8s", "nodes", 8)
    graph.add_decision("release_mode", "canary", rationale="Gradual 10% rollout")

    with tempfile.TemporaryDirectory() as tmp_dir:
        snap_path = Path(tmp_dir) / "state_checkpoint.json"

        # 1. Save and seal snapshot
        saved = AtomicCheckpoint.save_to_file(graph, snap_path)
        print(f"1. Snapshot sealed and written to: {saved}")

        # 2. Restore and verify
        hydrated_graph = AtomicCheckpoint.restore_from_file(snap_path)
        print(f"2. Successfully hydrated {len(hydrated_graph.nodes)} memory nodes with valid SHA-256 digest.")

        # 3. Query hydrated state
        release = hydrated_graph.query(subject="release_mode")
        print(f"3. Verified restored decision: {release[0].subject} = {release[0].object_value}")
