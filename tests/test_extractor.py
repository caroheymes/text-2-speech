"""Tests unitaires pour le module d'extraction de documents."""

import pytest
from pathlib import Path
from src.extractor import extract_text_from_file, clean_extracted_text, ExtractionError


def test_clean_extracted_text():
    raw = "Ceci est un mot-\ncoupé dans une phrase.\nEt voici un autre paragraphe."
    cleaned = clean_extracted_text(raw)
    assert "mot-coupé" not in cleaned
    assert "motcoupé" in cleaned
    assert "phrase." in cleaned


def test_extract_from_txt(tmp_path: Path):
    sample_file = tmp_path / "sample.txt"
    sample_file.write_text("Introduction au projet Text2Speech.\nFonctionnalite de lecture vocale.", encoding="utf-8")

    text = extract_text_from_file(sample_file)
    assert "Introduction au projet Text2Speech." in text
    assert "Fonctionnalite de lecture vocale." in text


def test_unsupported_format(tmp_path: Path):
    invalid_file = tmp_path / "sample.xyz"
    invalid_file.write_text("Contenu arbitraire")

    with pytest.raises(ExtractionError):
        extract_text_from_file(invalid_file)
