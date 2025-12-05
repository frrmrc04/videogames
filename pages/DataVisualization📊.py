import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="Game Sales Dashboard",
    layout="wide",
    page_icon="🎮"
)

DATA_PATH = Path(r"data/vgsales_clean.csv")

@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    return df

df = load_data()
FEATURE_COLS=['Year_of_Release', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Global_Sales', 'Critic_Score']

df_valid = df.dropna(subset=["Year_of_Release"])
df_valid["Year_of_Release"] = df_valid["Year_of_Release"].astype(int)

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

df_filtered = df_valid[
    (df_valid["Year_of_Release"] >= year_range[0]) &
    (df_valid["Year_of_Release"] <= year_range[1])
]

if selected_genre != "Tutti":
    df_filtered = df_filtered[df_filtered["Genre"] == selected_genre]

if selected_platform != "Tutte":
    df_filtered = df_filtered[df_filtered["Platform"] == selected_platform]

st.title("🎮 Video Game Sales Dashboard")

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

with col_c:
    st.subheader("🎲 Distribuzione Critic Score")
    st.image(r"my_graphs/2.png", caption="Didascalia", width=300)

with col_d:
    st.subheader("🎲 Distribuzione User Score")
    st.image(r"my_graphs/output.png", caption="Didascalia", width=300)

st.markdown("---")

col_new1, col_new2 = st.columns(2)

with col_new1:
    st.subheader("💰 ROI per Genere (Vendite Medie per Titolo)")
    genre_roi = df_filtered.groupby("Genre").agg({
        sales_colname: 'sum',
        'Name': 'count'
    }).reset_index()
    genre_roi['ROI'] = genre_roi[sales_colname] / genre_roi['Name']
    genre_roi = genre_roi.sort_values('ROI', ascending=False).head(10)
    
    fig_roi = px.bar(
        genre_roi,
        x='Genre',
        y='ROI',
        labels={'ROI': 'Vendite Medie per Titolo (M)', 'Genre': 'Genere'},
        title='Profittabilità per Genere'
    )
    st.plotly_chart(fig_roi, use_container_width=True)

with col_new2:
    st.subheader("🌍 Confronto Regionale per Genere")
    regional_data = df_filtered.groupby("Genre")[['NA_Sales', 'EU_Sales', 'JP_Sales']].sum().reset_index()
    regional_data = regional_data.nlargest(8, 'NA_Sales')
    
    fig_regional = go.Figure()
    fig_regional.add_trace(go.Bar(name='NA', x=regional_data['Genre'], y=regional_data['NA_Sales']))
    fig_regional.add_trace(go.Bar(name='EU', x=regional_data['Genre'], y=regional_data['EU_Sales']))
    fig_regional.add_trace(go.Bar(name='JP', x=regional_data['Genre'], y=regional_data['JP_Sales']))
    fig_regional.update_layout(barmode='group', title='Vendite per Regione (Top 8 Generi)')
    st.plotly_chart(fig_regional, use_container_width=True)

st.subheader("📈 Concentrazione di Mercato nel Tempo")
yearly_concentration = []
for year in df_filtered['Year_of_Release'].unique():
    year_data = df_filtered[df_filtered['Year_of_Release'] == year]
    top5_sales = year_data.nlargest(5, sales_colname)[sales_colname].sum()
    total_sales = year_data[sales_colname].sum()
    concentration = (top5_sales / total_sales * 100) if total_sales > 0 else 0
    yearly_concentration.append({'Year': year, 'Top5_Share': concentration})

concentration_df = pd.DataFrame(yearly_concentration).sort_values('Year')

fig_concentration = px.line(
    concentration_df,
    x='Year',
    y='Top5_Share',
    markers=True,
    labels={'Top5_Share': '% Vendite Top 5 Giochi', 'Year': 'Anno'},
    title='Quanto il mercato è dominato dai top 5 giochi per anno'
)
st.plotly_chart(fig_concentration, use_container_width=True)