import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import cv2
from io import BytesIO
from PIL import Image

# === APP CONFIG ===
st.set_page_config(page_title="Kolam Suite", layout="wide")
st.title("🌸 Unified Kolam Suite")

# === TABS ===
tab1, tab2, tab3 = st.tabs(["🎨 Kolam Generator (Types)", "🔷 Unsymmetrical Dots Generator", "📊 Kolam Analyzer"])

# --------------------------------------------------------------------------------
# === TAB 1: Previous Generator ===
with tab1:
    st.header("Kolam Pattern Generator (Multiple Types)")
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

    def draw_diamond(ax, x, y, s=1):
        pts = [(x, y+s/2), (x+s/2, y), (x, y-s/2), (x-s/2, y), (x, y+s/2)]
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=line_color, lw=line_width)

    def draw_arc(ax, x, y, r=0.6, start=0, end=180):
        theta = np.linspace(np.radians(start), np.radians(end), 100)
        ax.plot(x + r*np.cos(theta), y + r*np.sin(theta), color=line_color, lw=line_width)

    def draw_loop(ax, x, y, r=0.5):
        theta = np.linspace(0, 2*np.pi, 200)
        ax.plot(x + r*np.cos(theta), y + r*np.sin(theta), color=line_color, lw=line_width)

    def draw_straight(ax, n, spacing):
        for i in range(n):
            ax.plot([0, (n-1)*spacing], [i*spacing, i*spacing], color=line_color, lw=line_width)
            ax.plot([i*spacing, i*spacing], [0, (n-1)*spacing], color=line_color, lw=line_width)

    def generate_kolam(n):
        fig, ax = plt.subplots(figsize=(8,8))
        ax.set_facecolor(bg_color)
        ax.axis("off")
        spacing = 1
        r = 0.5
        offset = 0.01
        if show_dots:
            for i in range(n):
                for j in range(n):
                    ax.plot(i*spacing, j*spacing, 'o', color=dot_color, markersize=5)

        if kolam_type == "Straight Lines":
            draw_straight(ax, n, spacing)
        elif kolam_type == "Connected Diamonds":
            for i in range(n-1):
                for j in range(n-1):
                    draw_diamond(ax, (i+0.5)*spacing, (j+0.5)*spacing, s=spacing)
        elif kolam_type == "Diamond with Arcs":
            for i in range(n-1):
                for j in range(n-1):
                    draw_diamond(ax, (i+0.5)*spacing, (j+0.5)*spacing, s=spacing)
            for i in range(1, n-1):
                draw_arc(ax, (i-0.5)*spacing + r, (n-1)+offset, r=r, start=0, end=180)
                draw_arc(ax, (i-0.5)*spacing + r, -offset, r=r, start=180, end=360)
            for j in range(1, n-1):
                draw_arc(ax, -offset, (j-0.5)*spacing + r, r=r, start=90, end=270)
                draw_arc(ax, (n-1)+offset, (j-0.5)*spacing + r, r=r, start=270, end=450)
        elif kolam_type == "Loops/Arcs":
            for i in range(n):
                for j in range(n):
                    draw_loop(ax, i*spacing, j*spacing, r=spacing/2.2)
        elif kolam_type == "Mixed":
            for i in range(n-1):
                for j in range(n-1):
                    if (i+j) % 2 == 0:
                        draw_diamond(ax, (i+0.5)*spacing, (j+0.5)*spacing, s=spacing)
                    else:
                        draw_loop(ax, (i+0.5)*spacing, (j+0.5)*spacing, r=spacing/2.2)
            for i in range(1, n-1):
                draw_arc(ax, (i-0.5)*spacing, (n-1)+offset, r=r, start=180, end=360)
                draw_arc(ax, (i-0.5)*spacing, -offset, r=r, start=0, end=180)
            for j in range(1, n-1):
                draw_arc(ax, -offset, (j-0.5)*spacing, r=r, start=270, end=450)
                draw_arc(ax, (n-1)+offset, (j-0.5)*spacing, r=r, start=90, end=270)
        ax.set_aspect("equal")
        st.pyplot(fig)

    if st.button("🎨 Generate Kolam", key="tab1"):
        generate_kolam(size)

# --------------------------------------------------------------------------------
# === TAB 2: Unsymmetrical Dots ===
with tab2:
    st.header("Unsymmetrical Dots Kolam Generator")
    max_dots = st.slider("Max Dots in Middle Rows:", 3, 9, 5)
    line_color2 = st.color_picker("Line Color:", "#FFFFFF")
    dot_color2 = st.color_picker("Dot Color:", "#FFFFFF")
    bg_color2 = st.color_picker("Background Color:", "#000000")
    line_width2 = st.slider("Line Width:", 1.0, 5.0, 2.5)
    spacing2 = st.slider("Dot Spacing:", 0.5, 2.0, 1.0)
    show_dots2 = st.checkbox("Show Dots", value=True, key="dots2")

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

    def draw_diamond2(ax, x, y, s=1):
        points = [(x, y + s/2), (x + s/2, y), (x, y - s/2), (x - s/2, y), (x, y + s/2)]
        xs, ys = zip(*points)
        ax.plot(xs, ys, color=line_color2, lw=line_width2)

    def find_border_indices(dot_positions, rows):
        borders = set()
        row_dict = {}
        for idx, (x, y) in enumerate(dot_positions):
            row_dict.setdefault(y, []).append(idx)
        for row in row_dict.values():
            if len(row) > 1:
                borders.add(row[0])
                borders.add(row[-1])
            else:
                borders.add(row[0])
        return borders

    def generate_kolam2():
        dot_positions, rows = generate_dot_positions(max_dots, spacing2)
        borders = find_border_indices(dot_positions, rows)
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_facecolor(bg_color2)
        ax.axis("off")
        if show_dots2:
            xs, ys = zip(*dot_positions)
            ax.scatter(xs, ys, color=dot_color2, s=40)
        for idx, (x, y) in enumerate(dot_positions):
            if idx not in borders:
                draw_diamond2(ax, x, y, s=spacing2)
        for idx1, (x1, y1) in enumerate(dot_positions):
            for idx2, (x2, y2) in enumerate(dot_positions):
                if idx1 < idx2 and abs(x1 - x2) == spacing2 and abs(y1 - y2) == spacing2:
                    ax.plot([x1, x2], [y1, y2], color=line_color2, lw=line_width2)
        ax.set_aspect("equal")
        st.pyplot(fig)

    if st.button("🎨 Generate Kolam", key="tab2"):
        generate_kolam2()

# --------------------------------------------------------------------------------
# === TAB 3: Analyzer ===
with tab3:
    st.header("Kolam Design Principles Analyzer")
    uploaded_file = st.file_uploader("Upload a Kolam image", type=["jpg", "jpeg", "png"])
    def analyze_kolam(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape
        mid = w // 2
        left = gray[:, :mid]
        right = cv2.flip(gray[:, mid:], 1)
        min_width = min(left.shape[1], right.shape[1])
        left = left[:, :min_width]
        right = right[:, :min_width]
        symmetry_score = np.sum(left == right) / left.size
        edges = cv2.Canny(gray, 50, 150)
        line_density = np.sum(edges > 0) / edges.size
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        complexity = len(contours)
        return symmetry_score, line_density, complexity, edges

    def generate_principles(symmetry_score, line_density, complexity):
        principles = []
        if symmetry_score > 0.8:
            principles.append("The Kolam shows **high bilateral symmetry**, symbolizing balance and harmony.")
        else:
            principles.append("The Kolam displays **asymmetry**, suggesting a creative interpretation.")
        if line_density > 0.15:
            principles.append("It features **dense linework**, indicating intricacy and abundance.")
        else:
            principles.append("The design has **light linework**, reflecting minimalism and simplicity.")
        if complexity > 20:
            principles.append("The pattern is **highly complex**, with advanced structural planning.")
        elif complexity > 10:
            principles.append("The Kolam shows **moderate complexity**, balancing detail with clarity.")
        else:
            principles.append("The Kolam is **simple and elegant**, focusing on fundamental forms.")
        principles.append("The dots and connecting lines reflect **continuity and unity** in Kolam traditions.")
        principles.append("The structure indicates **repetition and rhythm**, symbolizing infinite cycles in nature.")
        return "\n\n".join(principles)

    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Kolam", use_column_width=True)
        img_array = np.array(img.convert("RGB"))
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        symmetry_score, line_density, complexity, edges = analyze_kolam(img_array)
        principles = generate_principles(symmetry_score, line_density, complexity)
        st.subheader("📊 Kolam Design Principles")
        st.write(principles)
        st.subheader("Detected Edges")
        st.image(edges, caption="Edge Detection Output", use_column_width=True)
        output = BytesIO()
        output.write(principles.encode('utf-8'))
        output.seek(0)
        st.download_button(
            label="📥 Download Principles as Text",
            data=output,
            file_name="kolam_principles.txt",
            mime="text/plain"
        )
