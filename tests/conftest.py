"""Pytest configuration and shared fixtures for agent-memory-mesh."""

from pathlib import Path
import pytest

from memory_mesh.core.graph import MemoryGraph
from memory_mesh.storage.sqlite import SqliteStorage


@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    return tmp_path


@pytest.fixture
def empty_graph() -> MemoryGraph:
    return MemoryGraph()


@pytest.fixture
def sample_graph() -> MemoryGraph:
    g = MemoryGraph()
    g.add_fact(
        subject="user:alice",
        predicate="role",
        object_value="software_engineer",
        valid_from="2026-01-01T00:00:00+00:00",
    )
    # Alice gets promoted to tech lead later
    g.add_fact(
        subject="user:alice",
        predicate="role",
        object_value="tech_lead",
        valid_from="2026-06-01T00:00:00+00:00",
    )
    g.add_decision(
        subject="database_choice",
        chosen_option="postgresql_16",
        rationale="Superior JSONB and bi-temporal query extensions",
        alternatives=["mongodb", "mysql_8"],
    )
    return g


@pytest.fixture
def sqlite_storage(temp_dir: Path) -> SqliteStorage:
    db_file = temp_dir / "test_memory.db"
    return SqliteStorage(db_file)
