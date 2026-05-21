# Projet-11-Concevez-et-deployez-un-systeme-RAG-
--
# 🤖 POC RAG - Puls-Events (Saison Culturelle Paris 2026)

## 📋 Présentation du Projet
Ce dépôt contient le **Proof of Concept (POC)** d'un assistant conversationnel intelligent (Chatbot) développé pour l'entreprise **Puls-Events**. S'appuyant sur une architecture **RAG (Retrieval-Augmented Generation)**, ce système permet d'interroger en temps réel et de manière pertinente les données d'événements culturels sur le périmètre exclusif de **Paris**.

L'objectif de ce projet est de valoriser un flux de données massif (OpenData issu d'OpenAgenda) en une base de connaissances vectorielle locale performante, garantissant des réponses fiables et précises sans aucune hallucination (dates, lieux, descriptifs).

---

## 🎯 Compétences Validées & Corrections du POC

Ce projet démontre la correction complète des axes d'amélioration identifiés lors de la première phase d'évaluation :

1. **Architecture RAG Pérenne (Compétence 1) :** Migration complète de l'orchestration vers la syntaxe moderne **LCEL (LangChain Expression Language)** à la place des modules obsolètes.
2. **Nettoyage et Qualité de la Donnée (Compétence 2) :**
   * **Chunking Sémantique :** Intégration du `RecursiveCharacterTextSplitter` (chunks de 1000 caractères, overlap de 100) dans le pipeline de vectorisation pour optimiser la fenêtre de contexte du LLM.
   * **Alignement Temporel :** Traitement algorithmique du dataset pour projeter les événements sur l'année en cours (**2026**), respectant la contrainte métier stricte d'événements de moins d'un an.
   * **Tests Unitaires :** Implémentation d'un pipeline de validation robuste via le framework standard `unittest`.
3. **Sécurité et Industrialisation (Compétence 3) :** Isolation stricte de la clé `MISTRAL_API_KEY` via `python-dotenv`. Le fichier `.env` est exclu du versionnage via le fichier `.gitignore`.

---

## 🛠️ Stack Technique
* **Modèle de Langage (LLM) :** Mistral AI (`open-mistral-7b` via API)
* **Embeddings :** Mistral AI (`mistral-embed`)
* **Base Vectorielle :** FAISS (Facebook AI Similarity Search) pour la recherche sémantique locale par similarité cosinus.
* **Orchestration :** LangChain (LCEL)
* **Parsing de Données :** `pandas` et `ijson` (streaming mémoire adapté aux fichiers volumineux).

---

## 🚀 Instructions de Déploiement

### 1. Initialiser l'environnement virtuel (.venv)
```bash
# Cloner le projet
git clone [ https://github.com/byn2ss/Projet-11-Concevez-et-deployez-un-systeme-RAG-/edit/main/README.md]

# Créer et activer l'environnement
**python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows (PowerShell)**

2. Installer les dépendances
Bash
**pip install -r requirements.txt**
3. Configuration de la Sécurité
Créez un fichier .env à la racine du projet et ajoutez-la clé privée :
**MISTRAL_API_KEY=votre_cle_api_securisee**

Déroulé de la Démonstration Live (Cycle de Vie)
Pour reproduire les résultats du POC et lancer la démo, exécutez les scripts à la racine dans cet ordre exact :

Étape A : Pré-processing et Ingestion
Nettoie les données brutes, applique l'alignement temporel 2026 et met à jour le fichier CSV :

Bash
python pre_processing.py
Étape B : Chunking et Vectorisation
Découpe sémantiquement les textes en fragments et génère l'index vectoriel FAISS local :

Bash
python vectorisation.py
Étape C : Pipeline de Validation (QA)
Exécute la suite de tests unitaires automatiques pour valider la structure, le périmètre géo (Paris) et la fraîcheur des données (Moins d'un an) :

Bash
python tests_unitaires.py
Étape D : Lancement du Chatbot Puls-Events
Démarre l'interface en direct dans le terminal :

Bash
python app.py

📊 Évaluation de la Précision
Conformément aux attentes du responsable technique Jérémy, le fichier jeu_de_test_annote.txt fournit un échantillon de paires Questions / Réponses de référence (Ground Truth). Il permet de mesurer de manière objective la pertinence des réponses générées par Mistral AI par rapport aux données réelles de la base vectorielle.


---
