import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import cv2
from io import BytesIO
from PIL import Image
from streamlit.components.v1 import html

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Kolam Konnect", layout="wide")

# Session state to track page navigation
if "page" not in st.session_state:
    st.session_state.page = "home"

# ------------------ NAVIGATION ------------------
def go_to(page):
    st.session_state.page = page

# ------------------ HOME PAGE ------------------
def home():
    page_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <script src="https://cdn.tailwindcss.com"></script>
      <title>Kolam Konnect</title>
    </head>
    <body class="bg-gradient-to-b from-orange-50 to-pink-50 text-gray-800">

      <!-- Header -->
      <header class="flex justify-between items-center px-6 py-4 shadow-sm bg-white">
      <img src="logo.jpg" alt="Kolam Logo" class="w-8 h-8 rounded-md"/>
        <div class="flex items-center space-x-2">
          <div class="w-8 h-8 bg-gray-300 rounded-md"></div>
          <h1 class="font-semibold text-lg">Kolam Konnect</h1>
        </div>
        <nav class="hidden md:flex space-x-6 font-medium">
          <a href="#" onclick="parent.postMessage({type:'draw'}, '*')" class="hover:text-orange-500">Draw</a>
          <a href="#" class="hover:text-orange-500">Community</a>
          <a href="#" class="hover:text-orange-500">Learn</a>
        </nav>
        <button onclick="alert('Login clicked')" class="bg-orange-900 text-white px-4 py-2 rounded-md hover:bg-orange-800">Login</button>
      </header>

      <!-- Hero Section -->
      <section class="text-center px-4 py-16">
        <span class="bg-orange-100 text-orange-700 px-4 py-1 rounded-full text-sm font-medium">
          ✨ Traditional Art Meets Digital Innovation
        </span>
        <h2 class="mt-6 text-4xl md:text-5xl font-bold">
          Create Beautiful <span class="bg-clip-text text-transparent bg-gradient-to-r from-red-500 to-orange-400">Kolam Arts</span>
        </h2>
        <p class="mt-4 text-gray-600 max-w-2xl mx-auto">
          Discover the ancient art of Kolam through our interactive digital canvas. Draw, learn, and connect with traditional Indian patterns and a global community.
        </p>
        <div class="mt-8 flex justify-center space-x-4">
          <button onclick="parent.postMessage({type:'draw'}, '*')" class="bg-orange-900 text-white px-6 py-3 rounded-md shadow hover:bg-orange-800">
            Start Drawing ⬇
          </button>
          <button onclick="alert('Learn About Kolam clicked')" class="border border-orange-300 text-orange-700 px-6 py-3 rounded-md hover:bg-orange-50">
            Learn About Kolam
          </button>
        </div>
      </section>

      <section id="tools" class="bg-white rounded-t-3xl shadow-inner px-6 py-12">
        <h3 class="text-center text-2xl font-bold mb-6">Kolam Tools</h3>
        <p class="text-center text-gray-600 mb-8">
          Generate random kolam patterns and analyze existing designs with our advanced tools.
        </p>

        <div class="flex flex-wrap justify-center gap-4">
          <button onclick="parent.postMessage({type:'draw'}, '*')" class="flex items-center space-x-2 bg-gray-100 px-4 py-2 rounded-md hover:bg-gray-200">
            ✨ <span>Random Kolam Art</span>
          </button>
          <button onclick="parent.postMessage({type:'dots'}, '*')" class="flex items-center space-x-2 bg-gray-100 px-4 py-2 rounded-md hover:bg-gray-200">
            ✨ <span>Asymmetric Patterns</span>
          </button>
          <button onclick="parent.postMessage({type:'analyze'}, '*')" class="flex items-center space-x-2 bg-gray-100 px-4 py-2 rounded-md hover:bg-gray-200">
            🔍 <span>Kolam Recognizer</span>
          </button>
        </div>
      </section>

      <footer class="text-center py-6 text-gray-500 text-sm">
        © 2025 Kolam Konnect. All rights reserved.
      </footer>
    </body>
    </html>
    """
    html(page_html, height=1000)
    # Capture clicks from iframe
    st.markdown(
        """
        <script>
        window.addEventListener('message', (e) => {
          if (e.data.type === 'draw') {
            parent.postMessage({type:'streamlit:setSessionState', key:'page', value:'draw'}, '*');
          }
          if (e.data.type === 'dots') {
            parent.postMessage({type:'streamlit:setSessionState', key:'page', value:'dots'}, '*');
          }
          if (e.data.type === 'analyze') {
            parent.postMessage({type:'streamlit:setSessionState', key:'page', value:'analyze'}, '*');
          }
        });
        </script>
        """,
        unsafe_allow_html=True,
    )

# ------------------ DRAW GENERATOR ------------------
def draw_generator():
    st.title("🎨 Kolam Generator (Types)")
    kolam_type = st.selectbox(
        "Choose Kolam Type:", ["Straight Lines", "Connected Diamonds", "Diamond with Arcs", "Loops/Arcs", "Mixed"]
    )
    size = st.slider("Grid Size:", 4, 10, 6)
    line_color = st.color_picker("Kolam Line Color:", "#B22222")
    dot_color = st.color_picker("Dot Color:", "#000000")
    bg_color = st.color_picker("Background Color:", "#FFFFFF")
    line_width = st.slider("Line Width:", 1.0, 5.0, 2.0)
    show_dots = st.checkbox("Show Dots", value=True)

    def draw_diamond(ax, x, y, s=1):
        pts = [(x, y+s/2), (x+s/2, y), (x, y-s/2), (x-s/2, y), (x, y+s/2)]
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=line_color, lw=line_width)

    def generate_kolam(n):
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_facecolor(bg_color)
        ax.axis("off")
        spacing = 1
        if show_dots:
            for i in range(n):
                for j in range(n):
                    ax.plot(i*spacing, j*spacing, 'o', color=dot_color)
        if kolam_type == "Straight Lines":
            for i in range(n):
                ax.plot([0, (n-1)*spacing], [i*spacing, i*spacing], color=line_color, lw=line_width)
        else:
            for i in range(n-1):
                for j in range(n-1):
                    draw_diamond(ax, i, j, s=spacing)
        ax.set_aspect("equal")
        st.pyplot(fig)

    if st.button("Generate"):
        generate_kolam(size)

# ------------------ DOTS GENERATOR ------------------
def dots_generator():
    st.title("🔷 Unsymmetrical Dots Kolam Generator")
    st.write("Your second generator code goes here (reuse Tab 2 code).")

# ------------------ ANALYZER ------------------
def analyzer():
    st.title("📊 Kolam Analyzer")
    uploaded_file = st.file_uploader("Upload Kolam Image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Kolam", use_column_width=True)

# ------------------ ROUTING ------------------
if st.session_state.page == "home":
    home()
elif st.session_state.page == "draw":
    draw_generator()
elif st.session_state.page == "dots":
    dots_generator()
elif st.session_state.page == "analyze":
    analyzer()

st.sidebar.button("🏠 Home", on_click=lambda: go_to("home"))
