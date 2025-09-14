import streamlit as st
import matplotlib.pyplot as plt

# --- UI Controls ---
st.set_page_config(page_title="Kolam Diamond Generator", layout="wide")
st.title("✨ Kolam Diamond Pattern Generator")

max_dots = st.slider("Max dots in middle rows:", 3, 10, 5)
dot_color = st.color_picker("Dot Color:", "#FFFFFF")
line_color = st.color_picker("Line Color:", "#FFFFFF")
bg_color = st.color_picker("Background Color:", "#000000")
line_width = st.slider("Line Width:", 1.0, 5.0, 2.0)

# --- Helper function to draw a diamond ---
def draw_diamond(ax, x, y, s):
    # Draw small diamond centered at (x,y)
    ax.plot([x, x+s/2], [y, y+s/2], color=line_color, lw=line_width)
    ax.plot([x, x-s/2], [y, y+s/2], color=line_color, lw=line_width)
    ax.plot([x, x+s/2], [y, y-s/2], color=line_color, lw=line_width)
    ax.plot([x, x-s/2], [y, y-s/2], color=line_color, lw=line_width)

# --- Pattern generation ---
def generate_pattern(n):
    rows = n + 1  # total rows of dots
    spacing = 1.0
    fig, ax = plt.subplots(figsize=(8,8))
    ax.set_facecolor(bg_color)
    ax.axis("off")

    # Build the pattern of dots
    dots = []
    half = rows // 2
    for i in range(rows):
        # dots in current row (symmetrical like diamond)
        if i <= half:
            dots_in_row = 1 + 2*i
        else:
            dots_in_row = 1 + 2*(rows-i-1)
        offset = (2*n-1 - dots_in_row) / 2
        for j in range(dots_in_row):
            x = (j + offset) * spacing
            y = -i * spacing
            dots.append((x, y))
            ax.plot(x, y, 'o', color=dot_color)

    # Draw diamonds for inner dots (exclude border dots)
    for x, y in dots:
        # Skip border dots: border dots are those having <4 diagonal neighbors
        neighbors = [
            (x+spacing, y+spacing),
            (x-spacing, y+spacing),
            (x+spacing, y-spacing),
            (x-spacing, y-spacing)
        ]
        neighbor_count = sum(1 for nb in neighbors if nb in dots)
        if neighbor_count == 4:
            draw_diamond(ax, x, y, spacing)

    # Connect inner dots diagonally for continuity
    for x, y in dots:
        neighbors = [
            (x+spacing, y+spacing),
            (x-spacing, y+spacing),
            (x+spacing, y-spacing),
            (x-spacing, y-spacing)
        ]
        for nx, ny in neighbors:
            if (x,y) in dots and (nx,ny) in dots:
                # Only draw if both are non-border (>=3 neighbors)
                nb1 = sum(1 for nb in [
                    (x+spacing, y+spacing), (x-spacing, y+spacing),
                    (x+spacing, y-spacing), (x-spacing, y-spacing)
                ] if nb in dots)
                nb2 = sum(1 for nb in [
                    (nx+spacing, ny+spacing), (nx-spacing, ny+spacing),
                    (nx+spacing, ny-spacing), (nx-spacing, ny-spacing)
                ] if nb in dots)
                if nb1 >= 3 and nb2 >= 3:
                    ax.plot([x,nx], [y,ny], color=line_color, lw=line_width)

    ax.set_aspect('equal')
    return fig

# --- Generate button ---
if st.button("🎨 Generate Kolam"):
    fig = generate_pattern(max_dots)
    st.pyplot(fig)
