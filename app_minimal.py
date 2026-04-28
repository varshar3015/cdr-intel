import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium
import requests
from datetime import datetime
import io
import re

# Page config
st.set_page_config(
    page_title="CDR Intelligence Platform",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Simple CSS
st.markdown("""
<style>
.main { padding: 2rem; }
.metric-card { 
    background: #f8f9fa; 
    padding: 1rem; 
    border-radius: 8px; 
    border: 1px solid #dee2e6; 
    text-align: center; 
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("CDR Intelligence")
    page = st.radio("Select Module", ["Cell Tower Intelligence", "CDR Analysis"])

if page == "Cell Tower Intelligence":
    st.title("Cell Tower Intelligence")
    st.info("Locate cell tower positions using cellular parameters")
    
    # Demo mode enabled by default
    demo_mode = st.checkbox("Demo Mode", value=True)
    
    col1, col2 = st.columns(2)
    with col1:
        mcc = st.number_input("MCC", value=404)
        lac = st.number_input("LAC", value=1001)
    with col2:
        mnc = st.number_input("MNC", value=10)
        cid = st.number_input("CID", value=12345)
    
    if st.button("Locate Tower"):
        if demo_mode:
            # Bangalore coordinates
            lat, lon = 12.9716, 77.5946
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Latitude", f"{lat:.6f}")
            with col2:
                st.metric("Longitude", f"{lon:.6f}")
            with col3:
                st.metric("Accuracy", "500m")
            
            # Create map
            m = folium.Map(location=[lat, lon], zoom_start=15)
            folium.Marker([lat, lon], popup="Cell Tower").add_to(m)
            st_folium(m, width=700, height=500)
        else:
            st.error("API key required for real geolocation")

else:
    st.title("CDR Analysis")
    st.info("Upload call detail records for analysis")
    
    uploaded_file = st.file_uploader("Upload CDR File", type=["csv", "xlsx"])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success(f"Loaded {len(df)} records")
            
            # Basic analysis
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Records", len(df))
            with col2:
                st.metric("Columns", len(df.columns))
            with col3:
                st.metric("Data Types", df.dtypes.nunique())
            
            # Show data
            st.subheader("Data Preview")
            st.dataframe(df.head())
            
            # Simple chart if numeric columns exist
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                st.subheader("Data Distribution")
                col = st.selectbox("Select column", numeric_cols)
                fig = px.histogram(df, x=col)
                st.plotly_chart(fig)
                
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
    else:
        st.info("Upload a CSV or Excel file to begin analysis")

st.markdown("---")
st.markdown("**CDR Intelligence Platform v2.0** - Professional Call Detail Record Analysis")