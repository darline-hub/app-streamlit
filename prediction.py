import streamlit as st
import pandas as pd
import joblib
import numpy as np

#Définition des noms de fichiers de modèle
MODEL_CLASSIFICATION_FILE = 'model/model.joblib'
MODEL_REGRESSION_FILE = 'model/model_regression.joblib'
SEUIL_DEBIT = 256000 # Le seuil de 2 Mbps utilisé pour la classification

def page_prediction():
    #Chargement des Modèles
    
    # Tentative de chargement du modèle de Classification
    model_classification = None
    try:
        model_classification = joblib.load(MODEL_CLASSIFICATION_FILE)
    except FileNotFoundError:
        st.error(f"Erreur: Le modèle de Classification '{MODEL_CLASSIFICATION_FILE}' est manquant.")
        
    # Tentative de chargement du modèle de Régression
    model_regression = None
    try:
        model_regression = joblib.load(MODEL_REGRESSION_FILE)
    except FileNotFoundError:
        st.error(f"Erreur: Le modèle de Régression '{MODEL_REGRESSION_FILE}' est manquant.")

    # Arrêter si aucun modèle n'est chargé
    if model_classification is None and model_regression is None:
        return # Quitter la fonction si aucun modèle n'est disponible

    #Configuration de l'interface utilisateur
    st.set_page_config(page_title="Prédiction de Qualité de Service Réseau", layout="wide")
    st.title("Qualité du Réseau Mobile : Prédiction par IA")
    st.markdown("Cette application permet de prédire soit le **Succès/Échec** de la connexion (Classification), soit la valeur exacte du **Débit** (Régression).")

    #Sélection du type de modèle par l'utilisateur
    model_options = {}
    if model_classification is not None:
        model_options['Classification (Succès/Échec)'] = model_classification
    if model_regression is not None:
        model_options['Régression (Débit exact)'] = model_regression

    if not model_options:
        st.error("Aucun modèle utilisable n'a pu être chargé.")
        return

    selected_model_type = st.radio(
        "Choisissez le type de prédiction :", 
        list(model_options.keys())
    )
    
    current_model = model_options[selected_model_type]
    
    # Créer des champs de saisie pour les caractéristiques du modèle
    st.header("Entrez les paramètres radiofréquence :")

    col1, col2 = st.columns(2)

    with col1:
        # Note: 'Avg throughput (ETSI A)' est une CARACTÉRISTIQUE dans le modèle de CLASSIFICATION
        # mais la CIBLE dans le modèle de RÉGRESSION. Pour la prédiction de régression, on ne l'utilise pas.
        # Pour simplifier l'interface, nous allons l'omettre des entrées utilisateur pour les deux modèles
        # et n'utiliser que les paramètres radiofréquence comme dans le code original: 
        # rsrp, rsrq, sinr
        rsrp = st.number_input("AvgRSRP (Puissance du signal)", value=-90, help="Puissance du signal (RSRP)")

    with col2:
        rsrq = st.number_input("AvgRSRQ (Qualité du signal)", value=-10, help="Qualité du signal (RSRQ)")
        sinr = st.number_input("SINR (Rapport Signal/Bruit)", value=25, help="Rapport Signal/Bruit (SINR)")

    #Exécuter la prédiction
    if st.button("Prédire le résultat"):
        # Créer un DataFrame avec les données de l'utilisateur. 
        # Assurez-vous que l'ordre des colonnes correspond à celui du modèle entraîné
        input_data = pd.DataFrame([[rsrp, rsrq, sinr]], 
                                columns=['AvgRSRP', 'AvgRSRQ', 'SINR']) 
        # NOTE: Si votre modèle entraîné a d'autres colonnes comme 'Avg throughput (ETSI A)' dans X, 
        # vous devrez l'inclure ici avec une valeur fictive pour que l'ordre et le nombre de features correspondent.

        st.divider()
        st.subheader("Résultat de la prédiction :")
        
        # Faire la prédiction
        prediction = current_model.predict(input_data)
        
        if selected_model_type.startswith('Classification'):
            #Affichage pour la Classification
            if prediction[0] == 1:
                st.success(f"✅ Succès : La connexion est prédite comme étant **Supérieure à {SEUIL_DEBIT / 1000} KB/s**.")
            else:
                st.error(f"❌ Échec : La connexion est prédite comme étant **Inférieure à {SEUIL_DEBIT / 1000} KB/s**.")
                
        elif selected_model_type.startswith('Régression'):
            # Affichage pour la Régression
            predicted_throughput = prediction[0]
            
            # Affichage formaté pour la lisibilité
            st.info(f"Le débit moyen prédit est de **{predicted_throughput:,.2f}** octets/s.")
            
            # Interprétation visuelle
            if predicted_throughput >= SEUIL_DEBIT:
                st.success(f"Cela correspond à un **Succès** (Débit supérieur à {SEUIL_DEBIT/1000} KB/s).")
            else:
                st.warning(f"Cela correspond à un **Échec** (Débit inférieur à {SEUIL_DEBIT/1000} KB/s).")