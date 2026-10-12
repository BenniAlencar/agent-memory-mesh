"""
Example 05: Model Context Protocol (MCP) Memory Server.

Demonstrates using McpMemoryServer to power Claude Desktop, Cursor, and Antigravity.
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from memory_mesh import McpMemoryServer

if __name__ == "__main__":
    print("--- [MEMORY-MESH] Model Context Protocol (MCP) Memory Server ---")
    server = McpMemoryServer()

    print("\n1. Registered MCP Tools:")
    for tool in server.get_tool_definitions():
        print(f"   • {tool['name']}: {tool['description']}")

    # Simulate client calling memory_store
    print("\n2. Executing 'memory_store' via MCP call:")
    res_store = server.call_tool(
        "memory_store",
        {"subject": "infra:vpc", "predicate": "cidr", "object_value": "10.0.0.0/16"},
    )
    print("   Output:", res_store["content"][0]["text"])

    # Simulate client calling memory_recall
    print("\n3. Executing 'memory_recall' via MCP call:")
    res_recall = server.call_tool("memory_recall", {"subject": "infra:vpc"})
    print("   Output:", res_recall["content"][0]["text"])
