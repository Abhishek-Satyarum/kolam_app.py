import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Kolam Diamond Pattern", layout="wide")
st.title("✨ Kolam Diamond Pattern Generator")

# === User Controls ===
max_dots = st.slider("Max dots (mid rows):", 3, 12, 6)
dot_color = st.color_picker("Dot Color:", "#000000")
line_color = st.color_picker("Line Color:", "#B22222")
bg_color = st.color_picker("Background Color:", "#FFFFFF")
line_width = st.slider("Line Width:", 1.0, 5.0, 2.0)

spacing = 1.0  # Even spacing between dots

# === Generate Button ===
if st.button("🎨 Generate Kolam"):
    rows = max_dots + 1  # Total rows
    dots_per_row = []    # Store number of dots for each row

    # Build the top half pattern (including mid rows)
    for i in range(rows):
        if i == 0 or i == rows-1:
            dots_per_row.append(1)  # Top and bottom always 1
        elif i in [rows//2 - 1, rows//2]:  # Mid two rows = max_dots
            dots_per_row.append(max_dots)
        else:
            # Gradual increase/decrease
            step = min(i, rows-1-i)
            dots = 1 + 2*(step)
            dots = min(dots, max_dots)
            dots_per_row.append(dots)

    # === Compute Dot Positions ===
    coords = []
    y = 0
    for dots in dots_per_row:
        start_x = -(dots-1)/2 * spacing  # Center align
        for j in range(dots):
            coords.append((start_x + j*spacing, y))
        y -= spacing  # Move down for next row

    # === Plotting ===
    fig, ax = plt.subplots(figsize=(8,8))
    ax.set_facecolor(bg_color)
    ax.axis("off")

    # Draw dots
    for x, y in coords:
        ax.plot(x, y, 'o', color=dot_color, markersize=8)

    # Draw diamonds excluding border dots
    # Border dots = first and last row or dots on edges of a row
    for idx, (x, y) in enumerate(coords):
        # Find neighbors (up, down, left, right)
        # A dot is considered border if it is at the outer edge
        # Find nearest dots vertically and horizontally
        # Check if this dot is border by row count
        row_idx = None
        count = 0
        total = 0
        # Find which row this dot belongs to
        total = 0
        for ridx, count in enumerate(dots_per_row):
            if idx < total + count:
                row_idx = ridx
                break
            total += count
        pos_in_row = idx - total

        # Skip border rows
        if row_idx == 0 or row_idx == rows-1:
            continue
        # Skip first and last in the row (border dots)
        if pos_in_row == 0 or pos_in_row == dots_per_row[row_idx]-1:
            continue

        # Find neighbors for diamonds (connect to up, down, left, right)
        # Find dot above (same pos_in_row in previous row or closest)
        def get_dot(row, pos):
            count_before = sum(dots_per_row[:row])
            if pos < 0 or pos >= dots_per_row[row]:
                return None
            return coords[count_before + pos]

        # Horizontal neighbors
        left = get_dot(row_idx, pos_in_row-1)
        right = get_dot(row_idx, pos_in_row+1)

        # Vertical neighbors: choose closest based on x
        up_row = row_idx-1
        down_row = row_idx+1
        # Find closest x in up row
        up_positions = [get_dot(up_row, k) for k in range(dots_per_row[up_row])]
        down_positions = [get_dot(down_row, k) for k in range(dots_per_row[down_row])]
        up = min(up_positions, key=lambda p: abs(p[0]-x)) if up_positions else None
        down = min(down_positions, key=lambda p: abs(p[0]-x)) if down_positions else None

        for neighbor in [left, right, up, down]:
            if neighbor:
                ax.plot([x, neighbor[0]], [y, neighbor[1]], color=line_color, lw=line_width)

    ax.set_aspect('equal')
    st.pyplot(fig)

