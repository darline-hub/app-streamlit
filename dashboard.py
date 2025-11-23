import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
import numpy as np

def dashboard_page():
    st.title("Tableau de Bord : Analyse des Débits Réseau")
    st.markdown("### Visualisation des performances du réseau en temps réel.")

    #téléchargement de fichier
    uploaded_file = st.file_uploader("Choisissez un fichier EXCEL ou CSV", type=["xlsx", "csv", "xlsm"])
    
    if uploaded_file is not None:
        try:
            # Déterminer le type de fichier et le lire
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, sep=";", on_bad_lines='skip')
                sheets = [None] # Il n'y a pas de feuille pour les fichiers CSV
            elif uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xlsm'):
                # Lecture pour obtenir les noms des feuilles de calcul
                xls = pd.ExcelFile(uploaded_file)
                sheets = xls.sheet_names
                
                # Permettre à l'utilisateur de choisir la feuille
                sheet_name = st.sidebar.selectbox("Sélectionnez la feuille de calcul :", sheets)
                
                # Lire les données de la feuille sélectionnée
                df = pd.read_excel(uploaded_file, sheet_name=sheet_name, engine='openpyxl')
            
            else:
                st.error("Format de fichier non pris en charge. Veuillez télécharger un fichier CSV ou Excel.")
                return

        except Exception as e:
            st.error(f"Erreur lors du chargement ou de la lecture du fichier. Assurez-vous que le nom de la feuille de calcul est correct ou que les données sont bien formatées. Détails : {e}")
            return

        st.success("Fichier chargé avec succès ! Voici un aperçu des données :")
        st.dataframe(df.head())


        # Définir les colonnes par défaut 
        default_cols = {
            'throughput': 'Avg throughput (ETSI A)',
            'time': 'Test start time',
            'latitude': 'Test start latitude',
            'longitude': 'Test start longitude'
        }
        
        # Permettre à l'utilisateur de sélectionner les colonnes pertinentes
        st.sidebar.header("Paramètres des Données")
        throughput_col = st.sidebar.selectbox("Sélectionnez la colonne de débit :", options=df.columns, index=df.columns.get_loc(default_cols['throughput']) if default_cols['throughput'] in df.columns else 0)
        time_col = st.sidebar.selectbox("Sélectionnez la colonne de temps :", options=df.columns, index=df.columns.get_loc(default_cols['time']) if default_cols['time'] in df.columns else 0)
        lat_col = st.sidebar.selectbox("Sélectionnez la colonne de latitude :", options=df.columns, index=df.columns.get_loc(default_cols['latitude']) if default_cols['latitude'] in df.columns else 0)
        lon_col = st.sidebar.selectbox("Sélectionnez la colonne de longitude :", options=df.columns, index=df.columns.get_loc(default_cols['longitude']) if default_cols['longitude'] in df.columns else 0)
        
        # Assurer que les colonnes sont bien présentes
        if not all(col in df.columns for col in [throughput_col, time_col, lat_col, lon_col]):
            st.warning("Veuillez sélectionner des colonnes valides pour l'analyse.")
            return

        df[throughput_col] = pd.to_numeric(df[throughput_col], errors='coerce')
        df = df.dropna(subset=[throughput_col, lat_col, lon_col])

        st.header("1. Statistiques Clés")
        avg_throughput = df[throughput_col].mean()
        max_throughput = df[throughput_col].max()
        min_throughput = df[throughput_col].min()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Débit Moyen", f"{avg_throughput:.2f} B/s")
        with col2:
            st.metric("Débit Maximum", f"{max_throughput:.2f} B/s")
        with col3:
            st.metric("Débit Minimum", f"{min_throughput:.2f} B/s")

        st.markdown("---")

        st.header("2. Débit au fil du temps")
        df[time_col] = pd.to_datetime(df[time_col])
        df_time = df.set_index(time_col)
        st.line_chart(df_time[throughput_col])
        
        st.markdown("---")

        st.header("3. Carte Géographique des Performances")
        center = [df[lat_col].mean(), df[lon_col].mean()]
        m = folium.Map(location=center, zoom_start=13)
        
        for _, row in df.iterrows():
            color = 'blue' if row[throughput_col] >= 256000 else 'red'
            folium.CircleMarker(
                location=[row[lat_col], row[lon_col]],
                radius=5,
                color=color,
                fill=True,
                fill_color=color,
                tooltip=f"Débit : {row[throughput_col]:.2f} B/s"
            ).add_to(m)
        st_folium(m)

    else:
        st.info("Veuillez télécharger un fichier excel pour afficher le tableau de bord.")