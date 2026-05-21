import streamlit as st

from login_page import login_page
from signup_page import signup_page
from accueil import page_accueil
from dashboard import dashboard_page
from prediction import page_prediction
from sfm import sfm_page
from analyse import page_analyse_ia

st.set_page_config(
    page_title="Analyse IA des Débits Réseau",
    page_icon="📡",
    layout="wide"
)


def main():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "username" not in st.session_state:
        st.session_state.username = ""

    if "current_page" not in st.session_state:
        st.session_state.current_page = "Connexion"
    

    if not st.session_state.logged_in:
        auth_choice_options = ["Connexion", "Inscription"]

        selected_auth_page = st.sidebar.selectbox(
            "Choisissez une page ", 
            auth_choice_options,
            key="auth_choice_selectbox", 
            index=auth_choice_options.index(st.session_state.current_page) if st.session_state.current_page in auth_choice_options else 0
        )

        if selected_auth_page != st.session_state.current_page:
            st.session_state.current_page = selected_auth_page
            st.rerun() 

        if st.session_state.current_page == "Connexion":
            login_page() 
        elif st.session_state.current_page == "Inscription":
            signup_page() 
    else:
        st.sidebar.write(f"Connecté en tant que : **{st.session_state.username}**")

        if st.sidebar.button("Déconnexion"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.current_page = "Connexion" 
            st.rerun() 

        page_options = ["🏠 Accueil", "📊 Dashboard Réseau", "🤖 Analyse IA & ML", "📈 Prédictions Réseau", "🏢 SFM Technologies"]
        
        selected_main_page = st.sidebar.selectbox(
            "Choisissez une page",
            page_options,
            index=page_options.index(st.session_state.current_page)
            if st.session_state.current_page in page_options
            else 0
        )

        if selected_main_page != st.session_state.current_page:
            st.session_state.current_page = selected_main_page
            st.rerun() 

        if st.session_state.current_page == "🏠 Accueil":
            page_accueil()
        elif st.session_state.current_page == "📊 Dashboard Réseau":
            dashboard_page()
        elif st.session_state.current_page == "🤖 Analyse IA & ML":
            page_analyse_ia()
        elif st.session_state.current_page == "📈 Prédictions Réseau":
            page_prediction()
        elif st.session_state.current_page == "🏢 SFM Technologies":
            sfm_page()


if __name__ == "__main__":
    main()