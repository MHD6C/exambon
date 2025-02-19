import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get

# Configuration de la page
st.set_page_config(page_title="Scraper Coinafrique", page_icon="👕👞", layout="wide")

# Appliquer un style CSS personnalisé
st.markdown(
    """
    <style>
        body {
            background-color: #f5f5f5;
        }
        .stApp {
            background: linear-gradient(to right, #4b79a1, #283e51);
            color: white;
        }
        .css-18e3th9 {
            background-color: rgba(255, 255, 255, 0.1) !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Titre de l'application
st.title("👕👞 Scraper Coinafrique - Vêtements et Chaussures Homme")

# Fonction pour scraper les vêtements
def scrape_vetements(num_pages):
    Data = []
    for page in range(1, num_pages + 1):
        url = f'https://sn.coinafrique.com/categorie/vetements-homme?page={page}'
        res = get(url)
        soup = bs(res.text, 'html.parser')
        containers = soup.find_all('div', class_='col s6 m4 l3')
        for container in containers:
            try:
                prix = container.find('p', class_='ad__card-price').text.strip().replace('CFA', '').strip()
                type_habit = container.find('p', class_='ad__card-description').text.strip()
                adresse = container.find('p', class_='ad__card-location').text.strip().replace('location_on', '').strip()
                img_link = 'https://sn.coinafrique.com' + container.find('img', class_='ad__card-img')['src']
                dic = {
                    'prix': prix,
                    'type_habit': type_habit,
                    'adresse': adresse,
                    'img': img_link
                }
                Data.append(dic)
            except:
                pass
    return pd.DataFrame(Data)

# Fonction pour scraper les chaussures
def scrape_chaussures(num_pages):
    Data = []
    for page in range(1, num_pages + 1):
        url = f'https://sn.coinafrique.com/categorie/chaussures-homme?page={page}'
        res = get(url)
        soup = bs(res.text, 'html.parser')
        containers = soup.find_all('div', class_='col s6 m4 l3')
        for container in containers:
            try:
                type_shoes = container.find('p', class_='ad__card-description').text.strip()
                price = container.find('p', class_='ad__card-price').text.strip().replace('CFA', '').strip()
                adresse = container.find('p', class_='ad__card-location').text.strip().replace('location_on', '').strip()
                img = 'https://sn.coinafrique.com' + container.find('img', class_='ad__card-img')['src']
                dic = {
                    'type_chaussure': type_shoes,
                    'prix': price,
                    'adresse': adresse,
                    'image': img
                }
                Data.append(dic)
            except:
                pass
    return pd.DataFrame(Data)

# Charger les fichiers WebScraper
vetements_file = "vetements.csv"
chaussures_file = "shoes.csv"

# Interface utilisateur
st.sidebar.header("Paramètres")
option = st.sidebar.radio("Afficher les données de :", ["BeautifulSoup", "Web Scraper"])

if option == "BeautifulSoup":
    category = st.sidebar.radio("Choisissez une catégorie", ["Vêtements", "Chaussures"])
    num_pages = st.sidebar.slider("Nombre de pages à scraper", min_value=1, max_value=10, value=3)
    if st.sidebar.button("Lancer le scraping"):
        with st.spinner("Scraping en cours..."):
            df = scrape_vetements(num_pages) if category == "Vêtements" else scrape_chaussures(num_pages)
            st.success("Scraping terminé !")
            st.dataframe(df)
else:
    file_choice = st.sidebar.radio("Choisissez un fichier Web Scraper", ["Vêtements", "Chaussures"])
    file_path = vetements_file if file_choice == "Vêtements" else chaussures_file
    df = pd.read_csv(file_path)
    st.subheader(f"Données extraites de {file_choice}")
    st.dataframe(df)

# Intégration des formulaires
st.subheader("Formulaires")
st.markdown("""
    <iframe src="https://docs.google.com/forms/d/e/1FAIpQLSfmCdrr255NdjSBMKHpSx4_eW3zE3YWW4po6CwBDOijg3COiA/viewform?embedded=true" width="800" height="1100" frameborder="0" marginheight="0" marginwidth="0">Chargement en cours...</iframe>
""", unsafe_allow_html=True)

st.markdown("""
    <iframe src="https://ee.kobotoolbox.org/x/fjdlDw9S" width="800" height="1100" frameborder="0" marginheight="0" marginwidth="0">Chargement en cours...</iframe>
""", unsafe_allow_html=True)
