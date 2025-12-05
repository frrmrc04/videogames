import streamlit as st
import joblib
import pandas as pd
import sklearn
import matplotlib.pyplot as plt
import seaborn as sns

sklearn.set_config(transform_output='pandas')

df = pd.read_csv(r'data/vgsales_clean.csv')
df.dropna(axis=0, inplace=True)
df = df[~df['Rating'].isin(["EC", "K-A", "RP", "AO"])]

model = joblib.load(r'davide/modello_finale.joblib')
encoder = joblib.load(r'davide/encoder_finale.joblib')

st.set_page_config(
    page_title="Previsione Vendite Videogiochi",
    layout="wide",
    initial_sidebar_state="collapsed"
)

CAT_COLS = ['Rating', 'Platform', 'Genre']
NUM_COLS = ['Year_of_Release']

FEATURE_LABELS = {
    "Rating": "Classificazione ESRB",
    "Platform": "Piattaforma",
    "Genre": "Genere",
    "Year_of_Release": "Anno di Uscita",
}

sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

st.markdown("""
    <style>
    .main > div {
        padding-top: 2rem;
    }
    h1 {
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .stButton > button {
        width: 100%;
        background-color: #262730;
        color: white;
        border: none;
        padding: 0.75rem;
        font-size: 1rem;
        font-weight: 500;
        margin-top: 1rem;
    }
    .stButton > button:hover {
        background-color: #3d3d4d;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

st.title('Previsione Vendite Videogiochi')
st.markdown("Stima delle vendite globali basata su caratteristiche del prodotto")

st.markdown("---")

st.subheader("Parametri di Input")

cols = st.columns(4)
user_input = {}

for i, col_name in enumerate(CAT_COLS):
    serie = df[col_name]
    label = FEATURE_LABELS[col_name]
    
    with cols[i]:
        user_input[col_name] = st.selectbox(
            label,
            options=serie.sort_values().unique().tolist()
        )

for i, col_name in enumerate(NUM_COLS):
    serie = df[col_name]
    label = FEATURE_LABELS[col_name]
    
    with cols[len(CAT_COLS) + i]:
        user_input[col_name] = st.number_input(
            label,
            min_value=int(serie.min()),
            max_value=int(serie.max()),
            value=int(serie.median()),
            step=1
        )

st.markdown("---")

if st.button("Calcola Previsione"):
    input_df = pd.DataFrame([user_input])
    input_df['Global_Sales'] = 0
    input_df_encoded = encoder.transform(input_df)
    input_df_encoded.drop(columns='Global_Sales', inplace=True)
    proba = model.predict(input_df_encoded)[0]

    st.markdown(f"### Vendite Globali Previste: **{proba:.2f}** milioni di unità")

st.markdown("---")

st.subheader("Importanza delle features")

importances = model.named_steps['regressor'].feature_importances_
feature_names = model.named_steps['scaler'].get_feature_names_out()
feature_importances = pd.Series(importances, index=feature_names).sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(10, 6))
feature_importances.plot.barh(ax=ax, color='#262730', edgecolor='none')
ax.set_xlabel('Importanza', fontsize=11)
ax.set_ylabel('')
ax.grid(axis='x', alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()

st.pyplot(fig)