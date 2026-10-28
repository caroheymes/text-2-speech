"""Module d'extraction et de nettoyage de texte pour Text2Speech."""

from pathlib import Path
import re
from typing import Union
from pypdf import PdfReader
from docx import Document


class ExtractionError(Exception):
    """Exception levee en cas d'echec d'extraction de document."""
    pass


def extract_text_from_file(file_path: Union[str, Path]) -> str:
    """Extrait le texte brut d'un fichier PDF, DOCX ou TXT."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Le fichier n'existe pas: {path}")

    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return _extract_from_pdf(path)
    elif suffix == ".docx":
        return _extract_from_docx(path)
    elif suffix in (".txt", ".md"):
        return _extract_from_txt(path)
    else:
        raise ExtractionError(
            f"Format de fichier non pris en charge: '{suffix}'. "
            "Formats acceptes: .pdf, .docx, .txt"
        )


def _extract_from_pdf(path: Path) -> str:
    try:
        reader = PdfReader(str(path))
        pages_text = []
        for page in reader.pages:
            text = page.extract_text() or ""
            if text.strip():
                pages_text.append(text)
        return clean_extracted_text("\n\n".join(pages_text))
    except Exception as exc:
        raise ExtractionError(f"Erreur lors de la lecture du fichier PDF: {exc}") from exc


def _extract_from_docx(path: Path) -> str:
    try:
        doc = Document(str(path))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return clean_extracted_text("\n\n".join(paragraphs))
    except Exception as exc:
        raise ExtractionError(f"Erreur lors de la lecture du fichier DOCX: {exc}") from exc


def _extract_from_txt(path: Path) -> str:
    for encoding in ("utf-8", "latin-1", "cp1252"):
        try:
            content = path.read_text(encoding=encoding)
            return clean_extracted_text(content)
        except UnicodeDecodeError:
            continue
    raise ExtractionError("Impossible de decoder le fichier texte (encodage inconnu).")


def clean_extracted_text(raw_text: str) -> str:
    """Nettoie le texte extrait: cesures, sauts de ligne redondants et espaces superflus."""
    if not raw_text:
        return ""

    # Recoller les cesures en fin de ligne (mot- \n suite)
    text = re.sub(r"(\w+)-\s*\n\s*(\w+)", r"\1\2", raw_text)

    # Remplacer les retours simples a l'interieur d'une phrase par des espaces
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    # Reduire les espaces consecutifs
    text = re.sub(r"[ \t]+", " ", text)

    # Reduire les sauts de lignes multiples a un double saut
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    return text.strip()
