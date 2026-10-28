"""Passerelle unifiee: Antigravity CLI local et Fournisseurs BYOK (Gemini, OpenAI, Mistral, Anthropic)."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
from typing import Optional, Tuple
import requests


MAX_SAFE_CLI_PROMPT_LEN = 7000

# Modeles recommandes par defaut
DEFAULT_MODELS = {
    "gemini": "gemini-2.5-flash",
    "openai": "gpt-4o-mini",
    "mistral": "mistral-small-latest",
    "anthropic": "claude-3-5-haiku-20241022",
}

# Liens vers les consoles de generation de cles
KEY_PORTAL_URLS = {
    "gemini": "https://aistudio.google.com/apikey",
    "openai": "https://platform.openai.com/api-keys",
    "mistral": "https://console.mistral.ai/api-keys/",
    "anthropic": "https://console.anthropic.com/settings/keys",
}


def get_agy_path() -> str:
    """Localise le binaire executable de la CLI Antigravity (agy)."""
    env_exe = os.environ.get("ANTIGRAVITY_AGENTAPI_EXE")
    if env_exe and Path(env_exe).is_file():
        return env_exe

    found = shutil.which("agy")
    if found:
        return found

    local_app_data = os.environ.get("LOCALAPPDATA", "")
    candidate = Path(local_app_data) / "agy" / "bin" / "agy.exe"
    if candidate.is_file():
        return str(candidate)

    return "agy"


def is_agy_available() -> bool:
    """Verifie si le binaire agy est installe et accessible."""
    path = get_agy_path()
    if path != "agy":
        return Path(path).is_file()
    return shutil.which("agy") is not None


def call_antigravity_cli(
    prompt: str, 
    model: Optional[str] = None, 
    timeout_seconds: int = 120
) -> Tuple[bool, str]:
    """Execute un appel en mode print non-interactif via agy -p."""
    agy_bin = get_agy_path()
    cmd = [
        agy_bin,
        "-p",
        prompt,
        "--dangerously-skip-permissions",
        "--disable-slash-commands",
    ]
    if model:
        cmd.extend(["--model", model])

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
            shell=False,
            env=env,
            check=False,
        )

        if result.returncode == 0 and result.stdout.strip():
            return True, result.stdout.strip()
        else:
            err = result.stderr.strip() or "La commande agy a retourne une reponse vide."
            return False, f"Erreur Antigravity CLI (code {result.returncode}): {err}"
    except subprocess.TimeoutExpired:
        return False, f"Delai depasse ({timeout_seconds}s) lors de l'appel a Antigravity CLI."
    except Exception as exc:
        return False, f"Exception lors de l'appel a Antigravity CLI: {exc}"


def call_gemini_api(
    prompt: str,
    api_key: str,
    model: str = "gemini-2.5-flash",
    timeout_seconds: int = 60,
) -> Tuple[bool, str]:
    """Appel direct a l'API Google Gemini via REST."""
    if not api_key or not api_key.strip():
        return False, "Cle d'API Google AI Studio manquante."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key.strip()}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 4096},
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=timeout_seconds)
        if resp.status_code == 200:
            data = resp.json()
            candidates = data.get("candidates", [])
            if candidates and "content" in candidates[0]:
                parts = candidates[0]["content"].get("parts", [])
                text_parts = [p.get("text", "") for p in parts]
                return True, "".join(text_parts).strip()
            return False, "Reponse Gemini vide ou filtree."
        err_msg = resp.json().get("error", {}).get("message", resp.text)
        return False, f"Erreur API Gemini ({resp.status_code}): {err_msg}"
    except Exception as exc:
        return False, f"Echec de connexion a l'API Gemini: {exc}"


def call_openai_api(
    prompt: str,
    api_key: str,
    model: str = "gpt-4o-mini",
    timeout_seconds: int = 60,
) -> Tuple[bool, str]:
    """Appel direct a l'API OpenAI via REST."""
    if not api_key or not api_key.strip():
        return False, "Cle d'API OpenAI manquante."

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key.strip()}",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=timeout_seconds)
        if resp.status_code == 200:
            data = resp.json()
            choices = data.get("choices", [])
            if choices and "message" in choices[0]:
                return True, choices[0]["message"].get("content", "").strip()
            return False, "Reponse OpenAI vide."
        err_msg = resp.json().get("error", {}).get("message", resp.text)
        return False, f"Erreur API OpenAI ({resp.status_code}): {err_msg}"
    except Exception as exc:
        return False, f"Echec de connexion a l'API OpenAI: {exc}"


def call_mistral_api(
    prompt: str,
    api_key: str,
    model: str = "mistral-small-latest",
    timeout_seconds: int = 60,
) -> Tuple[bool, str]:
    """Appel direct a l'API Mistral AI via REST."""
    if not api_key or not api_key.strip():
        return False, "Cle d'API Mistral AI manquante."

    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key.strip()}",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=timeout_seconds)
        if resp.status_code == 200:
            data = resp.json()
            choices = data.get("choices", [])
            if choices and "message" in choices[0]:
                return True, choices[0]["message"].get("content", "").strip()
            return False, "Reponse Mistral vide."
        err_msg = resp.json().get("message", resp.text)
        return False, f"Erreur API Mistral ({resp.status_code}): {err_msg}"
    except Exception as exc:
        return False, f"Echec de connexion a l'API Mistral: {exc}"


def call_anthropic_api(
    prompt: str,
    api_key: str,
    model: str = "claude-3-5-haiku-20241022",
    timeout_seconds: int = 60,
) -> Tuple[bool, str]:
    """Appel direct a l'API Anthropic via REST."""
    if not api_key or not api_key.strip():
        return False, "Cle d'API Anthropic manquante."

    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key.strip(),
        "anthropic-version": "2023-06-01",
    }
    payload = {
        "model": model,
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=timeout_seconds)
        if resp.status_code == 200:
            data = resp.json()
            content = data.get("content", [])
            if content and "text" in content[0]:
                return True, content[0].get("text", "").strip()
            return False, "Reponse Anthropic vide."
        err_msg = resp.json().get("error", {}).get("message", resp.text)
        return False, f"Erreur API Anthropic ({resp.status_code}): {err_msg}"
    except Exception as exc:
        return False, f"Echec de connexion a l'API Anthropic: {exc}"


def call_llm_provider(
    prompt: str,
    provider: str,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
) -> Tuple[bool, str]:
    """Aiguille la requete vers le bon fournisseur d'IA selon la configuration."""
    provider_clean = (provider or "").lower().strip()

    if provider_clean in ("agy", "antigravity"):
        return call_antigravity_cli(prompt, model=model)
    elif provider_clean == "gemini":
        target_model = model or DEFAULT_MODELS["gemini"]
        return call_gemini_api(prompt, api_key=api_key or "", model=target_model)
    elif provider_clean == "openai":
        target_model = model or DEFAULT_MODELS["openai"]
        return call_openai_api(prompt, api_key=api_key or "", model=target_model)
    elif provider_clean == "mistral":
        target_model = model or DEFAULT_MODELS["mistral"]
        return call_mistral_api(prompt, api_key=api_key or "", model=target_model)
    elif provider_clean == "anthropic":
        target_model = model or DEFAULT_MODELS["anthropic"]
        return call_anthropic_api(prompt, api_key=api_key or "", model=target_model)
    else:
        return False, f"Fournisseur inconnu: {provider}"
