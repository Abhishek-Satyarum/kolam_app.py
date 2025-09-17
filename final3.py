# file: kolam_suite_app.py
import streamlit as st
from streamlit.components.v1 import html
import matplotlib.pyplot as plt
import numpy as np
import cv2
from io import BytesIO
from PIL import Image

# --- CONFIG ---
st.set_page_config(page_title="Kolam Konnect", layout="wide")

# --- SESSION STATE for Tab Navigation ---
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Home"

def switch_tab(tab):
    st.session_state.active_tab = tab

# --- LOGO (placeholder) ---
st.sidebar.image("logo.jpg", width=100, caption="Kolam Konnect")

# === TABS LIST ===
tabs = ["Home", "Kolam Generator", "Unsymmetrical Dots", "Kolam Analyzer", "Community"]

# --- HOME TAB ---
if st.session_state.active_tab == "Home":
    page = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <script src="https://cdn.tailwindcss.com"></script>
      <title>Kolam Konnect</title>
    </head>
    <body class="bg-gradient-to-b from-orange-50 to-pink-50 text-gray-800">
      <header class="flex justify-between items-center px-6 py-4 shadow-sm bg-white">
        <div class="flex items-center space-x-2">
          <div class="w-8 h-8 bg-gray-300 rounded-md"></div>
          <h1 class="font-semibold text-lg">Kolam Konnect</h1>
        </div>
        <nav class="hidden md:flex space-x-6 font-medium">
          <a href="#" onclick="window.parent.postMessage({{type:'switch','tab':'Kolam Generator'}}, '*');return false;" class="hover:text-orange-500">Draw</a>
          <a href="#" onclick="window.parent.postMessage({{type:'switch','tab':'Community'}}, '*');return false;" class="hover:text-orange-500">Community</a>
          <a href="#" onclick="window.parent.postMessage({{type:'switch','tab':'Kolam Analyzer'}}, '*');return false;" class="hover:text-orange-500">Learn</a>
        </nav>
        <button class="bg-orange-900 text-white px-4 py-2 rounded-md hover:bg-orange-800">Login</button>
      </header>

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
          <button onclick="window.parent.postMessage({{type:'switch','tab':'Kolam Generator'}}, '*');" class="bg-orange-900 text-white px-6 py-3 rounded-md shadow hover:bg-orange-800">
            Start Drawing ⬇
          </button>
          <button onclick="window.parent.postMessage({{type:'switch','tab':'Kolam Analyzer'}}, '*');" class="border border-orange-300 text-orange-700 px-6 py-3 rounded-md hover:bg-orange-50">
            Learn About Kolam
          </button>
        </div>
      </section>

      <section id="tools" class="bg-white rounded-t-3xl shadow-inner px-6 py-12">
        <h3 class="text-center text-2xl font-bold mb-6">Kolam Tools</h3>
        <div class="flex flex-wrap justify-center gap-4">
          <button onclick="window.parent.postMessage({{type:'switch','tab':'Kolam Generator'}}, '*');" class="bg-gray-100 px-4 py-2 rounded-md hover:bg-gray-200">✨ Random Kolam Art</button>
          <button onclick="window.parent.postMessage({{type:'switch','tab':'Unsymmetrical Dots'}}, '*');" class="bg-gray-100 px-4 py-2 rounded-md hover:bg-gray-200">✨ Asymmetric Patterns</button>
          <button onclick="window.parent.postMessage({{type:'switch','tab':'Kolam Analyzer'}}, '*');" class="bg-gray-100 px-4 py-2 rounded-md hover:bg-gray-200">🔍 Kolam Recognizer</button>
        </div>
      </section>
    </body>
    <script>
      window.addEventListener('message', (e) => {{
        if (e.data.type === 'switch') {{
          window.parent.postMessage(e.data,'*');
        }}
      }});
    </script>
    </html>
    """
    html(page, height=1000, scrolling=True)

# --- TAB: Kolam Generator ---
elif st.session_state.active_tab == "Kolam Generator":
    st.title("🎨 Kolam Pattern Generator (Multiple Types)")
    kolam_type = st.selectbox("Choose Kolam Type:", ["Straight Lines","Connected Diamonds","Diamond with Arcs","Loops/Arcs","Mixed"])
    size = st.slider("Grid Size:",4,10,6)
    line_color = st.color_picker("Kolam Line Color","#B22222")
    dot_color = st.color_picker("Dot Color","#000000")
    bg_color = st.color_picker("Background Color","#FFFFFF")
    line_width = st.slider("Line Width:",1.0,5.0,2.0)
    show_dots = st.checkbox("Show Dots",value=True)

    def draw_diamond(ax,x,y,s=1):
        pts=[(x,y+s/2),(x+s/2,y),(x,y-s/2),(x-s/2,y),(x,y+s/2)]
        xs,ys=zip(*pts);ax.plot(xs,ys,color=line_color,lw=line_width)

    def draw_loop(ax,x,y,r=0.5):
        theta=np.linspace(0,2*np.pi,200)
        ax.plot(x+r*np.cos(theta),y+r*np.sin(theta),color=line_color,lw=line_width)

    def generate_kolam(n):
        fig,ax=plt.subplots(figsize=(8,8));ax.set_facecolor(bg_color);ax.axis("off")
        spacing=1
        if show_dots:
            for i in range(n):
                for j in range(n):
                    ax.plot(i*spacing,j*spacing,'o',color=dot_color,markersize=5)
        if kolam_type=="Straight Lines":
            for i in range(n):
                ax.plot([0,(n-1)*spacing],[i*spacing,i*spacing],color=line_color,lw=line_width)
                ax.plot([i*spacing,i*spacing],[0,(n-1)*spacing],color=line_color,lw=line_width)
        elif kolam_type=="Connected Diamonds":
            for i in range(n-1):
                for j in range(n-1):
                    draw_diamond(ax,(i+0.5)*spacing,(j+0.5)*spacing,s=spacing)
        elif kolam_type=="Loops/Arcs":
            for i in range(n):
                for j in range(n):
                    draw_loop(ax,i*spacing,j*spacing,r=spacing/2.2)
        st.pyplot(fig)

    if st.button("🎨 Generate Kolam"): generate_kolam(size)

# --- TAB: Unsymmetrical Dots ---
elif st.session_state.active_tab == "Unsymmetrical Dots":
    st.title("🔷 Unsymmetrical Dots Kolam Generator")
    max_dots=st.slider("Max Dots:",3,9,5)
    line_color2=st.color_picker("Line Color","#FFFFFF")
    dot_color2=st.color_picker("Dot Color","#FFFFFF")
    bg_color2=st.color_picker("Background Color","#000000")
    line_width2=st.slider("Line Width:",1.0,5.0,2.5)
    spacing2=st.slider("Dot Spacing:",0.5,2.0,1.0)
    show_dots2=st.checkbox("Show Dots",value=True)

    def generate_dot_positions(max_dots, spacing):
        rows=max_dots+1;dot_positions=[]
        half=rows//2
        for i in range(rows):
            count=1+2*i if i<half else 1+2*(rows-i-1)
            offset=-(count-1)/2*spacing
            for j in range(count):
                dot_positions.append((offset+j*spacing,-i*spacing))
        return dot_positions

    def generate_kolam2():
        dot_positions=generate_dot_positions(max_dots,spacing2)
        fig,ax=plt.subplots(figsize=(8,8));ax.set_facecolor(bg_color2);ax.axis("off")
        if show_dots2:
            xs,ys=zip(*dot_positions);ax.scatter(xs,ys,color=dot_color2,s=40)
        st.pyplot(fig)

    if st.button("🎨 Generate Kolam"): generate_kolam2()

# --- TAB: Kolam Analyzer ---
elif st.session_state.active_tab == "Kolam Analyzer":
    st.title("📊 Kolam Design Principles Analyzer")
    uploaded_file=st.file_uploader("Upload a Kolam image",type=["jpg","jpeg","png"])

    def analyze_kolam(image):
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        h,w=gray.shape;mid=w//2
        left=gray[:,:mid];right=cv2.flip(gray[:,mid:],1)
        min_width=min(left.shape[1],right.shape[1])
        left=left[:,:min_width];right=right[:,:min_width]
        symmetry_score=np.sum(left==right)/left.size
        edges=cv2.Canny(gray,50,150)
        line_density=np.sum(edges>0)/edges.size
        contours,_=cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        complexity=len(contours)
        return symmetry_score,line_density,complexity,edges

    if uploaded_file:
        img=Image.open(uploaded_file);st.image(img,caption="Uploaded Kolam")
        img_array=np.array(img.convert("RGB"));img_array=cv2.cvtColor(img_array,cv2.COLOR_RGB2BGR)
        symmetry_score,line_density,complexity,edges=analyze_kolam(img_array)
        st.write(f"**Symmetry Score:** {symmetry_score:.2f}")
        st.write(f"**Line Density:** {line_density:.2f}")
        st.write(f"**Complexity:** {complexity}")
        st.image(edges,caption="Detected Edges",use_column_width=True)

# --- TAB: Community ---
elif st.session_state.active_tab == "Community":
    st.title("🖼 Community Gallery")
    st.image([
        "https://source.unsplash.com/600x400/?kolam",
        "https://source.unsplash.com/600x400/?rangoli",
        "https://source.unsplash.com/600x400/?community,people"
    ], width=300, caption=["Kolam 1","Kolam 2","Community"])

# --- NAVIGATION BUTTONS ---
st.sidebar.markdown("### Navigation")
for t in tabs:
    if st.sidebar.button(t): switch_tab(t)

