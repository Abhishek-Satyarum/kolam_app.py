import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Arc
import random

# ----------- UI -----------
st.title("🎨 Advanced Kolam Generator")
st.markdown(
    "Generate beautiful Kolam (Rangoli) patterns: loops, diamonds, or a stunning mix of both."
)

kolam_type = st.selectbox(
    "Choose Kolam Style:",
    ["Rounded Loops", "Straight Lines", "Diamond Loops", "Mixed Loops & Diamonds"]
)
size = st.slider("Grid Size (dots per side):", 3, 9, 5)
color = st.color_picker("Kolam Line Color:", "#FFFFFF")
bg_color = st.color_picker("Background Color:", "#000000")
dot_color = st.color_picker("Dot Color:", "#FFFFFF")

# ----------- Kolam Generator -----------
def generate_kolam(style, n):
    fig, ax = plt.subplots(figsize=(7,7))
    ax.set_facecolor(bg_color)
    ax.axis("off")

    # Draw dots
    for i in range(n):
        for j in range(n):
            ax.plot(i, j, "o", color=dot_color, markersize=5)

    # Draw patterns
    for i in range(n-1):
        for j in range(n-1):
            if style == "Rounded Loops":
                loop = Arc((i+0.5, j+0.5), 1, 1, angle=0,
                           theta1=0, theta2=360, color=color, lw=2)
                ax.add_patch(loop)

            elif style == "Straight Lines":
                ax.plot([i, i+1], [j, j], color=color, lw=2)
                ax.plot([i, i], [j, j+1], color=color, lw=2)

            elif style == "Diamond Loops":
                diamond = Polygon(
                    [[i+0.5, j],
                     [i+1, j+0.5],
                     [i+0.5, j+1],
                     [i, j+0.5]],
                    closed=True, fill=False, edgecolor=color, lw=2
                )
                ax.add_patch(diamond)

            elif style == "Mixed Loops & Diamonds":
                if random.choice([True, False]):
                    # Draw loop
                    loop = Arc((i+0.5, j+0.5), 1, 1, angle=0,
                               theta1=0, theta2=360, color=color, lw=2)
                    ax.add_patch(loop)
                else:
                    # Draw diamond
                    diamond = Polygon(
                        [[i+0.5, j],
                         [i+1, j+0.5],
                         [i+0.5, j+1],
                         [i, j+0.5]],
                        closed=True, fill=False, edgecolor=color, lw=2
                    )
                    ax.add_patch(diamond)

    ax.set_aspect('equal')
    plt.gca().invert_yaxis()
    st.pyplot(fig)

# ----------- Button -----------
if st.button("Generate Kolam"):
    generate_kolam(kolam_type, size)

