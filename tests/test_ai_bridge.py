"""Tests unitaires pour la passerelle Antigravity CLI et BYOK."""

from src.ai_bridge import (
    get_agy_path, 
    is_agy_available, 
    call_llm_provider,
    call_gemini_api,
    call_openai_api,
    call_mistral_api,
    call_anthropic_api
)


def test_agy_path_resolution():
    path = get_agy_path()
    assert path is not None
    assert len(path) > 0


def test_is_agy_available():
    assert is_agy_available() is True


def test_gemini_missing_key():
    success, msg = call_gemini_api("Bonjour", api_key="")
    assert success is False
    assert "manquante" in msg


def test_openai_missing_key():
    success, msg = call_openai_api("Bonjour", api_key="")
    assert success is False
    assert "manquante" in msg


def test_mistral_missing_key():
    success, msg = call_mistral_api("Bonjour", api_key="")
    assert success is False
    assert "manquante" in msg


def test_anthropic_missing_key():
    success, msg = call_anthropic_api("Bonjour", api_key="")
    assert success is False
    assert "manquante" in msg


def test_call_llm_provider_unknown():
    success, msg = call_llm_provider("Bonjour", provider="unknown_provider")
    assert success is False
    assert "Inconnu" in msg or "inconnu" in msg
