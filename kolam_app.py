import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# ----------- Utility Drawing Functions -----------

def draw_diamond(ax, x, y, size=1, color='red', lw=2):
    # Draw a square rotated 45° (diamond)
    angle = np.pi / 4
    pts = []
    for i in range(4):
        theta = angle + i * np.pi / 2
        pts.append((x + size*np.cos(theta), y + size*np.sin(theta)))
    pts.append(pts[0])
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=lw)

def draw_arc(ax, center, radius, theta1, theta2, color='red', lw=2):
    # Draw a circular arc
    theta = np.linspace(np.radians(theta1), np.radians(theta2), 100)
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)
    ax.plot(x, y, color=color, lw=lw)

def draw_connected_diamonds(ax, n, with_arcs=False):
    for i in range(n):
        for j in range(n):
            x, y = i*2, j*2
            draw_diamond(ax, x, y)
            if with_arcs:
                # Add arcs rotated to form closed loops
                r = 1.4
                # Four corners arcs rotated 180°
                draw_arc(ax, (x, y+r), r, 0, 180)       # Top
                draw_arc(ax, (x, y-r), r, 180, 360)     # Bottom
                draw_arc(ax, (x-r, y), r, 90, 270)      # Left
                draw_arc(ax, (x+r, y), r, -90, 90)      # Right

def draw_loops(ax, n):
    for i in range(n):
        for j in range(n):
            circle = plt.Circle((i*2, j*2), 0.8, fill=False, color='blue', lw=2)
            ax.add_artist(circle)

def draw_straight(ax, n):
    for i in range(n):
        ax.plot([0, (n-1)*2], [i*2, i*2], color='green', lw=2)
        ax.plot([i*2, i*2], [0, (n-1)*2], color='green', lw=2)

def draw_mixed(ax, n):
    for i in range(n):
        for j in range(n):
            if (i+j) % 2 == 0:
                draw_diamond(ax, i*2, j*2, size=1, color='purple', lw=2)
            else:
                circle = plt.Circle((i*2, j*2), 0.8, fill=False, color='purple', lw=2)
                ax.add_artist(circle)

# ----------- Streamlit UI -----------

st.title("🎨 Kolam Design Generator")
st.sidebar.header("Controls")

kolam_type = st.sidebar.selectbox(
    "Choose Kolam Type:",
    [
        "Connected Diamonds",
        "Connected Diamonds with Arcs",
        "Loops Only",
        "Straight Lines",
        "Mixed (Diamonds + Loops)"
    ]
)

dots = st.sidebar.slider("Grid size (dots):", 3, 10, 5)
color = st.sidebar.color_picker("Pick a line color:", "#FF0000")

# ----------- Drawing -----------

fig, ax = plt.subplots(figsize=(6,6))
ax.set_aspect('equal')
ax.axis('off')

if kolam_type == "Connected Diamonds":
    draw_connected_diamonds(ax, dots, with_arcs=False)
elif kolam_type == "Connected Diamonds with Arcs":
    draw_connected_diamonds(ax, dots, with_arcs=True)
elif kolam_type == "Loops Only":
    draw_loops(ax, dots)
elif kolam_type == "Straight Lines":
    draw_straight(ax, dots)
elif kolam_type == "Mixed (Diamonds + Loops)":
    draw_mixed(ax, dots)

# Draw grid dots
for i in range(dots):
    for j in range(dots):
        ax.plot(i*2, j*2, 'o', color='black', markersize=4)

st.pyplot(fig)
