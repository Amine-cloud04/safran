# Documentation Technique Safran RH

## Architecture

### Frontend (Streamlit)
- Interface utilisateur interactive
- Gestion des sessions utilisateur
- Historique de conversation
- Upload et analyse de fichiers

### Backend (FastAPI)
- API RESTful
- Authentification par token
- Traitement NLP
- Logging et monitoring

### Modules

#### chatbot_backend.py
- Classe ChatbotBackend
- Embeddings avec sentence-transformers
- Index FAISS pour recherche rapide
- Détection de questions interdites

#### evaluations.py
- Classe EvaluationAnalyzer
- Analyse quantitative
- Analyse de sentiment
- Extraction de thèmes
- Clustering

#### auth.py
- Authentification utilisateur
- Gestion des sessions
- Hachage de mots de passe

#### monitoring.py
- Logging des interactions
- Calcul des KPI
- Export des métriques

## Base de Connaissances

Structure hiérarchique:
- Intents (salutations, congés, etc.)
- Keywords (mots-clés de déclenchement)
- Responses (réponses adaptées aux profils)
- Confidence (score de confiance)

## Sécurité

- Authentification par token
- Détection des questions sensibles
- Logging sécurisé
- Anonymisation des données
