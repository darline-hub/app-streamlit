import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import numpy as np

from streamlit_folium import st_folium


def dashboard_page():

    # =====================================================
    # CONFIGURATION PAGE
    # =====================================================

    st.title(
        "📊 Tableau de Bord Réseau"
    )

    st.markdown("""
    Supervision intelligente des performances réseau 
    à Bonamoussadi grâce à l’Intelligence Artificielle.
    """)

    st.markdown("---")

    # =====================================================
    # CHARGEMENT FICHIER
    # =====================================================

    uploaded_file = st.file_uploader(

        "📂 Charger un Dataset",

        type=["xlsx", "xlsm", "csv"]
    )

    if uploaded_file is None:

        st.info(
            "Veuillez charger un fichier."
        )

        return

    # =====================================================
    # LECTURE DATASET
    # =====================================================

    try:

        # ---------------- CSV ----------------

        if uploaded_file.name.endswith(".csv"):

            df = pd.read_csv(
                uploaded_file
            )

        # ---------------- EXCEL ----------------

        else:

            excel_file = pd.ExcelFile(

                uploaded_file,

                engine="openpyxl"
            )

            sheet_names = excel_file.sheet_names

            selected_sheet = st.sidebar.selectbox(

                "📄 Choisir une feuille Excel",

                sheet_names
            )

            df = pd.read_excel(

                excel_file,

                sheet_name=selected_sheet
            )

    except Exception as e:

        st.error(
            f"Erreur chargement fichier : {e}"
        )

        return

    # =====================================================
    # VÉRIFICATION DATAFRAME
    # =====================================================

    if df is None or df.empty:

        st.warning(
            "Le dataset est vide."
        )

        return

    # =====================================================
    # COLONNES PAR DÉFAUT
    # =====================================================

    default_cols = {

        "throughput": "Avg throughput (ETSI A)",

        "time": "Test start time",

        "latitude": "Test start latitude",

        "longitude": "Test start longitude"
    }

    st.sidebar.header(
        "⚙ Paramètres"
    )

    throughput_col = st.sidebar.selectbox(

        "📡 Colonne Débit",

        options=df.columns,

        index=(
            df.columns.get_loc(
                default_cols["throughput"]
            )

            if default_cols["throughput"] in df.columns

            else 0
        )
    )

    time_col = st.sidebar.selectbox(

        "⏱ Colonne Temps",

        options=df.columns,

        index=(
            df.columns.get_loc(
                default_cols["time"]
            )

            if default_cols["time"] in df.columns

            else 0
        )
    )

    lat_col = st.sidebar.selectbox(

        "🌍 Colonne Latitude",

        options=df.columns,

        index=(
            df.columns.get_loc(
                default_cols["latitude"]
            )

            if default_cols["latitude"] in df.columns

            else 0
        )
    )

    lon_col = st.sidebar.selectbox(

        "🌍 Colonne Longitude",

        options=df.columns,

        index=(
            df.columns.get_loc(
                default_cols["longitude"]
            )

            if default_cols["longitude"] in df.columns

            else 0
        )
    )

    # =====================================================
    # NETTOYAGE DONNÉES
    # =====================================================

    df[throughput_col] = pd.to_numeric(

        df[throughput_col],

        errors="coerce"
    )

    df = df.dropna(

        subset=[
            throughput_col
        ]
    )

    # =====================================================
    # CONVERSION Mbps
    # =====================================================

    df["throughput_mbps"] = (

        df[throughput_col] * 8

    ) / (1024 * 1024)


    # =====================================================
    # APERÇU DATASET
    # =====================================================

    st.header(
        "📋 Aperçu des Données"
    )

    st.dataframe(
        df.head(20)
    )

    st.markdown("---")


    # =====================================================
    # KPI
    # =====================================================

    avg_mbps = df["throughput_mbps"].mean()

    max_mbps = df["throughput_mbps"].max()

    min_mbps = df["throughput_mbps"].min()

    stable_rate = (

        (
            df["throughput_mbps"] >= 2
        ).mean()

    ) * 100

    st.header(
        "📌 Indicateurs Clés"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(

            "📡 Débit Moyen",

            f"{avg_mbps:.2f} Mbps"
        )

    with col2:

        st.metric(

            "🚀 Débit Maximum",

            f"{max_mbps:.2f} Mbps"
        )

    with col3:

        st.metric(

            "📉 Débit Minimum",

            f"{min_mbps:.2f} Mbps"
        )

    with col4:

        st.metric(

            "✅ Réseau Stable",

            f"{stable_rate:.1f}%"
        )

    st.markdown("---")

    # =====================================================
    # COURBE TEMPORELLE
    # =====================================================

    st.header(
        "📈 Évolution du Débit"
    )

    try:

        df[time_col] = pd.to_datetime(

            df[time_col]
        )

        df_sorted = df.sort_values(
            by=time_col
        )

        fig, ax = plt.subplots(
            figsize=(12, 5)
        )

        ax.plot(

            df_sorted[time_col],

            df_sorted["throughput_mbps"]
        )

        ax.set_xlabel(
            "Temps"
        )

        ax.set_ylabel(
            "Débit (Mbps)"
        )

        ax.set_title(
            "Évolution du Débit Réseau"
        )

        st.pyplot(fig)

    except:

        st.warning(
            "Impossible d'afficher "
            "la courbe temporelle."
        )

    st.markdown("---")

    # =====================================================
    # DISTRIBUTION DÉBITS
    # =====================================================

    st.header(
        "📊 Distribution des Débits"
    )

    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    sns.histplot(

        df["throughput_mbps"],

        bins=40,

        kde=True,

        ax=ax
    )

    ax.set_xlabel(
        "Débit (Mbps)"
    )

    ax.set_title(
        "Distribution des Débits"
    )

    st.pyplot(fig)

    st.markdown("---")

    # =====================================================
    # BOXPLOT
    # =====================================================

    st.header(
        "📦 Boxplot des Débits"
    )

    fig, ax = plt.subplots(
        figsize=(10, 3)
    )

    sns.boxplot(

        x=df["throughput_mbps"],

        ax=ax
    )

    ax.set_title(
        "Détection des Valeurs Extrêmes"
    )

    st.pyplot(fig)

    st.markdown("---")

   # =====================================================
    # MATRICE CORRÉLATION
    # =====================================================

    st.header(
        "🔥 Matrice de Corrélation"
    )

    corr_features = [

        "AvgRSRP",

        "AvgRSRQ",

        "SINR",

        "throughput_mbps"
    ]

    # garder seulement colonnes existantes
    corr_features = [

        col for col in corr_features

        if col in df.columns
    ]

    corr_matrix = df[
        corr_features
    ].corr()

    fig, ax = plt.subplots(
        figsize=(7, 5)
    )

    sns.heatmap(

        corr_matrix,

        annot=True,

        cmap="coolwarm",

        fmt=".2f",

        linewidths=0.5,

        ax=ax
    )

    ax.set_title(
        "Corrélation des Paramètres Réseau"
    )

    st.pyplot(fig)
    st.markdown("---")

    # =====================================================
    # CARTE FOLIUM
    # =====================================================

    st.header(
        "🗺 Carte des Performances Réseau"
    )

    try:

        df = df.dropna(

            subset=[
                lat_col,
                lon_col
            ]
        )

        center = [

            df[lat_col].mean(),

            df[lon_col].mean()
        ]

        m = folium.Map(

            location=center,

            zoom_start=13
        )

        for _, row in df.iterrows():

            color = (

                "green"

                if row["throughput_mbps"] >= 2

                else "red"
            )

            folium.CircleMarker(

                location=[

                    row[lat_col],

                    row[lon_col]
                ],

                radius=5,

                color=color,

                fill=True,

                fill_color=color,

                fill_opacity=0.7,

                tooltip=f"""
                Débit :
                {row['throughput_mbps']:.2f} Mbps
                """
            ).add_to(m)

        st_folium(

            m,

            width=1000,

            height=500
        )

    except:

        st.warning(
            "Impossible d'afficher "
            "la carte géographique."
        )

    st.markdown("---")

    # =====================================================
    # QUALITÉ RÉSEAU
    # =====================================================

    st.header(
        "📶 Qualité du Réseau"
    )

    quality_counts = pd.cut(

        df["throughput_mbps"],

        bins=[0, 2, 5, 10, 1000],

        labels=[
            "Faible",
            "Moyen",
            "Bon",
            "Excellent"
        ]

    ).value_counts()

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    ax.pie(

        quality_counts,

        labels=quality_counts.index,

        autopct="%1.1f%%"
    )

    ax.set_title(
        "Répartition Qualité Réseau"
    )

    st.pyplot(fig)

    st.markdown("---")

    # =====================================================
    # CONCLUSION
    # =====================================================

    st.header(
        "🧠 Conclusion Dashboard"
    )

    st.success(f"""
    ✔ Débit moyen observé :
    {avg_mbps:.2f} Mbps

    ✔ Taux de stabilité réseau :
    {stable_rate:.1f}%

    ✔ Les données réseau montrent des variations 
    importantes selon les zones et périodes.

    ✔ Le Dashboard permet une supervision 
    intelligente des performances réseau.
    """)