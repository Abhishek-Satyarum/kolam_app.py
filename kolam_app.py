import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------- UI ----------
st.title("🎨 AI Kolam Generator")
st.markdown("Generate beautiful Kolam (Rangoli) patterns based on your prompt.")

# User inputs
kolam_type = st.selectbox(
    "Choose Kolam Style:",
    ["Rounded Loops", "Straight Lines", "Diamond Loops"]
)
size = st.slider("Grid Size (dots per side):", 3, 9, 5)
color = st.color_picker("Select Kolam Color:", "#FFFFFF")
bg_color = st.color_picker("Select Background Color:", "#000000")

# ---------- Kolam Generation Logic ----------
def generate_kolam(style, n):
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_facecolor(bg_color)
    ax.axis("off")

    # Create dot grid
    x = np.arange(n)
    y = np.arange(n)
    for i in x:
        for j in y:
            ax.plot(i, j, "o", color=color, markersize=4)

    # Draw different styles
    for i in range(n-1):
        for j in range(n-1):
            if style == "Rounded Loops":
                # Rounded bezier-style loops between four dots
                loop = plt.Circle((i+0.5, j+0.5), 0.5, fill=False, color=color, lw=2)
                ax.add_artist(loop)
            elif style == "Straight Lines":
                ax.plot([i, i+1], [j, j], color=color, lw=2)
                ax.plot([i, i], [j, j+1], color=color, lw=2)
            elif style == "Diamond Loops":
                ax.plot([i+0.5, i, i+0.5, i+1, i+0.5],
                        [j, j+0.5, j+1, j+0.5, j], color=color, lw=2)

    ax.set_aspect('equal')
    plt.gca().invert_yaxis()
    st.pyplot(fig)

# ---------- Generate Button ----------
if st.button("Generate Kolam"):
    generate_kolam(kolam_type, size)
