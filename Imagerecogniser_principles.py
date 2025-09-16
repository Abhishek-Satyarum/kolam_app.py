import streamlit as st
import cv2
import numpy as np
import tempfile
from io import StringIO

st.set_page_config(page_title="Kolam Principles Analyzer", layout="centered")
st.title("🎨 Kolam Design Principles Analyzer")

uploaded_file = st.file_uploader("Upload your Kolam image", type=["jpg", "jpeg", "png"])

def analyze_kolam(image):
    """Analyze symmetry, repetition, and connectivity of a Kolam image."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # Count connected components (approx. number of motifs)
    num_labels, labels = cv2.connectedComponents(thresh)

    # Vertical symmetry check
    flipped = cv2.flip(thresh, 1)
    vertical_symmetry = np.sum(thresh == flipped) / thresh.size

    # Horizontal symmetry check
    flipped_h = cv2.flip(thresh, 0)
    horizontal_symmetry = np.sum(thresh == flipped_h) / thresh.size

    # Repetition check using contour areas
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    areas = [cv2.contourArea(c) for c in contours if cv2.contourArea(c) > 10]
    repetition = "Yes" if len(set(np.round(a, -1) for a in areas)) < len(areas)/2 else "Limited"

    # Connectivity estimation
    connectivity = "Highly connected" if num_labels < 10 else "Moderately connected"

    # Generate principles
    principles = []
    if vertical_symmetry > 0.85:
        principles.append("The design is **vertically symmetric**.")
    if horizontal_symmetry > 0.85:
        principles.append("The design is **horizontally symmetric**.")
    if not principles:
        principles.append("The design does **not** exhibit strong mirror symmetry.")

    principles.append(f"Repetition of motifs: **{repetition}**.")
    principles.append(f"Connectivity: **{connectivity}** (components detected: {num_labels}).")

    return "\n".join(principles)

if uploaded_file is not None:
    # Load image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption="Uploaded Kolam", use_column_width=True)

    # Analyze
    result = analyze_kolam(image)
    st.subheader("📜 Detected Design Principles")
    st.markdown(result)

    # Provide download option
    output = StringIO()
    output.write("Kolam Design Principles Analysis\n\n")
    output.write(result)
    st.download_button(
        label="📥 Download Analysis",
        data=output.getvalue(),
        file_name="kolam_principles.txt",
        mime="text/plain"
    )
else:
    st.info("Please upload a Kolam image to analyze.")
