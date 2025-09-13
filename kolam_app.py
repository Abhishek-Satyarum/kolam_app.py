import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# ---------- Drawing Functions ----------
def draw_diamond(ax, x, y, size=1, color='red', lw=2):
    angle = np.pi / 4
    pts = []
    for i in range(4):
        theta = angle + i * np.pi / 2
        pts.append((x + size*np.cos(theta), y + size*np.sin(theta)))
    pts.append(pts[0])
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=lw)

def draw_arc(ax, center, radius, theta1, theta2, color='red', lw=2):
    theta = np.linspace(np.radians(theta1), np.radians(theta2), 100)
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)
    ax.plot(x, y, color=color, lw=lw)

def draw_connected_diamonds(ax, n, with_arcs=False, color='red', lw=2):
    for i in range(n):
        for j in range(n):
            x, y = i*2, j*2
            draw_diamond(ax, x, y, color=color, lw=lw)
            if with_arcs:
                r = 1.4
                # Rotated arcs to form closed loops
                draw_arc(ax, (x, y+r), r, 0, 180, color, lw)      # Top
                draw_arc(ax, (x, y-r), r, 180, 360, color, lw)    # Bottom
                draw_arc(ax, (x-r, y), r, 90, 270, color, lw)     # Left
                draw_arc(ax, (x+r, y), r, -90, 90, color, lw)     # Right

def draw_loops(ax, n, color='blue', lw=2):
    for i in range(n):
        for j in range(n):
            circle = plt.Circle((i*2, j*2), 0.8, fill=False, color=color, lw=lw)
            ax.add_artist(circle)

def draw_straight(ax, n, color='green', lw=2):
    for i in range(n):
        ax.plot([0, (n-1)*2], [i*2, i*2], color=color, lw=lw)
        ax.plot([i*2, i*2], [0, (n-1)*2], color=color, lw=lw)

def draw_mixed(ax, n, color='purple', lw=2):
    for i in range(n):
        for j in range(n):
            if (i+j) % 2 == 0:
                draw_diamond(ax, i*2, j*2, size=1, color=color, lw=lw)
            else:
                circle = plt.Circle((i*2, j*2), 0.8, fill=False, color=color, lw=lw)
                ax.add_artist(circle)

# ---------- Streamlit UI ----------
st.title("🎨 Kolam Design Generator")

kolam_type = st.selectbox(
    "Kolam Type",
    [
        "Connected Diamonds",
        "Connected Diamonds with Arcs",
        "Loops Only",
        "Straight Lines",
        "Mixed (Diamonds + Loops)"
    ]
)

dots = st.slider("Grid Size (dots):", 3, 10, 5)
line_color = st.color_picker("Pick Line Color:", "#FF0000")
line_width = st.slider("Line Width:", 1.0, 5.0, 2.0)
show_dots = st.checkbox("Show grid dots", value=True)

# ---------- Generate Button ----------
if st.button("🎨 Generate Kolam"):
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_aspect('equal')
    ax.axis('off')

    if kolam_type == "Connected Diamonds":
        draw_connected_diamonds(ax, dots, with_arcs=False, color=line_color, lw=line_width)
    elif kolam_type == "Connected Diamonds with Arcs":
        draw_connected_diamonds(ax, dots, with_arcs=True, color=line_color, lw=line_width)
    elif kolam_type == "Loops Only":
        draw_loops(ax, dots, color=line_color, lw=line_width)
    elif kolam_type == "Straight Lines":
        draw_straight(ax, dots, color=line_color, lw=line_width)
    elif kolam_type == "Mixed (Diamonds + Loops)":
        draw_mixed(ax, dots, color=line_color, lw=line_width)

    # Draw dots
    if show_dots:
        for i in range(dots):
            for j in range(dots):
                ax.plot(i*2, j*2, 'o', color='black', markersize=4)

    st.pyplot(fig)
