# kolam_konnect_app.py
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import cv2
from io import BytesIO
from PIL import Image
import requests
import textwrap

# ---------------- App config ----------------
st.set_page_config(page_title="Kolam Konnect", layout="wide", initial_sidebar_state="auto")

# ---------------- Load logo ----------------
def load_logo(path="logo.jpg"):
    try:
        return Image.open(path)
    except Exception:
        return None

LOGO = load_logo("logo.jpg")

# ---------------- CSS (theme approx) ----------------
st.markdown(
    """
    <style>
    /* page background */
    .stApp {
        background: linear-gradient(90deg, #FFF1E6 0%, #FFEFF0 100%);
    }
    /* header style */
    .kolam-header {
        display:flex;
        align-items:center;
        gap:12px;
    }
    .kolam-title {
        font-size:20px;
        font-weight:700;
        color:#2b2b2b;
    }
    .hero-title {
        font-size:48px;
        font-weight:800;
        margin:0;
        line-height:1.0;
    }
    .hero-sub {
        color:#6b6b6b;
        font-size:18px;
        max-width:900px;
        margin:auto;
    }
    .rounded-btn {
        border-radius:10px;
        padding:10px 18px;
        background:#5a1f11;
        color:white;
        border:none;
    }
    .secondary-btn {
        border-radius:10px;
        padding:10px 18px;
        border:1px solid #f2b9a3;
        color:#b3472b;
        background:transparent;
    }
    .pill {
        display:inline-block;
        background:#fff1e0;
        color:#b3472b;
        padding:6px 12px;
        border-radius:999px;
        font-weight:600;
    }
    .tools-card {
        background:white;
        border-radius:16px;
        padding:18px;
        box-shadow: 0 6px 14px rgba(0,0,0,0.04);
    }
    /* small adjustments for streamlit elements */
    .stButton>button {
        border-radius:8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- Session state for navigation ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"

def navigate(page_name):
    st.session_state.page = page_name

# ---------------- Header (logo + name shown on every page) ----------------
def show_header():
    cols = st.columns([0.12, 0.88])
    with cols[0]:
        if LOGO:
            st.image(LOGO, width=60)
        else:
            st.markdown("<div style='width:60px;height:60px;background:#eee;border-radius:10px;'></div>", unsafe_allow_html=True)
    with cols[1]:
        st.markdown("<div class='kolam-header'><div class='kolam-title'>Kolam Konnect</div></div>", unsafe_allow_html=True)

# ---------------- Home Page ----------------
def home_page():
    show_header()
    st.write("")  # spacing
    # hero
    st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
    st.markdown("<div style='display:inline-block;padding:6px 14px;border-radius:999px;background:#fff4e8;color:#b3472b;font-weight:600;'>✨ Traditional Art Meets Digital Innovation</div>", unsafe_allow_html=True)
    st.markdown("<h1 class='hero-title' style='text-align:center;margin-top:18px;'>Create Beautiful <span style='background: linear-gradient(90deg,#ff3b3b,#ff8a3d); -webkit-background-clip: text; color: transparent;'>Kolam Arts</span></h1>", unsafe_allow_html=True)
    st.markdown("<p class='hero-sub' style='text-align:center;margin-top:12px;'>Discover the ancient art of Kolam through our interactive digital canvas. Draw, learn and connect with traditional Indian patterns and a global community.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # buttons row
    c1, c2, c3 = st.columns([1,1,1])
    with c1:
        if st.button("🎨 Start Drawing (Random Kolam Art)", key="home_gen"):
            navigate("generator")
    with c2:
        if st.button("🔷 Asymmetric Patterns", key="home_asym"):
            navigate("unsymmetrical")
    with c3:
        if st.button("🔍 Kolam Recognizer", key="home_analyze"):
            navigate("analyzer")

    st.write("")
    # Tools section
    st.markdown("<div style='margin-top:30px'/>", unsafe_allow_html=True)
    st.markdown("<div class='tools-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;margin-top:6px'>Kolam Tools</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#666;'>Generate random kolam patterns and analyze existing designs with our advanced tools.</p>", unsafe_allow_html=True)

    t1, t2, t3 = st.columns([1,1,1])
    with t1:
        if st.button("✨ Random Kolam Art (Generator)"):
            navigate("generator")
    with t2:
        if st.button("✨ Asymmetric Patterns (Unsymmetrical)"):
            navigate("unsymmetrical")
    with t3:
        if st.button("🔎 Kolam Recognizer (Analyzer)"):
            navigate("analyzer")

    st.markdown("</div>", unsafe_allow_html=True)

    # Community Gallery (fetch online placeholders)
    st.markdown("---")
    st.header("Community Gallery")
    # provide a small grid of fetched images (placeholder images)
    gallery_urls = [
        "https://picsum.photos/seed/kolamA/400/300",
        "https://picsum.photos/seed/kolamB/400/300",
        "https://picsum.photos/seed/kolamC/400/300",
        "https://picsum.photos/seed/kolamD/400/300",
        "https://picsum.photos/seed/kolamE/400/300",
        "https://picsum.photos/seed/kolamF/400/300",
    ]
    cols = st.columns(3)
    for i, url in enumerate(gallery_urls):
        try:
            resp = requests.get(url, timeout=5)
            img = Image.open(BytesIO(resp.content))
            cols[i % 3].image(img, use_column_width=True, caption=f"Community Kolam {i+1}")
        except Exception:
            cols[i % 3].write("Image load failed")

    st.markdown("---")
    st.write("Footer • Kolam Konnect — Prototype")

# ---------------- Generator (embedded Tab1 code) ----------------
def generator_page():
    show_header()
    st.markdown("---")
    st.header("🎨 Kolam Pattern Generator (Multiple Types)")
    # controls
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

    # drawing helpers
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

    if st.button("🎨 Generate Kolam"):
        generate_kolam(size)

# ---------------- Unsymmetrical dots page (embedded Tab2 code) ----------------
def unsymmetrical_page():
    show_header()
    st.markdown("---")
    st.header("🔷 Unsymmetrical Dots Kolam Generator")
    max_dots = st.slider("Max Dots in Middle Rows:", 3, 9, 5)
    line_color2 = st.color_picker("Line Color:", "#FFFFFF")
    dot_color2 = st.color_picker("Dot Color:", "#FFFFFF")
    bg_color2 = st.color_picker("Background Color:", "#000000")
    line_width2 = st.slider("Line Width:", 1.0, 5.0, 2.5)
    spacing2 = st.slider("Dot Spacing:", 0.5, 2.0, 1.0)
    show_dots2 = st.checkbox("Show Dots", value=True)

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

    if st.button("🎨 Generate Kolam (Asymmetric)"):
        generate_kolam2()

# ---------------- Analyzer page (embedded Tab3 code) ----------------
def analyzer_page():
    show_header()
    st.markdown("---")
    st.header("📊 Kolam Design Principles Analyzer")
    uploaded_file = st.file_uploader("Upload a Kolam image (jpg/png)", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Kolam", use_column_width=True)
        img_array = np.array(img.convert("RGB"))
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

        # analyze
        try:
            gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
            h, w = gray.shape
            mid = w // 2
            left = gray[:, :mid]
            right = cv2.flip(gray[:, mid:], 1)
            min_width = min(left.shape[1], right.shape[1])
            left = left[:, :min_width]
            right = right[:, :min_width]
            symmetry_score = np.sum(left == right) / left.size
        except Exception:
            symmetry_score = 0.0

        edges = cv2.Canny(gray, 50, 150)
        line_density = np.sum(edges > 0) / edges.size
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        complexity = len(contours)

        # generate principles text
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

        st.subheader("Detected Principles")
        for p in principles:
            st.markdown("- " + p)

        st.subheader("Detected Edges")
        st.image(edges, caption="Edge Detection (Canny)", use_column_width=True)

        # download button
        output = BytesIO()
        output.write(("\n\n".join(principles)).encode("utf-8"))
        output.seek(0)
        st.download_button(label="📥 Download Principles as Text", data=output, file_name="kolam_principles.txt", mime="text/plain")

# ---------------- Learn page ----------------
def learn_page():
    show_header()
    st.markdown("---")
    st.header("📚 Learn About Kolam")
    text = textwrap.dedent("""
    Kolam is a traditional South Indian floor art drawn using rice flour or chalk. Here are some design principles and cultural notes:

    1. **Dots & Grid:** Many kolams are based on a grid of dots; the number and arrangement of dots define the pattern's skeleton.
    2. **Continuity:** Lines often form a continuous loop weaving around dots — the unbroken path symbolizes harmony and continuity.
    3. **Symmetry & Rhythm:** Kolams frequently use symmetry and repeating motifs to create a sense of rhythmic balance.
    4. **Scale & Proportion:** The spacing between dots and the relative size of loops or diamonds determines visual smoothness.
    5. **Adaptability:** Patterns can be scaled, combined (loops + diamonds), and stylized, allowing both traditional and modern expressions.
    6. **Cultural Role:** Kolams are drawn to welcome prosperity and are part of daily ritual and festival practices in many households.
    """)
    st.markdown(text)

# ---------------- Community page ----------------
def community_page():
    show_header()
    st.markdown("---")
    st.header("🌍 Community")
    st.write("Example community kolams and contributor placeholders (images fetched online).")
    # Kolam images (placeholder sources)
    kolam_urls = [
        "https://picsum.photos/seed/col1/600/400",
        "https://picsum.photos/seed/col2/600/400",
        "https://picsum.photos/seed/col3/600/400",
        "https://picsum.photos/seed/col4/600/400",
    ]
    cols = st.columns(2)
    for i, url in enumerate(kolam_urls):
        try:
            r = requests.get(url, timeout=5)
            img = Image.open(BytesIO(r.content))
            cols[i % 2].image(img, use_column_width=True, caption=f"Community Kolam {i+1}")
        except Exception:
            cols[i % 2].write("Image load error")

    st.markdown("---")
    st.subheader("Community Contributors")
    avatars = [
        "https://i.pravatar.cc/150?img=10",
        "https://i.pravatar.cc/150?img=11",
        "https://i.pravatar.cc/150?img=12",
        "https://i.pravatar.cc/150?img=13",
    ]
    ccols = st.columns(4)
    for i, url in enumerate(avatars):
        try:
            r = requests.get(url, timeout=5)
            img = Image.open(BytesIO(r.content))
            ccols[i].image(img, width=80, caption=f"Artist {i+1}")
        except:
            ccols[i].write("avatar")

# ---------------- Main routing ----------------
def main():
    # top bar small nav
    with st.container():
        # header and small nav buttons
        show_header()
        nav_cols = st.columns([1,6,1])
        with nav_cols[1]:
            # small inline navigation
            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                if st.button("Home"):
                    navigate("home")
            with c2:
                if st.button("Random Kolam Art"):
                    navigate("generator")
            with c3:
                if st.button("Asymmetric Patterns"):
                    navigate("unsymmetrical")
            with c4:
                if st.button("Kolam Recognizer"):
                    navigate("analyzer")
            with c5:
                if st.button("Community"):
                    navigate("community")
    st.markdown("---")

    page = st.session_state.page
    if page == "home":
        home_page()
    elif page == "generator":
        generator_page()
    elif page == "unsymmetrical":
        unsymmetrical_page()
    elif page == "analyzer":
        analyzer_page()
    elif page == "learn":
        learn_page()
    elif page == "community":
        community_page()
    else:
        home_page()

    # Sidebar quick links
    st.sidebar.title("Navigate")
    if st.sidebar.button("🏠 Home"):
        navigate("home")
    if st.sidebar.button("🎨 Generator"):
        navigate("generator")
    if st.sidebar.button("🔷 Asymmetric"):
        navigate("unsymmetrical")
    if st.sidebar.button("🔍 Analyzer"):
        navigate("analyzer")
    if st.sidebar.button("🌍 Community"):
        navigate("community")
    if st.sidebar.button("📚 Learn"):
        navigate("learn")

if __name__ == "__main__":
    main()
