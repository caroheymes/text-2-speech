"""Tests unitaires pour le moteur TTS."""

from pathlib import Path
from src.tts_engine import speed_to_rate_str, synthesize_speech


def test_speed_to_rate_str():
    assert speed_to_rate_str(1.0) == "+0%"
    assert speed_to_rate_str(1.2) == "+20%"
    assert speed_to_rate_str(0.85) == "-15%"
    assert speed_to_rate_str(1.5) == "+50%"


def test_synthesize_speech_creates_file(tmp_path: Path):
    out_file = tmp_path / "output.mp3"
    result = synthesize_speech("Phrase d'essai pour le test unitaire.", out_file, speed=1.0)
    assert result.exists()
    assert result.stat().st_size > 1000
