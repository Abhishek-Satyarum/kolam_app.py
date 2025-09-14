import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Kolam Dot Pattern", layout="wide")
st.title("✨ Kolam Dot Pattern Generator")

# === User Controls ===
max_dots = st.slider("Maximum Dots (mid rows):", 3, 15, 5)
dot_color = st.color_picker("Dot Color:", "#FFFFFF")
bg_color = st.color_picker("Background Color:", "#000000")
spacing = st.slider("Dot Spacing:", 0.5, 2.0, 1.0)

# === Generate Pattern ===
def generate_dots(max_dots):
    rows = max_dots + 1  # Total rows
    pattern = []
    
    # First half (increasing rows)
    for i in range((rows // 2)):
        if i == rows // 2 - 1:  # Mid-two rows
            pattern.append(max_dots)
            pattern.append(max_dots)
        else:
            dots = 1 + 2*i if 1 + 2*i < max_dots else max_dots
            pattern.append(dots)
    
    # Bottom rows (mirror)
    while len(pattern) < rows:
        pattern.append(pattern[rows - len(pattern) - 1])
    
    return pattern

# === Plot Pattern ===
def plot_pattern(max_dots, dot_color, bg_color, spacing):
    pattern = generate_dots(max_dots)
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_facecolor(bg_color)
    ax.axis("off")
    
    y = 0
    for dots in pattern:
        # Centering: compute starting x so pattern is symmetric
        start_x = -(dots-1)/2 * spacing
        for i in range(dots):
            ax.plot(start_x + i*spacing, y, 'o', color=dot_color, markersize=10)
        y -= spacing  # Move down to next row
    
    ax.set_aspect('equal')
    st.pyplot(fig)

# === Button ===
if st.button("🎨 Generate Kolam"):
    plot_pattern(max_dots, dot_color, bg_color, spacing)
