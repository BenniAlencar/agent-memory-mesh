# Contributing to Agent Memory Mesh

Thank you for your interest in contributing to **Agent Memory Mesh**.

## Engineering Standards

1. **Reality-Locked Execution**: All pull requests must pass 100% of tests (`pytest tests`).
2. **Deterministic Time Handling**: Never query `datetime.now()` inside domain models without supporting explicit parameter overrides for reproducible time-travel queries.
3. **Type Safety**: Strictly typed Python adhering to PEP 561.

## Local Setup

```bash
git clone https://github.com/BenniAlencar/agent-memory-mesh.git
cd agent-memory-mesh

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

pip install -e ".[dev]"
pytest tests -v
```
