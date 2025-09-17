import streamlit as st
import base64
import requests
from io import BytesIO
from PIL import Image

# === PAGE CONFIG ===
st.set_page_config(page_title="Kolam Suite", layout="wide")

# === LOAD LOGO ===
def load_logo(path="logo.jpg"):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

logo_b64 = load_logo()

# === HEADER ===
header_html = f"""
<style>
    .main-header {{
        display: flex; justify-content: space-between; align-items: center;
        padding: 10px 40px; background-color: white; box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
    }}
    .logo-title {{
        display: flex; align-items: center;
    }}
    .logo-title img {{
        height: 50px; margin-right: 15px;
    }}
    .app-title {{
        font-size: 28px; font-weight: 700;
        background: linear-gradient(90deg, #FF512F, #F09819);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .nav-links a {{
        margin: 0 15px; text-decoration: none; font-weight: 500; color: #444;
        font-size: 18px;
    }}
    .nav-links a:hover {{
        color: #FF512F;
    }}
</style>
<div class="main-header">
  <div class="logo-title">
    {'<img src="data:image/png;base64,' + logo_b64 + '">' if logo_b64 else ''}
    <div class="app-title">Kolam Arts</div>
  </div>
  <div class="nav-links">
    <a href="#draw">Draw</a>
    <a href="#community">Community</a>
    <a href="#learn">Learn</a>
    <a href="#login">Login</a>
  </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# === HERO SECTION ===
st.markdown("""
<style>
.hero {
    text-align: center;
    padding: 80px 20px;
    background: #f9f9f9;
}
.hero h1 {
    font-size: 48px;
    font-weight: bold;
    margin-bottom: 10px;
}
.hero p {
    font-size: 20px;
    color: #666;
    margin-bottom: 30px;
}
.hero button {
    background: linear-gradient(90deg, #FF512F, #F09819);
    color: white; padding: 12px 28px; border: none; border-radius: 25px;
    font-size: 18px; cursor: pointer;
}
.hero button:hover {
    opacity: 0.9;
}
</style>
<div class="hero">
  <h1>Create Stunning Kolam Patterns</h1>
  <p>Discover, analyze, and share traditional Kolam art.</p>
  <form action="#draw">
    <button>Explore Kolam Suite</button>
  </form>
</div>
""", unsafe_allow_html=True)

# === MAIN CONTENT ===
st.markdown("<h2 id='draw'>🎨 Kolam Suite</h2>", unsafe_allow_html=True)
tab1, tab2, tab3, tab4 = st.tabs(
    ["Random Kolam Art", "Asymmetric Patterns", "Kolam Recognizer", "Community"]
)

# === TAB 1: Kolam Generator ===
with tab1:
    st.subheader("Kolam Generator")
    st.info("Embed your existing Kolam Generator app here.")

# === TAB 2: Unsymmetrical Dots ===
with tab2:
    st.subheader("Unsymmetrical Dots Generator")
    st.info("Embed your Unsymmetrical Dots app here.")

# === TAB 3: Kolam Analyzer ===
with tab3:
    st.subheader("Kolam Analyzer")
    st.info("Embed your Kolam Analyzer here.")

# === TAB 4: COMMUNITY ===
with tab4:
    st.subheader("Community Kolams")
    cols = st.columns(3)
    urls = [
        "https://upload.wikimedia.org/wikipedia/commons/9/9d/Kolam_1.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/6/67/Kolam_design.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/e/eb/Kolam_Rangoli.jpg",
    ]
    for i, url in enumerate(urls):
        resp = requests.get(url)
        img = Image.open(BytesIO(resp.content))
        cols[i].image(img, use_column_width=True, caption=f"Kolam {i+1}")

# === FOOTER ===
st.markdown("""
<hr>
<p style='text-align:center; color:#888;'>© 2025 Kolam Arts Community</p>
""", unsafe_allow_html=True)
