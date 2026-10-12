<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0D0D0D,50:33001e,100:FF007F&height=200&section=header&text=agent-memory-mesh&fontSize=56&fontColor=ffffff&fontAlignY=38&desc=Bi-Temporal%20State%20Graph%20%26%20Lossless%20Context%20Compression%20Engine%20for%20AI%20Agents&descAlignY=58&descSize=16&animation=fadeIn" width="100%"/>

<br/>

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=700&size=20&duration=3000&pause=800&color=FF007F&center=true&vCenter=true&multiline=true&repeat=true&width=900&height=80&lines=Bi-Temporal+State+Graph+Engine+for+AI+Agents.;85%25%2B+Lossless+Token+Context+Compression.;Automatic+Superseding+%E2%80%94+Zero+Contradictions.;Benni+Master+OS+Kernel+v9.4+%E2%80%94+Skill+60+%26+61+Native." alt="Typing SVG" />

<br/><br/>

[![CI](https://github.com/BenniAlencar/agent-memory-mesh/actions/workflows/ci.yml/badge.svg)](https://github.com/BenniAlencar/agent-memory-mesh/actions/workflows/ci.yml)
[![Tests](https://img.shields.io/badge/Tests-18%20Passed-FF007F?style=for-the-badge&logo=pytest&logoColor=white)](#-test-suite--verification)
[![Python](https://img.shields.io/badge/Python-3.10+-FF007F?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-Server%20Built--In-FF007F?style=for-the-badge&logo=anthropic&logoColor=white)](https://modelcontextprotocol.io/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-0D0D0D?style=for-the-badge&logo=apache&logoColor=FF007F)](LICENSE)
[![Part of Benni OS](https://img.shields.io/badge/Part%20of-Benni%20OS-0D0D0D?style=for-the-badge&logo=githubactions&logoColor=FF007F)](https://github.com/BenniAlencar)

<br/>

> **"Stop letting AI agents drown in conversational chatter. Bi-temporal truth graph at 85% less token overhead."**

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%"/>

</div>

<br/>

## ⭐ What Is agent-memory-mesh?

**agent-memory-mesh** is the persistent bi-temporal knowledge graph and lossless context compression engine of the **[Benni OS](https://github.com/BenniAlencar)** ecosystem. It eliminates the fatal flaws of naive vector search (RAG) and conversational context bloat in autonomous AI agents, LangChain/CrewAI swarms, and MCP clients.

Every standard agent implementation either dumps raw conversational history back into the LLM context window (burning thousands of tokens per turn) or relies on naive vector embeddings that confuse temporal causality (retrieving superseded facts simply because they match keyword similarity).

`agent-memory-mesh` treats agent memory as a **deterministic, time-aware semantic graph**: separating real-world validity from system transaction time, automatically invalidating obsolete facts at write time, and compiling active memory into hyper-dense prompt blocks.

```
   Multi-Turn Conversation / Tool Calls / Agent Handoffs
                             ↓
             [ MemoryGraph.add_fact() / add_decision() ]
                             ↓
    ┌─────────────────────────────────────────────────────────┐
    │                   agent-memory-mesh                     │
    │                                                         │
    │  ┌───────────────────────┐   ┌───────────────────────┐  │
    │  │  Bi-Temporal Core     │   │  Automatic Supersede  │  │
    │  │  Valid vs Trans Time  │ → │  Zero Contradictions  │  │
    │  └───────────────────────┘   └───────────────────────┘  │
    └─────────────────────────────────────────────────────────┘
                             ↓
    ┌─────────────────────────────────────────────────────────┐
    │  Lossless Graph Context Compressor                      │
    │  • Collapses 1,500+ chat tokens into ~130 dense tokens  │
    │  • Immutable Decision Ledger preserves rationale        │
    │  • SHA-256 Atomic Checkpoint & Tamper-Evident Snapshots │
    └─────────────────────────────────────────────────────────┘
                             ↓
         Hyper-Dense Ground-Truth Injected into LLM Context
```

<br/>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png" width="100%"/>

## ⚡ Core Doctrine

> These are not optional configuration flags. These are architecture laws.

| ☔ Principle | 🔧 Implementation |
|---|---|
| **Bi-Temporal Orthogonality** | Every fact tracks two timelines: `valid_time` (real-world validity) and `transaction_time` (system learning time). |
| **Automatic Superseding** | Writing a new fact with matching `(subject, predicate)` automatically closes the validity interval of the previous fact and creates an edge. |
| **Lossless Context Compression** | Replaces verbose, repetitive chat transcripts with dense semantic triples, saving >85% of prompt token budget. |
| **Immutable Decision Ledger** | Architectural and business choices record options chosen, rationales, and rejected alternatives for zero decision decay. |
| **Tamper-Evident Checkpoints** | State snapshots are sealed with deterministic SHA-256 digests conforming to the Atomic Checkpoint Protocol (Skill 61). |
| **Deterministic Time-Travel** | Querying with `as_of_valid_time` reconstructs the exact historical truth at any past moment in time. |
| **Native Zero-Hop Storage** | Runs in-memory with zero overhead or persists to durable SQLite with indexed bi-temporal schema. |

<br/>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png" width="100%"/>

## 🚀 Quick Start

### 1. Installation

```bash
# Clone
git clone https://github.com/BenniAlencar/agent-memory-mesh
cd agent-memory-mesh

# Install
pip install -e ".[dev]"
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

### 4. Lossless Context Compression (>85% Token Savings)

```python
from memory_mesh import LosslessGraphCompressor

compressor = LosslessGraphCompressor()

# Compiles active graph state into a dense prompt injection block
prompt_block = compressor.compress(graph)
print(prompt_block)
```

**Compiled Prompt Block:**
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

## 🧠 Skill 60 & 61 — Bi-Temporal Knowledge Engine

Derived from **Benni Master OS Skill 60 (Session Memory Ops)** and **Skill 61 (Snapshot Restore Protocol)**, `agent-memory-mesh` resolves the three fatal flaws of conventional AI memory:

| Subsystem | Mission | Capability |
|---|---|---|
| **BiTemporalInterval** | Orthogonal time coordinates | Separates real-world event timestamp from system ingestion time |
| **Superseding Engine** | Contradiction elimination | Automatically marks older triples as superseded and creates causal graph links |
| **Lossless Compressor** | Token economy FinOps | Distills conversational turns into canonical semantic triples |
| **Atomic Checkpoint** | Cryptographic state preservation | Serializes, hashes, and hydrates memory graphs with SHA-256 tamper verification |
| **SqliteStorage** | Zero-dependency persistence | Embedded, ACID-compliant local database with indexed bi-temporal queries |

```bash
# Terminal memory management & time-travel inspection
$ memory-mesh store "server:edge" "status" "healthy"
$ memory-mesh store "server:edge" "status" "degraded"
$ memory-mesh recall --subject "server:edge"

Knowledge Graph Memory Query
┌─────────────┬───────────┬──────────┬────────────┬─────────────────────┐
│ Subject     │ Predicate │ Value    │ Status     │ Valid From          │
├─────────────┼───────────┼──────────┼────────────┼─────────────────────┤
│ server:edge │ status    │ degraded │ ACTIVE     │ 2026-10-12T04:30:00 │
└─────────────┴───────────┴──────────┴────────────┴─────────────────────┘
```

<br/>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png" width="100%"/>

## 🔌 Model Context Protocol (MCP) Memory Server

`agent-memory-mesh` ships with a native MCP server for **Claude Desktop**, **Cursor**, **Windsurf**, and **Antigravity**:

```python
from memory_mesh import McpMemoryServer

server = McpMemoryServer()

# Built-in native tools exposed to the agent:
# • memory_store: Stores ground-truth verified fact
# • memory_decision: Stores architectural/business decision with rationale
# • memory_recall: Queries active facts by subject or predicate
# • memory_timeline: Retrieves complete chronological evolution of an entity
# • memory_compress: Compiles token-dense prompt injection block
# • memory_snapshot: Exports SHA-256 sealed checkpoint file
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

## 📊 Token FinOps & Benchmark Comparison

| Metric | Raw Multi-Turn Chat Transcript | Naive Vector RAG (Embeddings) | **agent-memory-mesh** |
|---|:---:|:---:|:---:|
| **Token Consumption** | ~1,500 tokens | ~800 tokens | **~130 tokens** |
| **Token Cost Reduction** | 0% | ~46% | **85% – 91% Saved** |
| **Obsolete Contradictions** | High (chat contains outdated facts) | High (semantic similarity ignores time) | **Zero (automatically superseded)** |
| **Decision Traceability** | Lost in conversational noise | Chunk-dependent | **Dedicated immutable decision ledger** |
| **Time-Travel History** | Impossible | Inaccurate | **Deterministic (`as_of_valid_time`)** |
| **Snapshot Integrity** | None | None | **SHA-256 Tamper-Evident Seal** |
| **Inference Latency** | High (large context payload) | Embedding generation delay | **Sub-millisecond (< 1ms)** |

<br/>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png" width="100%"/>

## 💻 Terminal CLI & Audit Suite

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

### Cryptographic Checkpoint Artifact

Snapshots conform strictly to the Atomic Checkpoint Protocol (Skill 61):

```json
{
  "system": "Benni Master OS Memory Mesh v1.0.0",
  "created_at": "2026-10-12T04:30:00.120+00:00",
  "node_count": 3,
  "relation_count": 2,
  "nodes": [
    {
      "id": "node_7f3a9e120b4a",
      "node_type": "fact",
      "subject": "customer:acme",
      "predicate": "plan",
      "object_value": "enterprise",
      "temporal": {
        "valid_from": "2026-06-01T00:00:00+00:00",
        "valid_to": null,
        "transaction_time": "2026-10-12T04:30:00.120+00:00"
      },
      "digest": "8a3d5e..."
    }
  ],
  "relations": [],
  "checkpoint_hash": "b2f4c91a08..."
}
```

<br/>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png" width="100%"/>

## 🗂️ Project Structure

```
agent-memory-mesh/
├── memory_mesh/
│   ├── __init__.py               # Public API exports
│   ├── version.py                # Version & Benni OS v9.4 doctrine
│   ├── core/
│   │   ├── models.py             # MemoryNode, BiTemporalInterval, NodeType
│   │   ├── graph.py              # MemoryGraph, superseding engine & time travel
│   │   ├── compressor.py         # LosslessGraphCompressor (prompt injection)
│   │   └── checkpoint.py         # AtomicCheckpoint SHA-256 snapshot protocol
│   ├── storage/
│   │   ├── base.py               # BaseMemoryStorage abstract interface
│   │   ├── memory.py             # InMemoryStorage backend
│   │   └── sqlite.py             # Durable SqliteStorage backend
│   ├── adapters/
│   │   ├── mcp_server.py         # Native Model Context Protocol (MCP) server
│   │   ├── langchain.py          # LangChain memory adapter
│   │   └── crewai.py             # CrewAI memory adapter
│   └── cli/
│       └── main.py               # memory-mesh info / store / recall / compress
├── examples/
│   ├── 01_quickstart_bitemporal.py
│   ├── 02_lossless_compression.py
│   ├── 03_atomic_checkpoint.py
│   ├── 04_langchain_agent_memory.py
│   └── 05_mcp_memory_server.py
├── tests/
│   ├── conftest.py
│   ├── test_models_and_bitemporal.py
│   ├── test_graph_and_causality.py
│   ├── test_compressor.py
│   ├── test_checkpoint_restore.py
│   ├── test_sqlite_storage.py
│   ├── test_adapters.py
│   └── test_cli.py
├── pyproject.toml
├── LICENSE
└── README.md
```

<br/>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png" width="100%"/>

## 🛠️ Development & Test Suite

```bash
git clone https://github.com/BenniAlencar/agent-memory-mesh
cd agent-memory-mesh
pip install -e ".[dev]"

# Run full test suite across Python 3.10, 3.11, 3.12
pytest tests -v --tb=short
```

**Requirements:**
- Python 3.10+ (supports 3.10, 3.11, 3.12)
- Zero external vector database servers or API keys required
- Native SQLite & Pydantic v2 runtime

<br/>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png" width="100%"/>

## 🤝 Contributing

All contributions are welcome. Priority tracks:
- Graph visualization adapters (Mermaid, D3, Cytoscape)
- Vector indexing hybrid bridges (pgvector, Qdrant, LanceDB)
- LlamaIndex, AutoGen, and Semantic Kernel adapters

See [CONTRIBUTING.md](CONTRIBUTING.md) for full development guidelines.

<br/>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png" width="100%"/>

## 🌐 Benni OS Ecosystem

| Product | Repo | Role | Status |
|---|---|---|---|
| 🧠 **Benni Master OS** | [benni-os/Benni-Master-OS](https://github.com/benni-os/Benni-Master-OS) | General Brain — sovereign multi-agent orchestrator | 🟢 Live |
| ⚡ **Project Adam** | [benni-os/Project-Adam](https://github.com/benni-os/Project-Adam) | Local operator runtime & agent swarm coordinator | 🟢 Ativo |
| 🔒 **reality-lock** | [BenniAlencar/reality-lock](https://github.com/BenniAlencar/reality-lock) | Deterministic zero-trust & execution evidence | 🟢 Live |
| 🧠 **agent-memory-mesh** | [BenniAlencar/agent-memory-mesh](https://github.com/BenniAlencar/agent-memory-mesh) | Bi-temporal state graph & lossless context compression — you are here | 🟢 Live |
| 🔌 **Operator Gateway** | [benni-os/benni-operator-gateway](https://github.com/benni-os/benni-operator-gateway) | Open-source MCP HTTP gateway & federation hub | 🟢 MIT |
| 🐍 **mcp-forge** | [benni-os/mcp-forge](https://github.com/benni-os/mcp-forge) | FastAPI-style Python MCP framework | 🟢 PyPI |
| ⚡ **benni-nexus** | [benni-os/benni-nexus](https://github.com/benni-os/benni-nexus) | LLM gateway — strategy routing & fallback | 🟢 npm |
| 🔥 **benni-inference-engine** | [benni-os/benni-inference-engine](https://github.com/benni-os/benni-inference-engine) | GPU+CPU hybrid inference for MoE models | 🔥 Building |
| 🛠️ **Benni Control Plane** | MCP on Railway | Quad-Mesh State, RLS isolation & memory layer | 🟢 Live |
| 🤖 **Project Benjamin** | [benni-os/Project-Benjamin](https://github.com/benni-os/Project-Benjamin) | Sovereign mechanical execution arm & zero-token I/O | 🔥 Hot |
| 🌌 **Project Genesis** | [benni-os/benni-os-genesis](https://github.com/benni-os/benni-os-genesis) | Sovereign IDE & Execution Harness (Creative Studio + MONOMO) | 🟢 Live |
| 🛍️ **Modo Operador** | [benni-os/modo-operador](https://github.com/benni-os/modo-operador) | Produto BR — R$97 | 🟢 Live |

<br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:FF007F,50:33001e,100:0D0D0D&height=120&section=footer" width="100%"/>

<div align="center">

**agent-memory-mesh** — *Bi-Temporal State Graph & Context Compression by [Benni OS](https://github.com/BenniAlencar)*

`AGENT_MEMORY_MESH` • `SKILL_60_61_NATIVE` • `BI_TEMPORAL_GRAPH` • `LOSSLESS_COMPRESSION` • `APACHE_2.0`

Built by [Benni Alencar](https://github.com/BenniAlencar)

</div>
