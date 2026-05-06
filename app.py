import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Lulu Dubai Sales Dashboard", layout="wide")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('lulu.csv')
    df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'])
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Options")
segment_filter = st.sidebar.multiselect("Select Customer Segment", 
                                        options=df['Customer_Segment'].unique(), 
                                        default=df['Customer_Segment'].unique())

category_filter = st.sidebar.multiselect("Select Product Category", 
                                          options=df['Product_Category'].unique(), 
                                          default=df['Product_Category'].unique())

filtered_df = df[(df['Customer_Segment'].isin(segment_filter)) & 
                 (df['Product_Category'].isin(category_filter))]

# Header
st.title("📊 Lulu Dubai Sales Performance Dashboard")
st.markdown("This dashboard provides insights into sales across various product categories and customer segments in the Middle Eastern region.")

# Top KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales (AED)", f"{filtered_df['Sales_Amount_AED'].sum():,.0f}")
col2.metric("Total Transactions", len(filtered_df))
col3.metric("Avg. Ticket Size", f"{filtered_df['Sales_Amount_AED'].mean():,.2f}")
col4.metric("Avg. Visit Freq", f"{filtered_df['Monthly_Visit_Frequency'].mean():.1f}")

st.divider()

# Row 1: Charts
c1, c2 = st.columns(2)

with c1:
    st.subheader("Sales by Product Category")
    cat_sales = filtered_df.groupby('Product_Category')['Sales_Amount_AED'].sum().reset_index().sort_values('Sales_Amount_AED', ascending=True)
    fig_cat = px.bar(cat_sales, x='Sales_Amount_AED', y='Product_Category', orientation='h', 
                     color='Sales_Amount_AED', color_continuous_scale='Viridis')
    st.plotly_chart(fig_cat, use_container_width=True)

with c2:
    st.subheader("Sales Contribution by Segment")
    fig_pie = px.pie(filtered_df, values='Sales_Amount_AED', names='Customer_Segment', hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

# Row 2: Trends and Locations
c3, c4 = st.columns(2)

with c3:
    st.subheader("Sales Trend (Daily)")
    daily_sales = filtered_df.groupby('Transaction_Date')['Sales_Amount_AED'].sum().reset_index()
    fig_trend = px.line(daily_sales, x='Transaction_Date', y='Sales_Amount_AED')
    st.plotly_chart(fig_trend, use_container_width=True)

with c4:
    st.subheader("Top Locations by Revenue")
    loc_sales = filtered_df.groupby('Store_Location')['Sales_Amount_AED'].sum().reset_index().sort_values('Sales_Amount_AED', ascending=False)
    fig_loc = px.bar(loc_sales, x='Store_Location', y='Sales_Amount_AED', color='Store_Location')
    st.plotly_chart(fig_loc, use_container_width=True)

# Data Table
st.subheader("Raw Data View")
st.dataframe(filtered_df, use_container_width=True)
