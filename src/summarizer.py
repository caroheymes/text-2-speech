"""Module de generation de syntheses et condensation de texte multi-fournisseurs."""

import re
from typing import List, Tuple, Optional

from src.ai_bridge import (
    call_llm_provider, 
    is_agy_available, 
    MAX_SAFE_CLI_PROMPT_LEN
)


def generate_condensed_script(
    text: str, 
    provider: str = "agy",
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    use_ai: bool = True
) -> str:
    """Genere une synthese verbale structuree en 3 volets sous 140 mots."""
    cleaned = text.strip()
    if not cleaned:
        return "Le document est vide."

    if use_ai and provider:
        ai_script = _generate_condensed_with_provider(cleaned, provider, api_key, model)
        if ai_script:
            return ai_script

    # Fallback heuristique deterministe offline
    return _generate_condensed_heuristic(cleaned)


def _generate_condensed_with_provider(
    text: str, 
    provider: str, 
    api_key: Optional[str], 
    model: Optional[str]
) -> Optional[str]:
    source_snippet = text[:MAX_SAFE_CLI_PROMPT_LEN - 1000]
    prompt = (
        "Tu es un assistant de lecture par synthese vocale.\n"
        "Resume le texte ci-dessous sous la forme d'un script oral fluide (strictement moins de 130 mots) "
        "articule en trois parties obligatoires:\n"
        "De quoi ca parle: [Explication directe du sujet en 1 a 2 phrases]\n"
        "Apports majeurs: [2 a 3 points essentiels]\n"
        "Synthese operationnelle: [Conclusion ou action recommandee en 1 phrase]\n\n"
        "Regles strictes:\n"
        "- Style oral direct et naturel en francais.\n"
        "- Zero formule de politesse, zero introduction meta.\n"
        "- Respecter exactement les trois balises 'De quoi ca parle:', 'Apports majeurs:', 'Synthese operationnelle:'.\n\n"
        f"Texte a condenser:\n{source_snippet}"
    )

    success, result = call_llm_provider(prompt, provider=provider, api_key=api_key, model=model)
    if success and "De quoi ca parle:" in result and "Apports majeurs:" in result:
        return result.strip()
    return None


def _generate_condensed_heuristic(cleaned: str) -> str:
    sentences = split_into_sentences(cleaned)
    if not sentences:
        return cleaned

    if len(sentences) <= 3:
        objet = sentences[0]
        apports = sentences[1] if len(sentences) > 1 else sentences[0]
        conclusion = sentences[2] if len(sentences) > 2 else "L'ensemble des elements est disponible dans le texte."
        return (
            f"De quoi ca parle: {objet} "
            f"Apports majeurs: {apports} "
            f"Synthese operationnelle: {conclusion}"
        )

    scored_sentences = score_sentences(sentences, cleaned)
    lead_candidates = [s for s, idx, score in scored_sentences if idx < max(3, len(sentences) // 4)]
    objet_sentence = lead_candidates[0] if lead_candidates else sentences[0]

    middle_candidates = [
        s for s, idx, score in scored_sentences 
        if s != objet_sentence and idx < len(sentences) * 0.8
    ]
    apports = middle_candidates[:2] if len(middle_candidates) >= 2 else middle_candidates[:1]

    tail_candidates = [
        s for s, idx, score in scored_sentences 
        if idx >= len(sentences) * 0.7 and s != objet_sentence and s not in apports
    ]
    if tail_candidates:
        conclusion = tail_candidates[0]
    else:
        remainder = [s for s, idx, score in scored_sentences if s != objet_sentence and s not in apports]
        conclusion = remainder[0] if remainder else "Prendre en compte les recommandations mentionnees."

    script_parts = [
        f"De quoi ca parle: {objet_sentence.strip()}",
        f"Apports majeurs: {' '.join(s.strip() for s in apports)}",
        f"Synthese operationnelle: {conclusion.strip()}"
    ]

    script = " ".join(script_parts)
    script_words = script.split()
    if len(script_words) > 140:
        script = " ".join(script_words[:135]) + "..."

    return script


def generate_half_summary(
    text: str, 
    provider: str = "agy",
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    use_ai: bool = True
) -> str:
    """Genere un resume a environ 50% de la longueur originale."""
    cleaned = text.strip()
    if not cleaned:
        return ""

    if use_ai and provider:
        source_snippet = cleaned[:MAX_SAFE_CLI_PROMPT_LEN - 1000]
        prompt = (
            "Tu es un assistant de lecture par synthese vocale.\n"
            "Produis un resume fidele du texte suivant correspondant a environ 50% de sa longueur d'origine.\n"
            "Conserve la chronologie et les arguments majeurs. Redige en francais fluide et continu, sans puces.\n\n"
            f"Texte:\n{source_snippet}"
        )
        success, result = call_llm_provider(prompt, provider=provider, api_key=api_key, model=model)
        if success and len(result.strip()) > 30:
            return result.strip()

    return _generate_half_summary_heuristic(cleaned)


def _generate_half_summary_heuristic(cleaned: str) -> str:
    sentences = split_into_sentences(cleaned)
    if len(sentences) <= 3:
        return cleaned

    total_words = len(cleaned.split())
    target_words = total_words // 2

    scored = score_sentences(sentences, cleaned)
    ranked = sorted(scored, key=lambda item: item[2], reverse=True)

    selected_indices = set()
    current_word_count = 0

    selected_indices.add(0)
    current_word_count += len(sentences[0].split())

    for s, idx, score in ranked:
        if idx in selected_indices:
            continue
        words_in_s = len(s.split())
        selected_indices.add(idx)
        current_word_count += words_in_s
        if current_word_count >= target_words:
            break

    ordered_sentences = [sentences[i] for i in sorted(selected_indices)]
    return " ".join(ordered_sentences)


def split_into_sentences(text: str) -> List[str]:
    """Decoupe le texte en phrases coherentes."""
    raw_sentences = re.split(r"(?<=[.!?])\s+", text)
    cleaned = []
    for s in raw_sentences:
        candidate = s.strip()
        if len(candidate) > 15 and len(candidate.split()) >= 3:
            cleaned.append(candidate)
    return cleaned if cleaned else [s.strip() for s in raw_sentences if s.strip()]


def score_sentences(sentences: List[str], full_text: str) -> List[Tuple[str, int, float]]:
    """Calcule un score de pertinence pour chaque phrase base sur les frequences lexicales."""
    stop_words = {
        "le", "la", "les", "un", "une", "des", "du", "de", "ce", "ces", "cet", "cette",
        "et", "ou", "mais", "donc", "or", "ni", "car", "pour", "dans", "sur", "par",
        "en", "au", "aux", "avec", "sans", "sous", "vers", "chez", "qui", "que", "quoi",
        "dont", "est", "sont", "ete", "etre", "avoir", "fait", "ont", "a", "il", "ils",
        "elle", "elles", "on", "nous", "vous", "se", "sa", "son", "ses", "leur", "leurs"
    }

    words = re.findall(r"\b[a-zA-Z0-9àâäéèêëîïôöùûüçÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ]+\b", full_text.lower())
    freqs = {}
    for w in words:
        if len(w) > 2 and w not in stop_words:
            freqs[w] = freqs.get(w, 0) + 1

    scored = []
    total_sentences = len(sentences)

    for idx, sentence in enumerate(sentences):
        s_words = re.findall(r"\b[a-zA-Z0-9àâäéèêëîïôöùûüçÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ]+\b", sentence.lower())
        score = sum(freqs.get(w, 0) for w in s_words) / (len(s_words) + 1)

        if idx == 0:
            score *= 1.5
        elif idx < 3:
            score *= 1.2
        elif idx >= total_sentences - 2:
            score *= 1.15

        scored.append((sentence, idx, score))

    return scored
