import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

st.set_page_config(page_title="Supply Chain Analytics Dashboard", layout="wide")
st.title("📦 Supply Chain Analytics Dashboard")
st.markdown("**Tech Stack: Python, SQL, Tableau Ready**")

@st.cache_data
def load_data_from_sql():
    conn = sqlite3.connect('supply_chain.db')
    try:
        df = pd.read_sql("SELECT * FROM orders", conn)
    except:
        df_excel = pd.read_excel("SupplyChainData.xlsx", parse_dates=['Date'])
        df_excel.to_sql('orders', conn, if_exists='replace', index=False)
        df = pd.read_sql("SELECT * FROM orders", conn)
    conn.close()
    return df

df = load_data_from_sql()

conn = sqlite3.connect('supply_chain.db')
total_orders = pd.read_sql("SELECT COUNT(DISTINCT Order_ID) as cnt FROM orders", conn).iloc[0]['cnt']
on_time_rate = pd.read_sql("SELECT ROUND(AVG(CASE WHEN Delivery_Status='On-Time' THEN 100.0 ELSE 0 END),2) as rate FROM orders", conn).iloc[0]['rate']
avg_lead_time = pd.read_sql("SELECT ROUND(AVG(Lead_Time_Days),2) as avg FROM orders", conn).iloc[0]['avg']
conn.close()

col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", total_orders)
col2.metric("On-Time Delivery %", f"{on_time_rate}%")
col3.metric("Avg Lead Time", f"{avg_lead_time} days")
st.markdown("---")

st.subheader("1. 📊 Inventory Tracking")
conn = sqlite3.connect('supply_chain.db')
inv_df = pd.read_sql("SELECT Warehouse, SUM(Inventory_Level) as Total_Inventory FROM orders GROUP BY Warehouse", conn)
conn.close()
fig1 = px.bar(inv_df, x='Warehouse', y='Total_Inventory')
st.plotly_chart(fig1, use_container_width=True)

st.subheader("2. 🚚 Supplier Performance")
conn = sqlite3.connect('supply_chain.db')
sup_df = pd.read_sql("SELECT Supplier, Lead_Time_Days FROM orders", conn)
conn.close()
fig2 = px.box(sup_df, x='Supplier', y='Lead_Time_Days')
st.plotly_chart(fig2, use_container_width=True)

st.subheader("3. 📦 Delivery Monitoring")
conn = sqlite3.connect('supply_chain.db')
del_df = pd.read_sql("SELECT Delivery_Status, COUNT(*) as cnt FROM orders GROUP BY Delivery_Status", conn)
conn.close()
fig3 = px.pie(del_df, names='Delivery_Status', values='cnt')
st.plotly_chart(fig3, use_container_width=True)

st.subheader("4. 📈 Demand Forecasting")
conn = sqlite3.connect('supply_chain.db')
demand_df = pd.read_sql("SELECT Date, SUM(Quantity) as Total_Quantity FROM orders GROUP BY Date ORDER BY Date", conn)
conn.close()
fig4 = px.line(demand_df, x='Date', y='Total_Quantity')
st.plotly_chart(fig4, use_container_width=True)
