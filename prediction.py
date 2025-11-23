import streamlit as st
import pandas as pd
import joblib
def page_prediction():
    # --- 1. Chargement du modèle ---
    # Le nom du fichier doit correspondre au nom sous lequel vous avez sauvegardé votre modèle
    MODEL_FILE = 'model/model.joblib'
    try:
        model = joblib.load(MODEL_FILE)
    except FileNotFoundError:
        st.error(f"Erreur : Le fichier du modèle '{MODEL_FILE}' n'a pas été trouvé. Veuillez vérifier qu'il est dans le même dossier que 'app.py'.")
        st.stop()

    # --- 2. Configuration de l'interface utilisateur ---
    st.set_page_config(page_title="Prédiction de Qualité de Service Réseau", layout="wide")
    st.title("Qualité du Réseau Mobile : Prédiction de Succès/Échec")
    st.markdown("Cette application prédit si le débit de téléversement sera supérieur à 2 Mbps (Succès) ou non (Échec) en se basant sur les paramètres radiofréquence.")

    # Créer des champs de saisie pour les caractéristiques du modèle
    st.header("Entrez les paramètres radiofréquence :")

    col1, col2 = st.columns(2)

    with col1:
        thr = st.number_input("Avg throughput (ETSI A)", value=130, help="Debit (throughput)")
        rsrp = st.number_input("AvgRSRP", value=-90, help="Puissance du signal (RSRP)")

    with col2:
        rsrq = st.number_input("AvgRSRQ", value=-10, help="Qualité du signal (RSRQ)")
        sinr = st.number_input("SINR", value=25, help="Rapport Signal/Bruit (SINR)")

    # --- 3. Exécuter la prédiction ---
    if st.button("Prédire le résultat"):
        # Créer un DataFrame avec les données de l'utilisateur
        input_data = pd.DataFrame([[thr, rsrp, rsrq, sinr]], 
                                columns=['Avg throughput (ETSI A)', 'AvgRSRP', 
                                        'AvgRSRQ', 'SINR'])
        
        # Faire la prédiction
        prediction = model.predict(input_data)
        
        st.divider()
        st.subheader("Résultat de la prédiction :")
        
        # Afficher le résultat
        if prediction[0] == 1:
            st.success("✅ **Succès !** Le modèle prédit que le débit sera supérieur à 2 Mbps.")
            st.balloons()
        else:
            st.error("❌ **Échec !** Le modèle prédit que le débit sera inférieur à 2 Mbps.")