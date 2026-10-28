"""Module de synthese vocale Text-to-Speech haute fidelite avec gestion des pauses."""

import asyncio
from pathlib import Path
import re
from typing import List, Optional
import edge_tts


# Voix francaises naturelles recommandees
DEFAULT_VOICE = "fr-FR-HenriNeural"
VOICES = {
    "Henri (Homme, chaleureux)": "fr-FR-HenriNeural",
    "Denise (Femme, claire)": "fr-FR-DeniseNeural",
    "Vivienne (Femme, posée)": "fr-FR-VivienneMultilingualNeural",
    "Remy (Homme, naturel)": "fr-FR-RemyMultilingualNeural",
}

# Trame MPEG-2 Layer III 24kHz 48kbps de silence pur (144 octets = 24 ms)
SILENT_FRAME = (
    b"\xff\xf3d\xc4|\x00\x00\x03H\x00\x00\x00\x00"
    b"UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU"
)


def make_silence(duration_seconds: float) -> bytes:
    """Genere une suite d'octets MP3 de silence pur sans artefact."""
    if duration_seconds <= 0:
        return b""
    frame_count = int(round(duration_seconds / 0.024))
    return SILENT_FRAME * frame_count


def speed_to_rate_str(speed: float) -> str:
    """Convertit un facteur de vitesse (ex: 1.15 ou 0.85) au format de commande edge-tts (+15% ou -15%)."""
    pct = int(round((speed - 1.0) * 100))
    return f"{pct:+d}%"


def split_text_for_pauses(text: str) -> List[str]:
    """Decoupe le texte en phrases pour l'insertion des pauses inter-phrases."""
    # Decoupage sur ponctuation terminale (. ! ? :) suivie d'espace ou retour
    raw = re.split(r"(?<=[.!?:\n])\s+", text.strip())
    segments = [s.strip() for s in raw if s.strip()]
    return segments if segments else [text.strip()]


async def _synthesize_chunk_async(text: str, voice: str, rate: str) -> bytes:
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
    chunks = []
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            chunks.append(chunk["data"])
    return b"".join(chunks)


async def _synthesize_with_pauses_async(
    text: str, 
    voice: str, 
    rate: str, 
    pause_seconds: float
) -> bytes:
    segments = split_text_for_pauses(text)
    if len(segments) <= 1 or pause_seconds <= 0:
        return await _synthesize_chunk_async(text, voice, rate)

    # Synthese concurrente de chaque phrase pour preserver la vitesse d'execution
    tasks = [_synthesize_chunk_async(seg, voice, rate) for seg in segments]
    audio_segments = await asyncio.gather(*tasks)

    silence_bytes = make_silence(pause_seconds)
    combined = []
    for i, seg_audio in enumerate(audio_segments):
        if not seg_audio:
            continue
        combined.append(seg_audio)
        if i < len(audio_segments) - 1:
            combined.append(silence_bytes)

    return b"".join(combined)


def synthesize_speech(
    text: str, 
    output_path: Path, 
    speed: float = 1.0, 
    voice: Optional[str] = None,
    pause_seconds: float = 0.8
) -> Path:
    """Genere un fichier audio MP3 avec pauses inter-phrases parametrables.
    
    Args:
        text: Texte a vocaliser.
        output_path: Chemin du fichier MP3 de sortie.
        speed: Vitesse de restitution (0.75 a 1.75).
        voice: Identifiant de la voix (defaut: fr-FR-HenriNeural).
        pause_seconds: Duree du silence entre chaque phrase en secondes (defaut: 0.8s).
        
    Returns:
        Path vers le fichier audio genere.
    """
    clean_text = text.strip()
    if not clean_text:
        clean_text = "Le contenu a lire est vide."

    chosen_voice = voice or DEFAULT_VOICE
    rate_str = speed_to_rate_str(speed)
    out_file = Path(output_path).resolve()

    try:
        audio_bytes = asyncio.run(
            _synthesize_with_pauses_async(clean_text, chosen_voice, rate_str, pause_seconds)
        )
        out_file.write_bytes(audio_bytes)
    except Exception as exc:
        raise RuntimeError(f"Echec de la synthese vocale edge-tts: {exc}") from exc

    return out_file
