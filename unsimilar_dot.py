import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# === Streamlit UI ===
st.set_page_config(page_title="Kolam Diamonds with Loops", layout="wide")
st.title("✨ Kolam Diamonds with Loops")

# --- Controls ---
max_dots = st.slider("Max Dots in Middle Rows", 3, 9, 5)
dot_color = st.color_picker("Dot Color", "#FFFFFF")
line_color = st.color_picker("Line Color", "#FFFFFF")
bg_color = st.color_picker("Background Color", "#000000")
line_width = st.slider("Line Width", 1.0, 5.0, 2.0)
dot_size = st.slider("Dot Size", 30, 100, 50)

# === Generate Dot Pattern ===
rows = max_dots + 1
pattern = []

# Top half (including mid)
for i in range(rows):
    if i < rows//2:
        count = 1 + 2*i
    else:
        count = 1 + 2*(rows - i - 1)
    pattern.append(count)

# === Plot ===
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

# === Draw Diamonds ===
def draw_diamond(x, y, s):
    pts = [(x, y+s/2), (x+s/2, y), (x, y-s/2), (x-s/2, y), (x, y+s/2)]
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=line_color, lw=line_width)

border_dots = []
# Find border dots (top/bottom rows or extreme ends of each row)
for i, (x, y) in enumerate(dot_positions):
    row_idx = int(abs(y)//spacing)
    if (row_idx == 0 or row_idx == len(pattern)-1 or
        x == min(px for px,py in dot_positions if py==y) or
        x == max(px for px,py in dot_positions if py==y)):
        border_dots.append((x, y))

# Draw diamonds for non-border dots
for x, y in dot_positions:
    if (x, y) not in border_dots:
        draw_diamond(x, y, s=spacing)

# === Draw Loops (ovals) around border dots ===
for x, y in border_dots:
    # Create oval arcs using parametric equations
    t = np.linspace(0, 2*np.pi, 200)
    # Oval scale factors to make it slightly elongated
    a = spacing/1.5  # horizontal radius
    b = spacing/2.0  # vertical radius
    ax.plot(x + a*np.cos(t), y + b*np.sin(t), color=line_color, lw=line_width)

ax.set_aspect('equal')
st.pyplot(fig)
