"""
GAMEVERSE — Steam Gaming Analytics Dashboard
Dibuat dengan Python, Streamlit, Pandas, dan Plotly.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================
st.set_page_config(
    page_title="GAMEVERSE | Steam Analytics",
    page_icon="🎮",
    layout="wide",
)

# ============================================================
# STYLING (Premium Dark Theme)
# ============================================================
st.markdown(
    """
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
""",
    unsafe_allow_html=True,
)

# ============================================================
# KONSTANTA
# ============================================================
PRIMARY_COLOR = "#55d6e8"
SECONDARY_COLOR = "#6476d9"
MIN_VALID_YEAR = 1980
MAX_VALID_YEAR = 2030
DEFAULT_MIN_YEAR = 1980
DEFAULT_MAX_YEAR = 2025
MAX_SCATTER_POINTS = 2500
PLAYTIME_CAP_HOURS = 200

PLOTLY_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=55, b=10),
)


# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data() -> pd.DataFrame:
    """Muat dataset Steam yang sudah dibersihkan."""
    path = Path(__file__).parent / "dataset" / "steam_clean.csv"
    data = pd.read_csv(path)
    data["release_year"] = pd.to_numeric(data["release_year"], errors="coerce")
    return data


# ============================================================
# SIDEBAR FILTER
# ============================================================
def render_sidebar(df: pd.DataFrame) -> dict:
    """Render filter di sidebar dan return dict pilihan user."""
    st.sidebar.title("🎛️ Dashboard Filters")

    valid_years = df.loc[df["release_year"].between(MIN_VALID_YEAR, MAX_VALID_YEAR), "release_year"]
    min_year = int(valid_years.min()) if not valid_years.empty else DEFAULT_MIN_YEAR
    max_year = int(valid_years.max()) if not valid_years.empty else DEFAULT_MAX_YEAR

    year_range = st.sidebar.slider(
        "Rentang tahun rilis", min_year, max_year, (min_year, max_year)
    )

    genres = sorted(x for x in df["genre_primary"].dropna().unique() if x)
    selected_genres = st.sidebar.multiselect("Genre utama", genres, default=genres)

    price_choice = st.sidebar.selectbox("Jenis harga", ["Semua", "Free", "Paid"])
    platform_choice = st.sidebar.selectbox(
        "Platform", ["Semua", "Windows", "Mac", "Linux"]
    )

    return {
        "year_range": year_range,
        "selected_genres": selected_genres,
        "price_choice": price_choice,
        "platform_choice": platform_choice,
    }


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Terapkan filter ke dataframe."""
    result = df[df["release_year"].between(*filters["year_range"])]

    if filters["selected_genres"]:
        result = result[result["genre_primary"].isin(filters["selected_genres"])]

    if filters["price_choice"] != "Semua":
        result = result[result["price_type"] == filters["price_choice"]]

    if filters["platform_choice"] != "Semua":
        platform_key = filters["platform_choice"].lower()
        result = result[
            result["platforms"].fillna("").str.contains(platform_key, case=False)
        ]

    return result


# ============================================================
# KOMPONEN UI
# ============================================================
def render_hero() -> None:
    st.markdown(
        """
        <div class="hero">
          <h1>🎮 GAMEVERSE</h1>
          <p>Steam Gaming Analytics Dashboard · Jelajahi tren game, genre, harga, platform, dan respons pemain.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpis(df: pd.DataFrame) -> None:
    """Render 4 kartu KPI utama."""
    total_games = len(df)
    avg_price = df["price"].mean()

    with_ratings = df[df["total_ratings"] > 0]
    avg_positive = with_ratings["positive_rate"].mean()
    total_reviews = df["total_ratings"].sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Game", f"{total_games:,.0f}")
    c2.metric("Rata-rata Harga", f"${avg_price:,.2f}" if pd.notna(avg_price) else "N/A")
    c3.metric(
        "Rata-rata Rating Positif",
        f"{avg_positive:,.1f}%" if pd.notna(avg_positive) else "N/A",
    )
    c4.metric("Total Ulasan", f"{total_reviews:,.0f}")


def build_genre_chart(df: pd.DataFrame):
    counts = df["genre_primary"].value_counts().head(12).sort_values()
    fig = px.bar(
        counts,
        x=counts.values,
        y=counts.index,
        orientation="h",
        labels={"x": "Jumlah game", "y": "Genre"},
        title="12 Genre dengan Game Terbanyak",
        color=counts.values,
        color_continuous_scale="Teal",
    )
    fig.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False)
    return fig


def build_yearly_chart(df: pd.DataFrame) -> tuple[go.Figure, pd.DataFrame]:
    yearly = (
        df[df["release_year"] > 0]
        .groupby("release_year")
        .size()
        .reset_index(name="jumlah_game")
    )
    fig = px.line(
        yearly,
        x="release_year",
        y="jumlah_game",
        markers=True,
        labels={"release_year": "Tahun rilis", "jumlah_game": "Jumlah game"},
        title="Tren Jumlah Game Berdasarkan Tahun",
    )
    fig.update_traces(line_color=PRIMARY_COLOR, marker_color=PRIMARY_COLOR)
    fig.update_layout(**PLOTLY_LAYOUT)
    return fig, yearly


def build_price_chart(df: pd.DataFrame):
    counts = df["price_type"].value_counts().rename_axis("jenis").reset_index(name="jumlah")
    fig = px.pie(
        counts,
        names="jenis",
        values="jumlah",
        hole=0.58,
        title="Komposisi Game Gratis dan Berbayar",
        color="jenis",
        color_discrete_map={"Free": PRIMARY_COLOR, "Paid": SECONDARY_COLOR},
    )
    fig.update_layout(**{**PLOTLY_LAYOUT, "margin": dict(l=10, r=10, t=55, b=10)})
    return fig


def build_scatter_chart(df: pd.DataFrame):
    scatter_df = df[(df["total_ratings"] >= 10) & df["positive_rate"].notna()].copy()
    if len(scatter_df) > MAX_SCATTER_POINTS:
        scatter_df = scatter_df.sample(MAX_SCATTER_POINTS, random_state=42)

    fig = px.scatter(
        scatter_df,
        x="price",
        y="positive_rate",
        color="genre_primary",
        hover_name="name",
        hover_data=["developer", "total_ratings"],
        labels={
            "price": "Harga (USD)",
            "positive_rate": "Rating positif (%)",
            "genre_primary": "Genre",
        },
        title="Hubungan Harga dan Rating Positif",
        opacity=0.65,
    )
    fig.update_layout(**PLOTLY_LAYOUT, legend_title_text="Genre")
    return fig


def build_playtime_chart(df: pd.DataFrame):
    play_df = df[df["average_playtime_hours"].between(0, PLAYTIME_CAP_HOURS)]
    fig = px.histogram(
        play_df,
        x="average_playtime_hours",
        nbins=35,
        labels={"average_playtime_hours": "Rata-rata waktu bermain (jam)"},
        title="Distribusi Rata-rata Waktu Bermain",
    )
    fig.update_traces(marker_color=PRIMARY_COLOR)
    fig.update_layout(**PLOTLY_LAYOUT)
    return fig


def render_insights(df: pd.DataFrame, yearly: pd.DataFrame) -> None:
    """Tampilkan insight otomatis berbasis filter aktif."""
    st.markdown("### 💡 Insight Otomatis")

    top_genre = df["genre_primary"].value_counts()
    top_price = df["price_type"].value_counts()
    top_year = yearly.sort_values("jumlah_game", ascending=False)
    best_reviewed = df[df["total_ratings"] >= 50].sort_values(
        "positive_rate", ascending=False
    )

    insights: list[str] = []
    if not top_genre.empty:
        insights.append(
            f"Genre dengan jumlah judul terbanyak pada filter saat ini adalah "
            f"**{top_genre.index[0]}** ({top_genre.iloc[0]:,} game)."
        )
    if not top_price.empty:
        insights.append(
            f"Komposisi terbanyak adalah game **{top_price.index[0]}** "
            f"({top_price.iloc[0]:,} judul)."
        )
    if not top_year.empty:
        row = top_year.iloc[0]
        insights.append(
            f"Tahun dengan jumlah rilis tertinggi pada rentang terpilih adalah "
            f"**{int(row['release_year'])}** ({int(row['jumlah_game']):,} game)."
        )
    if not best_reviewed.empty:
        row = best_reviewed.iloc[0]
        insights.append(
            f"Di antara game dengan minimal 50 ulasan, rating positif tertinggi adalah "
            f"**{row['name']}** ({row['positive_rate']:.1f}%)."
        )

    for item in insights:
        st.markdown(f'<div class="insight">{item}</div>', unsafe_allow_html=True)


def render_top_games_table(df: pd.DataFrame) -> None:
    st.markdown("### 🏆 Game dengan Ulasan Terbanyak")
    top_games = df.nlargest(10, "total_ratings")[
        ["name", "genre_primary", "price", "positive_rate", "total_ratings", "release_year"]
    ].copy()
    top_games["price"] = top_games["price"].map(lambda x: f"${x:,.2f}")
    top_games["positive_rate"] = top_games["positive_rate"].map(
        lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A"
    )
    top_games.columns = ["Nama Game", "Genre", "Harga", "Rating Positif", "Jumlah Ulasan", "Tahun Rilis"]
    st.dataframe(top_games, use_container_width=True, hide_index=True)


def render_about() -> None:
    with st.expander("ℹ️ Tentang dataset & definisi metrik"):
        st.write(
            "Dashboard menggunakan dataset Steam Store Games yang disertakan pengguna. "
            "File utama berisi 27.075 baris dan 18 kolom sebelum pembersihan."
        )
        st.write("- Rating positif = positive_ratings / (positive_ratings + negative_ratings) × 100.")
        st.write("- Rata-rata harga dihitung dalam USD sesuai kolom price pada dataset.")
        st.write("- Total ulasan = positive_ratings + negative_ratings.")
        st.write("- Dataset merupakan snapshot historis; jangan menganggapnya sebagai data Steam real-time.")
        st.write("Sumber dataset Kaggle: https://www.kaggle.com/datasets/nikdavis/steam-store-games")


# ============================================================
# MAIN
# ============================================================
def main() -> None:
    df = load_data()

    render_hero()

    filters = render_sidebar(df)
    filtered = apply_filters(df, filters)

    if filtered.empty:
        st.warning("Tidak ada data untuk kombinasi filter ini. Silakan ubah filter.")
        st.stop()

    render_kpis(filtered)

    st.markdown("### 📊 Eksplorasi Data")

    left, right = st.columns(2)
    left.plotly_chart(build_genre_chart(filtered), use_container_width=True)
    fig_year, yearly = build_yearly_chart(filtered)
    right.plotly_chart(fig_year, use_container_width=True)

    left, right = st.columns(2)
    left.plotly_chart(build_price_chart(filtered), use_container_width=True)
    right.plotly_chart(build_scatter_chart(filtered), use_container_width=True)

    st.plotly_chart(build_playtime_chart(filtered), use_container_width=True)

    render_insights(filtered, yearly)
    render_top_games_table(filtered)
    render_about()

    st.caption("GAMEVERSE · Dibuat dengan Python, Streamlit, Pandas, dan Plotly")


if __name__ == "__main__":
    main()
