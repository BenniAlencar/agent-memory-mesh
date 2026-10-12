"""
Example 01: Bi-Temporal Agent Memory Quickstart.

Demonstrates how Agent Memory Mesh automatically invalidates obsolete facts
while preserving time-travel history.
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from memory_mesh import MemoryGraph

if __name__ == "__main__":
    print("--- [MEMORY-MESH] Bi-Temporal Agent Memory Quickstart ---")
    graph = MemoryGraph()

    # Step 1: Agent learns user is on free tier in January
    graph.add_fact(
        subject="customer:acme_corp",
        predicate="plan",
        object_value="free_tier",
        valid_from="2026-01-01T00:00:00Z",
        provenance="sales_onboarding",
    )

    # Step 2: Agent learns customer upgraded to enterprise in June
    graph.add_fact(
        subject="customer:acme_corp",
        predicate="plan",
        object_value="enterprise",
        valid_from="2026-06-01T00:00:00Z",
        provenance="stripe_webhook",
    )

    print("\n1. Querying Present (October 2026):")
    current = graph.query(subject="customer:acme_corp", predicate="plan")
    for fact in current:
        print(f"   • Active Plan: {fact.object_value} (Valid from: {fact.temporal.valid_from})")

    print("\n2. Time-Travel Query (What was the plan in March 2026?):")
    march = graph.query(
        subject="customer:acme_corp",
        predicate="plan",
        as_of_valid_time=datetime(2026, 3, 1, tzinfo=timezone.utc),
    )
    for fact in march:
        print(f"   • Historical Plan: {fact.object_value} (Was valid in March 2026)")

    print("\n3. Full Chronological Evolution Timeline:")
    for fact in graph.get_timeline("customer:acme_corp"):
        status = "CURRENT" if fact.temporal.is_current() else f"SUPERSEDED (closed at {fact.temporal.valid_to})"
        print(f"   • {fact.predicate} = {fact.object_value} [{status}]")
