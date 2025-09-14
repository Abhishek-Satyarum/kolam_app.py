import streamlit as st
import matplotlib.pyplot as plt

# === Streamlit UI ===
st.set_page_config(page_title="Kolam Diamonds Continuous Border", layout="wide")
st.title("✨ Kolam Diamonds - Continuous Border")

# --- Controls ---
max_dots = st.slider("Max Dots in Middle Rows", 3, 9, 5)
dot_color = st.color_picker("Dot Color", "#FFFFFF")
line_color = st.color_picker("Line Color", "#FFFFFF")
bg_color = st.color_picker("Background Color", "#000000")
line_width = st.slider("Line Width", 1.0, 5.0, 2.0)
dot_size = st.slider("Dot Size", 30, 100, 50)

# === Button to generate ===
if st.button("Generate Kolam"):
    rows = max_dots + 1
    pattern = []

    # Build pattern counts for rows
    for i in range(rows):
        if i < rows//2:
            count = 1 + 2*i
        else:
            count = 1 + 2*(rows - i - 1)
        pattern.append(count)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_facecolor(bg_color)
    ax.axis('off')

    spacing = 1.2
    y = 0
    dot_positions = []

    # Place dots
    for count in pattern:
        x_offset = -(count-1)/2 * spacing
        for j in range(count):
            dot_positions.append((x_offset + j*spacing, -y))
            ax.scatter(x_offset + j*spacing, -y, s=dot_size, color=dot_color)
        y += spacing

    # Draw diamonds
    def draw_diamond(x, y, s):
        pts = [(x, y+s/2), (x+s/2, y), (x, y-s/2), (x-s/2, y), (x, y+s/2)]
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=line_color, lw=line_width)

    border_dots = []
    for x, y in dot_positions:
        row_idx = int(abs(y)//spacing)
        xs_at_row = [px for px,py in dot_positions if py==y]
        if (row_idx == 0 or row_idx == len(pattern)-1 or
            x == min(xs_at_row) or x == max(xs_at_row)):
            border_dots.append((x, y))

    # Draw diamonds for non-border dots
    for x, y in dot_positions:
        if (x, y) not in border_dots:
            draw_diamond(x, y, s=spacing)

    # Connect border dots to form continuous border
    for x, y in border_dots:
        # Horizontal connections
        for x2, y2 in border_dots:
            if abs(y - y2) < 1e-6 and abs(x - x2 - spacing) < 1e-6:
                ax.plot([x, x2], [y, y2], color=line_color, lw=line_width)
        # Diagonal connections
        for x2, y2 in border_dots:
            if abs(abs(x - x2) - spacing) < 1e-6 and abs(abs(y - y2) - spacing) < 1e-6:
                ax.plot([x, x2], [y, y2], color=line_color, lw=line_width)

    ax.set_aspect('equal')
    st.pyplot(fig)

