# Demo Hardcoded Secret

Petite application Flask **volontairement vulnérable**, utilisée pour
démontrer le pipeline DevSecOps de bout en bout :

GitHub Actions -> DefectDojo -> security-console -> Jira -> résolution.

## La vulnérabilité (volontaire)

Dans `app.py`, deux secrets sont **codés en dur** dans le code source :

- `app.secret_key` (clé de session Flask, faux token Stripe)
- `API_TOKEN` (faux GitHub Personal Access Token)

C'est une mauvaise pratique classique (secrets exposés dans le code
versionné). Le job **Trivy Filesystem** du pipeline (scan de secrets) les
détecte et identifie même leur type exact (Stripe Secret Key, GitHub PAT).

> Les tokens présents dans `app.py` sont **factices** : ils ont les vrais
> préfixes (`sk_live_`, `ghp_`) pour être reconnus par les scanners, mais ne
> donnent accès à rien. Aucun vrai secret n'est commité.

## Comportement attendu du pipeline sur ce repo

Le pipeline a **un seul quality gate** qui bloque sur, entre autres, tout
secret détecté. Tant que la faille est présente, le gate affiche :

    ❌ SECURITY QUALITY GATE: FAILED
    🚫 APPLICATION STATUS: NOT READY FOR DEPLOYMENT

C'est **voulu** : ça démontre que le pipeline refuse le déploiement d'un code
contenant un secret. Le run apparaît donc en rouge, c'est normal et c'est le
message de la démo. En parallèle, les findings sont quand même importés dans
DefectDojo (le job import-defectdojo tourne indépendamment du gate).

## Le scénario de démo, étape par étape

1. **Push** du code vulnérable sur master -> le pipeline se déclenche.
2. **Trivy Filesystem** détecte les 2 secrets -> le quality gate passe en
   FAILED (déploiement bloqué).
3. Les findings sont **importés dans DefectDojo** (produit "Demo Hardcoded
   Secret", engagement "Automated Scans", créés automatiquement grâce à
   auto_create_context).
4. La vulnérabilité apparaît dans **security-console**, qui lit l'API
   DefectDojo.
5. Depuis security-console, on **crée un ticket Jira** pour attribuer la
   correction à une équipe.
6. **Correction** : on remplace les secrets par des variables
   d'environnement (voir plus bas), commit + push.
7. Nouveau run : Trivy ne détecte plus de secret -> le quality gate passe en
   **PASSED** (READY FOR DEPLOYMENT), et DefectDojo marque le finding comme
   **Mitigated** (grâce à close_old_findings).
8. security-console reflète la fermeture (statut "Fixed"), et on ferme le
   ticket Jira.

## Comment corriger (étape 6)

Version corrigée de app.py :

    import os
    from flask import Flask, jsonify, request

    app = Flask(__name__)

    # Corrigé : les secrets sont lus depuis l'environnement, plus dans le code.
    app.secret_key = os.environ["APP_SECRET_KEY"]
    API_TOKEN = os.environ["API_TOKEN"]

Fournir les valeurs au runtime, hors du code versionné :

    export APP_SECRET_KEY="une-vraie-cle-generee-aleatoirement"
    export API_TOKEN="un-vrai-token"
    python app.py

En production, ces variables viennent d'un gestionnaire de secrets, jamais du
code source.

## Réutiliser ce pipeline pour un autre projet

Le pipeline est dans .github/workflows/devsecops_pipeline.yml. Pour
l'adapter à un autre projet, éditer **uniquement** le bloc env: en haut du
fichier :

    env:
      IMAGE_REF: mon-image:ci
      DOCKERFILE: Dockerfile
      DD_PRODUCT: "Mon Produit"
      DD_ENGAGEMENT: "Automated Scans"

et, si besoin, les noms de branches sous on:.

## Mise en place

1. Créer un repo GitHub, y copier ces fichiers en respectant l'arborescence
   (.github/workflows/devsecops_pipeline.yml).
2. Dans **Settings > Secrets and variables > Actions** du repo, ajouter les
   secrets DEFECTDOJO_URL et DEFECTDOJO_TOKEN (ce pipeline lit les deux
   depuis les secrets ; contrairement au repo Juice Shop, il n'y a pas de
   fallback d'URL codé en dur, il faut donc bien définir DEFECTDOJO_URL).
3. Pousser sur master : le pipeline se déclenche.

## Note

Ce dépôt est volontairement non sécurisé, à des fins pédagogiques
uniquement. Ne pas déployer en production.
