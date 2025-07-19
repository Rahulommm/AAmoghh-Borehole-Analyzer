# app.py
import os
import sys
sys.path.append(os.path.dirname(__file__))

import streamlit as st
import pandas as pd

from modules import (
    raw_visualization, statistics, clustering, reliability,
    probability, bayesian, montecarlo, code_compliance,
    report_generator
)

# ------------------- Configuration ------------------- #
st.set_page_config(page_title="AAmoghh Borehole Analyzer", layout="wide")
st.title("🔎 AAmoghh Borehole Analyzer")

# ------------------- Reset Button ------------------- #
with st.sidebar:
    st.markdown("### 📁 File Upload & Controls")
    if st.button("🔄 Reset Session"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

# ------------------- File Upload ------------------- #
with st.sidebar:
    uploaded_file = st.file_uploader("Upload Borelog CSV", type=["csv"])

# ------------------- Session Initialization ------------------- #
if 'df' not in st.session_state:
    st.session_state.df = None
if 'uploaded_filename' not in st.session_state:
    st.session_state.uploaded_filename = None
if 'selected_borehole' not in st.session_state:
    st.session_state.selected_borehole = None

# ------------------- File Handling ------------------- #
if uploaded_file:
    try:
        df_new = pd.read_csv(uploaded_file)
        df_new.columns = df_new.columns.str.strip()  # Clean column names

        if not df_new.empty:
            st.session_state.df = df_new
            st.session_state.uploaded_filename = uploaded_file.name
            st.success(f"✅ {uploaded_file.name} uploaded successfully!")
        else:
            st.warning("⚠️ Uploaded file is empty.")
    except Exception as e:
        st.error(f"❌ Failed to read CSV: {e}")

df = st.session_state.df if st.session_state.df is not None else pd.DataFrame()

# ------------------- Borehole Selector ------------------- #
if not df.empty and "BOREHOLE" in df.columns:
    boreholes = df["BOREHOLE"].dropna().unique().tolist()
    st.session_state.selected_borehole = st.selectbox("Select Borehole for Module-Level Analysis", boreholes)
    df_borehole = df[df["BOREHOLE"] == st.session_state.selected_borehole]
else:
    df_borehole = pd.DataFrame()

# ------------------- Tabs for Each Module ------------------- #
tabs = st.tabs([
    "1️⃣ Raw Borelog Visualization",
    "2️⃣ Statistical Analysis",
    "3️⃣ K-Means Clustering",
    "4️⃣ Reliability Analysis",
    "5️⃣ Probability Analysis",
    "6️⃣ Bayesian Analysis",
    "7️⃣ Monte Carlo Simulation",
    "8️⃣ Code Compliance",
    "9️⃣ PDF Report Generator"
])

# ------------------- Tab Logic ------------------- #
with tabs[0]:
    st.subheader("Raw Borelog Visualization")
    if not df_borehole.empty:
        raw_visualization.render(df_borehole)
    else:
        st.info("Upload a CSV file with a valid 'BOREHOLE' column to begin.")

with tabs[1]:
    st.subheader("Statistical Analysis")
    if not df.empty:
        statistics.render(df)
    else:
        st.info("Please upload a CSV file.")

with tabs[2]:
    st.subheader("K-Means Clustering")
    if not df.empty:
        clustering.render(df)
    else:
        st.info("Please upload a CSV file.")

with tabs[3]:
    st.subheader("Reliability Analysis")
    if not df.empty:
        reliability.render(df)
    else:
        st.info("Please upload a CSV file.")

with tabs[4]:
    st.subheader("Probability Analysis")
    if not df.empty:
        probability.render(df)
    else:
        st.info("Please upload a CSV file.")

with tabs[5]:
    st.subheader("Bayesian Analysis")
    if not df.empty:
        bayesian.render(df)
    else:
        st.info("Please upload a CSV file.")

with tabs[6]:
    st.subheader("Monte Carlo Simulation")
    if not df.empty:
        montecarlo.render(df)
    else:
        st.info("Please upload a CSV file.")

with tabs[7]:
    st.subheader("Code Compliance (IS/Eurocode)")
    if not df.empty:
        code_compliance.render(df)
    else:
        st.info("Please upload a CSV file.")

with tabs[8]:
    st.subheader("PDF Report Generator")
    if not df.empty:
        report_generator.render(df)
    else:
        st.info("Please upload a CSV file.")
