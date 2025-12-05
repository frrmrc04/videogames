import streamlit as st

# definisci le pagine
page1 = st.Page(r"pages\DataVisualization📊.py", title="Data visualization", icon="📊")
page2 = st.Page(r"pages\Machine Learning Model ⚙️.py", icon="🤖")

# crea la navigazione
pg = st.navigation([page1, page2])

# esegui la pagina selezionata





import streamlit as st

st.set_page_config(
    page_title="🎮 Game Analytics Dashboard",
    layout="wide",
    page_icon="🏠"
)

# Titolo principale
st.title("🎮 Benvenuto nella Game Analytics Dashboard")

# Testo introduttivo
st.markdown(
    """
    Questa dashboard permette di esplorare e analizzare il catalogo videogiochi dal 2000 in poi.  
    Puoi navigare tra diverse sezioni per ottenere insight sulle vendite, sui generi e piattaforme, 
    e stimare la probabilità di successo commerciale dei nuovi titoli.
    """
)

# Sezione navigazione
st.markdown("## 📂 Navigazione")

# Pulsanti per andare alle sotto-pagine (funzionano se usi Streamlit > 1.10 con pages/)
st.markdown(
    """
    - **EDA Interattiva** → esplora vendite per piattaforma e genere, filtri dinamici e scatter plot recensioni.
    - **Modello ML** → inserisci le caratteristiche di un nuovo gioco e stima la probabilità di diventare un HIT.
    """
)

pg.run()