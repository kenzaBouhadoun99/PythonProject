import json
import pytest 
from selenium import webdriver
from pages.register_page import RegisterPage
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage") 

### chargement des donnéees de test depuis un fichier JSON ###
with open("data/register_data.json", "r", encoding="utf-8") as fichier:
    donnees = json.load(fichier) 

### test etudiant et chercheur 
@pytest.mark.parametrize(
    "profil",
    ["etudiant", "chercheur"]
)
def test_informations_complementaires(profil):

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    try: 
        page = RegisterPage(driver)

        #url de la page
        page.ouvrir_page("https://www.campusfrance.org/fr/user/register")  

        #accepter les cookies
        page.accepter_cookies()

        #récupérer des données du profil 
        informations = donnees[profil]["informations_complementaires"]
        domaine = informations["domaine_etudes"]
        niveau = informations["niveau_etudes"]

        #choix du profil 
        page.choisir_profil(profil)

        #remplissage 
        page.remplir_informations_complementaires(
            domaine,
            niveau
        )

        # vérification des informations
        page.verifier_domaine(domaine)
        page.verifier_niveau(niveau)

        #verifier que le bouton de creation de compte est present et a le bon nom
        page.verifier_bouton_creer_compte()

        #verifier que la checkbox d'acceptation est décochée
        page.verifier_checkbox_decochée()

    finally:
        driver.quit()