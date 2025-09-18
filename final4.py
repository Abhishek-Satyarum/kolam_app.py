import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import cv2
from io import BytesIO
from PIL import Image

# ---------------------- APP CONFIG ----------------------
st.set_page_config(page_title="Kolam Suite", layout="wide")

# --- CUSTOM STYLE ---
st.markdown("""
    <style>
    body {background: linear-gradient(135deg,#fdfbfb,#ebedee);}
    .stButton>button {background-color:#4CAF50;color:white;border-radius:8px;padding:8px 16px;}
    .stButton>button:hover {background-color:#45a049;color:white;}
    div[data-baseweb="slider"]>div>div {background-color:#4CAF50;}
    </style>
""", unsafe_allow_html=True)

# ---------------------- HOME TAB ----------------------
tabs = st.tabs(["🏠 Home", "🎨 Basic Kolam Generator", "🔷 Complex Kolam Generator", "📚 Learn More", "📊 Kolam Analyzer"])

with tabs[0]:
    col1, col2 = st.columns([3,1])
    with col2:
        if st.button("🔑 Login"):
            st.info("Login functionality placeholder.")
    st.image("logo.jpg", width=200)
    st.title("🌸 Welcome to Kolam Suite")
    st.markdown("""
        Experience the beauty of **Kolam Art**.  
        Choose from **Basic** and **Complex Kolam Generators**, analyze designs, or learn more about this ancient tradition.
    """)

# ---------------------- BASIC KOLAM GENERATOR ----------------------
with tabs[1]:
    st.header("🎨 Basic Kolam Generator")
    kolam_type = st.selectbox("Choose Kolam Type:",
        ["Straight Lines","Connected Diamonds","Loops/Arcs","Mixed"])
    size = st.slider("Grid Size (dots per side):",4,10,6)
    line_color = st.color_picker("Kolam Line Color:","#B22222")
    dot_color = st.color_picker("Dot Color:","#000000")
    bg_color = st.color_picker("Background Color:","#FFFFFF")
    line_width = st.slider("Line Width:",1.0,5.0,2.0)
    show_dots = st.checkbox("Show Dots",value=True,key="dots_basic")

    def draw_diamond(ax,x,y,s=1):
        pts=[(x,y+s/2),(x+s/2,y),(x,y-s/2),(x-s/2,y),(x,y+s/2)]
        xs,ys=zip(*pts);ax.plot(xs,ys,color=line_color,lw=line_width)

    def draw_loop(ax,x,y,r=0.5):
        theta=np.linspace(0,2*np.pi,200)
        ax.plot(x+r*np.cos(theta),y+r*np.sin(theta),color=line_color,lw=line_width)

    def draw_straight(ax,n,spacing):
        for i in range(n):
            ax.plot([0,(n-1)*spacing],[i*spacing,i*spacing],color=line_color,lw=line_width)
            ax.plot([i*spacing,i*spacing],[0,(n-1)*spacing],color=line_color,lw=line_width)

    def generate_basic_kolam(n):
        fig,ax=plt.subplots(figsize=(8,8))
        ax.set_facecolor(bg_color);ax.axis("off");spacing=1
        if show_dots:
            for i in range(n):
                for j in range(n):
                    ax.plot(i*spacing,j*spacing,'o',color=dot_color,markersize=5)
        if kolam_type=="Straight Lines":
            draw_straight(ax,n,spacing)
        elif kolam_type=="Connected Diamonds":
            for i in range(n-1):
                for j in range(n-1):
                    draw_diamond(ax,(i+0.5)*spacing,(j+0.5)*spacing,s=spacing)
        elif kolam_type=="Loops/Arcs":
            for i in range(n):
                for j in range(n):
                    draw_loop(ax,i*spacing,j*spacing,r=spacing/2.2)
        elif kolam_type=="Mixed":
            for i in range(n-1):
                for j in range(n-1):
                    if (i+j)%2==0:
                        draw_diamond(ax,(i+0.5)*spacing,(j+0.5)*spacing,s=spacing)
                    else:
                        draw_loop(ax,(i+0.5)*spacing,(j+0.5)*spacing,r=spacing/2.2)
        ax.set_aspect("equal");st.pyplot(fig)

    if st.button("🎨 Generate Basic Kolam"): generate_basic_kolam(size)

# ---------------------- COMPLEX KOLAM GENERATOR ----------------------
with tabs[2]:
    st.header("🔷 Complex Kolam Generator")
    complex_choice = st.selectbox("Choose Complex Type:",["Unsymmetrical Dots","Diamond with Arcs"])
    line_color2 = st.color_picker("Line Color:", "#FFFFFF")
    dot_color2 = st.color_picker("Dot Color:", "#FFFFFF")
    bg_color2 = st.color_picker("Background Color:", "#000000")
    line_width2 = st.slider("Line Width:",1.0,5.0,2.5)
    spacing2 = st.slider("Dot Spacing:",0.5,2.0,1.0)
    show_dots2 = st.checkbox("Show Dots",value=True,key="dots_complex")
    max_dots=st.slider("Max Dots:",3,9,5)

    def generate_dot_positions(max_dots,spacing):
        rows=max_dots+1;dot_positions=[];half=rows//2
        for i in range(rows):
            count=1+2*i if i<half else 1+2*(rows-i-1)
            offset=-(count-1)/2*spacing
            for j in range(count):
                dot_positions.append((offset+j*spacing,-i*spacing))
        return dot_positions,rows

    def draw_diamond2(ax,x,y,s=1):
        points=[(x,y+s/2),(x+s/2,y),(x,y-s/2),(x-s/2,y),(x,y+s/2)]
        xs,ys=zip(*points);ax.plot(xs,ys,color=line_color2,lw=line_width2)

    def generate_unsymmetrical():
        dot_positions,rows=generate_dot_positions(max_dots,spacing2)
        fig,ax=plt.subplots(figsize=(8,8))
        ax.set_facecolor(bg_color2);ax.axis("off")
        if show_dots2:
            xs,ys=zip(*dot_positions);ax.scatter(xs,ys,color=dot_color2,s=40)
        for idx,(x,y) in enumerate(dot_positions):
            draw_diamond2(ax,x,y,s=spacing2)
        st.pyplot(fig)

    def generate_diamond_arcs():
        n=max_dots;spacing=1;r=0.5;offset=0.01
        fig,ax=plt.subplots(figsize=(8,8))
        ax.set_facecolor(bg_color2);ax.axis("off")
        if show_dots2:
            for i in range(n):
                for j in range(n):
                    ax.plot(i*spacing,j*spacing,'o',color=dot_color2,markersize=5)
        for i in range(n-1):
            for j in range(n-1):
                draw_diamond2(ax,(i+0.5)*spacing,(j+0.5)*spacing,s=spacing)
        for i in range(1,n-1):
            theta=np.linspace(0,np.pi,100)
            ax.plot((i-0.5)*spacing+r+r*np.cos(theta),(n-1)+offset+r*np.sin(theta),color=line_color2,lw=line_width2)
            ax.plot((i-0.5)*spacing+r+r*np.cos(theta),-offset+r*np.sin(-theta),color=line_color2,lw=line_width2)
        ax.set_aspect("equal");st.pyplot(fig)

    if st.button("🎨 Generate Complex Kolam"):
        if complex_choice=="Unsymmetrical Dots":
            generate_unsymmetrical()
        else:
            generate_diamond_arcs()

# ---------------------- LEARN MORE TAB ----------------------
with tabs[3]:
    st.header("📚 Learn More about Kolam")
    st.markdown("""
    **Kolam** is a traditional South Indian art form of creating geometric patterns 
    using rice flour, chalk, or rock powder.  
    It symbolizes prosperity, harmony, and the cyclical nature of life.  
    Kolams are drawn daily at the entrance of homes, often featuring symmetry and repetition.  
    """)

# ---------------------- ANALYZER TAB ----------------------
with tabs[4]:
    st.header("📊 Kolam Design Principles Analyzer")
    uploaded_file = st.file_uploader("Upload a Kolam image",type=["jpg","jpeg","png"])
    def analyze_kolam(image):
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY);h,w=gray.shape;mid=w//2
        left=gray[:,:mid];right=cv2.flip(gray[:,mid:],1)
        min_w=min(left.shape[1],right.shape[1])
        left=left[:,:min_w];right=right[:,:min_w]
        symmetry_score=np.sum(left==right)/left.size
        edges=cv2.Canny(gray,50,150)
        line_density=np.sum(edges>0)/edges.size
        contours,_=cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        complexity=len(contours)
        return symmetry_score,line_density,complexity,edges

    def generate_principles(sym,line,comp):
        p=[]
        p.append("High bilateral symmetry" if sym>0.8 else "Asymmetry present")
        p.append("Dense linework" if line>0.15 else "Light linework")
        p.append("Highly complex" if comp>20 else "Moderate or simple complexity")
        p.append("Repetition and rhythm reflect nature's cycles.")
        return "\n".join(p)

    if uploaded_file:
        img=Image.open(uploaded_file);st.image(img,caption="Uploaded Kolam",use_column_width=True)
        img_array=np.array(img.convert("RGB"));img_array=cv2.cvtColor(img_array,cv2.COLOR_RGB2BGR)
        sym,line,comp,edges=analyze_kolam(img_array)
        st.subheader("📊 Kolam Design Principles");st.write(generate_principles(sym,line,comp))
        st.subheader("Detected Edges");st.image(edges,caption="Edges",use_column_width=True)
        output=BytesIO();output.write(generate_principles(sym,line,comp).encode('utf-8'));output.seek(0)
        st.download_button("📥 Download Principles",data=output,file_name="kolam_principles.txt",mime="text/plain")
