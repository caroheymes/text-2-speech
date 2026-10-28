FROM python:3.12-slim

LABEL maintainer="Henri"
LABEL description="Text2Speech - Lecteur vocal accessible deploye sur Cloud Run"

# Variables d'environnement standard Cloud Run et Streamlit
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080 \
    STREAMLIT_SERVER_PORT=8080 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /app

# Installation de curl pour le test de sante
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copie des dependances et installation
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie de l'application et de la configuration
COPY src/ ./src/
COPY .streamlit/ ./.streamlit/

# Utilisateur non-root pour les contraintes de securite Cloud Run
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT}/_stcore/health || exit 1

# Demarrage dynamique avec liaison au port injecte par Cloud Run
CMD ["sh", "-c", "streamlit run src/app.py --server.port=${PORT} --server.address=0.0.0.0"]
