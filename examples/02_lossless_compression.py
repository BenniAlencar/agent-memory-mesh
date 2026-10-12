"""
Example 02: Lossless Graph Context Compression.

Demonstrates condensing long, token-heavy conversations into hyper-dense,
accurate semantic triples for prompt injection.
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from memory_mesh import LosslessGraphCompressor, MemoryGraph

if __name__ == "__main__":
    print("--- [MEMORY-MESH] Lossless Graph Context Compression ---")
    graph = MemoryGraph()

    # Populate active verified facts
    graph.add_fact("user:alex", "role", "principal_architect")
    graph.add_fact("user:alex", "timezone", "UTC-3")
    graph.add_fact("project:nexus", "language", "python_3_11")
    graph.add_fact("project:nexus", "framework", "fastapi")
    graph.add_decision(
        subject="auth_architecture",
        chosen_option="jwt_ed25519",
        rationale="Superior signature verification speed and asymmetric security",
        alternatives=["rsa_4096", "shared_secret_hmac"],
    )

    compressor = LosslessGraphCompressor()
    prompt_context = compressor.compress(graph)

    print("\n--- Compiled Prompt Injection Block ---")
    print(prompt_context)

    # Simulated verbose conversation transcript
    raw_dialogue = (
        "User: Hey, Alex is our principal architect right?\n"
        "Agent: Yes, Alex works as principal architect and is based in UTC-3.\n"
        "User: What stack are we using for project nexus?\n"
        "Agent: We decided on Python 3.11 with FastAPI after reviewing several options.\n"
        "User: Did we pick JWT with Ed25519?\n"
        "Agent: Exactly, we evaluated RSA 4096 and HMAC, but Ed25519 gives us optimal speed and zero-trust security."
    ) * 15

    metrics = compressor.calculate_savings(raw_dialogue, prompt_context)
    print("\n--- Token FinOps Metrics ---")
    print(f"Raw Dialogue Tokens (est):      {metrics['raw_tokens_estimate']}")
    print(f"Compressed Graph Tokens (est):  {metrics['compressed_tokens_estimate']}")
    print(f"Tokens Saved:                   {metrics['tokens_saved']}")
    print(f"Compression Efficiency:         {metrics['savings_percentage']} reduction")
