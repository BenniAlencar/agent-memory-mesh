"""Tests for the memory-mesh CLI commands."""

from click.testing import CliRunner

from memory_mesh.cli.main import cli


def test_cli_info():
    runner = CliRunner()
    result = runner.invoke(cli, ["info"])
    assert result.exit_code == 0
    assert "Agent Memory Mesh" in result.output
    assert "Benni Master OS" in result.output


def test_cli_store_and_recall_and_compress():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Store
        res_store = runner.invoke(cli, ["store", "service:payment", "gateway", "stripe"])
        assert res_store.exit_code == 0
        assert "Fact stored successfully" in res_store.output

        # Recall
        res_recall = runner.invoke(cli, ["recall", "--subject", "service:payment"])
        assert res_recall.exit_code == 0
        assert "stripe" in res_recall.output

        # Compress
        res_compress = runner.invoke(cli, ["compress"])
        assert res_compress.exit_code == 0
        assert "service:payment" in res_compress.output

        # Snapshot
        res_snap = runner.invoke(cli, ["snapshot", "test_snap.json"])
        assert res_snap.exit_code == 0
        assert "Atomic snapshot created" in res_snap.output
