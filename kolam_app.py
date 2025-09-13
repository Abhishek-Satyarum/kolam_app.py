import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon, Arc

# --- Streamlit UI ---
st.set_page_config(page_title="Advanced Kolam Generator", layout="centered")
st.title("✨ Advanced Kolam Generator")
st.markdown("Choose a style and customize your Kolam.")

kolam_type = st.selectbox(
    "Kolam Style",
    ["Diamonds", "Loops", "Mixed", "Straight Lines", "Diamonds + Border Arcs"]
)
size = st.slider("Grid Size (dots per side):", 3, 10, 5)
line_color = st.color_picker("Kolam Line Color:", "#FFFFFF")
dot_color = st.color_picker("Dot Color:", "#FFFFFF")
bg_color = st.color_picker("Background Color:", "#000000")
line_width = st.slider("Line Width:", 1.0, 5.0, 2.0)
show_dots = st.checkbox("Show Dots", value=True)

# --- Helper Functions ---
def draw_diamond(ax, x, y, size=0.4):
    pts = [(x, y+size), (x+size, y), (x, y-size), (x-size, y), (x, y+size)]
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=line_color, lw=line_width)

def draw_arc(ax, x, y, r=0.4, start=0, end=90):
    theta = np.linspace(np.radians(start), np.radians(end), 50)
    ax.plot(x + r*np.cos(theta), y + r*np.sin(theta), color=line_color, lw=line_width)

def draw_line(ax, x1, y1, x2, y2):
    ax.plot([x1, x2], [y1, y2], color=line_color, lw=line_width)

# --- Kolam Generator ---
def generate_kolam(n, style):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_facecolor(bg_color)
    ax.axis('off')

    spacing = 1

    # Draw dots
    if show_dots:
        for i in range(n):
            for j in range(n):
                ax.plot(i * spacing, j * spacing, 'o', color=dot_color, markersize=5)

    for i in range(n):
        for j in range(n):
            x, y = i * spacing, j * spacing

            if style == "Diamonds":
                draw_diamond(ax, x, y)

            elif style == "Loops":
                draw_arc(ax, x, y, r=0.4, start=0, end=90)
                draw_arc(ax, x, y, r=0.4, start=90, end=180)
                draw_arc(ax, x, y, r=0.4, start=180, end=270)
                draw_arc(ax, x, y, r=0.4, start=270, end=360)

            elif style == "Mixed":
                if (i + j) % 2 == 0:
                    draw_diamond(ax, x, y)
                else:
                    draw_arc(ax, x, y, r=0.4, start=0, end=360)

            elif style == "Straight Lines":
                if i < n-1:
                    draw_line(ax, x, y, (i+1)*spacing, y)
                if j < n-1:
                    draw_line(ax, x, y, x, (j+1)*spacing)

            elif style == "Diamonds + Border Arcs":
                draw_diamond(ax, x, y)
                # Border arcs
                if j == 0 and 0 < i < n-1:
                    draw_arc(ax, x, y, r=0.5, start=180, end=360)
                if j == n-1 and 0 < i < n-1:
                    draw_arc(ax, x, y, r=0.5, start=0, end=180)
                if i == 0 and 0 < j < n-1:
                    draw_arc(ax, x, y, r=0.5, start=270, end=450)
                if i == n-1 and 0 < j < n-1:
                    draw_arc(ax, x, y, r=0.5, start=90, end=270)

    plt.gca().invert_yaxis()
    ax.set_aspect("equal")
    st.pyplot(fig)

# --- Button ---
if st.button("🎨 Generate Kolam"):
    generate_kolam(size, kolam_type)
