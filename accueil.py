import streamlit as st
import folium 
from streamlit_folium import st_folium

def page_accueil():
    

    st.title("Analyse des Débits de Téléversement à Bonamoussadi")
    st.markdown("### Votre partenaire pour une connectivité optimisée à Bonamoussadi.")    

    st.image("images/mapB.PNG", caption="Optimiser la connectivité à Bonamoussadi", width=650) # Image d'accroche

    st.markdown("""
        Bienvenue sur l'application dédiée à l'analyse et à l'optimisation des débits de téléversement
        dans la zone de Bonamoussadi. Dans un environnement numérique en constante évolution,
        une connexion internet fiable est essentielle. Notre plateforme utilise l'Intelligence Artificielle
        pour vous offrir une vision claire de la performance du réseau.
    """)

    st.header("Pourquoi cette application ?")
    st.markdown("""
        Les débits de téléversement sont cruciaux pour les appels vidéo, le partage de fichiers,
        et bien d'autres activités en ligne. Nous vous aidons à :
        * **Comprendre** les variations de débit au fil du temps.
        * **Identifier** les zones et les périodes de faible performance.
        * **Prédire** les tendances futures grâce à l'IA.
    """)

    st.header("Nos Fonctionnalités Clés")
    st.markdown("""
        Découvrez comment notre application transforme les données brutes en informations exploitables :
        * **Tableaux de bord interactifs :** Visualisez les débits moyens, les pics et les creux.
        * **Détection d'anomalies :** Soyez alerté des baisses de performance inattendues.
        * **Prédictions intelligentes :** Anticipez les futurs débits pour une meilleure planification.
    """)

    st.markdown("---") # Ligne de séparation

    st.subheader("Prêt à explorer les débits de Bonamoussadi ?")
    if st.button("Voir le Tableau de Bord"):
        st.session_state.current_page = "Tableau de Bord"
        st.rerun()

    if st.button("Obtenir une Prédiction IA"):
        st.session_state.current_page = "Prédiction IA"
        st.rerun()

    
    