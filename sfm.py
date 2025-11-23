import streamlit as st
import os 
def sfm_page():
    
    col1, col2 = st.columns([1, 4])

    with col1:
        logo = "images/logo_sfm.png"
        st.image(logo,  width=150)

    with col2:
        st.title("Bienvenue chez SFM Technologies")


    #Creation des onglets
    tabs = st.tabs(["A propos", "Solutions & Services", "Contact"])
    

    with tabs[0]:
        st.header("A PROPOS")
        col3, col4 = st.columns([2, 2])

        with col3:
            st.write(" SFM BUILDS YOUR DIGITAL ECOSYSTEM")
            st.markdown(
                """
                    SFM est une entreprise créée en 1995, issue du domaine des télécommunications et des réseaux.
                    Son équipe d'experts et d'ingénieurs de haut niveau réalise des missions d'ingénieurie et de 
                    conseil pour le compte de régulateurs des télécommunications, d'opérateurs, de Ministères des 
                    TIC et de bailleurs de fonds (BM, BAD)....
                """ 
            
            )
            st.markdown(
                """
                    C'est au cours de ses missions que SFM a développé des outils, applications et plateformes 
                    pour la digitalisation des process d'ingénierie, de suivi et de mesures de QoS/QoE, de 
                    contrôle des tarifs, ...
                """
            )
            st.markdown(
                """
                    <a href="https://www.sfmtechnologies.com/a-propos-de-sfm/" target="_blank" class="button-link">Voir plus</a>
                """,
            unsafe_allow_html=True
            )
            

        with col4:
            image = "images/login.jpg"
            st.image(image, width=700)
            

    with tabs[1]:
        st.header(" **SOLUTIONS & SERVICES** ")
        st.write("**LA DIGITALISATION DU COMPOSANT A L'ALGORITHME D'IA** ")
        col7, col8 = st.columns([2, 2])

        with col7:
            image= "images/iconT.jpg"
            st.image(image, width=90)
            st.write(" **Solutions Telco** ") 
            st.markdown(
                """
                  Le Groupe SFM, de par la confiance que lui accordent ses clients dont certains 
                  entretiennent des liens depuis plus de 20 ans, dispose de compétences et moyens 
                  techniques et financiers qui lui permettent la réalisation de missions de grande 
                  envergure et complexité dans les meilleures conditions possibles.
                """
            )
            st.markdown(
                """
                <a href="https://solutions-telco.sfmtechnologies.com/" target="_blank" class="button-link">En savoir plus</a>
                """,
                unsafe_allow_html=True
            )

        with col8:
            image = "images/telco.jpg"
            st.image(image, width=700)

            

        col9, col10 = st.columns([2, 2])
        with col9:
            image = "images/entreprise.jpg"
            st.image(image, width=700)
        with col10:
            image = "images/iconE.jpg"
            st.image(image, width=90)
            st.write(" **Solutions d'Entreprise** ")
            st.markdown(
                """
                   Engagée dans la digitalisation des activités spécifiques de régulation 
                   ou d'exploitation des infrastructures télécoms, SFM a élargi son offre 
                   en développant une suite de plateformes et outils de l'objet connecté 
                   aux applications et services basés sur des algorithmes d'intelligence
                   artificielle.
                """
            )
            st.markdown(
                """
                <a href="https://solutions-iot.sfmtechnologies.com/solutions-de-gestion-des-activites-dentreprise/ " target="_blank" class="button-link">En savoir plus</a>
                """,
                unsafe_allow_html=True
            )




    with tabs[2]:
        st.header("CONTACT")

        col5, col6 = st.columns([2, 3])

        with col5:
            st.write("RETROUVEZ-NOUS SUR GOOGLE MAP")
            image="images/map.jpg"
            st.image(image, width=700)
           
            st.markdown(
                """
                <a href="https://www.sfmtechnologies.com/" target="_blank" class="button-link">En savoir plus</a>
                """,
                unsafe_allow_html=True
            )

        with col6:
            st.write("ENVOYEZ-NOUS UN MESSAGE")
            with st.form(key='contact_form'):
                nom = st.text_input("Nom & Pénom")
                email = st.text_input("Email")
                telephone = st.text_input("Téléphone")
                message = st.text_area("Message")
                submit_button = st.form_submit_button("Envoyer")
                if submit_button:
                    st.success("Votre message a été envoyé avec succès !")
                    st.write("Nom & Prénom:", nom)
                    st.write("Email:", email)
                    st.write("Message:", message)

    def add_footer():
        st.markdown(
            """
        
                <div class="footer">
                    <a href="tel:+21671845248" class="footer-item" target="_blank">
                        <i class="fas fa-phone"></i> +216 71 845 248
                    </a>
                    <a href="wha:+21693588299" class="footer-item" target="_blank">
                        <i class="fab fa-whatsapp"></i> WhatsApp
                    </a>
                    <a href="mailto:info@sfmtelecom.com" class="footer-item" target="_blank">
                        <i class="fas fa-envelope"></i> info@sfmtelecom.com
                    </a>
                    <div style="flex-basis: 100%; order: 1; margin-top: 10px;"> <!-- Nouvelle ligne pour les icônes sociales -->
                        <a href="https://www.facebook.com/sfmtechnologies" class="footer-social-link" target="_blank">
                            <i class="fab fa-facebook-f"></i>
                        </a>
                        <a href="https://www.instagram.com/sfmtechnologies" class="footer-social-link" target="_blank">
                            <i class="fab fa-instagram"></i>
                        </a>
                        <a href="https://www.linkedin.com/company/groupe-sfm/" class="footer-social-link" target="_blank">
                            <i class="fab fa-linkedin-in"></i>
                        </a>
                </div>
            
            """,
            unsafe_allow_html=True
        )
    def load_css(file_name): # Le paramètre doit être un nom de variable valide, comme 'file_name'
        """Charge le contenu d'un fichier CSS et l'injecte dans Streamlit."""
        try:
            with open(file_name) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        except FileNotFoundError:
            st.error(f"Erreur: Le fichier CSS '{file_name}' n'a pas été trouvé. Assurez-vous qu'il est dans le même répertoire que votre script Streamlit ou que le chemin est correct.")
     
    # Charge le CSS en premier pour que les styles soient appliqués
    # Assurez-vous de passer le nom du fichier comme une chaîne de caractères
    load_css('style.css')

    # Appelle la fonction pour ajouter le pied de page
    add_footer()
    



    


    