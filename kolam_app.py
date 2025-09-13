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
size = st.slider("Grid Size (dots per side):", 4, 10, 6)
line_color = st.color_picker("Kolam Line Color:", "#B22222")
dot_color = st.color_picker("Dot Color:", "#000000")
bg_color = st.color_picker("Background Color:", "#FFFFFF")
line_width = st.slider("Line Width:", 1.0, 5.0, 2.0)
show_dots = st.checkbox("Show Dots", value=True)

# === Drawing Functions ===
def draw_diamond(ax, x, y, s=1):
    points = [(x, y+s/2), (x+s/2, y), (x, y-s/2), (x-s/2, y), (x, y+s/2)]
    xs, ys = zip(*points)
    ax.plot(xs, ys, color=line_color, lw=line_width)

def draw_arc(ax, x, y, r, start, end):
    theta = np.linspace(np.radians(start), np.radians(end), 100)
    ax.plot(x + r*np.cos(theta), y + r*np.sin(theta), color=line_color, lw=line_width)

# === Kolam Generator ===
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

    if kolam_type in ["Connected Diamonds", "Diamond with Arcs"]:
        # Diamonds
        for i in range(n-1):
            for j in range(n-1):
                draw_diamond(ax, (i+0.5)*spacing, (j+0.5)*spacing, s=spacing)

        if kolam_type == "Diamond with Arcs":
            # Parameters for arcs
            r = 0.5
            offset = 0.3  # bring arcs closer to diamonds

            # Top border arcs
            for i in range(1, n-2):
                draw_arc(ax, (i+0.5)*spacing, (n-1)+offset, r, 180, 360)

            # Bottom border arcs
            for i in range(1, n-2):
                draw_arc(ax, (i+0.5)*spacing, -offset, r, 0, 180)

            # Left border arcs
            for j in range(1, n-2):
                draw_arc(ax, -offset, (j+0.5)*spacing, r, 270, 450)

            # Right border arcs
            for j in range(1, n-2):
                draw_arc(ax, (n-1)+offset, (j+0.5)*spacing, r, 90, 270)

    elif kolam_type == "Straight Lines":
        for i in range(n):
            ax.plot([0, (n-1)*spacing], [i*spacing, i*spacing],
                    color=line_color, lw=line_width)
            ax.plot([i*spacing, i*spacing], [0, (n-1)*spacing],
                    color=line_color, lw=line_width)

    elif kolam_type == "Loops/Arcs":
        for i in range(n):
            for j in range(n):
                theta = np.linspace(0, 2*np.pi, 200)
                ax.plot(i*spacing + 0.5*np.cos(theta),
                        j*spacing + 0.5*np.sin(theta),
                        color=line_color, lw=line_width)

    elif kolam_type == "Mixed":
        for i in range(n-1):
            for j in range(n-1):
                if (i+j) % 2 == 0:
                    draw_diamond(ax, (i+0.5)*spacing, (j+0.5)*spacing, s=spacing)
                else:
                    theta = np.linspace(0, 2*np.pi, 200)
                    ax.plot((i+0.5)*spacing + 0.5*np.cos(theta),
                            (j+0.5)*spacing + 0.5*np.sin(theta),
                            color=line_color, lw=line_width)

    ax.set_aspect("equal")
    st.pyplot(fig)

# === Generate Button ===
if st.button("🎨 Generate Kolam"):
    generate_kolam(size)

