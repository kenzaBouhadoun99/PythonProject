from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RegisterPage : 

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)   

    ### Locators ###
    
    # Choix du profil 
    PROFIL_ETUDIANT = (By.CSS_SELECTOR, 'label[for="edit-field-publics-cibles-2"]')
    PROFIL_CHERCHEUR = (By.CSS_SELECTOR, 'label[for="edit-field-publics-cibles-3"]')

    #Domaine d'etude
    DOMAINE_ETUDES = (By.ID, 'edit-field-domaine-etudes-selectized')

    #niveau d'etude
    NIVEAU_ETUDES = (By.ID, 'edit-field-niveaux-etude-selectized')

    #bouton cookies
    BOUTON_COOKIES = (By.ID,"tarteaucitronPersonalize2")

    #bouton de creation de compte 
    BOUTON_CREER_COMPTE = (By.CSS_SELECTOR,"#user-form input#edit-submit")

    #checkbox d'acceptation des communications
    CHECKBOX_ACCEPTATION = (By.ID,"edit-field-accepte-communications-value")
    
    ### Actions ###

    def ouvrir_page(self, url):
        self.driver.get(url)

    # Accepter les cookies
    def accepter_cookies(self):

        bouton = self.wait.until(
            EC.element_to_be_clickable(self.BOUTON_COOKIES)
        )

        bouton.click()

        # Masquer les éléments flottants de gestion des cookies
        self.driver.execute_script("""
            var ids = [
                'tarteaucitronAlertBig',
                'tarteaucitronManager',
                'tarteaucitronCookiesNumber'
            ];

            ids.forEach(function(id) {
                var element = document.getElementById(id);
                if (element) {
                    element.style.display = 'none';
                }
            });
        """)

    def choisir_etudiant(self):
        element = self.wait.until(EC.element_to_be_clickable(self.PROFIL_ETUDIANT))
        element.click()

    def choisir_chercheur(self):
        element = self.wait.until(EC.element_to_be_clickable(self.PROFIL_CHERCHEUR))
        element.click() 

    def choisir_profil(self, profil):
        if profil.lower() == "etudiant":
            self.choisir_etudiant()
        elif profil.lower() == "chercheur":
            self.choisir_chercheur()
        else:
            raise ValueError("Profil inconnu : {}".format(profil))

    def remplir_informations_complementaires(self, domaine_etudes, niveau_etudes):

        # Domaine
        domaine = self.wait.until(
            EC.element_to_be_clickable(self.DOMAINE_ETUDES)
        )

        domaine.click()
        domaine.send_keys(domaine_etudes)

        option_domaine = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//div[contains(@class,'selectize-dropdown')]"
                    f"//div[contains(@class,'option') and normalize-space()='{domaine_etudes}']"
                )
            )
        )
        option_domaine.click()

        # Niveau
        niveau = self.wait.until(
            EC.element_to_be_clickable(self.NIVEAU_ETUDES)
        )

        niveau.click()
        niveau.send_keys(niveau_etudes)

        option_niveau = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//div[contains(@class,'selectize-dropdown')]"
                    f"//div[contains(@class,'option') and normalize-space()='{niveau_etudes}']"
                )
            )
        )
        option_niveau.click()

    #verification domaine 
    def verifier_domaine(self, domaine):

        element = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#edit-field-domaine-etudes + div")
            )
        )

        valeur = element.text.strip()

        assert valeur == domaine, (
            f"Domaine incorrect. "
            f"Attendu : {domaine}, "
            f"Obtenu : {valeur}"
        )

    #verifier niveau
    def verifier_niveau(self, niveau):

        element = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#edit-field-niveaux-etude + div")
            )
        )

        valeur = element.text.strip()

        assert valeur == niveau, (
            f"Niveau incorrect. "
            f"Attendu : {niveau}, "
            f"Obtenu : {valeur}"
        )

    #verifier que le bouton de creation de compte est present et a le bon nom
    def verifier_bouton_creer_compte(self):
        bouton = self.wait.until(
            EC.presence_of_element_located(self.BOUTON_CREER_COMPTE)
        )

        valeur = bouton.get_attribute("value")

        assert valeur == "Créer un compte", (
            f"Nom du bouton incorrect. "
            f"Attendu : Créer un compte, "
            f"Obtenu : {valeur}"
        )

    #verifier que la checkbox d'acceptation est décochée
    def verifier_checkbox_decochée(self):
        checkbox = self.wait.until(
            EC.presence_of_element_located(self.CHECKBOX_ACCEPTATION)
        )

        assert not checkbox.is_selected(), (
            "La case d'acceptation est cochée alors qu'elle devrait être décochée."
        )