# app.py
import os
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import cv2
from io import BytesIO
from PIL import Image

# ====== Page config ======
st.set_page_config(page_title="Kolam Konnect", layout="wide")

# ====== Safe logo load (avoid crash if missing) ======
LOGO_PATH = os.path.join(os.path.dirname(__file__), "logo.jpg")
logo_exists = os.path.exists(LOGO_PATH)

# ====== Simple CSS to match screenshot-like feel (not global gradient) ======
st.markdown(
    """
    <style>
      .header {
        display:flex;
        align-items:center;
        gap:12px;
        padding:10px 6px;
      }
      .app-title {
        font-size:22px;
        font-weight:700;
        background: linear-gradient(90deg,#FF512F,#F09819);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
      }
      .hero {
        background: linear-gradient(180deg, #fff7f3 0%, #fffaf8 100%);
        padding:32px;
        border-radius:8px;
        margin-bottom:12px;
      }
      .section-card {
        background: white;
        border-radius:10px;
        padding:16px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.04);
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ====== Header ======
header_cols = st.columns([0.12, 0.88])
with header_cols[0]:
    if logo_exists:
        st.image(LOGO_PATH, width=60)
    else:
        st.markdown("<div style='width:60px;height:60px;background:#eee;border-radius:8px;'></div>", unsafe_allow_html=True)
with header_cols[1]:
    st.markdown('<div class="header"><div class="app-title">🌸 Kolam Konnect</div></div>', unsafe_allow_html=True)

# ====== Tabs ======
tab_basic, tab_complex, tab_analyze, tab_community = st.tabs(
    ["🎨 Basic Level Kolam Generator", "🔷 Complex Kolam Generator", "📊 Kolam Analyzer", "👥 Community"]
)

# ------------------------------
# TAB 1: Basic Level Kolam Generator
# ------------------------------
with tab_basic:
    st.markdown('<div class="hero">', unsafe_allow_html=True)
    st.markdown("<h2 style='margin:0'>Basic Level Kolam Generator</h2>", unsafe_allow_html=True)
    st.markdown("<p style='margin-top:6px;color:#5b5b5b'>Choose a simple pattern and generate Kolam.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- widgets (unique keys) ---
    kolam_type = st.selectbox(
        "Choose Kolam Type:",
        ["Straight Lines", "Connected Diamonds", "Loops/Arcs", "Mixed"],
        key="basic_kolam_type",
    )
    size = st.slider("Grid Size (dots per side):", 4, 10, 6, key="basic_size")
    line_color = st.color_picker("Kolam Line Color:", "#B22222", key="basic_line_color")
    dot_color = st.color_picker("Dot Color:", "#000000", key="basic_dot_color")
    bg_color = st.color_picker("Background Color:", "#FFFFFF", key="basic_bg_color")
    line_width = st.slider("Line Width:", 1.0, 5.0, 2.0, key="basic_line_width")
    show_dots = st.checkbox("Show Dots", value=True, key="basic_show_dots")

    # --- drawing helpers (kept close to your original code) ---
    def draw_diamond_basic(ax, x, y, s=1):
        pts = [(x, y + s/2), (x + s/2, y), (x, y - s/2), (x - s/2, y), (x, y + s/2)]
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=line_color, lw=line_width)

    def draw_loop_basic(ax, x, y, r=0.5):
        theta = np.linspace(0, 2 * np.pi, 200)
        ax.plot(x + r * np.cos(theta), y + r * np.sin(theta), color=line_color, lw=line_width)

    def draw_straight_basic(ax, n, spacing):
        for i in range(n):
            ax.plot([0, (n - 1) * spacing], [i * spacing, i * spacing], color=line_color, lw=line_width)
            ax.plot([i * spacing, i * spacing], [0, (n - 1) * spacing], color=line_color, lw=line_width)

    def generate_basic_kolam(n):
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.set_facecolor(bg_color)
        ax.axis("off")
        spacing = 1
        if show_dots:
            for i in range(n):
                for j in range(n):
                    ax.plot(i * spacing, j * spacing, "o", color=dot_color, markersize=5)

        if kolam_type == "Straight Lines":
            draw_straight_basic(ax, n, spacing)
        elif kolam_type == "Connected Diamonds":
            for i in range(n - 1):
                for j in range(n - 1):
                    draw_diamond_basic(ax, (i + 0.5) * spacing, (j + 0.5) * spacing, s=spacing)
        elif kolam_type == "Loops/Arcs":
            for i in range(n):
                for j in range(n):
                    draw_loop_basic(ax, i * spacing, j * spacing, r=spacing / 2.2)
        elif kolam_type == "Mixed":
            for i in range(n - 1):
                for j in range(n - 1):
                    if (i + j) % 2 == 0:
                        draw_diamond_basic(ax, (i + 0.5) * spacing, (j + 0.5) * spacing, s=spacing)
                    else:
                        draw_loop_basic(ax, (i + 0.5) * spacing, (j + 0.5) * spacing, r=spacing / 2.2)
        ax.set_aspect("equal")
        st.pyplot(fig)

    if st.button("🎨 Generate Basic Kolam", key="basic_generate"):
        generate_basic_kolam(size)

# ------------------------------
# TAB 2: Complex Kolam Generator (Unsymmetrical Dots + Diamond with Arcs)
# ------------------------------
with tab_complex:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.header("Complex Kolam Generator")
    st.markdown("Choose between Unsymmetrical Dots Kolam and Diamond-with-Arcs Kolam.", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    choice = st.selectbox("Select Type", ["Unsymmetrical Dots Kolam", "Diamond with Arcs Kolam"], key="complex_choice")

    # ---------- Unsymmetrical Dots ----------
    if choice == "Unsymmetrical Dots Kolam":
        max_dots = st.slider("Max Dots in Middle Rows:", 3, 9, 5, key="complex_unsym_max_dots")
        line_color2 = st.color_picker("Line Color:", "#FFFFFF", key="complex_unsym_line_color")
        dot_color2 = st.color_picker("Dot Color:", "#FFFFFF", key="complex_unsym_dot_color")
        bg_color2 = st.color_picker("Background Color:", "#000000", key="complex_unsym_bg_color")
        line_width2 = st.slider("Line Width:", 1.0, 5.0, 2.5, key="complex_unsym_line_width")
        spacing2 = st.slider("Dot Spacing:", 0.5, 2.0, 1.0, key="complex_unsym_spacing")
        show_dots2 = st.checkbox("Show Dots", value=True, key="complex_unsym_show_dots")

        def generate_dot_positions_unsym(max_dots, spacing):
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

        def draw_diamond_unsym(ax, x, y, s=1):
            pts = [(x, y + s / 2), (x + s / 2, y), (x, y - s / 2), (x - s / 2, y), (x, y + s / 2)]
            xs, ys = zip(*pts)
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

        def generate_unsymmetrical_kolam():
            dot_positions, rows = generate_dot_positions_unsym(max_dots, spacing2)
            borders = find_border_indices(dot_positions, rows)

            fig, ax = plt.subplots(figsize=(7, 7))
            ax.set_facecolor(bg_color2)
            ax.axis("off")

            if show_dots2:
                xs, ys = zip(*dot_positions)
                ax.scatter(xs, ys, color=dot_color2, s=40)

            # Draw diamonds for non-border dots
            for idx, (x, y) in enumerate(dot_positions):
                if idx not in borders:
                    draw_diamond_unsym(ax, x, y, s=spacing2)

            # Connect diagonal neighbours (use tolerance for float comparison)
            for idx1, (x1, y1) in enumerate(dot_positions):
                for idx2, (x2, y2) in enumerate(dot_positions):
                    if idx1 < idx2 and np.isclose(abs(x1 - x2), spacing2) and np.isclose(abs(y1 - y2), spacing2):
                        ax.plot([x1, x2], [y1, y2], color=line_color2, lw=line_width2)

            ax.set_aspect("equal")
            st.pyplot(fig)

        if st.button("🎨 Generate Complex Kolam (Unsymmetrical)", key="complex_unsym_generate"):
            generate_unsymmetrical_kolam()

    # ---------- Diamond with Arcs Kolam ----------
    else:
        size = st.slider("Grid Size (dots per side):", 4, 10, 6, key="complex_diamond_size")
        line_color_d = st.color_picker("Line Color:", "#B22222", key="complex_diamond_line_color")
        dot_color_d = st.color_picker("Dot Color:", "#000000", key="complex_diamond_dot_color")
        bg_color_d = st.color_picker("Background:", "#FFFFFF", key="complex_diamond_bg_color")
        line_width_d = st.slider("Line Width:", 1.0, 5.0, 2.0, key="complex_diamond_line_width")
        show_dots_d = st.checkbox("Show Dots", value=True, key="complex_diamond_show_dots")

        def draw_diamond_arc(ax, x, y, s=1):
            pts = [(x, y + s / 2), (x + s / 2, y), (x, y - s / 2), (x - s / 2, y), (x, y + s / 2)]
            xs, ys = zip(*pts)
            ax.plot(xs, ys, color=line_color_d, lw=line_width_d)

        def draw_arc_arc(ax, x, y, r=0.6, start=0, end=180):
            theta = np.linspace(np.radians(start), np.radians(end), 200)
            ax.plot(x + r * np.cos(theta), y + r * np.sin(theta), color=line_color_d, lw=line_width_d)

        def generate_diamond_with_arcs(n):
            fig, ax = plt.subplots(figsize=(7, 7))
            ax.set_facecolor(bg_color_d)
            ax.axis("off")
            spacing = 1
            r = spacing / 2.0  # choose radius relative to spacing
            offset = 0.01

            if show_dots_d:
                for i in range(n):
                    for j in range(n):
                        ax.plot(i * spacing, j * spacing, "o", color=dot_color_d, markersize=5)

            # draw diamonds centered between dots
            for i in range(n - 1):
                for j in range(n - 1):
                    draw_diamond_arc(ax, (i + 0.5) * spacing, (j + 0.5) * spacing, s=spacing)

            # top & bottom arcs (facing inward)
            for i in range(1, n - 1):
                # shift arcs horizontally so arc center surrounds exactly one border dot
                cx = (i - 0.5) * spacing + 0.0  # slight shift possible if needed
                draw_arc_arc(ax, cx, (n - 1) + offset, r=r, start=0, end=180)  # top arcs (curve downward)
                draw_arc_arc(ax, cx, -offset, r=r, start=180, end=360)  # bottom arcs (curve upward)

            # left & right arcs (facing inward)
            for j in range(1, n - 1):
                cy = (j - 0.5) * spacing + 0.0
                draw_arc_arc(ax, -offset, cy, r=r, start=90, end=270)  # left arcs (curve right)
                draw_arc_arc(ax, (n - 1) + offset, cy, r=r, start=270, end=450)  # right arcs (curve left)

            ax.set_aspect("equal")
            st.pyplot(fig)

        if st.button("🎨 Generate Complex Kolam (Diamond+Arcs)", key="complex_diamond_generate"):
            generate_diamond_with_arcs(size)

# ------------------------------
# TAB 3: Kolam Analyzer
# ------------------------------
with tab_analyze:
    st.header("Kolam Design Principles Analyzer")

    uploaded_file = st.file_uploader("Upload a Kolam image", type=["jpg", "jpeg", "png"], key="analyzer_upload")

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
        try:
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

            # download button
            output = BytesIO()
            output.write(principles.encode("utf-8"))
            output.seek(0)
            st.download_button(label="📥 Download Principles as Text", data=output, file_name="kolam_principles.txt", mime="text/plain", key="analyzer_download")
        except Exception as e:
            st.error("Error analyzing image: " + str(e))

# ------------------------------
# TAB 4: Community
# ------------------------------
with tab_community:
    st.header("Kolam Community Showcase")
    st.write("Community-sourced Kolam examples (public images).")
    cols = st.columns(3)
    # A small curated list of public kolam images; if any fail to load they will be skipped
    community_urls = [
        "https://upload.wikimedia.org/wikipedia/commons/9/9d/Kolam_1.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/7/7a/Rangoli_design.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/e/eb/Kolam_Rangoli.jpg",
        # fallback placeholders (picsum) in case the above are inaccessible
        "https://picsum.photos/seed/kolam1/800/600",
        "https://picsum.photos/seed/kolam2/800/600",
    ]
    # Display up to 6 images in a responsive grid
    idx = 0
    for url in community_urls:
        try:
            col = cols[idx % 3]
            col.image(url, use_column_width=True)
            idx += 1
        except Exception:
            # skip failed image
            idx += 1
            continue

    st.markdown("---")
    st.write("Want to contribute? Add your Kolam images to the community repository and they will show up here.")

# ===== End of file =====
