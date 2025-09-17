import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import cv2
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Kolam Suite", layout="wide")
st.title("🌸 Unified Kolam Suite")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🏠 Home", "✨ Random Kolam Art", "🔷 Complex Kolam", "📊 Kolam Analyzer", "ℹ️ Info"]
)

# ---------------------- HOME ----------------------
with tab1:
    st.header("Kolam Konnect")
    st.write("✨ Placeholder for your front page content here.")

# ---------------------- RANDOM KOLAM ----------------------
with tab2:
    st.header("Random Kolam Art")
    st.write("Placeholder for your random kolam generator.")

# ---------------------- COMPLEX KOLAM ----------------------
with tab3:
    st.header("🔷 Complex Kolam Generator")
    kolam_choice = st.selectbox(
        "Select Kolam Type:", 
        ["Unsymmetrical Dots", "Diamonds with Arcs"]
    )

    # Common controls
    line_color = st.color_picker("Line Color:", "#FFFFFF")
    dot_color = st.color_picker("Dot Color:", "#FFFFFF")
    bg_color = st.color_picker("Background Color:", "#000000")
    line_width = st.slider("Line Width:", 1.0, 5.0, 2.5)
    spacing = st.slider("Dot Spacing:", 0.5, 2.0, 1.0)
    show_dots = st.checkbox("Show Dots", value=True)

    # ----------------- Unsymmetrical Dots -----------------
    def generate_dot_positions(max_dots, spacing):
        rows = max_dots + 1
        dot_positions = []
        half = rows // 2
        for i in range(rows):
            count = 1 + 2 * i if i < half else 1 + 2 * (rows - i - 1)
            offset = -(count - 1) / 2 * spacing
            for j in range(count):
                dot_positions.append((offset + j * spacing, -i * spacing))
        return dot_positions, rows

    def draw_diamond(ax, x, y, s=1):
        points = [(x, y + s/2), (x + s/2, y), (x, y - s/2), (x - s/2, y), (x, y + s/2)]
        xs, ys = zip(*points)
        ax.plot(xs, ys, color=line_color, lw=line_width)

    def unsymmetrical_kolam(max_dots):
        dot_positions, rows = generate_dot_positions(max_dots, spacing)
        fig, ax = plt.subplots(figsize=(8,8))
        ax.set_facecolor(bg_color)
        ax.axis("off")
        if show_dots:
            xs, ys = zip(*dot_positions)
            ax.scatter(xs, ys, color=dot_color, s=40)
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
        for idx, (x, y) in enumerate(dot_positions):
            if idx not in borders:
                draw_diamond(ax, x, y, s=spacing)
        for idx1, (x1, y1) in enumerate(dot_positions):
            for idx2, (x2, y2) in enumerate(dot_positions):
                if idx1 < idx2 and abs(x1 - x2) == spacing and abs(y1 - y2) == spacing:
                    ax.plot([x1, x2], [y1, y2], color=line_color, lw=line_width)
        ax.set_aspect("equal")
        st.pyplot(fig)

    # ----------------- Diamonds with Arcs -----------------
    def draw_arc(ax, x, y, r=0.5, start=0, end=180):
        theta = np.linspace(np.radians(start), np.radians(end), 100)
        ax.plot(x + r*np.cos(theta), y + r*np.sin(theta), color=line_color, lw=line_width)

    def diamonds_with_arcs(n):
        fig, ax = plt.subplots(figsize=(8,8))
        ax.set_facecolor(bg_color)
        ax.axis("off")
        if show_dots:
            for i in range(n):
                for j in range(n):
                    ax.plot(i*spacing, j*spacing, 'o', color=dot_color, markersize=5)
        for i in range(n-1):
            for j in range(n-1):
                draw_diamond(ax, (i+0.5)*spacing, (j+0.5)*spacing, s=spacing)
        for i in range(1, n-1):
            draw_arc(ax, (i-0.5)*spacing, (n-1)*spacing, r=spacing/2, start=0, end=180)
            draw_arc(ax, (i-0.5)*spacing, 0, r=spacing/2, start=180, end=360)
        for j in range(1, n-1):
            draw_arc(ax, 0, (j-0.5)*spacing, r=spacing/2, start=90, end=270)
            draw_arc(ax, (n-1)*spacing, (j-0.5)*spacing, r=spacing/2, start=270, end=450)
        ax.set_aspect("equal")
        st.pyplot(fig)

    # Input controls and button
    if kolam_choice == "Unsymmetrical Dots":
        max_dots = st.slider("Max Dots in Middle Rows:", 3, 9, 5)
        if st.button("🎨 Generate Unsymmetrical Dots Kolam"):
            unsymmetrical_kolam(max_dots)
    else:
        size = st.slider("Grid Size (dots per side):", 4, 10, 6)
        if st.button("💠 Generate Diamonds with Arcs"):
            diamonds_with_arcs(size)

# ---------------------- ANALYZER ----------------------
with tab4:
    st.header("📊 Kolam Design Principles Analyzer")
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

# ---------------------- INFO ----------------------
with tab5:
    st.header("ℹ️ About Kolam Konnect")
    st.write("Placeholder for detailed info about the Kolam project.")
