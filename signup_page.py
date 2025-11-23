import streamlit as st
from utils.auth_utils import save_users, hash_password, load_users, check_password

def signup_page():
    """Affiche le formulaire d'inscription."""
    st.title("📝 Inscription")
    st.markdown("Créez votre compte pour accéder à l'application d'analyse de liens.")

    with st.form("signup_form"):
        new_username = st.text_input("Nom d'utilisateur :")
        new_password = st.text_input("Mot de passe :", type="password")
        confirm_password = st.text_input("Confirmer le mot de passe :", type="password")
        
        submitted = st.form_submit_button("S'inscrire")

        if submitted:
            users = load_users()
            
            if not new_username or not new_password or not confirm_password:
                st.error("Veuillez remplir tous les champs.")
            elif new_username in users:
                st.error("Ce nom d'utilisateur existe déjà. Veuillez en choisir un autre.")
            elif new_password != confirm_password:
                st.error("Les mots de passe ne correspondent pas.")
            else:
                hashed_pw = hash_password(new_password)
                users[new_username] = {"password": hashed_pw}
                save_users(users)
                st.success("Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
                st.info("Veuillez naviguer vers la page **'Connexion'** pour vous connecter.")
                # Rediriger vers la page de connexion après l'inscription réussie
                st.session_state['current_page'] = "Connexion"
                st.rerun()
