import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def page_accueil():

    # =========================
    # TITRE PRINCIPAL
    # =========================

    st.markdown(
        """
        # 📡 Analyse IA des Débits Réseau à Bonamoussadi
        
        ### Plateforme intelligente de supervision et de prédiction des performances réseau
        """
    )

    st.markdown("---")

    # =========================
    # IMAGE PRINCIPALE
    # =========================

    st.image(
        "images/mapB.PNG",
        use_container_width=True
    )

    st.markdown("---")

    # =========================
    # KPI PRINCIPAUX
    # =========================

    st.subheader("📊 Aperçu Global du Projet")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="📍 Zone étudiée",
            value="Bonamoussadi"
        )

    with col2:
        st.metric(
            label="🤖 Modèles IA",
            value="3 modèles"
        )

    with col3:
        st.metric(
            label="📡 Type d’analyse",
            value="Téléversement"
        )

    with col4:
        st.metric(
            label="🧠 Technologie",
            value="IA + ML"
        )

    st.markdown("---")

    # =========================
    # PRESENTATION
    # =========================

    st.header("🌍 Présentation du Projet")

    st.markdown(
        """
        Cette application web intelligente a été développée dans le but 
        d’analyser les performances des débits de téléversement dans la zone 
        de Bonamoussadi grâce à des techniques d’Intelligence Artificielle.

        Dans un environnement numérique en constante évolution, 
        la qualité du réseau joue un rôle essentiel dans :
        
        - les appels vidéo,
        - le télétravail,
        - les jeux en ligne,
        - le streaming,
        - le partage de fichiers.

        Grâce au Machine Learning, cette plateforme permet :
        
        ✅ d’analyser les performances réseau  
        ✅ de détecter les anomalies  
        ✅ de visualiser les données réseau  
        ✅ de prédire les tendances futures  
        """
    )

    st.markdown("---")

    # =========================
    # TECHNOLOGIES
    # =========================

    st.header("🛠 Technologies Utilisées")

    tech1, tech2, tech3, tech4 = st.columns(4)

    with tech1:
        st.info("🐍 Python")

    with tech2:
        st.info("🌐 Streamlit")

    with tech3:
        st.info("🤖 Scikit-learn")

    with tech4:
        st.info("📊 Pandas")

    st.markdown("---")

    # =========================
    # APERÇU VISUEL IA
    # =========================

    st.header("📈 Aperçu des Performances Réseau")

    # Génération temporaire de données
    np.random.seed(42)

    data = pd.DataFrame({
        "Débit": np.random.normal(2.5, 0.5, 50)
    })

    st.line_chart(data)

    st.markdown(
        """
        Ce graphique représente une simulation des variations des débits 
        réseau observées dans la zone étudiée.
        """
    )

    st.markdown("---")

    # =========================
    # OBJECTIFS
    # =========================

    st.header("🎯 Objectifs de l’Application")

    obj1, obj2 = st.columns(2)

    with obj1:

        st.success(
            """
            ### Analyse Réseau
            
            - Surveillance des performances
            - Analyse des débits
            - Étude des variations réseau
            """
        )

    with obj2:

        st.success(
            """
            ### Intelligence Artificielle
            
            - Détection des anomalies
            - Prédiction des performances
            - Comparaison des modèles IA
            """
        )

    st.markdown("---")

    # =========================
    # FONCTIONNALITÉS
    # =========================

    st.header("🚀 Fonctionnalités Principales")

    feat1, feat2, feat3 = st.columns(3)

    with feat1:

        st.warning(
            """
            ### 📊 Dashboard
            
            Visualisation dynamique des données réseau.
            """
        )

    with feat2:

        st.warning(
            """
            ### 🤖 IA
            
            Modèles de Machine Learning pour l’analyse réseau.
            """
        )

    with feat3:

        st.warning(
            """
            ### 📍 Cartographie
            
            Localisation géographique des performances réseau.
            """
        )

    st.markdown("---")

    # =========================
    # SECTION IA
    # =========================

    st.header("🧠 Intelligence Artificielle")

    st.markdown(
        """
        L’application utilise plusieurs algorithmes de Machine Learning afin de :

        - prédire les performances réseau,
        - comparer les modèles IA,
        - identifier les anomalies,
        - améliorer l’analyse des débits de téléversement.

        Les modèles utilisés incluent :
        
        - Régression Linéaire
        - Random Forest
        - Gradient Boosting
        - Régression Logistique
        """
    )

    st.markdown("---")

    # =========================
    # BOUTONS DE NAVIGATION
    # =========================

    st.subheader("🚀 Commencer l’Analyse")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "📊 Accéder au Dashboard",
            use_container_width=True
        ):

            st.session_state.current_page = "📊 Dashboard Réseau"

            st.rerun()

    with col2:

        if st.button(
            "🤖 Lancer une Prédiction IA",
            use_container_width=True
        ):

            st.session_state.current_page = "📈 Prédictions Réseau"

            st.rerun()

    st.markdown("---")

    # =========================
    # FOOTER
    # =========================

    st.caption(
        "Application développée dans le cadre d’un projet "
        "d’initiation à l’Intelligence Artificielle appliquée "
        "à l’analyse des performances réseau."
    )