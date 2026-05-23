import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go


def page_prediction():

    # =====================================================
    # TITRE
    # =====================================================

    st.title(
        "🤖 Prédiction IA des Débits Réseau"
    )

    st.markdown("""
    Cette interface utilise l’Intelligence Artificielle
    pour prédire les performances du réseau mobile.
    """)

    st.markdown("---")

    # =====================================================
    # CHARGEMENT MODÈLES
    # =====================================================

    try:

        reg_model = joblib.load(
            "model/model_regression.joblib"
        )

        clf_model = joblib.load(
            "model/model_classification.joblib"
        )

        scaler = joblib.load(
            "model/scaler.joblib"
        )

    except Exception as e:

        st.error(
            f"Erreur chargement modèles : {e}"
        )

        return

    # =====================================================
    # SIDEBAR
    # =====================================================

    st.sidebar.header(
        "⚙ Paramètres Réseau"
    )

    rsrp = st.sidebar.slider(

        "📶 AvgRSRP",

        -140,

        -50,

        -95
    )

    rsrq = st.sidebar.slider(

        "📡 AvgRSRQ",

        -30,

        -1,

        -10
    )

    sinr = st.sidebar.slider(

        "📡 SINR",

        -10,

        40,

        15
    )

    # =====================================================
    # AFFICHAGE PARAMÈTRES
    # =====================================================

    st.header(
        "📋 Paramètres Sélectionnés"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "RSRP",
            rsrp
        )

    with col2:

        st.metric(
            "RSRQ",
            rsrq
        )

    with col3:

        st.metric(
            "SINR",
            sinr
        )

    st.markdown("---")

    # =====================================================
    # INPUT DATA
    # =====================================================

    FEATURES = [
        "AvgRSRP",
        "AvgRSRQ",
        "SINR"
    ]

    input_data = pd.DataFrame([{

        "AvgRSRP": rsrp,

        "AvgRSRQ": rsrq,

        "SINR": sinr
    }])

    # =====================================================
    # PRÉDICTION
    # =====================================================

    if st.button(
        "🚀 Lancer la Prédiction",
        use_container_width=True
    ):

        try:

            # =============================================
            # SCALING
            # =============================================

            input_scaled = scaler.transform(
                input_data
            )

            # =============================================
            # RÉGRESSION
            # =============================================

            predicted_throughput = reg_model.predict(
                input_scaled
            )[0]

            # éviter valeurs négatives
            predicted_throughput = max(
                predicted_throughput,
                0
            )

            # octets/s -> Mbps
            throughput_mbps = (

                predicted_throughput * 8

            ) / (1024 * 1024)

            # =============================================
            # CLASSIFICATION
            # =============================================

            predicted_class = clf_model.predict(
                input_scaled
            )[0]

            # =============================================
            # PROBABILITÉ
            # =============================================

            if hasattr(
                clf_model,
                "predict_proba"
            ):

                confidence = np.max(

                    clf_model.predict_proba(
                        input_scaled
                    )

                ) * 100

            else:

                confidence = 90

            # =============================================
            # STATUS
            # =============================================

            if predicted_class == 1:

                network_status = "Stable"

                status_color = "success"

            else:

                network_status = "Instable"

                status_color = "error"

            # =============================================
            # AFFICHAGE
            # =============================================

            st.header(
                "📊 Résultats IA"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(

                    "📡 Débit Prédit",

                    f"{throughput_mbps:.2f} Mbps"
                )

            with col2:

                if status_color == "success":

                    st.success(
                        "✅ Réseau Stable"
                    )

                else:

                    st.error(
                        "⚠ Réseau Instable"
                    )

            with col3:

                st.metric(

                    "🎯 Confiance IA",

                    f"{confidence:.1f}%"
                )

            st.markdown("---")

            # =============================================
            # JAUGE
            # =============================================

            st.header(
                "📶 Niveau de Performance"
            )

            gauge_value = min(
                throughput_mbps,
                20
            )

            fig = go.Figure(

                go.Indicator(

                    mode="gauge+number",

                    value=gauge_value,

                    number={
                        "suffix": " Mbps"
                    },

                    gauge={

                        "axis": {
                            "range": [0, 20]
                        },

                        "steps": [

                            {
                                "range": [0, 2],
                                "color": "#ff4b4b"
                            },

                            {
                                "range": [2, 5],
                                "color": "#ffa500"
                            },

                            {
                                "range": [5, 20],
                                "color": "#00cc96"
                            }
                        ]
                    }
                )
            )

            fig.update_layout(
                height=350
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.markdown("---")

            # =============================================
            # ANALYSE IA
            # =============================================

            st.header(
                "🧠 Interprétation IA"
            )

            if throughput_mbps >= 5:

                st.success("""
                ✔ Excellente qualité réseau.
                """)

            elif throughput_mbps >= 2:

                st.info("""
                ✔ Réseau acceptable.
                """)

            else:

                st.error("""
                ⚠ Réseau faible.
                """)

            # =============================================
            # CONSEILS
            # =============================================

            st.header(
                "💡 Recommandations"
            )

            recommendations = []

            if rsrp < -100:

                recommendations.append(
                    "Améliorer la couverture radio."
                )

            if rsrq < -15:

                recommendations.append(
                    "Réduire les interférences réseau."
                )

            if sinr < 10:

                recommendations.append(
                    "Optimiser la qualité du signal."
                )

            if len(recommendations) == 0:

                st.success("""
                ✔ Aucun problème majeur détecté.
                """)

            else:

                for rec in recommendations:

                    st.warning(rec)

        except Exception as e:

            st.error(
                f"Erreur prédiction : {e}"
            )