import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cm as cm
import matplotlib

matplotlib.use("Agg")  # Headless for Streamlit

def render(df):
    #st.header("📊 Raw Borelog Visualization")

    if df.empty:
        st.warning("⚠️ No data loaded.")
        return

    if 'BOREHOLE' not in df.columns or 'Depth' not in df.columns:
        st.error("❌ Required columns ('BOREHOLE', 'Depth') are missing.")
        return

    df = df.copy()
    df['Depth'] = pd.to_numeric(df['Depth'], errors='coerce')
    df = df.dropna(subset=['Depth'])

    boreholes = df['BOREHOLE'].dropna().unique().tolist()
    if not boreholes:
        st.warning("⚠️ No borehole names found.")
        return

    selected_borehole = st.selectbox("🕳️ Select Borehole", sorted(boreholes), key="rv_selected_borehole")
    show_plot = st.button("📈 Show Visualization", key="rv_show_button")

    if show_plot:
        st.session_state.rv_last_selected_borehole = selected_borehole

    # Persist result
    if "rv_last_selected_borehole" in st.session_state:
        selected_borehole = st.session_state.rv_last_selected_borehole
        st.markdown(f"🔍 Showing results for: **{selected_borehole}**")

        borehole_data = df[df['BOREHOLE'] == selected_borehole].sort_values(by='Depth')
        if borehole_data.empty:
            st.warning("⚠️ No data found for selected borehole.")
            return

        props = [
            'SPTValue', 'DryDensity', 'WaterContent', 'LiquidLimit', 'PlasticLimit',
            'Gravel', 'SandContent', 'SiltContent', 'ClayContent',
            'Cohesion', 'AngleOfInternalFriction'
        ]
        props = [p for p in props if p in df.columns and pd.api.types.is_numeric_dtype(df[p])]

        layer_col = 'Classification'
        if layer_col not in df.columns:
            st.error("❌ 'Classification' column is missing.")
            return

        borehole_data[layer_col] = borehole_data[layer_col].astype('category')
        unique_layers = borehole_data[layer_col].dropna().unique().tolist()
        cmap = cm.get_cmap('tab10', len(unique_layers))
        layer_colors = {layer: cmap(i) for i, layer in enumerate(unique_layers)}

        fig, axes = plt.subplots(1, len(props) + 1, figsize=(3.5 * (len(props) + 1), 12), sharey=True)
        ax_layer = axes[0]

        for i in range(len(borehole_data)):
            row = borehole_data.iloc[i]
            depth = row['Depth']
            next_depth = borehole_data.iloc[i + 1]['Depth'] if i + 1 < len(borehole_data) else borehole_data['Depth'].max()
            height = next_depth - depth
            if height <= 0:
                continue

            layer = row[layer_col]
            color = layer_colors.get(layer, (0.8, 0.8, 0.8))
            rect = patches.Rectangle((0, depth), 1, height, linewidth=0, facecolor=color, alpha=0.7)
            ax_layer.add_patch(rect)

        ax_layer.set_xlim(0, 1)
        ax_layer.set_xticks([])
        ax_layer.set_title(layer_col)
        ax_layer.set_ylabel("Depth (m)")
        ax_layer.invert_yaxis()

        for i, prop in enumerate(props):
            ax = axes[i + 1]
            sub_df = borehole_data.dropna(subset=[prop])
            if sub_df.empty:
                continue
            ax.plot(sub_df[prop], sub_df['Depth'], marker='o', linestyle='-')
            ax.set_title(prop)
            ax.grid(True)

        st.pyplot(fig)
