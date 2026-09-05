FROM python:3.12-slim

# Met à jour pip pour corriger les CVE du pip embarqué dans l'image de base
RUN pip install --no-cache-dir --upgrade pip

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Crée un utilisateur non-root et l'utilise (corrige missing-user / DS-0002)
RUN useradd --create-home --uid 10001 appuser
USER appuser

EXPOSE 5000
CMD ["python", "app.py"]
