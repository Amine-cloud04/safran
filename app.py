import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime
import os

st.set_page_config(page_title="Safran RH & Formation", layout="wide", initial_sidebar_state="expanded")

API_URL = os.getenv("API_URL", "http://localhost:8000")

if "user_token" not in st.session_state:
    st.session_state.user_token = None
if "user_profile" not in st.session_state:
    st.session_state.user_profile = "CDI"
if "user_language" not in st.session_state:
    st.session_state.user_language = "fr"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def login_page():
    st.title("🔐 Connexion - Safran RH")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("---")
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        
        if st.button("Se connecter", use_container_width=True):
            try:
                response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.user_token = data["token"]
                    st.session_state.user_profile = data["profile"]
                    st.success("Connexion réussie!")
                    st.rerun()
                else:
                    st.error("Identifiants invalides")
            except Exception as e:
                st.error(f"Erreur de connexion: {e}")
        
        st.markdown("---")
        st.info("Identifiants de test:\nUtilisateur: user1\nMot de passe: password123\n\nAdmin: admin\nMot de passe: admin123")

def chatbot_page():
    st.title("💬 Assistant RH Safran")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.user_profile = st.selectbox("Votre profil", ["CDI", "CDD", "Intérim", "Stagiaire", "Apprenti"])
    with col2:
        st.session_state.user_language = st.selectbox("Langue", ["fr", "ar"])
    
    st.markdown("---")
    
    question = st.text_input("Posez votre question RH:")
    
    if st.button("Envoyer"):
        if question:
            try:
                response = requests.post(f"{API_URL}/ask", json={
                    "question": question,
                    "profile": st.session_state.user_profile,
                    "language": st.session_state.user_language
                })
                
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.chat_history.append({
                        "question": question,
                        "response": result["response"],
                        "confidence": result["confidence"],
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })
                    st.success("Réponse reçue!")
                else:
                    st.error("Erreur lors de la requête")
            except Exception as e:
                st.error(f"Erreur: {e}")
    
    st.markdown("---")
    st.subheader("Historique de conversation")
    
    for item in reversed(st.session_state.chat_history):
        with st.container():
            st.markdown(f"**[{item['timestamp']}] Vous:** {item['question']}")
            st.markdown(f"**Assistant:** {item['response']}")
            st.caption(f"Confiance: {item['confidence']:.2%}")
            st.divider()

def evaluations_page():
    st.title("📊 Analyse des Évaluations de Formation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader("Charger un fichier d'évaluations", type=["csv", "xlsx"])
        
        if uploaded_file:
            if uploaded_file.type == "text/csv":
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.write("Aperçu des données:")
            st.dataframe(df.head())
            
            if st.button("Analyser"):
                try:
                    file_path = f"data/{uploaded_file.name}"
                    df.to_csv(file_path, index=False)
                    
                    response = requests.post(f"{API_URL}/evaluate", json={"file_path": file_path})
                    
                    if response.status_code == 200:
                        report = response.json()
                        st.success("Analyse complétée!")
                        
                        st.subheader("Résultats Quantitatifs")
                        if "quantitative" in report:
                            st.json(report["quantitative"])
                        
                        st.subheader("Analyse de Sentiment")
                        if "sentiment" in report:
                            st.json(report["sentiment"])
                        
                        st.subheader("Thèmes Identifiés")
                        if "themes" in report:
                            st.json(report["themes"])
                        
                        st.subheader("Signaux Faibles")
                        if "weak_signals" in report and report["weak_signals"]:
                            for signal in report["weak_signals"][:5]:
                                st.warning(f"⚠️ {signal['text']}")
                    else:
                        st.error("Erreur lors de l'analyse")
                except Exception as e:
                    st.error(f"Erreur: {e}")
    
    with col2:
        st.info("📋 Format attendu:\n- Colonnes numériques (1-5)\n- Colonnes texte pour commentaires\n- Format CSV ou Excel")
        
        if st.button("Charger exemple"):
            try:
                df = pd.read_csv("data/evaluations.csv")
                st.write("Données d'exemple chargées:")
                st.dataframe(df)
            except:
                st.error("Fichier d'exemple non trouvé")

def dashboard_page():
    st.title("📈 Tableau de Bord KPI")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Questions Chatbot", "0", "+0")
    with col2:
        st.metric("Évaluations Traitées", "0", "+0")
    with col3:
        st.metric("Utilisateurs Actifs", "0", "+0")
    with col4:
        st.metric("Temps Réponse Moyen", "0.5s", "-0.1s")
    
    st.markdown("---")
    
    st.subheader("Graphiques KPI")
    st.info("Les graphiques KPI seront affichés ici")

def main():
    if not st.session_state.user_token:
        login_page()
    else:
        st.sidebar.title("🏢 Safran RH")
        st.sidebar.markdown(f"**Utilisateur:** {st.session_state.user_profile}")
        
        page = st.sidebar.radio("Navigation", ["Chatbot RH", "Évaluations", "Tableau de Bord"])
        
        if st.sidebar.button("Se déconnecter"):
            st.session_state.user_token = None
            st.session_state.chat_history = []
            st.rerun()
        
        st.sidebar.markdown("---")
        st.sidebar.info("Assistant RH Safran v1.0")
        
        if page == "Chatbot RH":
            chatbot_page()
        elif page == "Évaluations":
            evaluations_page()
        elif page == "Tableau de Bord":
            dashboard_page()

if __name__ == "__main__":
    main()
