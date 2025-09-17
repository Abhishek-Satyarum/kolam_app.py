import streamlit as st
import numpy as np
import cv2
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Kolam Design Analyzer", layout="centered")
st.title("🎨 Kolam Design Principles Analyzer")

def analyze_kolam(image):
    # Convert image to grayscale for consistent comparison
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # === Symmetry Analysis ===
    h, w = gray.shape
    mid = w // 2
    left = gray[:, :mid]
    right = cv2.flip(gray[:, mid:], 1)

    # Ensure left and right halves are the same width
    min_width = min(left.shape[1], right.shape[1])
    left = left[:, :min_width]
    right = right[:, :min_width]

    symmetry_score = np.sum(left == right) / left.size

    # === Edge Detection ===
    edges = cv2.Canny(gray, 50, 150)

    # === Line Density ===
    line_density = np.sum(edges > 0) / edges.size

    # === Complexity === (based on contour count)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    complexity = len(contours)

    return symmetry_score, line_density, complexity, edges

def generate_principles(symmetry_score, line_density, complexity):
    principles = []
    if symmetry_score > 0.8:
        principles.append("The Kolam shows **high bilateral symmetry**, a hallmark of traditional designs symbolizing balance and harmony.")
    else:
        principles.append("The Kolam displays **asymmetrical or free-form symmetry**, suggesting a creative or modern interpretation.")

    if line_density > 0.15:
        principles.append("It features **dense linework**, indicating intricate craftsmanship and possibly representing complexity or abundance.")
    else:
        principles.append("The design has **light linework**, reflecting minimalism and simplicity.")

    if complexity > 20:
        principles.append("The pattern is **highly complex**, with multiple interlacing curves and advanced structural planning.")
    elif complexity > 10:
        principles.append("The Kolam shows **moderate complexity**, balancing detail with clarity.")
    else:
        principles.append("The Kolam is **simple and elegant**, focusing on fundamental geometric forms.")

    principles.append("The use of dots and connecting lines reflects **continuity and unity**, common in Kolam traditions.")
    principles.append("The structure indicates **repetition and rhythm**, symbolizing infinite cycles in nature.")
    return "\n\n".join(principles)

# === File Upload ===
uploaded_file = st.file_uploader("Upload a Kolam image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read and display uploaded image
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Kolam", use_column_width=True)

    # Convert to OpenCV format
    img_array = np.array(img.convert("RGB"))
    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    # Analyze
    symmetry_score, line_density, complexity, edges = analyze_kolam(img_array)
    principles = generate_principles(symmetry_score, line_density, complexity)

    st.subheader("📊 Kolam Design Principles")
    st.write(principles)

    # Display detected edges
    st.subheader("Detected Edges")
    st.image(edges, caption="Edge Detection Output", use_column_width=True)

    # Prepare a downloadable text file
    output = BytesIO()
    output.write(principles.encode('utf-8'))
    output.seek(0)
    st.download_button(
        label="📥 Download Principles as Text",
        data=output,
        file_name="kolam_principles.txt",
        mime="text/plain"
    )
