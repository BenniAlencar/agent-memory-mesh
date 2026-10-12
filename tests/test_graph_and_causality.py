"""Tests for MemoryGraph, automatic superseding, and time-travel queries."""

from datetime import datetime, timezone

from memory_mesh.core.graph import MemoryGraph
from memory_mesh.core.models import NodeType


def test_automatic_superseding():
    graph = MemoryGraph()

    # Fact 1: User status is trial
    node1 = graph.add_fact(
        subject="user:123",
        predicate="subscription",
        object_value="trial",
        valid_from="2026-01-01T00:00:00+00:00",
    )

    assert node1.temporal.is_current() is True
    assert graph.count_active_facts() == 1

    # Fact 2: User upgrades to pro on Feb 1st
    node2 = graph.add_fact(
        subject="user:123",
        predicate="subscription",
        object_value="pro",
        valid_from="2026-02-01T00:00:00+00:00",
    )

    # Node 1 should now be superseded
    assert node1.temporal.is_current() is False
    assert node1.temporal.valid_to == "2026-02-01T00:00:00+00:00"
    assert node2.temporal.is_current() is True
    assert graph.count_active_facts() == 1

    # Relations should link them
    relations = graph.get_relations_for(node2.id)
    assert len(relations) == 1
    assert relations[0].relation_type == "supersedes"
    assert relations[0].target_id == node1.id


def test_time_travel_queries():
    graph = MemoryGraph()
    graph.add_fact(
        subject="service:api",
        predicate="version",
        object_value="v1.0.0",
        valid_from="2026-01-01T00:00:00+00:00",
    )
    graph.add_fact(
        subject="service:api",
        predicate="version",
        object_value="v2.0.0",
        valid_from="2026-06-01T00:00:00+00:00",
    )

    # Querying present
    current_res = graph.query(subject="service:api", predicate="version")
    assert len(current_res) == 1
    assert current_res[0].object_value == "v2.0.0"

    # Querying past (March 2026)
    march_dt = datetime(2026, 3, 15, tzinfo=timezone.utc)
    past_res = graph.query(subject="service:api", predicate="version", as_of_valid_time=march_dt)
    assert len(past_res) == 1
    assert past_res[0].object_value == "v1.0.0"

    # Querying all including superseded
    all_res = graph.query(subject="service:api", predicate="version", include_superseded=True)
    assert len(all_res) == 2


def test_timeline():
    graph = MemoryGraph()
    graph.add_fact(subject="db", predicate="port", object_value=5432, valid_from="2026-01-01T00:00:00+00:00")
    graph.add_fact(subject="db", predicate="port", object_value=5433, valid_from="2026-02-01T00:00:00+00:00")

    timeline = graph.get_timeline("db")
    assert len(timeline) == 2
    assert timeline[0].object_value == 5432
    assert timeline[1].object_value == 5433


def test_add_decision():
    graph = MemoryGraph()
    dec_node = graph.add_decision(
        subject="caching_layer",
        chosen_option="redis_cluster",
        rationale="Sub-millisecond latency requirement",
        alternatives=["memcached", "dynamodb"],
    )

    assert dec_node.node_type == NodeType.DECISION
    assert dec_node.metadata["rationale"] == "Sub-millisecond latency requirement"
    assert "memcached" in dec_node.metadata["alternatives"]
