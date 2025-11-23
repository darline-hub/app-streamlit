import streamlit as st
from utils.auth_utils import save_users, hash_password, load_users, check_password

def login_page():
    """Affiche le formulaire de connexion."""
    st.title(" 🔑Connexion ")
    st.markdown("Connectez-vous pour accéder à l'application.")

    with st.form("login_form"):
        username = st.text_input("Nom d'utilisateur :")
        password = st.text_input("Mot de passe :", type="password")
        
        submitted = st.form_submit_button("Se connecter")

        if submitted:
            users = load_users()
            if username in users:
                if check_password(password, users[username]["password"]):
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.success(f"Bienvenue, **{username}** ! Connexion réussie.")
                    st.info("Veuillez choisir une page dans le menu latéral.")
                    # Rediriger vers l'application principale après la connexion
                    st.session_state['current_page'] = "Application d'Analyse de Liens par IA"
                    st.rerun()
                else:
                    st.error("Nom d'utilisateur ou mot de passe incorrect.")
            else:
                st.error("Nom d'utilisateur ou mot de passe incorrect.")
    
    st.markdown("---")
    st.markdown("Pas encore de compte ? Rendez-vous sur la page **'Inscription'**.")
