import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dot Pattern Kolam", layout="wide")
st.title("✨ Dot Pattern Kolam Generator")

# === User Inputs ===
min_dots = st.number_input("Enter minimum dots:", min_value=1, value=1, step=1)
max_dots = st.number_input("Enter maximum dots (odd number preferred):", min_value=3, value=5, step=1)

dot_color = st.color_picker("Dot Color:", "#000000")
line_color = st.color_picker("Line Color:", "#B22222")  # Included for future extensions
bg_color = st.color_picker("Background Color:", "#FFFFFF")
dot_size = st.slider("Dot Size:", 20, 100, 50)

# === Generate Button ===
if st.button("🎨 Generate Kolam"):
    # Ensure max_dots is odd for symmetry
    if max_dots % 2 == 0:
        max_dots += 1

    # Collect coordinates for the pattern
    points = []
    # Top part (increasing dots)
    for i in range(min_dots, max_dots + 1, 2):
        x_start = -(i // 2)
        for k in range(i):
            points.append((x_start + k, (max_dots - i) // 2))

    # Bottom part (decreasing dots)
    for i in range(max_dots - 2, min_dots - 1, -2):
        x_start = -(i // 2)
        for k in range(i):
            points.append((x_start + k, (max_dots - i) // 2 + (max_dots - i) + 2))

    # === Plotting ===
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_facecolor(bg_color)

    # Scatter plot of dots
    xs, ys = zip(*points)
    ax.scatter(xs, ys, s=dot_size, c=dot_color)

    # Formatting the plot
    ax.set_aspect("equal")
    ax.axis("off")
    st.pyplot(fig)
