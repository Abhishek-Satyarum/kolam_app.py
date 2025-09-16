import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

st.set_page_config(page_title="Kolam Principles Analyzer", layout="wide")
st.title("🎨 Kolam Principles Analyzer (Image-Based)")

uploaded_file = st.file_uploader("Upload a Kolam image (PNG/JPG):", type=["png", "jpg", "jpeg"])

def analyze_kolam(img_array):
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 100, 200)

    # Estimate symmetry (compare left/right halves)
    h, w = edges.shape
    left = edges[:, :w//2]
    right = np.fliplr(edges[:, w//2:])
    symmetry_score = np.sum(left == right) / left.size

    # Estimate line density (ratio of edge pixels)
    line_density = np.sum(edges > 0) / edges.size

    # Detect number of contours (complexity)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    complexity = len(contours)

    return symmetry_score, line_density, complexity, edges

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)
    st.image(image, caption="Uploaded Kolam Image", use_column_width=True)

    # Download option
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    st.download_button("📥 Download Image", data=buf.getvalue(), file_name="kolam_uploaded.png")

    # Analyze
    symmetry_score, line_density, complexity, edges = analyze_kolam(img_array)
    st.subheader("Edge Detection Preview")
    st.image(edges, use_column_width=True)

    # Generate tailored principles
    st.subheader("🌟 Kolam Design Principles for Your Image:")
    principles = []

    # Symmetry principle
    if symmetry_score > 0.85:
        principles.append(
            f"1. **High Symmetry** – Your Kolam exhibits near-perfect mirror symmetry "
            f"({symmetry_score:.2f}), a hallmark of traditional patterns symbolizing balance and harmony."
        )
    else:
        principles.append(
            f"1. **Moderate Symmetry** – The symmetry score is {symmetry_score:.2f}, suggesting a creative, "
            f"slightly asymmetric layout that breaks from tradition while remaining aesthetically appealing."
        )

    # Line density principle
    if line_density > 0.08:
        principles.append(
            f"2. **Dense Linework** – A higher line density ({line_density:.2f}) indicates rich decorative detail "
            f"and intricate weaving around the dots."
        )
    else:
        principles.append(
            f"2. **Minimal Linework** – With a lower line density ({line_density:.2f}), the design emphasizes "
            f"simplicity and open space, typical of minimalist Kolam styles."
        )

    # Complexity principle
    if complexity > 50:
        principles.append(
            f"3. **Complex Motifs** – The design contains {complexity} unique contours, showing fractal-like repetition "
            f"and advanced geometric composition."
        )
    else:
        principles.append(
            f"3. **Moderate Complexity** – With {complexity} contours, this Kolam balances simplicity with ornamental elements."
        )

    # Continuity principle
    principles.append(
        "4. **Continuity of Curves** – The edges show smooth, continuous curves typical of Kolams, symbolizing the unbroken flow of life."
    )

    # Cultural context
    principles.append(
        "5. **Cultural Symbolism** – Such patterns traditionally represent prosperity, welcoming energy, "
        "and respect for natural order, reinforcing harmony between art and environment."
    )

    for p in principles:
        st.markdown(p)

else:
    st.info("⬆️ Please upload a Kolam image to analyze its unique design principles.")
