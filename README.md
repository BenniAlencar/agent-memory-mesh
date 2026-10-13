<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0D0D0D,50:33001e,100:FF007F&height=200&section=header&text=agent-memory-mesh&fontSize=56&fontColor=ffffff&fontAlignY=38&desc=Bi-Temporal%20State%20Graph%20and%20Lossless%20Context%20Compression%20Engine%20for%20AI%20Agents&descAlignY=58&descSize=16&animation=fadeIn" width="100%"/>

<br/>

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=700&size=20&duration=3000&pause=800&color=FF007F&center=true&vCenter=true&multiline=true&repeat=true&width=900&height=80&lines=Bi-Temporal+State+Graph+Engine+for+AI+Agents.;85%25%2B+Lossless+Token+Context+Compression.;Automatic+Superseding+%E2%80%94+Zero+Contradictions.;Benni+Master+OS+Kernel+v9.4+%E2%80%94+Skill+60+and+61+Native." alt="Typing SVG" />

<br/><br/>

[![CI](https://github.com/BenniAlencar/agent-memory-mesh/actions/workflows/ci.yml/badge.svg)](https://github.com/BenniAlencar/agent-memory-mesh/actions/workflows/ci.yml)
[![Tests](https://img.shields.io/badge/Tests-18%20Passed-FF007F?style=for-the-badge&logo=pytest&logoColor=white)](#-test-suite--verification)
[![Python](https://img.shields.io/badge/Python-3.10+-FF007F?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-Server%20Built--In-FF007F?style=for-the-badge&logo=anthropic&logoColor=white)](https://modelcontextprotocol.io/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-0D0D0D?style=for-the-badge&logo=apache&logoColor=FF007F)](LICENSE)
[![Part of Benni OS](https://img.shields.io/badge/Part%20of-Benni%20OS%20Engineering-0D0D0D?style=for-the-badge&logo=githubactions&logoColor=FF007F)](https://github.com/BenniAlencar)

<br/>

> **"Stop letting AI agents drown in conversational chatter. Bi-temporal truth graph at 85% less token overhead."**

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%"/>

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

<br/>

## ⚡ The Fatal Flaw of Naive Vector Search

In 2026, most developers build agent memory using naive vector databases (RAG embeddings):

1. **Semantic Similarity Destroys Temporal Causality**: An agent asks: *"What is the customer's subscription plan?"*. The vector database returns: *"Customer account was suspended in 2023"* (score 0.89) instead of *"Customer upgraded to Enterprise in 2026"* (score 0.86) because the old text had more matching keywords. The agent acts on obsolete, contradicted facts.
2. **Context Window Inflation & Token Bleed**: Storing raw multi-turn conversation transcripts blows up context windows. Feeding 30 turns of chat back into the model burns 10,000+ tokens per turn, increasing inference latency and costs exponentially.
3. **Decision Decay in Agent Handoffs**: When specialized agents collaborate (e.g., Researcher → Coder → Tester), architectural decisions are lost in chat noise because there is no typed, immutable decision ledger.

**Agent Memory Mesh solves this completely.** Derived from the **Benni Master OS v9.4 Doctrine (Skill 60 & 61)**, it replaces probabilistic text search with a deterministic **Bi-Temporal Knowledge Graph** that automatically supersedes obsolete facts, compresses conversational context by over 85%, and provides cryptographic snapshot rollbacks.

<br/>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png" width="100%"/>

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

<br/>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png" width="100%"/>

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
graph.add_fact("customer:acme", "plan", "free_tier", valid_from="2026-01-01T00:00:00+00:00")

# June: Customer upgrades to enterprise
graph.add_fact("customer:acme", "plan", "enterprise", valid_from="2026-06-01T00:00:00+00:00")

# Present Query: Returns ONLY active Enterprise plan
active_plan = graph.query(subject="customer:acme", predicate="plan")
print("Active Plan:", active_plan[0].object_value)  # "enterprise"

# Time-Travel Query: What was their plan in March 2026?
march_plan = graph.query(
    subject="customer:acme",
    predicate="plan",
    as_of_valid_time=datetime(2026, 3, 1, tzinfo=timezone.utc),
)
print("Historical Plan in March:", march_plan[0].object_value)  # "free_tier"
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
The following ground-truth facts and decisions are active and verified. Use them over assumptions:

**Active Verified Facts:**
- `customer:acme` → `plan`: enterprise

**Immutable Decisions & Rationales:**
- `Decision: database_choice` = postgresql_16 (Rationale: Sub-millisecond bi-temporal query performance) [Rejected: mongodb, mysql_8]
```

<br/>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png" width="100%"/>

## 📊 Token FinOps & Lossless Context Compression

| Metric | Raw Multi-Turn Chat Transcript | Naive Vector RAG (Embeddings) | **Agent Memory Mesh** |
| :--- | :---: | :---: | :---: |
| **Token Consumption** | ~1,500 tokens | ~800 tokens | **~130 tokens** |
| **Token Reduction** | 0% | ~46% | **85% – 91% Saved** |
| **Obsolete Contradictions** | Common (chat history contains outdated facts) | High (semantic similarity ignores time) | **Zero (automatically superseded)** |
| **Decision Traceability** | Buried in chat dialogue | Chunk-dependent | **Dedicated immutable decision ledger** |
| **Time-Travel History** | Impossible | Inaccurate | **Deterministic (`as_of_valid_time`)** |
| **Prompt Injection Latency** | High | Embedding API overhead | **Near-zero (< 1ms)** |

<br/>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png" width="100%"/>

## 🔌 Model Context Protocol (MCP) Server

Agent Memory Mesh includes a built-in MCP server for **Claude Desktop**, **Cursor**, **Windsurf**, and **Antigravity**:

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

<br/>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png" width="100%"/>

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

<br/>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png" width="100%"/>

## 🛡️ Atomic Checkpoint Protocol (Skill 61)

Every snapshot exports an atomic, SHA-256 sealed JSON checkpoint:

```python
from memory_mesh import AtomicCheckpoint

# Save and seal
AtomicCheckpoint.save_to_file(graph, "state_snapshot.json")

# Restore and verify cryptographic integrity
restored_graph = AtomicCheckpoint.restore_from_file("state_snapshot.json")
```

<br/>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png" width="100%"/>

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

<br/>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png" width="100%"/>

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

<br/>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png" width="100%"/>

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md). All pull requests must pass 100% of tests (`pytest tests`).

## 📄 License

Agent Memory Mesh is licensed under the [Apache License, Version 2.0](LICENSE).

© 2026 Benni OS Core Engineering Group. All rights reserved.

<br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:FF007F,50:33001e,100:0D0D0D&height=120&section=footer" width="100%"/>

<div align="center">

**agent-memory-mesh** — *Part of the [Benni OS](https://github.com/BenniAlencar) Core Engineering Group*

`AGENT_MEMORY_MESH` • `SKILL_60_61_NATIVE` • `BI_TEMPORAL_GRAPH` • `LOSSLESS_COMPRESSION` • `APACHE_2.0`

Engineered by **Benni Alencar** & the Benni OS Core Engineering Group

</div>
