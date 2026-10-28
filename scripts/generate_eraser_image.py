import json
import urllib.request
import os

dsl = """
typeface clean
colorMode bold
direction right

Clients [color: blue, icon: user] {
  Web_Browser [icon: globe, label: "Navigateur Web (HTML5 Audio)"]
  Windows_Explorer [icon: monitor, label: "Explorateur Windows (Clic droit)"]
}

Routing [color: purple, icon: cloud] {
  Cloud_Run [icon: google-cloud, label: "Google Cloud Run (Scale-to-zero)"]
  Cloudflare_Tunnel [icon: cloudflare, label: "Tunnel Cloudflare (Port 9001)"]
}

App_Core [color: green, icon: server] {
  Streamlit_UI [icon: streamlit, label: "Interface Streamlit (app.py)"]
  Mini_Player [icon: terminal, label: "Lecteur Tkinter (audio_player.py)"]
  Doc_Extractor [icon: file-text, label: "Extracteur PDF, DOCX, TXT"]
  TTS_Engine [icon: speaker, label: "Moteur TTS + Silences MP3"]
}

AI_Summarizer [color: orange, icon: cpu] {
  Gemini_API [icon: google, label: "Google Gemini (BYOK gratuit)"]
  OpenAI_Mistral [icon: server, label: "OpenAI / Mistral / Anthropic"]
  Antigravity_CLI [icon: terminal, label: "CLI Antigravity (agy local)"]
  Local_Fallback [icon: database, label: "Heuristique TF-IDF (Hors-ligne)"]
}

Edge_TTS [icon: mic, label: "Microsoft Neural Edge-TTS (fr-FR-HenriNeural)"]

Web_Browser > Cloud_Run: Requete HTTPS
Web_Browser > Cloudflare_Tunnel: Requete distante
Windows_Explorer > Mini_Player: Lancement direct

Cloud_Run > Streamlit_UI
Cloudflare_Tunnel > Streamlit_UI

Streamlit_UI > Doc_Extractor: Extraction texte
Mini_Player > Doc_Extractor: Extraction texte

Doc_Extractor > Gemini_API
Doc_Extractor > OpenAI_Mistral
Doc_Extractor > Antigravity_CLI
Doc_Extractor > Local_Fallback

Gemini_API > TTS_Engine: Texte condense
OpenAI_Mistral > TTS_Engine: Texte condense
Antigravity_CLI > TTS_Engine: Texte condense
Local_Fallback > TTS_Engine: Texte nettoye

TTS_Engine > Edge_TTS: Streaming neuronal
Edge_TTS > TTS_Engine: Flux MP3 24kHz

TTS_Engine > Web_Browser: Audio sans latence
TTS_Engine > Mini_Player: Controle clavier
"""

payload = {
    "elements": [{
        "type": "diagram",
        "id": "architecture-text2speech",
        "code": dsl.strip(),
        "diagramType": "cloud-architecture-diagram"
    }],
    "scale": 2,
    "theme": "dark",
    "background": False
}

req = urllib.request.Request(
    "https://app.eraser.io/api/render/elements",
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "X-Skill-Source": "gemini"
    }
)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        img_url = res.get("imageUrl")
        file_url = res.get("createEraserFileUrl")
        print("SUCCESS")
        print("IMAGE_URL:", img_url)
        print("FILE_URL:", file_url)
        
        # Telechargement de l'image en local
        os.makedirs("docs", exist_ok=True)
        img_path = os.path.join("docs", "architecture.png")
        urllib.request.urlretrieve(img_url, img_path)
        print("SAVED_TO:", img_path)
except urllib.error.HTTPError as e:
    print("HTTPError:", e.code, e.read().decode())
