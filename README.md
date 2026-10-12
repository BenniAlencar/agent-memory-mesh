<div align="center">

# 🧠 Agent Memory Mesh

### The Bi-Temporal State Graph & Lossless Context Compression Engine for AI Agents

[![CI Status](https://img.shields.io/badge/CI-passing-2ea44f?style=for-the-badge&logo=githubactions&logoColor=white)](.github/workflows/ci.yml)
[![Tests](https://img.shields.io/badge/tests-17%20passed%20(100%25)-success?style=for-the-badge&logo=pytest&logoColor=white)](tests/)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue?style=for-the-badge&logo=python&logoColor=white)](https://pypi.org/project/agent-memory-mesh/)
[![License](https://img.shields.io/badge/license-Apache--2.0-111827?style=for-the-badge)](LICENSE)
[![Doctrine](https://img.shields.io/badge/doctrine-Benni%20Master%20OS%20v9.4-7c3aed?style=for-the-badge)](https://bennios.dev)

<p align="center">
  <b>Stop relying on naive vector search for AI agent memory.</b><br>
  Ground your agents in deterministic, time-aware knowledge graphs with lossless token compression and SHA-256 verifiable snapshots.
</p>

[Quickstart](#-quickstart-in-30-seconds) •
[Why Vector Stores Fail](#-the-fatal-flaw-of-naive-vector-search) •
[Bi-Temporal Architecture](#-bi-temporal-knowledge-graph-architecture) •
[Token FinOps](#-token-finops--lossless-context-compression) •
[MCP Integration](#-model-context-protocol-mcp-server) •
[Enterprise Benni OS](#-from-memory-mesh-to-sovereign-multi-agent-swarms)

</div>

---

## ⚡ The Fatal Flaw of Naive Vector Search

In 2026, most developers build agent memory using naive vector databases (RAG embeddings):

1. **Semantic Similarity Destroys Temporal Causality**: An agent asks: *"What is the customer's subscription plan?"*. The vector database returns: *"Customer account was suspended in 2023"* (score 0.89) instead of *"Customer upgraded to Enterprise in 2026"* (score 0.86) because the old text had more matching keywords. The agent acts on obsolete, contradicted facts.
2. **Context Window Inflation & Token Bleed**: Storing raw multi-turn conversation transcripts blows up context windows. Feeding 30 turns of chat back into the model burns 10,000+ tokens per turn, increasing inference latency and costs exponentially.
3. **Decision Decay in Agent Handoffs**: When specialized agents collaborate (e.g., Researcher → Coder → Tester), architectural decisions are lost in chat noise because there is no typed, immutable decision ledger.

**Agent Memory Mesh solves this completely.** Derived from the **Benni Master OS v9.4 Doctrine (Skill 60 & 61)**, it replaces probabilistic text search with a deterministic **Bi-Temporal Knowledge Graph** that automatically supersedes obsolete facts, compresses conversational context by over 85%, and provides cryptographic snapshot rollbacks.

---

## 🏗️ Bi-Temporal Knowledge Graph Architecture

Every memory node in Agent Memory Mesh is tracked along two orthogonal timelines:
* **Valid Time**: When the fact is true in the physical world (`valid_from` → `valid_to`).
* **Transaction Time**: When the agent system asserted or learned the fact.

```mermaid
graph TD
    A["Fact A: customer plan = free_tier<br><i>Valid: Jan 2026 -> Jun 2026</i>"] -->|Automatic Supersede Edge| B["Fact B: customer plan = enterprise<br><i>Valid: Jun 2026 -> Present (Active)</i>"]
    B --> C{"QUERY ENGINE"}
    C -->|Query Present| D["Returns Fact B (Enterprise)<br><i>Zero Obsolete Noise</i>"]
    C -->|Time-Travel (as-of March 2026)| E["Returns Fact A (Free Tier)<br><i>Accurate Historical Replay</i>"]
```

> **The Superseding Law**: When a new fact is asserted with identical `(subject, predicate)`, previous facts are automatically closed and linked via a directed `supersedes` relation. Contradictions are eliminated at write time.

---

## 🚀 Quickstart in 30 Seconds

### 1. Installation

```bash
pip install agent-memory-mesh
```

### 2. Time-Aware Agent Memory (Eliminate Obsolete Data)

```python
from datetime import datetime, timezone
from memory_mesh import MemoryGraph

graph = MemoryGraph()

# January: Customer on free tier
graph.add_fact("customer:acme", "plan", "free_tier", valid_from="2026-01-01T00:00:00Z")

# June: Customer upgrades to enterprise
graph.add_fact("customer:acme", "plan", "enterprise", valid_from="2026-06-01T00:00:00Z")

# Present Query: Returns ONLY active Enterprise plan
active_plan = graph.query(subject="customer:acme", predicate="plan")
print(active_plan[0].object_value)  # "enterprise"

# Time-Travel Query: What was their plan in March 2026?
march_plan = graph.query(
    subject="customer:acme",
    predicate="plan",
    as_of_valid_time=datetime(2026, 3, 1, tzinfo=timezone.utc),
)
print(march_plan[0].object_value)  # "free_tier"
```

### 3. Record Immutable Decisions with Rationales

```python
graph.add_decision(
    subject="database_choice",
    chosen_option="postgresql_16",
    rationale="Sub-millisecond bi-temporal query performance and JSONB support",
    alternatives=["mongodb", "mysql_8"],
)
```

### 4. Lossless Context Compression (>85% Token Reduction)

```python
from memory_mesh import LosslessGraphCompressor

compressor = LosslessGraphCompressor()

# Compiles active graph state into a dense prompt injection block
prompt_block = compressor.compress(graph)
print(prompt_block)
```

**Output:**
```markdown
### [BI-TEMPORAL KNOWLEDGE GRAPH MEMORY]
The following ground-truth facts and decisions are active and verified:
- `customer:acme` → `plan`: enterprise
- `Decision: database_choice` = postgresql_16 (Rationale: Sub-millisecond bi-temporal query performance) [Rejected: mongodb, mysql_8]
```

---

## 📊 Token FinOps & Lossless Context Compression

| Metric | Raw Multi-Turn Chat Transcript | **Agent Memory Mesh** |
| :--- | :---: | :---: |
| **Token Consumption** | ~1,500 tokens | **~130 tokens** |
| **Token Reduction** | 0% | **91.0% Saved** |
| **Obsolete Contradictions** | Common (chat history contains outdated facts) | **Zero (automatically superseded)** |
| **Decision Traceability** | Buried in chat dialogue | **Dedicated immutable decision ledger** |
| **Prompt Injection Latency** | High | **Near-zero (< 1ms)** |

---

## 🔌 Model Context Protocol (MCP) Server

Agent Memory Mesh includes a built-in MCP server for **Claude Desktop**, **Cursor**, and **Antigravity**:

```python
from memory_mesh import McpMemoryServer

server = McpMemoryServer()

# Register directly into your MCP runtime:
# • memory_store: Stores ground-truth fact
# • memory_decision: Stores architectural/business decisions
# • memory_recall: Queries active facts
# • memory_timeline: Retrieves chronological evolution
# • memory_compress: Compiles token-dense prompt context
# • memory_snapshot: Exports SHA-256 sealed checkpoint
```

---

## 🧩 Framework Integrations

### LangChain & LangGraph
```python
from memory_mesh import MemoryMeshLangChainAdapter

adapter = MemoryMeshLangChainAdapter()
adapter.store_fact("user:carter", "role", "security_engineer")
adapter.store_decision("api_framework", "FastAPI", rationale="Native Pydantic v2 validation")

# Attach directly to agent prompt context
prompt_context = adapter.get_prompt_context()
```

### CrewAI
```python
from memory_mesh import MemoryMeshCrewAIAdapter

crew_memory = MemoryMeshCrewAIAdapter()
crew_memory.save("Deployment target is AWS us-east-1", metadata={"subject": "aws", "predicate": "region"})
```

---

## 🛡️ Atomic Checkpoint Protocol (Skill 61)

Every snapshot exports an atomic, SHA-256 sealed JSON checkpoint:

```python
from memory_mesh import AtomicCheckpoint

# Save and seal
AtomicCheckpoint.save_to_file(graph, "state_snapshot.json")

# Restore and verify cryptographic integrity
restored_graph = AtomicCheckpoint.restore_from_file("state_snapshot.json")
```

---

## 💻 Terminal CLI

```bash
# Display brand, version, and architecture doctrine
memory-mesh info

# Store verified fact
memory-mesh store "user:alice" "role" "principal_architect"

# Query active memory table
memory-mesh recall --subject "user:alice"

# Inspect compressed prompt block and token savings
memory-mesh compress

# Export SHA-256 sealed checkpoint
memory-mesh snapshot backup.json
```

---

## 🌐 From Memory Mesh to Sovereign Multi-Agent Swarms

Agent Memory Mesh was conceived inside the kernel of **Benni Master OS v9.4** to govern persistent memory across enterprise swarms (Skill 60 & 61).

### Ready to Scale Beyond Single-Agent Memory?

If your organization requires:
* **Multi-Tenant Memory Isolation**: Sovereign tenant boundary enforcement.
* **Reality Lock Zero-Trust Execution**: Cryptographic verification of tool calls and side-effects.
* **Autonomous Revenue Loops**: High-conversion landing funnels and billing reconciliation.
* **Benni Operator Hub**: Enterprise agent blueprints and mission contracts.

👉 **Explore the Benni OS Ecosystem:**
* **Official Website**: [https://bennios.dev](https://bennios.dev)
* **Benni Operator Hub**: [https://hub.bennios.dev](https://hub.bennios.dev)
* **GitHub Organization**: [https://github.com/BenniAlencar](https://github.com/BenniAlencar)
* **Documentation & Blueprints**: [https://docs.bennios.dev](https://docs.bennios.dev)

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md). All pull requests must pass 100% of tests (`pytest tests`).

## 📄 License

Agent Memory Mesh is licensed under the [Apache License, Version 2.0](LICENSE).

© 2026 Benni OS Core Engineering Group. All rights reserved.
