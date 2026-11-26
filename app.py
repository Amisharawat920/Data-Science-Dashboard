import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Diamonds Price Analysis Dashboard",
    page_icon="💎",
    layout="wide"
)


NAVY = "#0B2239"
GREEN = "#119B7D"
BLUE = "#3B82F6"
ORANGE = "#F5A400"
RED = "#E4572E"
LIGHT = "#F3F5F8"

st.markdown("""
<style>
.stApp {
    background-color: #F3F5F8;
}
h1, h2, h3 {
    color: #0B2239;
}
div[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #dddddd;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/diamonds.csv"
    df = pd.read_csv(url)

    # Remove duplicate records
    df = df.drop_duplicates()

    # Remove rows having zero-size measurements
    df = df[(df["x"] > 0) & (df["y"] > 0) & (df["z"] > 0)]

    return df

df = load_data()

# ---------------- CARAT RANGE ----------------
carat_bins = [0, 0.5, 1, 1.5, 2, float("inf")]
carat_labels = ["0-0.5", "0.5-1", "1-1.5", "1.5-2", "2+"]

df["carat_range"] = pd.cut(
    df["carat"],
    bins=carat_bins,
    labels=carat_labels,
    right=False
)

# ---------------- PRICE RANGE ----------------
price_bins = [0, 2000, 4000, 6000, 8000, 10000, float("inf")]
price_labels = ["Under 2k", "2-4k", "4-6k", "6-8k", "8-10k", "10k+"]

df["price_range"] = pd.cut(
    df["price"],
    bins=price_bins,
    labels=price_labels,
    right=False
)

# ---------------- TITLE ----------------
st.markdown(
    f"<h1 style='text-align:center;color:{NAVY};'>💎 Diamonds Price Analysis Dashboard</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;'>Analysis of Cut, Color, Clarity, Carat and Price</p>",
    unsafe_allow_html=True
)

st.divider()

# ---------------- KPI CARDS ----------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Diamonds", f"{len(df):,}")
col2.metric("Average Price", f"${df['price'].mean():,.0f}")
col3.metric("Average Carat", f"{df['carat'].mean():.2f}")
col4.metric("Maximum Price", f"${df['price'].max():,}")

st.divider()

# ---------------- CHART 1 ----------------
st.subheader("Chart 1: Diamonds by Cut")

cut_counts = df["cut"].value_counts()

cut_order = ["Fair", "Good", "Very Good", "Premium", "Ideal"]
cut_counts = cut_counts.reindex(cut_order)

fig1 = px.pie(
    values=cut_counts.values,
    names=cut_counts.index,
    hole=0.55,
    title="Distribution of Diamond Cut",
    color=cut_counts.index,
    color_discrete_map={
        "Fair": "#9CA3AF",
        "Good": ORANGE,
        "Very Good": GREEN,
        "Premium": BLUE,
        "Ideal": NAVY
    }
)

fig1.update_traces(textinfo="percent")
fig1.update_layout(
    legend_title="Cut",
    paper_bgcolor="white",
    plot_bgcolor="white"
)

st.plotly_chart(fig1, use_container_width=True)

st.info(
    "Insight: Ideal cut diamonds form the largest category, "
    "while Fair cut diamonds form the smallest category."
)

st.divider()

# ---------------- CHART 2 ----------------
st.subheader("Chart 2: Average Price by Carat Range")

carat_price = (
    df.groupby("carat_range", observed=False)["price"]
    .mean()
    .reset_index()
)

fig2 = px.line(
    carat_price,
    x="carat_range",
    y="price",
    markers=True,
    text="price",
    title="Average Price Across Carat Ranges"
)

fig2.update_traces(
    line=dict(color=GREEN, width=4),
    marker=dict(size=10),
    texttemplate="$%{text:,.0f}",
    textposition="top center"
)

fig2.update_layout(
    xaxis_title="Carat Range",
    yaxis_title="Average Price (USD)",
    paper_bgcolor="white",
    plot_bgcolor="white"
)

st.plotly_chart(fig2, use_container_width=True)

st.info(
    "Insight: Average diamond price increases significantly "
    "as the carat range increases."
)

st.divider()

# ---------------- CHART 3 ----------------
st.subheader("Chart 3: Diamonds by Clarity")

clarity_order = ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"]

clarity_counts = (
    df["clarity"].value_counts()
    .reindex(clarity_order)
    .reset_index()
)

clarity_counts.columns = ["clarity", "count"]

# Sort bars from low to high count for horizontal display
clarity_counts = clarity_counts.sort_values("count")

fig3 = px.bar(
    clarity_counts,
    x="count",
    y="clarity",
    orientation="h",
    text="count",
    title="Number of Diamonds by Clarity",
    color_discrete_sequence=[BLUE]
)

fig3.update_traces(textposition="outside")

fig3.update_layout(
    xaxis_title="Number of Diamonds",
    yaxis_title="Clarity",
    paper_bgcolor="white",
    plot_bgcolor="white"
)

st.plotly_chart(fig3, use_container_width=True)

st.info(
    "Insight: SI1 and VS2 are the most common clarity grades, "
    "while I1 is the least common."
)

st.divider()

# ---------------- CHART 4 ----------------
st.subheader("Chart 4: Average Price by Color")

color_order = ["D", "E", "F", "G", "H", "I", "J"]

color_price = (
    df.groupby("color")["price"]
    .mean()
    .reindex(color_order)
    .reset_index()
)

fig4 = px.bar(
    color_price,
    x="color",
    y="price",
    text="price",
    title="Average Diamond Price by Color",
    color="color",
    color_discrete_sequence=[
        BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, ORANGE
    ]
)

fig4.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)

fig4.update_layout(
    xaxis_title="Color Grade (D Best, J Lowest)",
    yaxis_title="Average Price (USD)",
    showlegend=False,
    paper_bgcolor="white",
    plot_bgcolor="white"
)

st.plotly_chart(fig4, use_container_width=True)

st.info(
    "Insight: J color diamonds show a higher average price "
    "in this dataset, which may be influenced by carat weight."
)

st.divider()

# ---------------- CHART 5 ----------------
st.subheader("Chart 5: Diamonds by Price Range")

price_counts = (
    df["price_range"].value_counts(sort=False)
    .reindex(price_labels)
    .reset_index()
)

price_counts.columns = ["price_range", "count"]

fig5 = px.bar(
    price_counts,
    x="price_range",
    y="count",
    text="count",
    title="Number of Diamonds Across Price Ranges",
    color_discrete_sequence=[RED]
)

fig5.update_traces(
    textposition="outside"
)

fig5.update_layout(
    xaxis_title="Price Range (USD)",
    yaxis_title="Number of Diamonds",
    paper_bgcolor="white",
    plot_bgcolor="white"
)

st.plotly_chart(fig5, use_container_width=True)

st.info(
    "Insight: A large proportion of diamonds are priced below $2,000."
)

st.divider()

# ---------------- CHART 6 ----------------
st.subheader("Chart 6: Diamonds by Carat Range and Cut")

area_data = (
    df.groupby(["carat_range", "cut"], observed=False)
    .size()
    .reset_index(name="count")
)

fig6 = px.area(
    area_data,
    x="carat_range",
    y="count",
    color="cut",
    title="Diamond Distribution by Carat Range and Cut",
    category_orders={
        "carat_range": carat_labels,
        "cut": cut_order
    },
    color_discrete_map={
        "Fair": "#9CA3AF",
        "Good": ORANGE,
        "Very Good": GREEN,
        "Premium": BLUE,
        "Ideal": NAVY
    }
)

fig6.update_layout(
    xaxis_title="Carat Range",
    yaxis_title="Number of Diamonds",
    paper_bgcolor="white",
    plot_bgcolor="white"
)

st.plotly_chart(fig6, use_container_width=True)

st.info(
    "Insight: Diamonds under one carat form a large part of the dataset, "
    "and Ideal cut contributes significantly to smaller carat ranges."
)

# ---------------- FOOTER ----------------
st.divider()

st.markdown(
    f"<h4 style='text-align:center;color:{NAVY};'>"
    "Diamond Price Analysis | Data Visualization Project"
    "</h4>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;'>Created using Python, Pandas, Streamlit and Plotly</p>",
    unsafe_allow_html=True
)