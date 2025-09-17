import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import cv2
from io import BytesIO
from PIL import Image

# ========== PAGE CONFIG ==========
st.set_page_config(page_title="Kolam Konnect", layout="wide")

# === CUSTOM STYLE ===
st.markdown("""
    <style>
    body {background-color: #faf7f5; font-family: 'Arial', sans-serif;}
    h1, h2, h3 {font-weight: 600; color: #7b3f61;}
    .stTabs [role="tablist"] button {font-size:16px; font-weight:600;}
    .title-bar {display:flex; align-items:center; gap:15px; margin-bottom:20px;}
    .title-bar img {border-radius:50%;}
    </style>
""", unsafe_allow_html=True)

# === HEADER WITH LOGO ===
st.markdown('<div class="title-bar"><img src="logo.jpg" width="60"><h1>🌸 Kolam Konnect</h1></div>', unsafe_allow_html=True)

# === TABS ===
tab1, tab2, tab3, tab4 = st.tabs(["🎨 Basic Level Kolam Generator", "🔷 Complex Kolam Generator", "📊 Kolam Analyzer", "👥 Community"])

# --------------------------------------------------------------------------
# === BASIC LEVEL KOLAM GENERATOR ===
with tab1:
    st.subheader("Generate Simple Kolam Patterns")
    kolam_type = st.selectbox("Choose Kolam Type", ["Straight Lines", "Connected Diamonds", "Loops/Arcs", "Mixed"])
    size = st.slider("Grid Size (dots per side):", 4, 10, 6)
    line_color = st.color_picker("Kolam Line Color:", "#B22222")
    dot_color = st.color_picker("Dot Color:", "#000000")
    bg_color = st.color_picker("Background Color:", "#FFFFFF")
    line_width = st.slider("Line Width:", 1.0, 5.0, 2.0)
    show_dots = st.checkbox("Show Dots", value=True)

    def draw_diamond(ax, x, y, s=1):
        pts = [(x,y+s/2),(x+s/2,y),(x,y-s/2),(x-s/2,y),(x,y+s/2)]
        ax.plot(*zip(*pts), color=line_color, lw=line_width)

    def draw_loop(ax, x, y, r=0.5):
        theta = np.linspace(0,2*np.pi,200)
        ax.plot(x+r*np.cos(theta), y+r*np.sin(theta), color=line_color, lw=line_width)

    def draw_straight(ax, n, spacing):
        for i in range(n):
            ax.plot([0,(n-1)*spacing],[i*spacing,i*spacing], color=line_color, lw=line_width)
            ax.plot([i*spacing,i*spacing],[0,(n-1)*spacing], color=line_color, lw=line_width)

    def generate_basic_kolam(n):
        fig, ax = plt.subplots(figsize=(7,7))
        ax.set_facecolor(bg_color); ax.axis("off"); spacing = 1
        if show_dots:
            for i in range(n):
                for j in range(n):
                    ax.plot(i*spacing, j*spacing, 'o', color=dot_color, markersize=5)

        if kolam_type == "Straight Lines":
            draw_straight(ax, n, spacing)
        elif kolam_type == "Connected Diamonds":
            for i in range(n-1):
                for j in range(n-1):
                    draw_diamond(ax,(i+0.5)*spacing,(j+0.5)*spacing,s=spacing)
        elif kolam_type == "Loops/Arcs":
            for i in range(n):
                for j in range(n):
                    draw_loop(ax,i*spacing,j*spacing,r=spacing/2.2)
        elif kolam_type == "Mixed":
            for i in range(n-1):
                for j in range(n-1):
                    if (i+j)%2==0:
                        draw_diamond(ax,(i+0.5)*spacing,(j+0.5)*spacing,s=spacing)
                    else:
                        draw_loop(ax,(i+0.5)*spacing,(j+0.5)*spacing,r=spacing/2.2)
        ax.set_aspect("equal")
        st.pyplot(fig)

    if st.button("🎨 Generate Basic Kolam"):
        generate_basic_kolam(size)

# --------------------------------------------------------------------------
# === COMPLEX KOLAM GENERATOR ===
with tab2:
    st.subheader("Generate Complex Kolam Patterns")
    choice = st.selectbox("Select Type", ["Unsymmetrical Dots Kolam", "Diamond with Arcs Kolam"])

    if choice == "Unsymmetrical Dots Kolam":
        max_dots = st.slider("Max Dots in Middle Rows:",3,9,5)
        line_color2 = st.color_picker("Line Color:","#FFFFFF")
        dot_color2 = st.color_picker("Dot Color:","#FFFFFF")
        bg_color2 = st.color_picker("Background Color:","#000000")
        line_width2 = st.slider("Line Width:",1.0,5.0,2.5)
        spacing2 = st.slider("Dot Spacing:",0.5,2.0,1.0)
        show_dots2 = st.checkbox("Show Dots", value=True)

        def generate_dot_positions(max_dots, spacing):
            rows = max_dots+1; dots=[]; half=rows//2
            for i in range(rows):
                count=1+2*i if i<half else 1+2*(rows-i-1)
                offset=-(count-1)/2*spacing
                for j in range(count): dots.append((offset+j*spacing,-i*spacing))
            return dots, rows

        def draw_diamond2(ax,x,y,s=1):
            points=[(x,y+s/2),(x+s/2,y),(x,y-s/2),(x-s/2,y),(x,y+s/2)]
            ax.plot(*zip(*points), color=line_color2, lw=line_width2)

        def find_border_indices(dot_positions, rows):
            borders=set(); row_dict={}
            for idx,(x,y) in enumerate(dot_positions):
                row_dict.setdefault(y,[]).append(idx)
            for row in row_dict.values():
                if len(row)>1:
                    borders.add(row[0]); borders.add(row[-1])
                else: borders.add(row[0])
            return borders

        def generate_unsymmetrical():
            dots, rows = generate_dot_positions(max_dots, spacing2)
            borders = find_border_indices(dots, rows)
            fig,ax=plt.subplots(figsize=(7,7)); ax.set_facecolor(bg_color2); ax.axis("off")
            if show_dots2:
                xs,ys=zip(*dots); ax.scatter(xs,ys,color=dot_color2,s=40)
            for idx,(x,y) in enumerate(dots):
                if idx not in borders:
                    draw_diamond2(ax,x,y,s=spacing2)
            for idx1,(x1,y1) in enumerate(dots):
                for idx2,(x2,y2) in enumerate(dots):
                    if idx1<idx2 and abs(x1-x2)==spacing2 and abs(y1-y2)==spacing2:
                        ax.plot([x1,x2],[y1,y2],color=line_color2,lw=line_width2)
            ax.set_aspect("equal")
            st.pyplot(fig)

        if st.button("🎨 Generate Complex Kolam"):
            generate_unsymmetrical()

    else:  # Diamond with Arcs Kolam
        size = st.slider("Grid Size (dots per side):",4,10,6)
        line_color = st.color_picker("Line Color:", "#B22222")
        dot_color = st.color_picker("Dot Color:", "#000000")
        bg_color = st.color_picker("Background:", "#FFFFFF")
        line_width = st.slider("Line Width:",1.0,5.0,2.0)
        show_dots = st.checkbox("Show Dots", value=True)

        def draw_diamond(ax,x,y,s=1):
            pts=[(x,y+s/2),(x+s/2,y),(x,y-s/2),(x-s/2,y),(x,y+s/2)]
            ax.plot(*zip(*pts), color=line_color, lw=line_width)

        def draw_arc(ax,x,y,r=0.6,start=0,end=180):
            theta=np.linspace(np.radians(start),np.radians(end),100)
            ax.plot(x+r*np.cos(theta), y+r*np.sin(theta), color=line_color,lw=line_width)

        def generate_diamond_arcs(n):
            fig,ax=plt.subplots(figsize=(7,7))
            ax.set_facecolor(bg_color); ax.axis("off"); spacing=1; r=0.5; offset=0.01
            if show_dots:
                for i in range(n):
                    for j in range(n):
                        ax.plot(i*spacing,j*spacing,'o',color=dot_color,markersize=5)
            for i in range(n-1):
                for j in range(n-1):
                    draw_diamond(ax,(i+0.5)*spacing,(j+0.5)*spacing,s=spacing)
            for i in range(1,n-1):
                draw_arc(ax,(i-0.5)*spacing+r,(n-1)+offset,r=r,start=0,end=180)
                draw_arc(ax,(i-0.5)*spacing+r,-offset,r=r,start=180,end=360)
            for j in range(1,n-1):
                draw_arc(ax,-offset,(j-0.5)*spacing+r,r=r,start=90,end=270)
                draw_arc(ax,(n-1)+offset,(j-0.5)*spacing+r,r=r,start=270,end=450)
            ax.set_aspect("equal")
            st.pyplot(fig)

        if st.button("🎨 Generate Diamond-Arcs Kolam"):
            generate_diamond_arcs(size)

# --------------------------------------------------------------------------
# === ANALYZER ===
with tab3:
    st.subheader("Kolam Design Principles Analyzer")
    uploaded_file = st.file_uploader("Upload a Kolam image", type=["jpg","jpeg","png"])
    def analyze_kolam(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        h,w = gray.shape; mid = w//2
        left = gray[:,:mid]; right = cv2.flip(gray[:,mid:],1)
        min_w=min(left.shape[1],right.shape[1])
        left,right = left[:,:min_w],right[:,:min_w]
        symmetry_score = np.sum(left==right)/left.size
        edges = cv2.Canny(gray,50,150)
        line_density = np.sum(edges>0)/edges.size
        contours,_=cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        complexity=len(contours)
        return symmetry_score,line_density,complexity,edges

    def generate_principles(symmetry_score,line_density,complexity):
        p=[]
        p.append("High bilateral symmetry" if symmetry_score>0.8 else "Asymmetry suggesting creativity")
        p.append("Dense linework" if line_density>0.15 else "Light linework for simplicity")
        if complexity>20: p.append("Highly complex structure")
        elif complexity>10: p.append("Moderate complexity")
        else: p.append("Simple and elegant")
        p.append("Dots and lines reflect continuity and unity")
        p.append("Repetition and rhythm indicate infinite cycles in nature")
        return "\n\n".join(p)

    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Kolam", use_column_width=True)
        img_array = np.array(img.convert("RGB"))
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        symmetry_score,line_density,complexity,edges = analyze_kolam(img_array)
        st.subheader("📊 Kolam Design Principles")
        st.write(generate_principles(symmetry_score,line_density,complexity))
        st.subheader("Detected Edges")
        st.image(edges,use_column_width=True)

# --------------------------------------------------------------------------
# === COMMUNITY TAB ===
with tab4:
    st.subheader("Kolam Community Showcase")
    st.write("Explore beautiful Kolam designs shared by the community:")
    cols = st.columns(3)
    urls = [
        "https://upload.wikimedia.org/wikipedia/commons/5/59/Kolam_Design_1.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/2/2e/Kolam2.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/4/4e/Kolam_pattern.jpg"
    ]
    for i, url in enumerate(urls):
        with cols[i]:
            st.image(url, use_column_width=True)
