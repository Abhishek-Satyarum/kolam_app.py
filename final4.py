# kolam_app.py
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import cv2
from io import BytesIO
from PIL import Image
import requests
from math import cos, sin, radians

# === APP CONFIG ===
st.set_page_config(page_title="Kolam Konnect", layout="wide", initial_sidebar_state="expanded")

# === THEME / GLOBAL CSS (light, vibrant) ===
st.markdown(
    """
    <style>
    /* App background and text */
    .stApp {
        background: linear-gradient(180deg, #FFF8F0 0%, #FFECEC 100%);
        color: #222222;
    }
    /* Header / nav bar styling */
    .top-nav {
        display:flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 16px;
        background: rgba(255,255,255,0.75);
        border-radius: 8px;
        margin-bottom: 14px;
    }
    .nav-links { display:flex; gap:12px; align-items:center; }
    .nav-button {
        background: transparent;
        border: none;
        font-weight:600;
        color: #3b3b3b;
        padding:8px 12px;
        border-radius:8px;
    }
    .nav-button:hover { background:#FFF0E5; cursor:pointer; color:#d04500; }
    /* Home card */
    .home-card {
        text-align:center;
        padding: 50px 20px;
        border-radius: 14px;
        background: linear-gradient(90deg, rgba(255,248,240,0.9), rgba(255,240,238,0.9));
        margin-bottom: 18px;
    }
    .badge {
        display:inline-block;
        background: #FFF3CD;
        color: #9A6700;
        padding:6px 14px;
        border-radius:20px;
        font-weight:600;
    }
    .main-title {
        font-size: 42px;
        font-weight:800;
        margin-top:18px;
        margin-bottom:10px;
        line-height:1.05;
    }
    .main-title .accent {
        background: linear-gradient(90deg, #ff5a3c, #ff8c42);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .subtitle {
        color:#555555;
        max-width:900px;
        margin: 0 auto 20px auto;
        font-size:16px;
    }
    .learn-btn {
        padding:10px 20px;
        background: transparent;
        border: 2px solid rgba(255,140,66,0.14);
        color:#d35400;
        border-radius:10px;
        font-weight:600;
    }
    .cta {
        padding:10px 18px;
        background: #6D2E7F;
        color:white;
        border-radius:10px;
        font-weight:700;
        box-shadow: 0 6px 18px rgba(109,46,127,0.18);
    }
    /* small responsive tweaks */
    @media (max-width: 800px) {
        .main-title { font-size: 28px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# === SIDEBAR WITH LOGO (larger) ===
with st.sidebar:
    st.write("")  # spacing
    try:
        # try local file first
        logo = Image.open("logo.jpg")
    except Exception:
        # fallback to online placeholder if local not present
        try:
            url = "https://images.unsplash.com/photo-1549880338-65ddcdfd017b?w=800&q=80"
            resp = requests.get(url, timeout=5)
            logo = Image.open(BytesIO(resp.content))
        except Exception:
            logo = None

    if logo:
        st.image(logo, use_column_width=False, width=160, caption="Kolam Konnect")
    else:
        st.markdown("**Kolam Konnect**")
    st.markdown("---")
    st.markdown("**Navigation**")
    # navigation via session_state to simulate tabs
    if "page" not in st.session_state:
        st.session_state.page = "Home"
    page = st.radio("", ["Home", "Basic Level Kolam Generator", "Complex Kolam Generator", "Kolam Analyzer", "Learn More"],
                    index=["Home", "Basic Level Kolam Generator", "Complex Kolam Generator", "Kolam Analyzer", "Learn More"].index(st.session_state.page))
    st.session_state.page = page
    st.markdown("---")
    st.markdown("**Settings**")
    st.caption("Logo and theme controls available in code.")
    st.markdown("---")

# === TOP NAV (replicates header feel) ===
nav_cols = st.columns([1, 2, 1])
with nav_cols[0]:
    st.write("")  # left spacing
with nav_cols[1]:
    # Render a small top nav area (visual only)
    st.markdown(
        f"""
        <div class="top-nav">
            <div style="display:flex;align-items:center;gap:12px;">
                <div style="width:36px;height:36px;border-radius:8px;background:#221f1f"></div>
                <div style="font-weight:700;font-size:18px;">Kolam Konnect</div>
            </div>
            <div class="nav-links">
                <button class="nav-button" onclick="window.location.reload()">Draw</button>
                <button class="nav-button" onclick="window.location.reload()">Community</button>
                <button class="nav-button" onclick="window.location.reload()">Learn</button>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with nav_cols[2]:
    st.write("")

# --- Helper functions (Generators + Analyzer) ---
# Drawing helpers (kept largely as you provided - with unique keys not necessary here)
def draw_diamond_ax(ax, x, y, s=1, color="#B22222", lw=2.0):
    pts = [(x, y + s/2), (x + s/2, y), (x, y - s/2), (x - s/2, y), (x, y + s/2)]
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle='round')

def draw_arc_ax(ax, x, y, r=0.6, start=0, end=180, color="#B22222", lw=2.0):
    theta = np.linspace(np.radians(start), np.radians(end), 120)
    ax.plot(x + r*np.cos(theta), y + r*np.sin(theta), color=color, lw=lw, solid_capstyle='round')

def draw_loop_ax(ax, x, y, r=0.5, color="#B22222", lw=2.0):
    theta = np.linspace(0, 2*np.pi, 240)
    ax.plot(x + r*np.cos(theta), y + r*np.sin(theta), color=color, lw=lw, solid_capstyle='round')

def draw_straight_ax(ax, n, spacing, color="#B22222", lw=2.0):
    for i in range(n):
        ax.plot([0, (n-1)*spacing], [i*spacing, i*spacing], color=color, lw=lw)
        ax.plot([i*spacing, i*spacing], [0, (n-1)*spacing], color=color, lw=lw)


# === PAGE: HOME ===
def page_home():
    # If Learn button clicked: switch to Learn More page
    if "goto_learn" not in st.session_state:
        st.session_state.goto_learn = False

    st.markdown(
        """
        <div class="home-card">
            <div class="badge">✨ Traditional Art Meets Digital Innovation</div>
            <div class="main-title">Create Beautiful <span class="accent">Kolam</span> Arts</div>
            <div class="subtitle">
                Discover the ancient art of Kolam through our interactive digital canvas.
                Draw, learn, and connect with traditional Indian patterns and a global community.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        if st.button("Start Drawing ⬇", key="home_start"):
            st.session_state.page = "Basic Level Kolam Generator"
            st.experimental_rerun()
    with c2:
        if st.button("Learn About Kolam", key="home_learn"):
            st.session_state.page = "Learn More"
            st.experimental_rerun()
    with c3:
        st.write("")

    st.markdown("---")
    st.markdown("### Kolam Tools")
    st.markdown("Generate random kolam patterns and analyze existing designs with our advanced tools.")
    # quick action buttons to jump to tools
    a1, a2, a3 = st.columns(3)
    with a1:
        if st.button("✨ Random Kolam Art", key="home_random"):
            st.session_state.page = "Basic Level Kolam Generator"
            st.experimental_rerun()
    with a2:
        if st.button("✨ Asymmetric Patterns", key="home_asym"):
            st.session_state.page = "Complex Kolam Generator"
            st.experimental_rerun()
    with a3:
        if st.button("🔍 Kolam Recognizer", key="home_recognizer"):
            st.session_state.page = "Kolam Analyzer"
            st.experimental_rerun()

# === PAGE: BASIC LEVEL KOLAM GENERATOR (Random Kolam Art) ===
def page_basic():
    st.header("🎨 Basic Level Kolam Generator")
    kolam_type = st.selectbox("Choose Kolam Type:", ["Straight Lines", "Connected Diamonds", "Loops/Arcs", "Mixed"], key="basic_type")
    size = st.slider("Grid Size (dots per side):", 4, 10, 6, key="basic_size")
    line_color = st.color_picker("Kolam Line Color:", "#B22222", key="basic_line_color")
    dot_color = st.color_picker("Dot Color:", "#000000", key="basic_dot_color")
    bg_color = st.color_picker("Background Color:", "#FFFFFF", key="basic_bg")
    line_width = st.slider("Line Width:", 1.0, 6.0, 2.5, key="basic_line_width")
    show_dots = st.checkbox("Show Dots", value=True, key="basic_show_dots")

    def generate_kolam_basic(n):
        fig, ax = plt.subplots(figsize=(7,7))
        ax.set_facecolor(bg_color)
        ax.axis("off")
        spacing = 1
        r = 0.5
        offset = 0.01
        if show_dots:
            for i in range(n):
                for j in range(n):
                    ax.plot(i*spacing, j*spacing, 'o', color=dot_color, markersize=4)
        if kolam_type == "Straight Lines":
            draw_straight_ax(ax, n, spacing, color=line_color, lw=line_width)
        elif kolam_type == "Connected Diamonds":
            for i in range(n-1):
                for j in range(n-1):
                    draw_diamond_ax(ax, (i+0.5)*spacing, (j+0.5)*spacing, s=spacing, color=line_color, lw=line_width)
        elif kolam_type == "Loops/Arcs":
            for i in range(n):
                for j in range(n):
                    draw_loop_ax(ax, i*spacing, j*spacing, r=spacing/2.2, color=line_color, lw=line_width)
        elif kolam_type == "Mixed":
            for i in range(n-1):
                for j in range(n-1):
                    if (i+j) % 2 == 0:
                        draw_diamond_ax(ax, (i+0.5)*spacing, (j+0.5)*spacing, s=spacing, color=line_color, lw=line_width)
                    else:
                        draw_loop_ax(ax, (i+0.5)*spacing, (j+0.5)*spacing, r=spacing/2.2, color=line_color, lw=line_width)
        ax.set_aspect("equal")
        st.pyplot(fig)

    if st.button("🎨 Generate Kolam", key="generate_basic"):
        generate_kolam_basic(size)

# === PAGE: COMPLEX KOLAM GENERATOR (Unsymmetrical Dots + Diamond with Arcs) ===
def page_complex():
    st.header("🔷 Complex Kolam Generator")
    option = st.selectbox("Choose pattern:", ["Unsymmetrical Dots (Dots -> Diamonds)", "Diamond with Arcs (border arcs)"], key="complex_option")
    # Shared controls
    line_color = st.color_picker("Line Color:", "#B22222", key="complex_line_color")
    dot_color = st.color_picker("Dot Color:", "#000000", key="complex_dot_color")
    bg_color = st.color_picker("Background Color:", "#FFFFFF", key="complex_bg")
    line_width = st.slider("Line Width:", 1.0, 6.0, 2.5, key="complex_line_width")
    show_dots = st.checkbox("Show Dots", value=True, key="complex_show_dots")

    if option == "Unsymmetrical Dots (Dots -> Diamonds)":
        max_dots = st.slider("Max Dots in Middle Rows:", 3, 9, 5, key="complex_max_dots")
        spacing = st.slider("Dot Spacing:", 0.5, 2.0, 1.0, key="complex_spacing")

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

        def find_border_indices(dot_positions):
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

        def generate_unsymmetrical():
            dot_positions, rows = generate_dot_positions(max_dots, spacing)
            borders = find_border_indices(dot_positions)
            fig, ax = plt.subplots(figsize=(7,7))
            ax.set_facecolor(bg_color)
            ax.axis("off")
            if show_dots:
                xs, ys = zip(*dot_positions)
                ax.scatter(xs, ys, color=dot_color, s=40)
            # Draw diamonds around non-border dots
            for idx, (x, y) in enumerate(dot_positions):
                if idx not in borders:
                    draw_diamond_ax(ax, x, y, s=spacing, color=line_color, lw=line_width)
            # Connect neighboring diamond corners diagonally to create continuous lines
            for idx1, (x1, y1) in enumerate(dot_positions):
                for idx2, (x2, y2) in enumerate(dot_positions):
                    if idx1 < idx2 and abs(round(x1 - x2,5)) == round(spacing,5) and abs(round(y1 - y2,5)) == round(spacing,5):
                        ax.plot([x1, x2], [y1, y2], color=line_color, lw=line_width)
            ax.set_aspect("equal")
            st.pyplot(fig)

        if st.button("🎨 Generate Complex Kolam (Unsymmetrical)", key="gen_unsym"):
            generate_unsymmetrical()

    else:  # Diamond with Arcs (moved here)
        # Use the diamond-with-arcs implementation you provided earlier
        size = st.slider("Grid Size (dots per side):", 4, 10, 6, key="dia_size")
        spacing = 1
        r = st.slider("Arc radius:", 0.2, 1.0, 0.5, key="dia_r")
        offset = st.slider("Arc offset (inward):", 0.0, 0.5, 0.01, key="dia_offset")

        def generate_diamond_arcs(n):
            fig, ax = plt.subplots(figsize=(7,7))
            ax.set_facecolor(bg_color)
            ax.axis("off")
            # draw dots
            if show_dots:
                for i in range(n):
                    for j in range(n):
                        ax.plot(i*spacing, j*spacing, 'o', color=dot_color, markersize=4)
            # diamonds
            for i in range(n-1):
                for j in range(n-1):
                    draw_diamond_ax(ax, (i+0.5)*spacing, (j+0.5)*spacing, s=spacing, color=line_color, lw=line_width)
            # top border arcs (inward: curve downward)
            # number of arcs = n - 2 (skip corners) placed centered above each interior dot
            for i in range(1, n-1):
                cx = (i-0.5)*spacing + r  # small shift to the right by radius as you requested earlier
                cy_top = (n-1) + offset
                draw_arc_ax(ax, cx, cy_top, r=r, start=0, end=180, color=line_color, lw=line_width)
                # bottom
                cy_bot = -offset
                draw_arc_ax(ax, cx, cy_bot, r=r, start=180, end=360, color=line_color, lw=line_width)
            # left and right border arcs (facing inward)
            for j in range(1, n-1):
                cy = (j-0.5)*spacing + r
                draw_arc_ax(ax, -offset, cy, r=r, start=90, end=270, color=line_color, lw=line_width)
                draw_arc_ax(ax, (n-1)+offset, cy, r=r, start=270, end=450, color=line_color, lw=line_width)
            ax.set_aspect("equal")
            st.pyplot(fig)

        if st.button("🎨 Generate Complex Kolam (Diamond+Arcs)", key="gen_dia"):
            generate_diamond_arcs(size)


# === PAGE: ANALYZER ===
def page_analyzer():
    st.header("📊 Kolam Design Principles Analyzer")
    uploaded_file = st.file_uploader("Upload a Kolam image", type=["jpg","jpeg","png"], key="analyzer_upload")
    st.markdown("Drop a clear image of a kolam (high contrast). The tool will analyze symmetry, edge density and complexity.")

    def analyze_kolam(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Resize or pad to reasonable size for stable processing
        h, w = gray.shape
        if h < 64 or w < 64:
            gray = cv2.resize(gray, (max(64,w), max(64,h)))
            h, w = gray.shape
        mid = w // 2
        left = gray[:, :mid]
        right = cv2.flip(gray[:, mid:], 1)
        # ensure equal widths
        minw = min(left.shape[1], right.shape[1])
        left = left[:, :minw]
        right = right[:, :minw]
        # binary threshold to reduce noise
        _, leftt = cv2.threshold(left, 128, 255, cv2.THRESH_BINARY)
        _, rightt = cv2.threshold(right, 128, 255, cv2.THRESH_BINARY)
        symmetry_score = float(np.sum(leftt == rightt) / leftt.size)
        edges = cv2.Canny(gray, 50, 150)
        line_density = float(np.sum(edges > 0) / edges.size)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        complexity = int(len(contours))
        return symmetry_score, line_density, complexity, edges

    def generate_principles(symmetry_score, line_density, complexity):
        principles = []
        if symmetry_score > 0.85:
            principles.append("High bilateral symmetry: The design balances left and right halves strongly, a traditional hallmark indicating harmony.")
        elif symmetry_score > 0.6:
            principles.append("Moderate symmetry: Evidences of balance but with intentional asymmetry or stylization.")
        else:
            principles.append("Low symmetry / asymmetrical: likely creative or regionally stylized kolam forms.")

        if line_density > 0.12:
            principles.append("Dense linework: intricate, probably advanced patterning with many crossings.")
        else:
            principles.append("Light linework: simpler patterns with emphasis on geometry rather than ornamentation.")

        if complexity > 30:
            principles.append("High structural complexity: many contours and interlacing lines (may indicate nested loops and multiple motifs).")
        elif complexity > 12:
            principles.append("Moderate complexity: a balanced patterning with clear motifs.")
        else:
            principles.append("Simple and elegant: likely classic dot-and-line patterns with minimal crossings.")

        principles.append("Dots and continuous lines imply continuity and rhythm: core principles in kolam practice.")
        principles.append("Repetition and symmetry often represent cosmic or auspicious cycles in traditional practice.")
        return "\n\n".join(principles)

    if uploaded_file is not None:
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, caption="Uploaded Kolam", use_column_width=True)
        img_array = np.array(img)
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        try:
            symmetry_score, line_density, complexity, edges = analyze_kolam(img_array)
            principles = generate_principles(symmetry_score, line_density, complexity)
            st.subheader("📊 Kolam Design Principles")
            st.write(principles)
            st.subheader("Detected Edges")
            st.image(edges, clamp=True, use_column_width=True)
            # Download
            output = BytesIO()
            output.write(principles.encode('utf-8'))
            output.seek(0)
            st.download_button("📥 Download Principles as Text", data=output, file_name="kolam_principles.txt", mime="text/plain", key="download_princ")
        except Exception as e:
            st.error(f"Analysis failed: {e}")

# === PAGE: LEARN MORE ===
def page_learn_more():
    st.header("📘 Learn About Kolam")
    st.markdown(
        """
        **What is Kolam?**

        Kolam is a traditional South Indian (especially Tamil) floor drawing made with rice flour or chalk powder. It is composed of dots arranged in a grid and continuous lines that interweave around them to form geometric and curvilinear motifs.

        **Cultural significance**
        - Kolam patterns are drawn daily in many households as an auspicious practice — to welcome guests and bring prosperity.
        - The patterns balance symmetry and rhythm; simpler kolams are for everyday use while complex ones mark festivals and celebrations.
        - Traditionally, kolam uses ephemeral materials (rice flour) to feed insects and birds, reflecting non-attachment and ecological sensibility.

        **Design principles (brief)**
        1. **Dot-grid foundation** — dots create a scaffolding for lines and motifs.
        2. **Continuity** — lines are usually drawn in single, unbroken strokes weaving around dots.
        3. **Symmetry & rhythm** — many kolams emphasize bilateral symmetry and repeated motifs.
        4. **Local styles & improvisation** — regional variants and personal creativity coexist.
        5. **Temporality & community** — kolam is ephemeral and often a community practice.

        Use the Generators tab to experiment with dot counts and pattern types, and the Analyzer tab to inspect an uploaded kolam image.
        """
    )

# === Page Router ===
page_map = {
    "Home": page_home,
    "Basic Level Kolam Generator": page_basic,
    "Complex Kolam Generator": page_complex,
    "Kolam Analyzer": page_analyzer,
    "Learn More": page_learn_more
}

# Render the selected page
current = st.session_state.page if "page" in st.session_state else "Home"
page_map.get(current, page_home)()
