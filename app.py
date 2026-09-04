"""
Petite application Flask de démonstration pour le pipeline DevSecOps.

VULNÉRABILITÉ VOLONTAIRE (à corriger en direct pendant la démo) :
la clé secrète et le token API sont codés en dur dans le code source.
Semgrep (règles p/owasp-top-ten) détecte ce motif comme un secret
hardcodé. La correction consiste à les lire depuis des variables
d'environnement (voir README).
"""
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# --- VULNÉRABILITÉ : secrets codés en dur -------------------------------
# Ces valeurs ne devraient JAMAIS apparaître dans le code source versionné.
# Elles devraient être lues depuis l'environnement (os.environ).
app.secret_key = "sk_live_51H8x2kL9dQr7vNpM3wYtZbAcEfGhIjKl"
API_TOKEN = "ghp_aB3dEf6HiJk9LmNoPqR2sTuVwX5yZ0123456"
# ------------------------------------------------------------------------


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/data")
def data():
    token = request.headers.get("Authorization", "")
    if token != f"Bearer {API_TOKEN}":
        return jsonify(error="unauthorized"), 401
    return jsonify(message="Voici des données protégées", items=[1, 2, 3])


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
