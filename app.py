import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# Load professional dashboard styling
def load_css():
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )



# Page configuration
st.set_page_config(
    page_title="Sales Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)
load_css()

# Dashboard title
st.title("📊 Sales & Business Intelligence Dashboard")
st.caption("Business performance and sales analytics")

# Load sales data
@st.cache_data
def load_data():
    df = pd.read_csv("data/sales_data.csv")
    df.columns = df.columns.str.strip()
    df["Product"] = df["Product"].str.strip()
    df["Category"] = df["Category"].str.strip()
    df["Region"] = df["Region"].str.strip()
    df["Date"] = pd.to_datetime(df["Date"])

    df["Revenue"] = df["Quantity"] * df["Unit_Price"]
    df["Profit"] = (
        df["Quantity"] *
        (df["Unit_Price"] - df["Cost_Price"])
    )
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Dashboard Filters")

regions = ["All"] + sorted(df["Region"].unique().tolist())
selected_region = st.sidebar.selectbox(
    "Select Region", regions
)

categories = ["All"] + sorted(df["Category"].unique().tolist())
selected_category = st.sidebar.selectbox(
    "Select Category", categories
)

filtered_df = df.copy()

if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]

# Key business metrics
st.subheader("Business Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"₹{filtered_df['Revenue'].sum():,.0f}")
col2.metric("Total Profit", f"₹{filtered_df['Profit'].sum():,.0f}")
col3.metric("Total Orders", len(filtered_df))
col4.metric("Units Sold", int(filtered_df["Quantity"].sum()))

st.divider()

# Monthly sales analysis
st.subheader("Monthly Revenue")

monthly_sales = (
    filtered_df
    .set_index("Date")
    .resample("ME")["Revenue"]
    .sum()
)

fig, ax = plt.subplots(figsize=(10, 4))
monthly_sales.plot(kind="bar", ax=ax)
ax.set_xlabel("Month")
ax.set_ylabel("Revenue (₹)")
ax.set_title("Monthly Revenue Analysis")
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)
plt.close(fig)

# Product analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Selling Products")
    product_sales = (
        filtered_df.groupby("Product")["Quantity"]
        .sum()
        .sort_values(ascending=False)
    )
    st.bar_chart(product_sales)

with col2:
    st.subheader("Revenue by Category")
    category_sales = (
        filtered_df.groupby("Category")["Revenue"]
        .sum()
    )
    st.bar_chart(category_sales)

# Regional performance
st.subheader("Regional Sales Performance")

region_sales = (
    filtered_df.groupby("Region")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)
st.bar_chart(region_sales)

# Sales data table
st.subheader("Detailed Sales Records")
st.dataframe(filtered_df, use_container_width=True)

# Download report
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Sales Report",
    data=csv_data,
    file_name="sales_report.csv",
    mime="text/csv"
)

st.success("Sales dashboard loaded successfully!")