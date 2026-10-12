# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-12

### Added
- **Bi-Temporal Knowledge Graph**: Valid Time (real world) separated from Transaction Time (system assertion).
- **Automatic Fact Superseding**: Invalidation of obsolete conflicting facts with causal `supersedes` relation edges.
- **Lossless Graph Context Compression**: Distills multi-turn chat dialogues into compact semantic triples (>80% token reduction).
- **Atomic Checkpoint Protocol (Skill 61)**: Tamper-evident snapshot export and restore with SHA-256 cryptographic verification.
- **SQLite Durable Storage**: Local zero-dependency ACID persistence with WAL mode and bi-temporal indexes.
- **Adapters**:
  - LangChain / LangGraph knowledge graph memory adapter.
  - CrewAI search and persistence adapter.
  - Model Context Protocol (MCP) server endpoints (`memory_store`, `memory_recall`, `memory_timeline`, etc.).
- **Rich Terminal CLI**: Interactive commands for storage, query, compression metrics, and snapshots.
