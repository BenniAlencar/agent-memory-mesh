# Agent Memory Mesh — Architecture Specification

**Doctrine:** Benni Master OS v9.4 — Skill 60 (Session Memory Ops) & Skill 61 (Snapshot Restore Protocol)

---

## 1. System Overview

`agent-memory-mesh` replaces noisy vector-similarity RAG transcripts with a deterministic **Bi-Temporal Knowledge Graph**. Facts are tracked along two orthogonal timelines (**Valid Time** and **Transaction Time**), contradictions are eliminated at write time via automatic `supersedes` edges, and active state is compiled into hyper-dense semantic triples.

```text
  LangChain / CrewAI / MCP Clients / Multi-Agent Swarms
         │
         ├──► MemoryGraph.add_fact / add_decision / query
         └──► McpMemoryServer (JSON-RPC 2.0 Tools)
                       │
                       ▼
  ┌─────────────────────────────────────────────────────────────────────┐
  │                         agent-memory-mesh                           │
  │                                                                     │
  │  ┌───────────────────┐  ┌───────────────────┐  ┌─────────────────┐  │
  │  │ Bi-Temporal Graph │  │  Lossless Graph   │  │ Atomic          │  │
  │  │ • Valid Time      │─►│  Compressor       │─►│ Checkpoint      │  │
  │  │ • Transaction Time│  │  • Semantic Triple│  │ • SHA-256 Seal  │  │
  │  │ • Auto-Supersede  │  │  • Decision Ledger│  │ • Tamper Guard  │  │
  │  └───────────────────┘  └───────────────────┘  └─────────────────┘  │
  │                                                                     │
  │  ┌───────────────────┐  ┌───────────────────┐  ┌─────────────────┐  │
  │  │ Storage Backends  │  │  Framework        │  │ Tools & CLI     │  │
  │  │ • SQLite Graph DB │  │  Adapters         │  │ • doctor        │  │
  │  │ • In-Memory       │  │  • LangChain      │  │ • bench_matrix  │  │
  │  │ • BaseMemoryABC   │  │  • CrewAI / MCP   │  │ • store/query   │  │
  │  └───────────────────┘  └───────────────────┘  └─────────────────┘  │
  └─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Core Components

| Module | Responsibility |
|---|---|
| `memory_mesh/core/models.py` | `MemoryNode`, `MemoryRelation`, `BiTemporalInterval`, `NodeType` |
| `memory_mesh/core/graph.py` | `MemoryGraph` with automatic superseding and `as_of_valid_time` time-travel queries |
| `memory_mesh/core/compressor.py` | `LosslessGraphCompressor` compiling active triples & decisions into minimal-token context |
| `memory_mesh/core/checkpoint.py` | `AtomicCheckpoint` producing and verifying SHA-256 `CheckpointPayload` archives |
| `memory_mesh/storage/sqlite.py` | `SqliteStorage` persisting nodes, temporal intervals, and causal edges |
| `memory_mesh/storage/memory.py` | `InMemoryStorage` for zero-I/O testing |
| `memory_mesh/adapters/` | Drop-in integrations for `langchain`, `crewai`, and `mcp_server` |
| `memory_mesh/tools/` | `doctor.py` environment/bi-temporal probe and `bench_matrix.py` compression matrix |
| `memory_mesh/cli/main.py` | Click + Rich terminal CLI (`info`, `store`, `query`, `compress`, `snapshot`, `doctor`, `matrix`) |

---

## 3. Verification Gates

- `scripts/gate_bitemporal_integrity.py`: Fail-closed gate verifying superseding, time-travel queries, decision preservation, and SHA-256 checkpoint tamper rejection.
- `scripts/benchmark_compression_ratio.py`: Token savings and throughput benchmark across graph scales.
