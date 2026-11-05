import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="GAMEVERSE | Steam Analytics", page_icon="🎮", layout="wide")

# Premium dark styling
st.markdown("""
<style>
    .stApp { background: #0b1020; color: #edf2ff; }
    [data-testid="stSidebar"] { background: #111a2e; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    h1, h2, h3 { color: #f4f7ff; }
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #17243b, #111a2e);
        border: 1px solid #263957; padding: 16px 18px; border-radius: 14px;
    }
    div[data-testid="stMetric"] label { color: #9fb2d1 !important; }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] { color: #55d6e8 !important; }
    .hero {
        background: linear-gradient(110deg, #17243b, #142b43 55%, #123b50);
        border: 1px solid #28415e; border-radius: 18px; padding: 24px 28px;
        margin-bottom: 18px;
    }
    .hero p { color: #b8c7df; margin-bottom: 0; }
    .insight {
        background: #14243a; border-left: 4px solid #55d6e8;
        border-radius: 8px; padding: 13px 16px; margin: 8px 0;
    }
    .small-note { color: #9fb2d1; font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    path = Path(__file__).parent / "dataset" / "steam_clean.csv"
    data = pd.read_csv(path)
    data["release_year"] = pd.to_numeric(data["release_year"], errors="coerce")
    return data

df = load_data()
st.markdown("""
<div class="hero">
  <h1>🎮 GAMEVERSE</h1>
  <p>Steam Gaming Analytics Dashboard · Jelajahi tren game, genre, harga, platform, dan respons pemain.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar filters
st.sidebar.title("🎛️ Dashboard Filters")
valid_years = df.loc[df["release_year"].between(1980, 2030), "release_year"]
min_year = int(valid_years.min()) if not valid_years.empty else 1980
max_year = int(valid_years.max()) if not valid_years.empty else 2025
year_range = st.sidebar.slider("Rentang tahun rilis", min_year, max_year, (min_year, max_year))
genres = sorted([x for x in df["genre_primary"].dropna().unique() if x])
selected_genres = st.sidebar.multiselect("Genre utama", genres, default=genres)
price_choice = st.sidebar.selectbox("Jenis harga", ["Semua", "Free", "Paid"])
platform_choices = ["Semua", "Windows", "Mac", "Linux"]
platform_choice = st.sidebar.selectbox("Platform", platform_choices)

filtered = df[df["release_year"].between(year_range[0], year_range[1])]
if selected_genres:
    filtered = filtered[filtered["genre_primary"].isin(selected_genres)]
if price_choice != "Semua":
    filtered = filtered[filtered["price_type"] == price_choice]
if platform_choice != "Semua":
    filtered = filtered[filtered["platforms"].fillna("").str.contains(platform_choice.lower(), case=False)]

if filtered.empty:
    st.warning("Tidak ada data untuk kombinasi filter ini. Silakan ubah filter.")
    st.stop()

# KPI cards
total_games = len(filtered)
avg_price = filtered["price"].mean()
avg_positive = filtered.loc[filtered["total_ratings"] > 0, "positive_rate"].mean()
total_reviews = filtered["total_ratings"].sum()
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Game", f"{total_games:,.0f}")
k2.metric("Rata-rata Harga", f"${avg_price:,.2f}" if pd.notna(avg_price) else "N/A")
k3.metric("Rata-rata Rating Positif", f"{avg_positive:,.1f}%" if pd.notna(avg_positive) else "N/A")
k4.metric("Total Ulasan", f"{total_reviews:,.0f}")

st.markdown("### 📊 Eksplorasi Data")
left, right = st.columns(2)

# 1. Bar chart: games by genre
genre_counts = filtered["genre_primary"].value_counts().head(12).sort_values()
fig_genre = px.bar(genre_counts, x=genre_counts.values, y=genre_counts.index, orientation="h",
                   labels={"x":"Jumlah game", "y":"Genre"}, title="12 Genre dengan Game Terbanyak",
                   color=genre_counts.values, color_continuous_scale="Teal")
fig_genre.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        coloraxis_showscale=False, margin=dict(l=10,r=10,t=55,b=10))
left.plotly_chart(fig_genre, use_container_width=True)

# 2. Line chart: release trend
yearly = filtered[filtered["release_year"] > 0].groupby("release_year").size().reset_index(name="jumlah_game")
fig_year = px.line(yearly, x="release_year", y="jumlah_game", markers=True,
                   labels={"release_year":"Tahun rilis","jumlah_game":"Jumlah game"},
                   title="Tren Jumlah Game Berdasarkan Tahun")
fig_year.update_traces(line_color="#55d6e8", marker_color="#55d6e8")
fig_year.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       margin=dict(l=10,r=10,t=55,b=10))
right.plotly_chart(fig_year, use_container_width=True)

left, right = st.columns(2)

# 3. Donut chart: free vs paid
price_counts = filtered["price_type"].value_counts().rename_axis("jenis").reset_index(name="jumlah")
fig_price = px.pie(price_counts, names="jenis", values="jumlah", hole=0.58,
                   title="Komposisi Game Gratis dan Berbayar",
                   color="jenis", color_discrete_map={"Free":"#55d6e8","Paid":"#6476d9"})
fig_price.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=10,r=10,t=55,b=10))
left.plotly_chart(fig_price, use_container_width=True)

# 4. Scatter: price vs positive rating percentage
scatter_df = filtered[(filtered["total_ratings"] >= 10) & filtered["positive_rate"].notna()].copy()
if len(scatter_df) > 2500:
    scatter_df = scatter_df.sample(2500, random_state=42)
fig_scatter = px.scatter(scatter_df, x="price", y="positive_rate", color="genre_primary",
                         hover_name="name", hover_data=["developer","total_ratings"],
                         labels={"price":"Harga (USD)","positive_rate":"Rating positif (%)","genre_primary":"Genre"},
                         title="Hubungan Harga dan Rating Positif", opacity=0.65)
fig_scatter.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          margin=dict(l=10,r=10,t=55,b=10), legend_title_text="Genre")
right.plotly_chart(fig_scatter, use_container_width=True)

# 5. Histogram: playtime distribution
play_df = filtered[filtered["average_playtime_hours"].between(0, 200)]
fig_play = px.histogram(play_df, x="average_playtime_hours", nbins=35,
                        labels={"average_playtime_hours":"Rata-rata waktu bermain (jam)"},
                        title="Distribusi Rata-rata Waktu Bermain")
fig_play.update_traces(marker_color="#55d6e8")
fig_play.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       margin=dict(l=10,r=10,t=55,b=10))
st.plotly_chart(fig_play, use_container_width=True)

# Dynamic insight/storytelling
st.markdown("### 💡 Insight Otomatis")
top_genre = filtered["genre_primary"].value_counts()
top_price = filtered["price_type"].value_counts()
top_year = yearly.sort_values("jumlah_game", ascending=False)
best_reviewed = filtered[filtered["total_ratings"] >= 50].sort_values("positive_rate", ascending=False)
insights = []
if not top_genre.empty:
    insights.append(f"Genre dengan jumlah judul terbanyak pada filter saat ini adalah **{top_genre.index[0]}** ({top_genre.iloc[0]:,} game).")
if not top_price.empty:
    insights.append(f"Komposisi terbanyak adalah game **{top_price.index[0]}** ({top_price.iloc[0]:,} judul).")
if not top_year.empty:
    insights.append(f"Tahun dengan jumlah rilis tertinggi pada rentang terpilih adalah **{int(top_year.iloc[0]['release_year'])}** ({int(top_year.iloc[0]['jumlah_game']):,} game).")
if not best_reviewed.empty:
    insights.append(f"Di antara game dengan minimal 50 ulasan, rating positif tertinggi adalah **{best_reviewed.iloc[0]['name']}** ({best_reviewed.iloc[0]['positive_rate']:.1f}%).")
for item in insights:
    st.markdown(f'<div class="insight">{item}</div>', unsafe_allow_html=True)

st.markdown("### 🏆 Game dengan Ulasan Terbanyak")
top_games = filtered.nlargest(10, "total_ratings")[["name","genre_primary","price","positive_rate","total_ratings","release_year"]].copy()
top_games["price"] = top_games["price"].map(lambda x: f"${x:,.2f}")
top_games["positive_rate"] = top_games["positive_rate"].map(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")
top_games.columns = ["Nama Game","Genre","Harga","Rating Positif","Jumlah Ulasan","Tahun Rilis"]
st.dataframe(top_games, use_container_width=True, hide_index=True)

with st.expander("ℹ️ Tentang dataset & definisi metrik"):
    st.write("Dashboard menggunakan dataset Steam Store Games yang disertakan pengguna. File utama berisi 27.075 baris dan 18 kolom sebelum pembersihan.")
    st.write("- Rating positif = positive_ratings / (positive_ratings + negative_ratings) × 100.")
    st.write("- Rata-rata harga dihitung dalam USD sesuai kolom price pada dataset.")
    st.write("- Total ulasan = positive_ratings + negative_ratings.")
    st.write("- Dataset merupakan snapshot historis; jangan menganggapnya sebagai data Steam real-time.")
    st.write("Sumber dataset Kaggle: https://www.kaggle.com/datasets/nikdavis/steam-store-games")

st.caption("GAMEVERSE · Dibuat dengan Python, Streamlit, Pandas, dan Plotly")
