
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def render(df):
    st.header("📈 Statistical Analysis")
    numeric_cols = df.select_dtypes(include='number').columns.tolist()

    if not numeric_cols:
        st.error("No numeric columns found in the uploaded file.")
        return

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Descriptive Statistics",
        "🧮 Correlation Heatmap",
        "📉 Histogram",
        "📦 Box Plot"
    ])

    with tab1:
        st.subheader("Descriptive Statistics")
        desc_stats = df[numeric_cols].describe().T
        st.dataframe(desc_stats)

        st.markdown("### 🧠 Interpretation")
        st.markdown("""
        - **Mean** and **Median** close together indicates symmetric distribution.
        - **High Std Dev** indicates more variation (heterogeneous soil).
        - Watch for **Min** or **Max** values that deviate sharply — may indicate errors or changes in soil layer.
        """)

    with tab2:
        st.subheader("Correlation Heatmap")
        corr_matrix = df[numeric_cols].corr()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        st.pyplot(fig)

        st.markdown("### 🧠 Interpretation")
        st.markdown("""
        - Correlation close to +1 or -1 indicates strong linear relationship.
        - For example, **SPT** may correlate with **Gravel %** or negatively with **Moisture %**.
        - Helps identify redundant parameters or hidden patterns.
        """)

    with tab3:
        st.subheader("Histogram")
        selected_col = st.selectbox("Choose a column to plot", numeric_cols, key="hist_select")
        fig, ax = plt.subplots()
        sns.histplot(df[selected_col].dropna(), kde=True, ax=ax, bins='auto', color='skyblue')
        ax.set_title(f"Histogram of {selected_col}")
        st.pyplot(fig)

        st.markdown("### 🧠 Interpretation")
        st.markdown("""
        - Histogram shows the distribution shape of the variable.
        - **Bell-shaped** → likely normal distribution.
        - **Skewed** → may indicate special treatment in geotechnical decisions.
        - **KDE curve** helps visualize smooth probability distribution.
        """)

    with tab4:
        st.subheader("Box Plot")
        selected_col = st.selectbox("Choose a column for Box Plot", numeric_cols, key="box_select")
        fig, ax = plt.subplots()
        sns.boxplot(x=df[selected_col], color='lightgreen', ax=ax)
        ax.set_title(f"Box Plot of {selected_col}")
        st.pyplot(fig)

        st.markdown("### 🧠 Interpretation")
        st.markdown("""
        - Box plot shows median, quartiles, and outliers.
        - Points outside whiskers = **potential outliers** (extreme soil behaviors).
        - Helps detect anomalies before reliability or clustering analysis.
        """)
