"""Tests for LangChain, CrewAI, and MCP adapters."""

from memory_mesh.adapters.crewai import MemoryMeshCrewAIAdapter
from memory_mesh.adapters.langchain import MemoryMeshLangChainAdapter
from memory_mesh.adapters.mcp_server import McpMemoryServer
from memory_mesh.core.graph import MemoryGraph


def test_langchain_adapter():
    adapter = MemoryMeshLangChainAdapter()
    node_id = adapter.store_fact("user", "preference", "dark_mode")
    assert node_id.startswith("node_")

    ctx = adapter.get_prompt_context()
    assert "user" in ctx
    assert "dark_mode" in ctx

    mem_vars = adapter.load_memory_variables({})
    assert "knowledge_graph_memory" in mem_vars


def test_crewai_adapter():
    adapter = MemoryMeshCrewAIAdapter()
    adapter.save("Active deployment target is AWS us-east-1", metadata={"subject": "aws", "predicate": "region"})

    results = adapter.search("aws")
    assert len(results) >= 1
    assert results[0]["subject"] == "aws"


def test_mcp_memory_server():
    server = McpMemoryServer()
    tools = server.get_tool_definitions()
    assert len(tools) == 6

    # Test memory_store tool
    store_res = server.call_tool(
        "memory_store",
        {"subject": "api_gateway", "predicate": "port", "object_value": 8080},
    )
    assert store_res["isError"] is False
    assert "Stored fact" in store_res["content"][0]["text"]

    # Test memory_recall tool
    recall_res = server.call_tool("memory_recall", {"subject": "api_gateway"})
    assert recall_res["isError"] is False
    assert "8080" in recall_res["content"][0]["text"]

    # Test memory_compress tool
    comp_res = server.call_tool("memory_compress", {})
    assert comp_res["isError"] is False
    assert "api_gateway" in comp_res["content"][0]["text"]
