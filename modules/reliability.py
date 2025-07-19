import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

# Utility: Convert matplotlib figure to downloadable link
def fig_to_download_link(fig, filename):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    href = f'<a href="data:image/png;base64,{b64}" download="{filename}">📥 Download {filename}</a>'
    return href

# Main render function
def render(df):
    st.header("🔍 Reliability Analysis")

    # --- Data Quality Summary ---
    st.subheader("📊 Data Quality Summary")

    # Missing values percentage
    missing_values_percent = (df.isnull().sum() / len(df)) * 100

    # Numeric columns for COV
    numeric_df = df.select_dtypes(include=np.number)

    # Coefficient of Variation (COV)
    cov_values = numeric_df.apply(
        lambda x: (x.std() / x.mean()) * 100 if x.mean() != 0 and x.std() is not np.nan and x.nunique() > 1 else np.nan
    )

    # Create summary table
    reliability_summary = pd.DataFrame({
        'Missing Values (%)': missing_values_percent,
        'Coefficient of Variation (COV %)': cov_values
    })

    reliability_summary = reliability_summary.loc[numeric_df.columns]  # focus only on numeric

    st.dataframe(reliability_summary.round(2), use_container_width=True)

    # --- Smart Warnings ---
    high_missing = reliability_summary[reliability_summary['Missing Values (%)'] > 20]
    high_cov = reliability_summary[reliability_summary['Coefficient of Variation (COV %)'] > 100]

    if not high_missing.empty:
        st.warning(f"⚠️ {len(high_missing)} column(s) have more than **20% missing values**.")
        st.dataframe(high_missing.round(2))

    if not high_cov.empty:
        st.warning(f"⚠️ {len(high_cov)} column(s) have **COV > 100%** (very high variability).")
        st.dataframe(high_cov.round(2))

    # --- Visualization: Missing Values ---
    st.subheader("📉 Missing Values per Column")

    reliability_summary_sorted_missing = reliability_summary.sort_values('Missing Values (%)', ascending=False)

    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.barplot(
        x=reliability_summary_sorted_missing.index,
        y='Missing Values (%)',
        data=reliability_summary_sorted_missing,
        palette='viridis',
        ax=ax1
    )
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90)
    ax1.set_ylabel("Missing Values (%)")
    ax1.set_title("Percentage of Missing Values per Column")
    st.pyplot(fig1)
    st.markdown(fig_to_download_link(fig1, "missing_values.png"), unsafe_allow_html=True)

    # --- Visualization: COV ---
    st.subheader("📉 Coefficient of Variation per Column")

    reliability_summary_sorted_cov = reliability_summary.dropna(subset=['Coefficient of Variation (COV %)']) \
        .sort_values('Coefficient of Variation (COV %)', ascending=False)

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.barplot(
        x=reliability_summary_sorted_cov.index,
        y='Coefficient of Variation (COV %)',
        data=reliability_summary_sorted_cov,
        palette='plasma',
        ax=ax2
    )
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90)
    ax2.set_ylabel("COV (%)")
    ax2.set_title("Coefficient of Variation per Column")
    st.pyplot(fig2)
    st.markdown(fig_to_download_link(fig2, "cov_plot.png"), unsafe_allow_html=True)
