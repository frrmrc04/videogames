
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------------------
st.set_page_config(
    page_title="Game Sales Dashboard",
    layout="wide",
    page_icon="🎮"
)

# -------------------------------------------------------------------
# DATA
# -------------------------------------------------------------------
DATA_PATH = Path(r"data\vgsales_clean.csv")

@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    return df

df = load_data()
FEATURE_COLS=['Year_of_Release', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Global_Sales', 'Critic_Score']

# -------------------------------------------------------------------
# PREPARAZIONE DATA
# -------------------------------------------------------------------
df_valid = df.dropna(subset=["Year_of_Release"])
df_valid["Year_of_Release"] = df_valid["Year_of_Release"].astype(int)

# -------------------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------------------
st.sidebar.header("⚙️ Filtri")

sales_choice = st.sidebar.selectbox(
    "Scegli area vendite",
    ["Global_Sales", "NA_Sales", "EU_Sales", "JP_Sales"],
    format_func=lambda x: {
        "Global_Sales": "🌍 Global Sales",
        "NA_Sales": "🇺🇸 North America",
        "EU_Sales": "🇪🇺 Europe",
        "JP_Sales": "🇯🇵 Japan"
    }[x]
)

sales_colname = sales_choice

min_year = int(df_valid["Year_of_Release"].min())
max_year = int(df_valid["Year_of_Release"].max())
year_range = st.sidebar.slider(
    "Seleziona periodo (anni)",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

all_genres = sorted(df_valid["Genre"].dropna().unique().tolist())
selected_genre = st.sidebar.selectbox(
    "Seleziona genere",
    ["Tutti"] + all_genres
)

all_platforms = sorted(df_valid["Platform"].dropna().unique().tolist())
selected_platform = st.sidebar.selectbox(
    "Seleziona piattaforma",
    ["Tutte"] + all_platforms
)

# -------------------------------------------------------------------
# APPLICAZIONE FILTRI
# -------------------------------------------------------------------
df_filtered = df_valid[
    (df_valid["Year_of_Release"] >= year_range[0]) &
    (df_valid["Year_of_Release"] <= year_range[1])
]

if selected_genre != "Tutti":
    df_filtered = df_filtered[df_filtered["Genre"] == selected_genre]

if selected_platform != "Tutte":
    df_filtered = df_filtered[df_filtered["Platform"] == selected_platform]

# -------------------------------------------------------------------
# TITOLI
# -------------------------------------------------------------------
st.title("🎮 Video Game Sales Dashboard")

# -------------------------------------------------------------------
# 1) LINE CHART — VENDITE PER GENERE
# -------------------------------------------------------------------
with st.expander("📋 Clicca qui per vedere l'head del dataset"):
    st.dataframe(df_filtered.head(5))

st.subheader(f"📈 Vendite nel tempo per GENERE ({sales_choice.upper()})")

sales_genre = (
    df_filtered.groupby(["Year_of_Release", "Genre"])[sales_colname]
    .sum()
    .reset_index()
)

fig1 = px.line(
    sales_genre,
    x="Year_of_Release",
    y=sales_colname,
    color="Genre",
    markers=True,
    labels={
        "Year_of_Release": "Anno",
        sales_colname: "Vendite (milioni)"
    },
    title=f"Vendite per Genere nel tempo — {sales_choice.upper()}"
)

st.plotly_chart(fig1, use_container_width=True)

# -------------------------------------------------------------------
# 2) LINE CHART — VENDITE PER PIATTAFORMA
# -------------------------------------------------------------------
st.subheader(f"📈 Vendite nel tempo per PIATTAFORMA ({sales_choice.upper()})")

sales_platform = (
    df_filtered.groupby(["Year_of_Release", "Platform"])[sales_colname]
    .sum()
    .reset_index()
)

fig2 = px.line(
    sales_platform,
    x="Year_of_Release",
    y=sales_colname,
    color="Platform",
    markers=True,
    labels={
        "Year_of_Release": "Anno",
        sales_colname: "Vendite (milioni)"
    },
    title=f"Vendite per Piattaforma nel tempo — {sales_choice.upper()}"
)

st.plotly_chart(fig2, use_container_width=True)

# -------------------------------------------------------------------
# 3) SCATTER — CRITIC SCORE vs SALES
# -------------------------------------------------------------------
st.subheader(f"🎯 Critic Score vs Vendite ({sales_choice.upper()})")

df_scatter = df_filtered.dropna(subset=["Critic_Score"])

fig3 = px.scatter(
    df_scatter,
    x="Critic_Score",
    y=sales_colname,
    opacity=0.6,
    labels={
        "Critic_Score": "Critic Score",
        sales_colname: "Vendite (milioni)"
    },
    title=f"Critic Score vs Vendite — {sales_choice.upper()}"
)

st.plotly_chart(fig3, use_container_width=True)

# -------------------------------------------------------------------
col_a, col_b = st.columns(2)
with col_a:
    st.subheader("🏆 Top 10 Publisher per Vendite Totali")
    top_publishers = (
        df_filtered.groupby("Publisher")[sales_colname]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_top_publishers = px.bar(
        top_publishers,
        x="Publisher",
        y=sales_colname,
        labels={sales_colname: "Vendite (milioni)", "Publisher": "Publisher"},
        title="Top 10 Publisher per Vendite Totali"
    )
    st.plotly_chart(fig_top_publishers, use_container_width=True)

with col_b:
    st.subheader("📊 Vendite totali per ESRB Rating")
    esrb_sales = (
        df_filtered.groupby("Rating")[sales_colname]
        .sum()
        .reset_index()
        .sort_values(by=sales_colname, ascending=False)
    )
    fig_esrb_sales = px.bar(
        esrb_sales,
        x="Rating",
        y=sales_colname,
        labels={sales_colname: "Vendite totali (milioni)", "Rating": "ESRB Rating"},
        title="Vendite totali per ESRB Rating"
    )
    st.plotly_chart(fig_esrb_sales, use_container_width=True)


col_c, col_d = st.columns(2)


# distribuzione critic score e user score
with col_c:
    st.subheader("🎲 Distribuzione Critic Score")
    st.image(r" my_graphs/2.png", caption="Didascalia", width=300)

with col_d:
    st.subheader("🎲 Distribuzione User Score")
    st.image(r" my_graphs/output.png", caption="Didascalia", width=300)



