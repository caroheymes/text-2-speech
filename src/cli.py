"""Point d'entree en ligne de commande pour Text2Speech."""

import argparse
from pathlib import Path
import sys
import tempfile

from src.extractor import extract_text_from_file, ExtractionError
from src.summarizer import generate_condensed_script, generate_half_summary
from src.tts_engine import synthesize_speech, DEFAULT_VOICE
from src.audio_player import play_audio_direct, launch_mini_player


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Text2Speech: convertisseur de document en synthese vocale accessible."
    )
    parser.add_argument(
        "--file", "-f", 
        type=str, 
        required=True, 
        help="Chemin du document source (.pdf, .docx, .txt)"
    )
    parser.add_argument(
        "--mode", "-m", 
        choices=["condense", "summary_50", "full"], 
        default="condense",
        help="Mode de restitution: condense (<1 min), summary_50 (50%%), ou full (texte integral)"
    )
    parser.add_argument(
        "--speed", "-s", 
        type=float, 
        default=1.0, 
        help="Vitesse d'elocution (de 0.75 a 1.75, defaut: 1.0)"
    )
    parser.add_argument(
        "--voice", "-v", 
        type=str, 
        default=DEFAULT_VOICE, 
        help="Nom de la voix TTS (defaut: fr-FR-HenriNeural)"
    )
    parser.add_argument(
        "--out", "-o", 
        type=str, 
        default=None, 
        help="Chemin du fichier audio MP3 de sortie"
    )
    parser.add_argument(
        "--gui", 
        action="store_true", 
        help="Ouvre le mini-lecteur fenetre (utilise pour le clic droit Windows)"
    )
    parser.add_argument(
        "--play", 
        action="store_true", 
        help="Joue l'audio directement en console apres generation"
    )

    args = parser.parse_args()
    doc_path = Path(args.file)

    if not doc_path.exists():
        print(f"Erreur: le fichier '{doc_path}' n'existe pas.", file=sys.stderr)
        return 1

    print(f"Traitement du document: {doc_path.name}")
    try:
        raw_text = extract_text_from_file(doc_path)
    except (ExtractionError, FileNotFoundError) as exc:
        print(f"Erreur d'extraction: {exc}", file=sys.stderr)
        return 1

    if not raw_text.strip():
        print("Erreur: aucun texte exploitable extrait du document.", file=sys.stderr)
        return 1

    # Selection du mode textuel
    if args.mode == "condense":
        print("Generation de la synthese condensee (< 1 min)...")
        speech_text = generate_condensed_script(raw_text)
        mode_label = "Synthese condensee"
    elif args.mode == "summary_50":
        print("Generation du resume a 50%...")
        speech_text = generate_half_summary(raw_text)
        mode_label = "Resume a 50%"
    else:
        print("Preparation de la lecture integrale...")
        speech_text = raw_text
        mode_label = "Lecture integrale"

    # Preparation du chemin de sortie
    if args.out:
        out_path = Path(args.out)
    else:
        temp_dir = Path(tempfile.gettempdir()) / "text2speech"
        temp_dir.mkdir(parents=True, exist_ok=True)
        out_path = temp_dir / f"{doc_path.stem}_{args.mode}.mp3"

    print(f"Synthese vocale en cours avec la voix {args.voice} (vitesse: x{args.speed})...")
    try:
        audio_file = synthesize_speech(
            text=speech_text, 
            output_path=out_path, 
            speed=args.speed, 
            voice=args.voice
        )
        print(f"Fichier audio pret: {audio_file}")
    except Exception as exc:
        print(f"Erreur TTS: {exc}", file=sys.stderr)
        return 1

    # Lecture optionnelle
    if args.gui:
        launch_mini_player(
            audio_path=audio_file, 
            title=f"Text2Speech: {doc_path.name}", 
            subtitle=f"{mode_label} | Vitesse: x{args.speed}"
        )
    elif args.play:
        print("Lecture en cours (Ctrl+C pour interrompre)...")
        play_audio_direct(audio_file)

    return 0


if __name__ == "__main__":
    sys.exit(main())
