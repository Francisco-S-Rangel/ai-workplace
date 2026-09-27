# tests/test_mcp_server.py — WHY: checks the MCP tools' contract without starting a process
# (topic 6: MCP; topic 11: tests). FastMCP's decorators return the plain functions, so they
# can be called directly. The full stdio round-trip is shown by scripts/list_mcp_tools.py.
from mcp_server.server import get_chunk, index_stats_resource, list_sources, search_notes


def test_search_notes_returns_citations_and_caps_top_k():
    results = search_notes("lost in the middle", top_k=50)
    assert 0 < len(results) <= 10
    assert results[0]["citation"] == "context-window.md#Lost in the Middle"


def test_list_sources_and_get_chunk():
    assert "rag-basics.md" in list_sources()
    chunk = get_chunk("rag-basics-00")
    assert chunk["source"] == "rag-basics.md" and chunk["citation"].startswith("rag-basics.md#")
    assert "error" in get_chunk("does-not-exist")


def test_index_stats_resource():
    stats = index_stats_resource()
    assert stats["chunk_count"] > 0 and stats["source_count"] == len(list_sources())
