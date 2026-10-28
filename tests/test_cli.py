"""Tests unitaires d'integration pour l'interface CLI."""

import subprocess
import sys
from pathlib import Path


def test_cli_help():
    result = subprocess.run(
        [sys.executable, "-m", "src.cli", "--help"],
        capture_output=True,
        text=True,
        check=True
    )
    assert "Text2Speech" in result.stdout
    assert "--file" in result.stdout
    assert "--mode" in result.stdout


def test_cli_execution_on_txt(tmp_path: Path):
    doc = tmp_path / "test_doc.txt"
    doc.write_text("Ceci est un document de demonstration pour verifier l'execution de bout en bout.", encoding="utf-8")
    out_audio = tmp_path / "result.mp3"

    result = subprocess.run(
        [sys.executable, "-m", "src.cli", "--file", str(doc), "--mode", "condense", "--out", str(out_audio)],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert out_audio.exists()
    assert out_audio.stat().st_size > 500
