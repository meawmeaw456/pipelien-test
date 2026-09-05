"""
Petite application Flask de démonstration pour le pipeline DevSecOps.
Version corrigée : les secrets sont lus depuis l'environnement.
"""
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

app.secret_key = os.environ.get("APP_SECRET_KEY", "")
API_TOKEN = "ghp_aB3dEf6HiJk9LmNoPqR2sTuVwX5yZ0123456"


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/data")
def data():
    token = request.headers.get("Authorization", "")
    if token != f"Bearer {API_TOKEN}":
        return jsonify(error="unauthorized"), 401
    return jsonify(message="Voici des donnees protegees", items=[1, 2, 3])


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
