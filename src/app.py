"""Application Streamlit de lecture vocale accessible avec support multi-IA et BYOK."""

import base64
import os
from pathlib import Path
import sys
import tempfile

# Injection de la racine du projet dans sys.path pour resoudre le paquet src
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import streamlit.components.v1 as components

from src.extractor import extract_text_from_file, ExtractionError
from src.summarizer import generate_condensed_script, generate_half_summary
from src.tts_engine import synthesize_speech, VOICES, DEFAULT_VOICE

try:
    from src.ai_bridge import is_agy_available, DEFAULT_MODELS, KEY_PORTAL_URLS
except ImportError:
    from src.ai_bridge import is_agy_available
    DEFAULT_MODELS = {
        "gemini": "gemini-2.5-flash",
        "openai": "gpt-4o-mini",
        "mistral": "mistral-small-latest",
        "anthropic": "claude-3-5-haiku-20241022",
    }
    KEY_PORTAL_URLS = {
        "gemini": "https://aistudio.google.com/apikey",
        "openai": "https://platform.openai.com/api-keys",
        "mistral": "https://console.mistral.ai/api-keys/",
        "anthropic": "https://console.anthropic.com/settings/keys",
    }


st.set_page_config(
    page_title="Lecteur vocal accessible",
    page_icon="🔊",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Style ergonomique et lisible conforme a DESIGN.md et EXPERIENCE.md
st.markdown("""
<style>
    /* Grille et conteneur principal bride a 780px pour eviter la dispersion occulaire */
    .block-container {
        max-width: 780px !important;
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
    }
    .main-title {
        font-size: 2.25rem;
        font-weight: 700;
        color: #0F172A;
        letter-spacing: -0.02em;
        line-height: 1.25;
        margin-bottom: 0.35rem;
    }
    .subtitle {
        font-size: 1.15rem;
        color: #475569;
        line-height: 1.6;
        margin-bottom: 1.8rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #2563EB;
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        min-height: 48px;
        padding: 0.75rem 1.25rem;
        border-radius: 8px;
        border: none;
        transition: background-color 0.15s ease;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
    }
    .stButton>button:active {
        background-color: #1E40AF;
    }
    .doc-success {
        background-color: #F0FDF4;
        border: 1px solid #BBF7D0;
        color: #166534;
        padding: 0.85rem 1.15rem;
        border-radius: 8px;
        font-weight: 500;
        font-size: 0.98rem;
        margin: 1rem 0;
    }
    .text-preview {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #2563EB;
        padding: 1.25rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-size: 1.08rem;
        line-height: 1.7;
        letter-spacing: 0.015em;
        color: #0F172A;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
    }
    .byok-badge {
        font-size: 0.85rem;
        padding: 8px 12px;
        background-color: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-radius: 6px;
        margin-bottom: 12px;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)


def render_html5_audio_player(audio_bytes: bytes, filename: str, initial_speed: float = 1.0):
    """Lecteur HTML5 avec acceleration instantanee cote client sans rechargement serveur."""
    b64 = base64.b64encode(audio_bytes).decode()
    speed_val = f"{initial_speed:.2f}"
    player_html = f"""
    <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 16px; margin: 14px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <audio id="audio-player" controls autoplay style="width: 100%; height: 46px; outline: none;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            Votre navigateur ne prend pas en charge l'element audio.
        </audio>
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; margin-top: 14px; padding-top: 12px; border-top: 1px solid #E2E8F0;">
            <div style="display: flex; align-items: center; gap: 6px;">
                <span style="font-weight: 600; color: #334155; font-size: 0.92rem; margin-right: 4px;">Vitesse :</span>
                <button type="button" onclick="setSpeed(0.85)" style="cursor: pointer; border: 1px solid #CBD5E1; background: white; border-radius: 6px; padding: 4px 10px; font-size: 0.85rem; font-weight: 500;">0.85x</button>
                <button type="button" onclick="setSpeed(1.0)" style="cursor: pointer; border: 1px solid #CBD5E1; background: white; border-radius: 6px; padding: 4px 10px; font-size: 0.85rem; font-weight: 500;">1.0x</button>
                <button type="button" onclick="setSpeed(1.2)" style="cursor: pointer; border: 1px solid #CBD5E1; background: white; border-radius: 6px; padding: 4px 10px; font-size: 0.85rem; font-weight: 500;">1.2x</button>
                <button type="button" onclick="setSpeed(1.5)" style="cursor: pointer; border: 1px solid #CBD5E1; background: white; border-radius: 6px; padding: 4px 10px; font-size: 0.85rem; font-weight: 500;">1.5x</button>
                <button type="button" onclick="setSpeed(1.75)" style="cursor: pointer; border: 1px solid #CBD5E1; background: white; border-radius: 6px; padding: 4px 10px; font-size: 0.85rem; font-weight: 500;">1.75x</button>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 0.88rem; color: #64748B;">Reglage fin :</span>
                <input type="range" id="speed-slider" min="0.75" max="2.0" step="0.05" value="{speed_val}" 
                       style="cursor: pointer; width: 130px; accent-color: #2563EB;"
                       oninput="setSpeed(this.value)">
                <span id="speed-indicator" style="font-weight: 700; color: #2563EB; min-width: 48px; font-size: 0.95rem; text-align: right;">{speed_val}x</span>
            </div>
        </div>
    </div>
    <script>
        function setSpeed(val) {{
            var player = document.getElementById('audio-player');
            if (player) {{
                var num = parseFloat(val);
                player.playbackRate = num;
                document.getElementById('speed-slider').value = num;
                document.getElementById('speed-indicator').innerText = num.toFixed(2) + 'x';
            }}
        }}
        setTimeout(function() {{ setSpeed({speed_val}); }}, 100);
    </script>
    """
    components.html(player_html, height=140)


def main():
    st.markdown('<div class="main-title">Lecteur vocal accessible</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Deposez votre document et ecoutez-le en quelques secondes a la vitesse de votre choix.</div>',
        unsafe_allow_html=True
    )

    if "speech_text" not in st.session_state:
        st.session_state["speech_text"] = None
    if "audio_bytes" not in st.session_state:
        st.session_state["audio_bytes"] = None
    if "audio_filename" not in st.session_state:
        st.session_state["audio_filename"] = None

    # Barre laterale de configuration
    with st.sidebar:
        st.header("Moteur d'intelligence")

        agy_ready = is_agy_available()
        engine_options = []
        if agy_ready:
            engine_options.append("CLI Antigravity (Local & sans cle)")
        engine_options.extend([
            "Google Gemini (BYOK - Cle gratuite)",
            "OpenAI (BYOK)",
            "Mistral AI (BYOK)",
            "Anthropic (BYOK)",
            "Heuristique autonome (Sans IA)"
        ])

        selected_engine = st.selectbox(
            "Choix du fournisseur :",
            options=engine_options,
            index=0,
            help="Selectionnez la passerelle pour la synthese textuelle."
        )

        provider_code = "agy"
        api_key_val = ""
        model_name = None

        if selected_engine == "CLI Antigravity (Local & sans cle)":
            st.success("Connecte a Antigravity CLI (agy)")
            provider_code = "agy"

        elif selected_engine == "Google Gemini (BYOK - Cle gratuite)":
            provider_code = "gemini"
            st.markdown(f"""
            <div class="byok-badge">
                <a href="{KEY_PORTAL_URLS['gemini']}" target="_blank" style="text-decoration: underline; color: #2563EB; font-weight: 600;">
                    Obtenir une cle gratuite sur Google AI Studio
                </a><br>
                <span style="color: #16A34A; font-weight: 500;">Quota gratuit : 15 requetes/min sans CB.</span>
            </div>
            """, unsafe_allow_html=True)

            api_key_val = st.text_input(
                "Cle API Gemini :",
                value=st.session_state.get("gemini_key", os.environ.get("GEMINI_API_KEY", "")),
                type="password",
                placeholder="AIzaSy...",
                help="Votre cle reste stockee dans votre navigateur."
            )
            st.session_state["gemini_key"] = api_key_val

            model_name = st.selectbox(
                "Modele Gemini :",
                options=["gemini-2.5-flash", "gemini-1.5-flash", "gemini-2.5-pro"],
                index=0
            )

        elif selected_engine == "OpenAI (BYOK)":
            provider_code = "openai"
            st.markdown(f"""
            <div class="byok-badge">
                <a href="{KEY_PORTAL_URLS['openai']}" target="_blank" style="text-decoration: underline; color: #2563EB; font-weight: 600;">
                    Generer une cle sur OpenAI Platform
                </a>
            </div>
            """, unsafe_allow_html=True)

            api_key_val = st.text_input(
                "Cle API OpenAI :",
                value=st.session_state.get("openai_key", os.environ.get("OPENAI_API_KEY", "")),
                type="password",
                placeholder="sk-...",
            )
            st.session_state["openai_key"] = api_key_val

            model_name = st.selectbox(
                "Modele OpenAI :",
                options=["gpt-4o-mini", "gpt-4o"],
                index=0
            )

        elif selected_engine == "Mistral AI (BYOK)":
            provider_code = "mistral"
            st.markdown(f"""
            <div class="byok-badge">
                <a href="{KEY_PORTAL_URLS['mistral']}" target="_blank" style="text-decoration: underline; color: #2563EB; font-weight: 600;">
                    Generer une cle sur Mistral Console
                </a>
            </div>
            """, unsafe_allow_html=True)

            api_key_val = st.text_input(
                "Cle API Mistral :",
                value=st.session_state.get("mistral_key", os.environ.get("MISTRAL_API_KEY", "")),
                type="password",
                placeholder="cle mistral...",
            )
            st.session_state["mistral_key"] = api_key_val

            model_name = st.selectbox(
                "Modele Mistral :",
                options=["mistral-small-latest", "open-mistral-nemo"],
                index=0
            )

        elif selected_engine == "Anthropic (BYOK)":
            provider_code = "anthropic"
            st.markdown(f"""
            <div class="byok-badge">
                <a href="{KEY_PORTAL_URLS['anthropic']}" target="_blank" style="text-decoration: underline; color: #2563EB; font-weight: 600;">
                    Generer une cle sur Anthropic Console
                </a>
            </div>
            """, unsafe_allow_html=True)

            api_key_val = st.text_input(
                "Cle API Anthropic :",
                value=st.session_state.get("anthropic_key", os.environ.get("ANTHROPIC_API_KEY", "")),
                type="password",
                placeholder="sk-ant-...",
            )
            st.session_state["anthropic_key"] = api_key_val

            model_name = st.selectbox(
                "Modele Anthropic :",
                options=["claude-3-5-haiku-20241022", "claude-3-5-sonnet-20241022"],
                index=0
            )

        else:
            provider_code = None

        st.header("Reglages de la voix")
        selected_voice_label = st.selectbox(
            "Choix de la voix",
            options=list(VOICES.keys()),
            index=0,
            help="Selectionnez la voix qui vous est la plus agreable."
        )
        voice_id = VOICES[selected_voice_label]

        speed_factor = st.slider(
            "Vitesse de lecture",
            min_value=0.75,
            max_value=2.0,
            value=float(st.session_state.get("current_speed", 1.0)),
            step=0.05,
            format="%.2fx",
            key="user_speed_slider",
            help="Accélérez ou ralentissez la voix en temps reel sans regenerer l'audio."
        )
        st.session_state["current_speed"] = speed_factor

        pause_duration = st.slider(
            "Pause entre les phrases",
            min_value=0.2,
            max_value=2.5,
            value=0.8,
            step=0.1,
            format="%.1fs",
            help="Augmentez le silence entre chaque phrase pour une ecoute plus posee et reposante."
        )

        st.markdown("---")
        st.caption("Application concue pour l'accessibilite visuelle et cognitive.")

    # Zone de televersement du document
    uploaded_file = st.file_uploader(
        "Choisissez votre document (PDF, Word ou Texte)",
        type=["pdf", "docx", "txt", "md"],
        help="Glissez-deposez votre document ici."
    )

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_path = Path(tmp_file.name)

        try:
            with st.spinner("Lecture du document en cours..."):
                raw_text = extract_text_from_file(tmp_path)
        except ExtractionError as exc:
            st.error(f"Impossible de lire ce document: {exc}")
            return
        finally:
            if tmp_path.exists():
                tmp_path.unlink()

        word_count = len(raw_text.split())
        st.markdown(
            f'<div class="doc-success">Document valide : <strong>{uploaded_file.name}</strong> ({word_count} mots detectes)</div>',
            unsafe_allow_html=True
        )

        st.subheader("Choisissez le niveau de detail")
        mode = st.radio(
            "Mode de lecture souhaite:",
            options=[
                ("condense", "Synthese eclair (< 1 minute) : objet, apports et actions cles"),
                ("summary_50", "Resume a mi-longueur (environ 50 % du document)"),
                ("full", "Lecture integrale du texte original")
            ],
            format_func=lambda opt: opt[1],
            index=0
        )[0]

        if st.button("Generer et ecouter", type="primary"):
            # Etape 1: Preparation et condensation du texte
            with st.spinner("Preparation et condensation du texte..."):
                use_ai = provider_code is not None
                if mode == "condense":
                    speech_text = generate_condensed_script(
                        raw_text, 
                        provider=provider_code or "", 
                        api_key=api_key_val, 
                        model=model_name, 
                        use_ai=use_ai
                    )
                elif mode == "summary_50":
                    speech_text = generate_half_summary(
                        raw_text, 
                        provider=provider_code or "", 
                        api_key=api_key_val, 
                        model=model_name, 
                        use_ai=use_ai
                    )
                else:
                    speech_text = raw_text

            st.session_state["speech_text"] = speech_text
            st.session_state["audio_filename"] = f"{Path(uploaded_file.name).stem}_{mode}.mp3"

            # Etape 2: Generation audio avec les pauses inter-phrases configurees
            with st.spinner("Synthese vocale haute fidelite en cours..."):
                output_dir = Path(tempfile.gettempdir()) / "text2speech"
                output_dir.mkdir(parents=True, exist_ok=True)
                audio_file = output_dir / st.session_state["audio_filename"]

                try:
                    synthesize_speech(
                        text=speech_text, 
                        output_path=audio_file, 
                        speed=1.0, 
                        voice=voice_id,
                        pause_seconds=pause_duration
                    )
                    with open(audio_file, "rb") as f:
                        st.session_state["audio_bytes"] = f.read()
                except Exception as exc:
                    st.error(f"Erreur lors de la synthese vocale: {exc}")
                    return

    if st.session_state.get("audio_bytes") is not None:
        st.markdown("### Votre audio est pret")
        
        if st.session_state.get("speech_text"):
            with st.expander("Consulter le texte de la synthese", expanded=True):
                st.markdown(f'<div class="text-preview">{st.session_state["speech_text"]}</div>', unsafe_allow_html=True)

        active_speed = float(st.session_state.get("current_speed", 1.0))
        render_html5_audio_player(
            st.session_state["audio_bytes"], 
            st.session_state["audio_filename"],
            initial_speed=active_speed
        )

        st.download_button(
            label="Telecharger le fichier audio (.mp3)",
            data=st.session_state["audio_bytes"],
            file_name=st.session_state["audio_filename"],
            mime="audio/mp3"
        )


if __name__ == "__main__":
    main()
