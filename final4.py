# kolam_app.py
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from PIL import Image
import requests

# Try to import OpenCV, but fail gracefully if missing
try:
    import cv2
except Exception:
    cv2 = None

# ---------------- App config ----------------
st.set_page_config(page_title="Kolam Konnect", layout="wide", initial_sidebar_state="expanded")

# ---------------- Theme / CSS ----------------
st.markdown(
    """
    <style>
    /* Page background: peach/pastel from screenshot */
    .stApp {
        background: linear-gradient(180deg, #FFF8F0 0%, #C9ADA7 100%);
        color: #FFD580;
    }

    /* Header (visual) */
    .top-header {
        display:flex; justify-content:space-between; align-items:center;
        padding:8px 14px; background: rgba(255,255,255,0.7);
        border-radius:10px; margin-bottom:12px;
    }

    /* Home hero */
    .home-card {
        text-align:center; padding:40px 18px; border-radius:12px;
        background: linear-gradient(90deg, rgba(255,248,240,0.9), rgba(255,240,238,0.9));
        margin-bottom:18px;
    }
    .badge { display:inline-block; background:#FFF3CD; color:#9A6700; padding:6px 14px; border-radius:20px; font-weight:600; }
    .main-title { font-size:40px; font-weight:800; margin-top:12px; margin-bottom:8px; }
    .main-title .accent { background: linear-gradient(90deg,#ff5a3c,#ff8c42); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

    /* Buttons hover */
    div.stButton > button:hover { background: #E0F0FF !important; color: #0066CC !important; }

    /* Slider styling (thumb & track) */
    div[data-baseweb="slider"] > div > div { background: #CCE5FF !important; }
    div[data-baseweb="slider"] [role="slider"] { background: #0066CC !important; border: 2px solid #004C99 !important; }

    /* Login button style for header */
    .login-btn {
        background:#0066CC; color:white; padding:8px 14px; border-radius:8px; font-weight:700;
        border:none;
    }
    .login-btn:hover { background:#004C99; cursor:pointer; }

    /* Make images in community nicely rounded */
    .community-img { border-radius:8px; box-shadow:0px 6px 18px rgba(0,0,0,0.08); }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- Sidebar with logo & navigation ----------------
with st.sidebar:
    st.write("")  # spacing
    # Try local logo.jpg else fetch fallback
    try:
        logo = Image.open("logo.jpg")
    except Exception:
        logo = None
    if logo:
        st.image(logo, width=160, caption="Kolam Konnect")
    else:
        # fallback placeholder image
        try:
            resp = requests.get("https://images.unsplash.com/photo-1549880338-65ddcdfd017b?w=800&q=80", timeout=5)
            logo = Image.open(BytesIO(resp.content))
            st.image(logo, width=160, caption="Kolam Konnect")
        except Exception:
            st.markdown("## Kolam Konnect")

    st.markdown("---")
    # Page navigation via radio (keeps state)
    if "page" not in st.session_state:
        st.session_state.page = "Home"
    page = st.radio(
        "Go to",
        ["Home", "Basic Kolam", "Complex Kolam", "Analyzer", "Learn More", "Community"],
        index=["Home", "Basic Kolam", "Complex Kolam", "Analyzer", "Learn More", "Community"].index(st.session_state.page),
    )
    st.session_state.page = page
    st.markdown("---")
    st.caption("Tip: change design colors inside each tool.")

# ---------------- Top header with login ----------------
header_cols = st.columns([1, 4, 1])
with header_cols[0]:
    st.write("")  # left spacer
with header_cols[1]:
    st.markdown(
        """
        <div class="top-header">
            <div style="display:flex;align-items:center;gap:12px;">
                <div style="width:36px;height:36px;border-radius:8px;background:white"></div>
                <div style="font-weight:700;font-size:18px;">Kolam Konnect</div>
            </div>
            <div style="display:flex;gap:10px;align-items:center;">
                <button class="login-btn" onclick="window.location.reload()">Login</button>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with header_cols[2]:
    st.write("")  # right spacer

# ---------------- Drawing helper functions ----------------
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

# ---------------- Pages ----------------
def page_home():
    # Hero like the screenshot
    st.markdown(
        """
        <div class="home-card">
            <div class="badge">✨ Traditional Art Meets Digital Innovation</div>
            <div class="main-title">Create Beautiful <span class="accent">Kolam</span> Arts</div>
            <div style="color:#555; max-width:900px; margin:10px auto 0;">
                Discover the ancient art of Kolam through our interactive digital canvas.
                Draw, learn, and connect with traditional Indian patterns and a global community.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        if st.button("Start Drawing ↓", key="home_start"):
            st.session_state.page = "Basic Kolam"
            st.experimental_rerun()
    with c2:
        if st.button("Learn About Kolam", key="home_learn"):
            st.session_state.page = "Learn More"
            st.experimental_rerun()
    with c3:
        st.write("")

def page_basic():
    st.header("🎨 Basic Kolam Generator")
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

    if st.button("🎨 Generate Basic Kolam", key="generate_basic"):
        generate_kolam_basic(size)

    # Back to Home
    if st.button("⬅ Back to Home", key="basic_back"):
        st.session_state.page = "Home"
        st.experimental_rerun()

def page_complex():
    st.header("🔷 Complex Kolam Generator")
    option = st.selectbox("Choose pattern:", ["Unsymmetrical Dots (Dots → Diamonds)", "Diamond with Arcs"], key="complex_option")
    line_color = st.color_picker("Line Color:", "#B22222", key="complex_line_color")
    dot_color = st.color_picker("Dot Color:", "#000000", key="complex_dot_color")
    bg_color = st.color_picker("Background Color:", "#FFFFFF", key="complex_bg")
    line_width = st.slider("Line Width:", 1.0, 6.0, 2.5, key="complex_line_width")
    show_dots = st.checkbox("Show Dots", value=True, key="complex_show_dots")

    if option == "Unsymmetrical Dots (Dots → Diamonds)":
        max_dots = st.slider("Max Dots in Middle Rows:", 3, 9, 5, key="unsym_max_dots")
        spacing = st.slider("Dot Spacing:", 0.5, 2.0, 1.0, key="unsym_spacing")
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
                    borders.add(row[0]); borders.add(row[-1])
                else:
                    borders.add(row[0])
            return borders

        def generate_unsymmetrical():
            dot_positions, rows = generate_dot_positions(max_dots, spacing)
            borders = find_border_indices(dot_positions)
            fig, ax = plt.subplots(figsize=(7,7))
            ax.set_facecolor(bg_color); ax.axis("off")
            if show_dots:
                xs, ys = zip(*dot_positions); ax.scatter(xs, ys, color=dot_color, s=40)
            # Draw diamonds around non-border dots
            for idx, (x, y) in enumerate(dot_positions):
                if idx not in borders:
                    draw_diamond_ax(ax, x, y, s=spacing, color=line_color, lw=line_width)
            # Connect diagonal adjacent diamond corners to make continuous borders
            for idx1, (x1, y1) in enumerate(dot_positions):
                for idx2, (x2, y2) in enumerate(dot_positions):
                    if idx1 < idx2 and abs(round(x1 - x2,5)) == round(spacing,5) and abs(round(y1 - y2,5)) == round(spacing,5):
                        ax.plot([x1, x2], [y1, y2], color=line_color, lw=line_width)
            ax.set_aspect("equal"); st.pyplot(fig)

        if st.button("🎨 Generate Unsymmetrical Kolam", key="gen_unsym"):
            generate_unsymmetrical()

    else:  # Diamond with Arcs
        n = st.slider("Grid Size (dots per side):", 4, 10, 6, key="dia_n")
        spacing = 1
        r = st.slider("Arc radius:", 0.2, 1.0, 0.45, key="dia_r")
        offset = st.slider("Arc offset (inward):", 0.0, 0.5, 0.01, key="dia_offset")

        def generate_diamond_arcs(n):
            fig, ax = plt.subplots(figsize=(7,7))
            ax.set_facecolor(bg_color); ax.axis("off")
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
            # number of arcs = n - 2, centered above each interior dot, skip corners
            for i in range(1, n-1):
                cx_top = (i-0.5)*spacing + r  # shift right by r for nicer connection
                cy_top = (n-1) + offset
                draw_arc_ax(ax, cx_top, cy_top, r=r, start=0, end=180, color=line_color, lw=line_width)
                # bottom border (curve upward)
                cx_bot = (i-0.5)*spacing + r
                cy_bot = -offset
                draw_arc_ax(ax, cx_bot, cy_bot, r=r, start=180, end=360, color=line_color, lw=line_width)
            # left & right border arcs (facing inward)
            for j in range(1, n-1):
                cy = (j-0.5)*spacing + r
                draw_arc_ax(ax, -offset, cy, r=r, start=90, end=270, color=line_color, lw=line_width)
                draw_arc_ax(ax, (n-1)+offset, cy, r=r, start=270, end=450, color=line_color, lw=line_width)
            ax.set_aspect("equal"); st.pyplot(fig)

        if st.button("🎨 Generate Diamond+Arcs Kolam", key="gen_darcs"):
            generate_diamond_arcs(n)

    # Back to Home
    if st.button("⬅ Back to Home", key="complex_back"):
        st.session_state.page = "Home"
        st.experimental_rerun()

def page_analyzer():
    st.header("📊 Kolam Design Principles Analyzer")
    if cv2 is None:
        st.error("OpenCV (cv2) is not installed in this environment. Install opencv-python-headless to enable analyzer.")
        return

    uploaded_file = st.file_uploader("Upload a Kolam image", type=["jpg", "jpeg", "png"], key="analyzer_upload")
    st.markdown("Drop a clear high-contrast image of a kolam for best results.")

    def analyze_kolam(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape
        if h < 64 or w < 64:
            gray = cv2.resize(gray, (max(64,w), max(64,h)))
            h, w = gray.shape
        mid = w // 2
        left = gray[:, :mid]
        right = cv2.flip(gray[:, mid:], 1)
        minw = min(left.shape[1], right.shape[1])
        left = left[:, :minw]
        right = right[:, :minw]
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
            principles.append("High bilateral symmetry: strong left-right balance.")
        elif symmetry_score > 0.6:
            principles.append("Moderate symmetry: elements of balance with stylization.")
        else:
            principles.append("Low symmetry / asymmetrical pattern.")
        if line_density > 0.12:
            principles.append("Dense linework indicating intricate patterning.")
        else:
            principles.append("Light linework indicating minimal or geometric style.")
        if complexity > 30:
            principles.append("High structural complexity with many contours.")
        elif complexity > 12:
            principles.append("Moderate complexity with clear motifs.")
        else:
            principles.append("Simple and elegant design.")
        principles.append("Dots and continuous lines reflect continuity and rhythm.")
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
            output = BytesIO(); output.write(principles.encode('utf-8')); output.seek(0)
            st.download_button("📥 Download Principles as Text", data=output, file_name="kolam_principles.txt", mime="text/plain", key="download_princ")
        except Exception as e:
            st.error(f"Analysis failed: {e}")

    if st.button("⬅ Back to Home", key="analyzer_back"):
        st.session_state.page = "Home"
        st.experimental_rerun()

def page_learn_more():
    st.header("📘 Learn About Kolam")
    st.markdown(
        """
        **What is Kolam?**

        Kolam is a traditional South Indian floor drawing made with rice flour or chalk powder.
        It uses dots arranged in grids and continuous lines interweaving around them.

        **Cultural significance**
        - Drawn daily for auspiciousness and to welcome guests.
        - Symbolizes balance, continuity, and prosperity.
        - Simpler kolams are for everyday use; complex kolams for festivals.

        **Design principles**
        1. Dot-grid foundation — dots scaffold the lines.
        2. Continuity — lines are often drawn as unbroken strokes.
        3. Symmetry and rhythm — repeated motifs and bilateral balance.
        4. Local styles and improvisation — varied regional forms.
        5. Temporality and community — often an ephemeral, communal practice.
        """
    )
    if st.button("⬅ Back to Home", key="learn_back"):
        st.session_state.page = "Home"
        st.experimental_rerun()

def page_community():
    st.header("🌐 Community Kolam Gallery")
    st.markdown("Curated public kolam images (external sources).")
    # A few safe example URLs (commons)
    urls = [
        "https://upload.wikimedia.org/wikipedia/commons/5/57/Kolam_1.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/9/91/Kolam_design.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/d/d0/Tamil_Kolam.jpg"
    ]
    cols = st.columns(3)
    for i, url in enumerate(urls):
        try:
            cols[i].image(url, use_column_width=True, caption=f"Community {i+1}")
        except Exception:
            cols[i].write("Image load failed.")
    if st.button("⬅ Back to Home", key="community_back"):
        st.session_state.page = "Home"
        st.experimental_rerun()

# ---------------- Router ----------------
page_map = {
    "Home": page_home,
    "Basic Kolam": page_basic,
    "Complex Kolam": page_complex,
    "Analyzer": page_analyzer,
    "Learn More": page_learn_more,
    "Community": page_community
}

current = st.session_state.page if "page" in st.session_state else "Home"
page_map.get(current, page_home)()

# ------------- End of app -------------
