FROM python:3.12-slim

# Met à jour pip + les paquets système Python vulnérables de l'image de base
# (setuptools CVE-2025-47273, msgpack GHSA-6v7p-g79w-8964)
RUN pip install --no-cache-dir --upgrade "pip" "setuptools>=78.1.1" "msgpack>=1.2.1"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Utilisateur non-root (corrige missing-user / DS-0002)
RUN useradd --create-home --uid 10001 appuser
USER appuser

EXPOSE 5000
CMD ["python", "app.py"]
