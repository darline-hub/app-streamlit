import streamlit as st
import os

# --- Importation des fonctions de page depuis leurs fichiers respectifs ---
# Assurez-vous que ces fichiers existent dans le même répertoire que my_app.py
from login_page import login_page
from signup_page import signup_page
from accueil import page_accueil
from dashboard import dashboard_page
from prediction import page_prediction
from sfm import sfm_page

# --- Fonctions utilitaires (pour CSS et Footer) ---


# --- Fonction principale de l'application ---
def main():
    # Load CSS at the very beginning of the application
    #load_css('style.css')

    # Initialize session state variables if they don't exist
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Connexion" # Default page on startup


    if not st.session_state.logged_in:
        # If the user is not logged in, display login/signup options in the sidebar
        auth_choice_options = ["Connexion", "Inscription"]

        # Use st.sidebar.selectbox instead of st.sidebar.radio
        selected_auth_page = st.sidebar.selectbox(
            "Choisissez une page ", # Empty label for the selectbox
            auth_choice_options,
            key="auth_choice_selectbox", # Unique key for this widget
            index=auth_choice_options.index(st.session_state.current_page) if st.session_state.current_page in auth_choice_options else 0
        )

        # Update the current page if the selection changes
        if selected_auth_page != st.session_state.current_page:
            st.session_state.current_page = selected_auth_page
            st.rerun() # Rerun to display the new page

        # Display the content of the selected page (Login or Signup)
        if st.session_state.current_page == "Connexion":
            login_page() # Call the login page function
        elif st.session_state.current_page == "Inscription":
            signup_page() # Call the signup page function

    else:
        # If the user is logged in, display username and navigation options
        st.sidebar.write(f"Connecté en tant que : **{st.session_state.username}**")

        # Logout button in the sidebar
        if st.sidebar.button("Déconnexion"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.current_page = "Connexion" # Redirect to login page
            st.rerun() # Rerun to update the interface

        # Main page selection in the sidebar
        page_options = ["Accueil", "Tableau de Bord", "Prédiction IA", "SFM Technologies" ]
        
        # Use st.sidebar.selectbox instead of st.sidebar.radio
        selected_main_page = st.sidebar.selectbox(
            "Choisissez une page",
            page_options,
            key="main_page_selectbox", # Unique key for this widget
            index=page_options.index(st.session_state.current_page) if st.session_state.current_page in page_options else 0
        )

        # Update the current page if the selection changes
        if selected_main_page != st.session_state.current_page:
            st.session_state.current_page = selected_main_page
            st.rerun() # Force page rerun

        # Display the content of the selected page
        if st.session_state.current_page == "Accueil":
            page_accueil()
        elif st.session_state.current_page == "Tableau de Bord":
            dashboard_page()
        elif st.session_state.current_page == "Prédiction IA":
            page_prediction()
        elif st.session_state.current_page == "SFM Technologies":
            sfm_page()




# Entry point of the Streamlit application
if __name__ == "__main__":
    main()