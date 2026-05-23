import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.model_selection import (train_test_split)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (StandardScaler)
from sklearn.linear_model import (LinearRegression,LogisticRegression)
from sklearn.ensemble import (RandomForestRegressor,GradientBoostingRegressor,RandomForestClassifier,GradientBoostingClassifier)
from sklearn.metrics import (mean_squared_error,r2_score,accuracy_score,f1_score,confusion_matrix,ConfusionMatrixDisplay)


def page_analyse_ia():

    # TITRE
    st.title("🤖 Analyse des Modèles d'Intelligence Artificielle")
    st.markdown("""Cette section présente une analyse complète des modèles de Machine Learning utilisés pour prédire les performances du réseau mobile à Bonamoussadi.""")
    st.markdown("---")

    # UPLOAD DATASET
    uploaded_file = st.file_uploader("📂 Charger un Dataset", type=["xlsx", "xlsm", "csv"])
    if uploaded_file is None:
        st.info("Veuillez charger un dataset.")
        return

    # LECTURE DATASET
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            excel_file = pd.ExcelFile(uploaded_file, engine="openpyxl")
            sheet_names = excel_file.sheet_names
            selected_sheet = st.sidebar.selectbox("📄 Choisir une feuille Excel",sheet_names)
            df = pd.read_excel(excel_file,sheet_name=selected_sheet)
    except Exception as e:
        st.error(f"Erreur chargement fichier : {e}")
        return

    # PARAMÈTRES

    FEATURES = [

        "AvgRSRP",

        "AvgRSRQ",

        "SINR"
    ]

    TARGET_REG = "Avg throughput (ETSI A)"

    SEUIL_DEBIT = 256000

    # =====================================================
    # NETTOYAGE
    # =====================================================

    df[TARGET_REG] = pd.to_numeric(

        df[TARGET_REG],

        errors="coerce"
    )

    df["debit_class"] = df[TARGET_REG].apply(

        lambda x:
        1 if x >= SEUIL_DEBIT else 0
    )

    df_model = df[
        FEATURES + [TARGET_REG, "debit_class"]
    ].dropna()

    # =====================================================
    # APERÇU DATASET
    # =====================================================

    st.success(
        "Dataset chargé avec succès ✅"
    )

    st.header("📋 Aperçu du Dataset")

    st.dataframe(
        df_model.head(20)
    )

    st.markdown("---")

    # =====================================================
    # MATRICE X ET y
    # =====================================================

    X = df_model[FEATURES]

    y_reg = df_model[TARGET_REG]

    y_clf = df_model["debit_class"]

    # =====================================================
    # TRAIN TEST SPLIT
    # =====================================================

    X_train, X_test, y_reg_train, y_reg_test = train_test_split(

        X,

        y_reg,

        test_size=0.2,

        random_state=42
    )

    _, _, y_clf_train, y_clf_test = train_test_split(

        X,

        y_clf,

        test_size=0.2,

        random_state=42
    )

    # =====================================================
    # MODÈLES RÉGRESSION
    # =====================================================

    reg_models = {

        "Linear Regression": Pipeline([

            ("scaler", StandardScaler()),

            ("model", LinearRegression())
        ]),

        "Random Forest": Pipeline([

            ("model", RandomForestRegressor(

                n_estimators=200,

                random_state=42
            ))
        ]),

        "Gradient Boosting": Pipeline([

            ("model", GradientBoostingRegressor(

                random_state=42
            ))
        ])
    }

    # =====================================================
    # MODÈLES CLASSIFICATION
    # =====================================================

    clf_models = {

        "Logistic Regression": Pipeline([

            ("scaler", StandardScaler()),

            ("model", LogisticRegression(

                max_iter=1000
            ))
        ]),

        "Random Forest": Pipeline([

            ("model", RandomForestClassifier(

                n_estimators=200,

                random_state=42
            ))
        ]),

        "Gradient Boosting": Pipeline([

            ("model", GradientBoostingClassifier(

                random_state=42
            ))
        ])
    }

    # =====================================================
    # ENTRAÎNEMENT RÉGRESSION
    # =====================================================

    reg_results = []

    best_reg_model = None

    best_r2 = -999

    for name, model in reg_models.items():

        model.fit(
            X_train,
            y_reg_train
        )

        preds = model.predict(
            X_test
        )

        rmse = np.sqrt(

            mean_squared_error(
                y_reg_test,
                preds
            )
        )

        r2 = r2_score(
            y_reg_test,
            preds
        )

        reg_results.append({

            "Modèle": name,

            "RMSE": rmse,

            "R²": r2
        })

        if r2 > best_r2:

            best_r2 = r2

            best_reg_model = model

    reg_results = pd.DataFrame(
        reg_results
    )

    # =====================================================
    # ENTRAÎNEMENT CLASSIFICATION
    # =====================================================

    clf_results = []

    best_clf_model = None

    best_acc = -999

    for name, model in clf_models.items():

        model.fit(
            X_train,
            y_clf_train
        )

        preds = model.predict(
            X_test
        )

        acc = accuracy_score(
            y_clf_test,
            preds
        )

        f1 = f1_score(
            y_clf_test,
            preds
        )

        clf_results.append({

            "Modèle": name,

            "Accuracy": acc,

            "F1-score": f1
        })

        if acc > best_acc:

            best_acc = acc

            best_clf_model = model

    clf_results = pd.DataFrame(
        clf_results
    )

    # =====================================================
    # AFFICHAGE TABLEAUX
    # =====================================================

    st.header("📊 Résultats Régression")

    st.dataframe(
        reg_results
    )

    st.header("📊 Résultats Classification")

    st.dataframe(
        clf_results
    )

    st.markdown("---")

    # =====================================================
    # MATRICE CORRÉLATION
    # =====================================================

    st.header("🔥 Matrice de Corrélation")

    corr = df_model[
        FEATURES + [TARGET_REG]
    ].corr()

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    sns.heatmap(

        corr,

        annot=True,

        cmap="coolwarm",

        fmt=".2f",

        ax=ax
    )

    st.pyplot(fig)

    st.markdown("---")

    # =====================================================
    # DISTRIBUTION DÉBITS
    # =====================================================

    st.header("📈 Distribution des Débits")

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    sns.histplot(

        df_model[TARGET_REG],

        bins=40,

        kde=True,

        ax=ax
    )

    st.pyplot(fig)

    st.markdown("---")

    # =====================================================
    # COMPARAISON RMSE
    # =====================================================

    st.header("📉 Comparaison RMSE")

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    ax.bar(

        reg_results["Modèle"],

        reg_results["RMSE"]
    )

    ax.set_ylabel("RMSE")

    st.pyplot(fig)

    st.markdown("---")

    # =====================================================
    # COMPARAISON R²
    # =====================================================

    st.header("📈 Comparaison R²")

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    ax.plot(

        reg_results["Modèle"],

        reg_results["R²"],

        marker="o"
    )

    ax.set_ylabel("R²")

    st.pyplot(fig)

    st.markdown("---")

    # =====================================================
    # COMPARAISON ACCURACY
    # =====================================================

    st.header("🎯 Accuracy des Modèles")

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    ax.bar(

        clf_results["Modèle"],

        clf_results["Accuracy"]
    )

    ax.set_ylabel("Accuracy")

    st.pyplot(fig)

    st.markdown("---")

    # =====================================================
    # COMPARAISON F1
    # =====================================================

    st.header("🚀 Comparaison F1-score")

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    ax.plot(

        clf_results["Modèle"],

        clf_results["F1-score"],

        marker="o"
    )

    ax.set_ylabel("F1-score")

    st.pyplot(fig)

    st.markdown("---")

    # =====================================================
    # MATRICE CONFUSION
    # =====================================================

    st.header("🧩 Matrice de Confusion")

    best_preds = best_clf_model.predict(
        X_test
    )

    cm = confusion_matrix(

        y_clf_test,

        best_preds
    )

    fig, ax = plt.subplots(
        figsize=(6, 5)
    )

    disp = ConfusionMatrixDisplay(

        confusion_matrix=cm,

        display_labels=[
            "Échec",
            "Succès"
        ]
    )

    disp.plot(ax=ax)

    st.pyplot(fig)

    st.markdown("---")

    # =====================================================
    # IMPORTANCE DES VARIABLES
    # =====================================================

    st.header("📡 Importance des Variables")

    try:

        model = best_reg_model.named_steps["model"]

    except:

        model = best_reg_model

    importance_df = None

    # =====================================================
    # RANDOM FOREST / BOOSTING
    # =====================================================

    if hasattr(model, "feature_importances_"):

        importance_df = pd.DataFrame({

            "Feature": FEATURES,

            "Importance": model.feature_importances_
        })

    # =====================================================
    # LINEAR REGRESSION
    # =====================================================

    elif hasattr(model, "coef_"):

        importance_df = pd.DataFrame({

            "Feature": FEATURES,

            "Importance": np.abs(model.coef_)
        })

    # =====================================================
    # AFFICHAGE
    # =====================================================

    if importance_df is not None:

        importance_df = importance_df.sort_values(

            by="Importance",

            ascending=True
        )

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        ax.barh(

            importance_df["Feature"],

            importance_df["Importance"]
        )

        ax.set_title(
            "Importance des Variables Réseau"
        )

        ax.set_xlabel(
            "Importance"
        )

        st.pyplot(fig)

        st.dataframe(
            importance_df
        )

    else:

        st.warning(
            "Impossible de calculer "
            "l’importance des variables."
        )
    # =====================================================
    # RÉEL VS PRÉDIT
    # =====================================================

    st.header("📡 Débit Réel vs Débit Prédit")

    y_pred = best_reg_model.predict(
        X_test
    )

    fig, ax = plt.subplots(
        figsize=(6, 6)
    )

    ax.scatter(

        y_reg_test,

        y_pred,

        alpha=0.5
    )

    ax.plot(

        [

            y_reg_test.min(),

            y_reg_test.max()
        ],

        [

            y_reg_test.min(),

            y_reg_test.max()
        ],

        "r--"
    )

    ax.set_xlabel(
        "Débit Réel"
    )

    ax.set_ylabel(
        "Débit Prédit"
    )

    st.pyplot(fig)

    st.markdown("---")

    # =====================================================
    # SAUVEGARDE MODÈLES
    # =====================================================

    joblib.dump(

        best_reg_model,

        "model/model_regression.joblib"
    )

    joblib.dump(

        best_clf_model,

        "model/model_classification.joblib"
    )

    # =====================================================
    # CONCLUSION
    # =====================================================

    st.header("🧠 Conclusion IA")

    best_reg_name = reg_results.loc[
        reg_results["R²"].idxmax()
    ]["Modèle"]

    best_clf_name = clf_results.loc[
        clf_results["Accuracy"].idxmax()
    ]["Modèle"]

    st.success(f"""
    ✔ Meilleur modèle de régression :
    {best_reg_name}

    ✔ Meilleur modèle de classification :
    {best_clf_name}

    ✔ Les paramètres radio influencent fortement 
    les performances réseau.

    ✔ L’IA permet d’automatiser l’analyse 
    des débits réseau mobiles.
    """)