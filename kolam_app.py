import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Kolam Generator", layout="wide")
st.title("✨ Kolam Pattern Generator")

# === Sidebar Controls ===
kolam_type = st.selectbox(
    "Choose Kolam Type:",
    ["Straight Lines", "Connected Diamonds", "Diamond with Arcs", "Loops/Arcs", "Mixed"]
)
size = st.slider("Grid Size (dots per side):", 4, 12, 7)
line_color = st.color_picker("Kolam Line Color:", "#8B0000")
dot_color = st.color_picker("Dot Color:", "#000000")
bg_color = st.color_picker("Background Color:", "#FFFFFF")
line_width = st.slider("Line Width:", 1.0, 5.0, 2.0)
show_dots = st.checkbox("Show Dots", value=True)

# === Utility Functions ===
def draw_diamond(ax, x, y, s=1):
    points = [(x, y+s/2), (x+s/2, y), (x, y-s/2), (x-s/2, y), (x, y+s/2)]
    xs, ys = zip(*points)
    ax.plot(xs, ys, color=line_color, lw=line_width)

def draw_arc(ax, x, y, r=0.5, start=0, end=180):
    theta = np.linspace(np.radians(start), np.radians(end), 100)
    ax.plot(x + r*np.cos(theta), y + r*np.sin(theta), color=line_color, lw=line_width)

def draw_loop(ax, x, y, r=0.5):
    theta = np.linspace(0, 2*np.pi, 200)
    ax.plot(x + r*np.cos(theta), y + r*np.sin(theta), color=line_color, lw=line_width)

def draw_straight(ax, n, spacing):
    for i in range(n):
        ax.plot([0, (n-1)*spacing], [i*spacing, i*spacing], color=line_color, lw=line_width)
        ax.plot([i*spacing, i*spacing], [0, (n-1)*spacing], color=line_color, lw=line_width)

def draw_border_arcs(ax, n, spacing):
    """Draw arcs perfectly connecting to diamond corners, skipping corners."""
    r = spacing/2.0  # Radius adjusted to touch diamond corners
    offset = spacing/2.0

    # Top border arcs
    for i in range(1, n-2):
        x = i*spacing + offset - spacing
        y = (n-1)*spacing + 0.01
        draw_arc(ax, x, y, r=r, start=0, end=180)

    # Bottom border arcs
    for i in range(1, n-2):
        x = i*spacing + offset - spacing
        y = -0.01
        draw_arc(ax, x, y, r=r, start=180, end=360)

    # Left border arcs
    for j in range(1, n-2):
        y = j*spacing + offset - spacing
        x = -0.01
        draw_arc(ax, x, y, r=r, start=270, end=450)

    # Right border arcs
    for j in range(1, n-2):
        y = j*spacing + offset - spacing
        x = (n-1)*spacing + 0.01
        draw_arc(ax, x, y, r=r, start=90, end=270)

def generate_kolam(n):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_facecolor(bg_color)
    ax.axis("off")
    spacing = 1

    # Draw dots
    if show_dots:
        for i in range(n):
            for j in range(n):
                ax.plot(i*spacing, j*spacing, 'o', color=dot_color, markersize=5)

    if kolam_type == "Straight Lines":
        draw_straight(ax, n, spacing)

    elif kolam_type == "Connected Diamonds":
        for i in range(n-1):
            for j in range(n-1):
                draw_diamond(ax, (i+0.5)*spacing, (j+0.5)*spacing, s=spacing)

    elif kolam_type == "Diamond with Arcs":
        for i in range(n-1):
            for j in range(n-1):
                draw_diamond(ax, (i+0.5)*spacing, (j+0.5)*spacing, s=spacing)
        draw_border_arcs(ax, n, spacing)

    elif kolam_type == "Loops/Arcs":
        for i in range(n):
            for j in range(n):
                draw_loop(ax, i*spacing, j*spacing, r=spacing/2.2)

    elif kolam_type == "Mixed":
        for i in range(n-1):
            for j in range(n-1):
                if (i+j) % 2 == 0:
                    draw_diamond(ax, (i+0.5)*spacing, (j+0.5)*spacing, s=spacing)
                else:
                    draw_loop(ax, (i+0.5)*spacing, (j+0.5)*spacing, r=spacing/2.2)
        draw_border_arcs(ax, n, spacing)

    ax.set_aspect("equal")
    st.pyplot(fig)

# === Button ===
if st.button("🎨 Generate Kolam"):
    generate_kolam(size)

