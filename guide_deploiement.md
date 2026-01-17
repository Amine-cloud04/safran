# Guide de Déploiement Safran RH

## Déploiement sur Streamlit Cloud

1. Créer un compte Streamlit Cloud
2. Connecter le repository GitHub
3. Configurer les secrets (API_URL)
4. Déployer l'application

## Déploiement Backend

### Option 1: Heroku
```
heroku create safran-rh-api
git push heroku main
```

### Option 2: Docker
```
docker build -t safran-rh .
docker run -p 8000:8000 safran-rh
```

## Variables d'Environnement

- API_URL: URL du backend FastAPI
- LOG_LEVEL: DEBUG, INFO, WARNING, ERROR
