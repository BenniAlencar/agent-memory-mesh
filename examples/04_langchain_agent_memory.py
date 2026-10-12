"""
Example 04: LangChain & LangGraph Integration.

Demonstrates plugging MemoryMesh into LangChain agent memory cycles.
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from memory_mesh import MemoryMeshLangChainAdapter

if __name__ == "__main__":
    print("--- [MEMORY-MESH] LangChain Knowledge Graph Memory Adapter ---")
    adapter = MemoryMeshLangChainAdapter()

    # Agent records user preferences and project constraints during workflow
    adapter.store_fact("user:carter", "role", "security_engineer")
    adapter.store_fact("user:carter", "enforces_mtls", True)
    adapter.store_decision("api_framework", "FastAPI", rationale="Native Pydantic v2 validation")

    # Injects directly into prompt
    prompt_injection = adapter.get_prompt_context()
    print("\nPrompt Injection Context Block:")
    print(prompt_injection)

    # Standard LangChain memory loader dictionary
    mem_vars = adapter.load_memory_variables({})
    print("\nLangChain Memory Variables Output:")
    print(f"Keys: {list(mem_vars.keys())}")
