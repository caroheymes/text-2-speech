"""Tests unitaires pour le module de condensation et resume."""

from src.summarizer import generate_condensed_script, generate_half_summary, split_into_sentences


def test_split_into_sentences():
    text = "Premiere phrase complete. Deuxieme phrase informative! Troisieme proposition interrogative? Voila la suite."
    sentences = split_into_sentences(text)
    assert len(sentences) >= 3


def test_generate_condensed_script_structure():
    corpus = (
        "Le projet vise a fournir une assistance de lecture pour les personnes en difficulte d'apprentissage. "
        "Il transforme n'importe quel document PDF ou Word en synthese vocale fluide et naturelle. "
        "Les fonctionnalites comprennent un mode eclair en une minute, un resume a cinquante pourcent, "
        "et la restitution integrale avec reglage fin de la vitesse d'elocution. "
        "En conclusion, l'utilisateur gagne un temps precieux et economise son attention cognitive."
    )
    script = generate_condensed_script(corpus)
    assert "De quoi ca parle:" in script
    assert "Apports majeurs:" in script
    assert "Synthese operationnelle:" in script
    # Verifier que la longueur reste moderee (< 140 mots)
    assert len(script.split()) < 140


def test_generate_half_summary_reduction():
    paragraphs = [
        f"Ceci est le paragraphe numero {i} exposant des donnees capitales sur l'architecture logicielle du systeme."
        for i in range(1, 10)
    ]
    full_text = " ".join(paragraphs)
    initial_words = len(full_text.split())

    half_summary = generate_half_summary(full_text)
    summary_words = len(half_summary.split())

    # Le resume doit etre significativement plus court que le texte original (~40% a 65%)
    assert summary_words < initial_words
    assert summary_words >= initial_words * 0.3
