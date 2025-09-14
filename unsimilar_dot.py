import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Kolam Generator", layout="wide")
st.title("✨ Kolam Pattern Generator")

# === Sidebar Controls ===
max_dots = st.slider("Max Dots in Middle Rows:", 3, 9, 5)
line_color = st.color_picker("Line Color:", "#FFFFFF")
dot_color = st.color_picker("Dot Color:", "#FFFFFF")
bg_color = st.color_picker("Background Color:", "#000000")
line_width = st.slider("Line Width:", 1.0, 5.0, 2.5)
spacing = st.slider("Dot Spacing:", 0.5, 2.0, 1.0)
show_dots = st.checkbox("Show Dots", value=True)

# === Generate Dot Coordinates ===
def generate_dot_positions(max_dots, spacing):
    rows = max_dots + 1
    dot_positions = []
    half = rows // 2
    for i in range(rows):
        if i < half:
            count = 1 + 2 * i
        else:
            count = 1 + 2 * (rows - i - 1)
        offset = -(count - 1) / 2 * spacing
        for j in range(count):
            dot_positions.append((offset + j * spacing, -i * spacing))
    return dot_positions, rows

# === Draw Diamond ===
def draw_diamond(ax, x, y, s=1):
    points = [(x, y + s/2), (x + s/2, y), (x, y - s/2), (x - s/2, y), (x, y + s/2)]
    xs, ys = zip(*points)
    ax.plot(xs, ys, color=line_color, lw=line_width)

# === Determine Border Dots ===
def find_border_indices(dot_positions, rows):
    # Find min/max Y for each row to locate border dots
    borders = set()
    row_dict = {}
    for idx, (x, y) in enumerate(dot_positions):
        row_dict.setdefault(y, []).append(idx)
    for row in row_dict.values():
        if len(row) > 1:
            borders.add(row[0])       # leftmost
            borders.add(row[-1])      # rightmost
        else:
            borders.add(row[0])       # single dot rows
    return borders

# === Generate Kolam ===
def generate_kolam():
    dot_positions, rows = generate_dot_positions(max_dots, spacing)
    borders = find_border_indices(dot_positions, rows)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_facecolor(bg_color)
    ax.axis("off")

    # Draw dots
    if show_dots:
        xs, ys = zip(*dot_positions)
        ax.scatter(xs, ys, color=dot_color, s=40)

    # Draw diamonds for non-border dots
    for idx, (x, y) in enumerate(dot_positions):
        if idx not in borders:
            draw_diamond(ax, x, y, s=spacing)

    # Connect border diamonds to make edges continuous
    for idx1, (x1, y1) in enumerate(dot_positions):
        for idx2, (x2, y2) in enumerate(dot_positions):
            if idx1 < idx2 and abs(x1 - x2) == spacing and abs(y1 - y2) == spacing:
                ax.plot([x1, x2], [y1, y2], color=line_color, lw=line_width)

    ax.set_aspect("equal")
    st.pyplot(fig)

# === Generate Button ===
if st.button("🎨 Generate Kolam"):
    generate_kolam()
