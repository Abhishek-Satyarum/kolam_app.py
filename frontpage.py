# file: kolam_frontpage.py
import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Kolam Konnect", layout="wide")

# Tailwind CDN + HTML content
page = """
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
    <!-- Logo placeholder -->
    <div class="flex items-center space-x-2">
      <div class="w-8 h-8 bg-gray-300 rounded-md"></div>
      <h1 class="font-semibold text-lg">Kolam Konnect</h1>
    </div>
    <nav class="hidden md:flex space-x-6 font-medium">
      <a href="#draw" class="hover:text-orange-500">Draw</a>
      <a href="#community" class="hover:text-orange-500">Community</a>
      <a href="#learn" class="hover:text-orange-500">Learn</a>
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
      <button onclick="alert('Start Drawing clicked')" class="bg-orange-900 text-white px-6 py-3 rounded-md shadow hover:bg-orange-800">
        Start Drawing ⬇
      </button>
      <button onclick="alert('Learn About Kolam clicked')" class="border border-orange-300 text-orange-700 px-6 py-3 rounded-md hover:bg-orange-50">
        Learn About Kolam
      </button>
    </div>
  </section>

  <!-- Kolam Tools -->
  <section id="tools" class="bg-white rounded-t-3xl shadow-inner px-6 py-12">
    <h3 class="text-center text-2xl font-bold mb-6">Kolam Tools</h3>
    <p class="text-center text-gray-600 mb-8">
      Generate random kolam patterns and analyze existing designs with our advanced tools.
    </p>

    <div class="flex flex-wrap justify-center gap-4">
      <button onclick="alert('Random Kolam Art clicked')" class="flex items-center space-x-2 bg-gray-100 px-4 py-2 rounded-md hover:bg-gray-200">
        ✨ <span>Random Kolam Art</span>
      </button>
      <button onclick="alert('Asymmetric Patterns clicked')" class="flex items-center space-x-2 bg-gray-100 px-4 py-2 rounded-md hover:bg-gray-200">
        ✨ <span>Asymmetric Patterns</span>
      </button>
      <button onclick="alert('Kolam Recognizer clicked')" class="flex items-center space-x-2 bg-gray-100 px-4 py-2 rounded-md hover:bg-gray-200">
        🔍 <span>Kolam Recognizer</span>
      </button>
    </div>

    <div class="mt-10 max-w-xl mx-auto bg-gray-50 border rounded-lg p-6">
      <h4 class="font-semibold text-lg">Kolam Pattern Recognizer</h4>
      <p class="text-gray-600 text-sm mt-2">
        Upload a kolam image to analyze its design principles and characteristics.
      </p>
      <button onclick="alert('Upload clicked')" class="mt-4 bg-orange-900 text-white px-4 py-2 rounded hover:bg-orange-800">
        Upload Image
      </button>
    </div>
  </section>

  <footer class="text-center py-6 text-gray-500 text-sm">
    © 2025 Kolam Konnect. All rights reserved.
  </footer>
</body>
</html>
"""

# Render HTML in Streamlit
html(page, height=1200, scrolling=True)
