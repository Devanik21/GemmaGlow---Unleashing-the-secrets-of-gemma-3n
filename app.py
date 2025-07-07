import streamlit as st
import google.generativeai as genai
import time
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from textblob import TextBlob
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import base64
from io import BytesIO
import random

# Configure page
st.set_page_config(
    page_title="GemmaGlow ✨",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ultra-premium CSS with next-level aesthetics
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&family=JetBrains+Mono:wght@100;200;300;400;500;600;700;800&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-container {
        backdrop-filter: blur(20px);
        background: rgba(255, 255, 255, 0.05);
        border-radius: 30px;
        padding: 2rem;
        margin: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    }
    
    .hero-section {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border-radius: 25px;
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
    }
    
    .hero-title {
        font-family: 'Inter', sans-serif;
        font-size: 4.5rem;
        font-weight: 900;
        background: linear-gradient(45deg, #fff, #f0f0f0, #fff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 30px rgba(255,255,255,0.3);
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 300;
        color: rgba(255,255,255,0.8);
        margin-bottom: 2rem;
        letter-spacing: 0.02em;
    }
    
    .floating-orbs {
        position: absolute;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1;
    }
    
    .orb {
        position: absolute;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0.1) 70%, transparent 100%);
        animation: float 6s ease-in-out infinite;
        filter: blur(1px);
    }
    
    .orb:nth-child(1) { width: 80px; height: 80px; top: 20%; left: 10%; animation-delay: 0s; }
    .orb:nth-child(2) { width: 60px; height: 60px; top: 60%; left: 80%; animation-delay: 2s; }
    .orb:nth-child(3) { width: 40px; height: 40px; top: 80%; left: 20%; animation-delay: 4s; }
    .orb:nth-child(4) { width: 100px; height: 100px; top: 10%; left: 70%; animation-delay: 1s; }
    .orb:nth-child(5) { width: 30px; height: 30px; top: 40%; left: 50%; animation-delay: 3s; }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    .navigation-bar {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        margin-bottom: 3rem;
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(15px);
        padding: 1rem;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .nav-button {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 15px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
        font-size: 0.9rem;
        letter-spacing: 0.01em;
    }
    
    .nav-button:hover, .nav-button.active {
        background: rgba(255,255,255,0.2);
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(255,255,255,0.1);
        border-color: rgba(255,255,255,0.4);
    }
    
    .feature-card {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 25px 50px rgba(0,0,0,0.2);
        background: rgba(255,255,255,0.12);
        border-color: rgba(255,255,255,0.3);
    }
    
    .glass-input {
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 15px !important;
        backdrop-filter: blur(10px) !important;
        color: white !important;
        font-family: 'Inter', sans-serif !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .glass-input:focus {
        border-color: rgba(255,255,255,0.5) !important;
        box-shadow: 0 0 0 3px rgba(255,255,255,0.1) !important;
        background: rgba(255,255,255,0.15) !important;
    }
    
    .premium-button {
        background: linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.1)) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 15px !important;
        color: white !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        padding: 0.8rem 2rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        backdrop-filter: blur(10px) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        font-size: 0.85rem !important;
    }
    
    .premium-button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 30px rgba(255,255,255,0.2) !important;
        background: linear-gradient(135deg, rgba(255,255,255,0.3), rgba(255,255,255,0.2)) !important;
        border-color: rgba(255,255,255,0.5) !important;
    }
    
    .emotion-indicator {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.5rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    
    .emotion-happy { background: linear-gradient(135deg, #ff9a9e, #fecfef); }
    .emotion-sad { background: linear-gradient(135deg, #a8edea, #fed6e3); }
    .emotion-angry { background: linear-gradient(135deg, #ff6b6b, #feca57); }
    .emotion-excited { background: linear-gradient(135deg, #f093fb, #f5576c); }
    .emotion-calm { background: linear-gradient(135deg, #4facfe, #00f2fe); }
    .emotion-neutral { background: linear-gradient(135deg, #667eea, #764ba2); }
    
    .result-container {
        background: rgba(255,255,255,0.05);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(15px);
        position: relative;
    }
    
    .result-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .result-content {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        line-height: 1.6;
        color: rgba(255,255,255,0.9);
        font-weight: 400;
    }
    
    .sparkle-animation {
        position: absolute;
        width: 4px;
        height: 4px;
        background: white;
        border-radius: 50%;
        animation: sparkle 2s infinite;
    }
    
    @keyframes sparkle {
        0% { opacity: 0; transform: scale(0) rotate(0deg); }
        50% { opacity: 1; transform: scale(1) rotate(180deg); }
        100% { opacity: 0; transform: scale(0) rotate(360deg); }
    }
    
    .loading-spinner {
        border: 3px solid rgba(255,255,255,0.3);
        border-top: 3px solid white;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 1rem auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .mind-map-container {
        background: rgba(0,0,0,0.3);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .theme-selector {
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 15px;
        padding: 1rem;
        z-index: 1000;
    }
    
    .theme-option {
        display: block;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .theme-option:hover {
        transform: scale(1.1);
        border-color: rgba(255,255,255,0.5);
    }
    
    .theme-dreamy { background: linear-gradient(135deg, #ffecd2, #fcb69f); }
    .theme-neon { background: linear-gradient(135deg, #08fdd8, #9d50bb); }
    .theme-solar { background: linear-gradient(135deg, #ff9a9e, #fad0c4); }
    .theme-cosmic { background: linear-gradient(135deg, #667eea, #764ba2); }
    .theme-aurora { background: linear-gradient(135deg, #4facfe, #00f2fe); }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        background: rgba(255,255,255,0.12);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.7);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Custom Streamlit overrides */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 15px !important;
        color: white !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stButton button {
        background: linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.1)) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 15px !important;
        color: white !important;
        font-weight: 600 !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 25px rgba(255,255,255,0.2) !important;
        background: linear-gradient(135deg, rgba(255,255,255,0.3), rgba(255,255,255,0.2)) !important;
    }
    
    .stSidebar {
        background: rgba(255,255,255,0.05) !important;
        backdrop-filter: blur(20px) !important;
    }
    
    .stMarkdown {
        color: rgba(255,255,255,0.9) !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .floating-particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    
    .particle {
        position: absolute;
        width: 2px;
        height: 2px;
        background: rgba(255,255,255,0.5);
        border-radius: 50%;
        animation: float-particle 20s infinite linear;
    }
    
    @keyframes float-particle {
        0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100vh) rotate(360deg); opacity: 0; }
    }
</style>
""", unsafe_allow_html=True)

# Add floating particles
def add_floating_particles():
    particles_html = '<div class="floating-particles">'
    for i in range(50):
        left = random.randint(0, 100)
        delay = random.randint(0, 20)
        particles_html += f'<div class="particle" style="left: {left}%; animation-delay: {delay}s;"></div>'
    particles_html += '</div>'
    st.markdown(particles_html, unsafe_allow_html=True)

add_floating_particles()

# Initialize Gemini
@st.cache_resource
def init_gemini():
    try:
        genai.configure(api_key=st.secrets["gemini_api_key"])
        return genai.GenerativeModel('gemma-3n-e4b-it')
    except Exception as e:
        st.error(f"Gemini initialization failed: {e}")
        return None

model = init_gemini()

def detect_emotion(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    if polarity > 0.3:
        return "happy", "✨", "#ff9a9e"
    elif polarity < -0.3:
        return "sad", "🌙", "#a8edea"
    elif subjectivity > 0.7:
        return "excited", "⚡", "#f093fb"
    elif polarity < -0.1 and subjectivity > 0.5:
        return "angry", "🔥", "#ff6b6b"
    elif abs(polarity) < 0.1 and subjectivity < 0.3:
        return "calm", "🌊", "#4facfe"
    else:
        return "neutral", "🎭", "#667eea"

def generate_response(prompt, context=""):
    if not model:
        return "Gemini API unavailable"
    try:
        response = model.generate_content(f"{context}\n\n{prompt}" if context else prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="floating-orbs">
            <div class="orb"></div>
            <div class="orb"></div>
            <div class="orb"></div>
            <div class="orb"></div>
            <div class="orb"></div>
        </div>
        <div class="hero-title">GemmaGlow</div>
        <div class="hero-subtitle">Next-Generation AI Companion</div>
    </div>
    """, unsafe_allow_html=True)

    # Theme Selector
    st.markdown("""
    <div class="theme-selector">
        <div class="theme-option theme-dreamy" onclick="changeTheme('dreamy')"></div>
        <div class="theme-option theme-neon" onclick="changeTheme('neon')"></div>
        <div class="theme-option theme-solar" onclick="changeTheme('solar')"></div>
        <div class="theme-option theme-cosmic" onclick="changeTheme('cosmic')"></div>
        <div class="theme-option theme-aurora" onclick="changeTheme('aurora')"></div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation
    features = [
        "🌸 MoodSync", "🧠 QuickThink", "✨ CreateSpark",
        "🎭 DebateBot", "🌐 MultiLingua", "🚀 PromptCraft", "💫 ThoughtLoop"
    ]
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(features)

    # Feature 1: MoodSync
    with tab1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🌸 MoodSync - Emotional Intelligence")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            user_input = st.text_area(
                "Express your feelings:",
                placeholder="Share what's on your mind...",
                height=120,
                key="mood_input"
            )
            
            if st.button("🔮 Analyze Emotion", key="mood_btn"):
                if user_input:
                    with st.spinner("Reading your emotional signature..."):
                        emotion, emoji, color = detect_emotion(user_input)
                        
                        empathy_prompt = f"""
                        User's message: "{user_input}"
                        Detected emotion: {emotion}
                        
                        Provide a deeply empathetic, thoughtful response that acknowledges their emotional state.
                        Be warm, understanding, and offer gentle guidance or comfort.
                        """
                        
                        ai_response = generate_response(empathy_prompt)
                        
                        st.markdown(f"""
                        <div class="result-container">
                            <div class="result-title">
                                {emoji} Emotional State: {emotion.title()}
                            </div>
                            <div class="result-content">
                                {ai_response}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 🎭 Emotion Palette")
            emotions = ["happy", "sad", "angry", "excited", "calm", "neutral"]
            for em in emotions:
                st.markdown(f'<div class="emotion-indicator emotion-{em}">{em.title()}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Feature 2: QuickThink
    with tab2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🧠 QuickThink - Cognitive Processing")
        
        text_input = st.text_area(
            "Input text for analysis:",
            placeholder="Paste your content here...",
            height=150,
            key="quickthink_input"
        )
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📝 Summarize", key="summarize_btn"):
                if text_input:
                    with st.spinner("Processing..."):
                        summary = generate_response(f"Create a concise, insightful summary: {text_input}")
                        st.markdown(f"""
                        <div class="result-container">
                            <div class="result-title">📋 Summary</div>
                            <div class="result-content">{summary}</div>
                        </div>
                        """, unsafe_allow_html=True)
        
        with col2:
            if st.button("🔍 Explain", key="explain_btn"):
                if text_input:
                    level = st.selectbox("Complexity:", ["Beginner", "Intermediate", "Expert"], key="explain_level")
                    with st.spinner("Explaining..."):
                        explanation = generate_response(f"Explain this at {level} level: {text_input}")
                        st.markdown(f"""
                        <div class="result-container">
                            <div class="result-title">💡 Explanation</div>
                            <div class="result-content">{explanation}</div>
                        </div>
                        """, unsafe_allow_html=True)
        
        with col3:
            if st.button("🎨 Metaphor", key="metaphor_btn"):
                if text_input:
                    with st.spinner("Creating metaphor..."):
                        metaphor = generate_response(f"Create a beautiful metaphor to explain: {text_input}")
                        st.markdown(f"""
                        <div class="result-container">
                            <div class="result-title">🌟 Metaphor</div>
                            <div class="result-content">{metaphor}</div>
                        </div>
                        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Feature 3: CreateSpark
    with tab3:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### ✨ CreateSpark - Creative Genesis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            prompt_input = st.text_input(
                "Creative prompt:",
                placeholder="A mystical forest where time flows backwards...",
                key="creative_prompt"
            )
            
            mood = st.selectbox(
                "Artistic mood:",
                ["Ethereal", "Noir", "Whimsical", "Epic", "Intimate", "Surreal"],
                key="creative_mood"
            )
        
        with col2:
            st.markdown("### 🎨 Creation Types")
            
            creation_types = [
                ("🌙 Poem", "poem"),
                ("📚 Story", "story"),
                ("🎭 Visual", "visual"),
                ("💫 Concept", "concept")
            ]
            
            for name, type_key in creation_types:
                if st.button(name, key=f"create_{type_key}"):
                    if prompt_input:
                        with st.spinner(f"Crafting {type_key}..."):
                            if type_key == "poem":
                                result = generate_response(f"Write a {mood.lower()} poem about: {prompt_input}")
                            elif type_key == "story":
                                result = generate_response(f"Write a {mood.lower()} micro-story about: {prompt_input}")
                            elif type_key == "visual":
                                result = generate_response(f"Create a {mood.lower()} visual art prompt for: {prompt_input}")
                            else:
                                result = generate_response(f"Generate a {mood.lower()} creative concept for: {prompt_input}")
                        
                        st.markdown(f"""
                        <div class="result-container">
                            <div class="result-title">{name} Creation</div>
                            <div class="result-content">{result}</div>
                        </div>
                        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Feature 4: DebateBot
    with tab4:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🎭 DebateBot - Perspective Engine")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            topic = st.text_input(
                "Debate topic:",
                placeholder="Should AI have rights?",
                key="debate_topic"
            )
        
        with col2:
            persona = st.selectbox(
                "AI Persona:",
                ["Philosopher", "Scientist", "Ethicist", "Futurist", "Skeptic", "Optimist"],
                key="debate_persona"
            )
        
        if st.button("🌟 Generate Debate", key="debate_btn"):
            if topic:
                with st.spinner("Constructing arguments..."):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        pro_arg = generate_response(f"As a {persona}, argue FOR: {topic}")
                        st.markdown(f"""
                        <div class="result-container">
                            <div class="result-title">✅ Pro Argument</div>
                            <div class="result-content">{pro_arg}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        con_arg = generate_response(f"As a {persona}, argue AGAINST: {topic}")
                        st.markdown(f"""
                        <div class="result-container">
                            <div class="result-title">❌ Con Argument</div>
                            <div class="result-content">{con_arg}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    synthesis = generate_response(f"Synthesize these perspectives on: {topic}")
                    st.markdown(f"""
                    <div class="result-container">
                        <div class="result-title">🤝 Synthesis</div>
                        <div class="result-content">{synthesis}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Feature 5: MultiLingua
    with tab5:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🌐 MultiLingua - Cultural Bridge")
        
        col1, col2 = st.columns(2)
        
        with col1:
            text_to_translate = st.text_area(
                "Text to translate:",
                placeholder="Enter text...",
                height=100,
                key="translate_text"
            )
            
            target_lang = st.selectbox(
                "Target language:",
                ["French", "Spanish", "German", "Italian", "Japanese", "Chinese", "Hindi", "Arabic", "Russian", "Portuguese"],
                key="target_lang"
            )
            if st.button("🌍 Translate", key="translate_btn"):
                if text_to_translate:
                    with st.spinner("Translating..."):
                        translation = generate_response(
                            f"Translate this to {target_lang} and provide a brief cultural note: {text_to_translate}"
                        )
                        st.markdown(f"""
                        <div class="result-container">
                            <div class="result-title">🌐 Translation ({target_lang})</div>
                            <div class="result-content">{translation}</div>
                        </div>
                        """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 🌏 Language Palette")
            langs = ["French", "Spanish", "German", "Italian", "Japanese", "Chinese", "Hindi", "Arabic", "Russian", "Portuguese"]
            lang_emojis = ["🇫🇷", "🇪🇸", "🇩🇪", "🇮🇹", "🇯🇵", "🇨🇳", "🇮🇳", "🇸🇦", "🇷🇺", "🇵🇹"]
            for l, e in zip(langs, lang_emojis):
                st.markdown(f'<div class="emotion-indicator emotion-neutral">{e} {l}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Feature 6: PromptCraft
    with tab6:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🚀 PromptCraft - AI Prompt Studio")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            user_goal = st.text_area(
                "Describe your goal or task:",
                placeholder="E.g., Summarize a research paper, generate creative ideas, etc.",
                height=100,
                key="promptcraft_goal"
            )
            style = st.selectbox(
                "Prompt style:",
                ["Concise", "Creative", "Analytical", "Conversational", "Instructional"],
                key="promptcraft_style"
            )
            if st.button("✨ Generate Prompt", key="promptcraft_btn"):
                if user_goal:
                    with st.spinner("Crafting your perfect prompt..."):
                        crafted_prompt = generate_response(
                            f"Create a {style.lower()} prompt for this goal: {user_goal}"
                        )
                        st.markdown(f"""
                        <div class="result-container">
                            <div class="result-title">🛠️ Crafted Prompt</div>
                            <div class="result-content">{crafted_prompt}</div>
                        </div>
                        """, unsafe_allow_html=True)
        with col2:
            st.markdown("#### 🧩 Prompt Styles")
            for s in ["Concise", "Creative", "Analytical", "Conversational", "Instructional"]:
                st.markdown(f'<div class="emotion-indicator emotion-excited">{s}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Feature 7: ThoughtLoop
    with tab7:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 💫 ThoughtLoop - Mind Mapping")
        
        st.markdown("Visualize your thoughts and connections. Enter a central idea and let GemmaGlow expand your mind map!")
        central_idea = st.text_input(
            "Central idea:",
            placeholder="E.g., Climate Change, Creativity, Quantum Computing...",
            key="thoughtloop_central"
        )
        if st.button("🧠 Generate Mind Map", key="thoughtloop_btn"):
            if central_idea:
                with st.spinner("Expanding your mind..."):
                    # Generate mind map nodes and edges using the model
                    mindmap_json = generate_response(
                        f"Generate a JSON list of 6-10 key concepts (nodes) and their relationships (edges) for a mind map about: {central_idea}. "
                        "Format: {{'nodes': [...], 'edges': [[from, to], ...]}}"
                    )
                    try:
                        mindmap = json.loads(mindmap_json.replace("'", '"'))
                        nodes = mindmap.get("nodes", [])
                        edges = mindmap.get("edges", [])
                    except Exception:
                        # fallback: simple structure
                        nodes = [central_idea, "Aspect 1", "Aspect 2", "Aspect 3"]
                        edges = [[central_idea, "Aspect 1"], [central_idea, "Aspect 2"], [central_idea, "Aspect 3"]]
                    
                    # Build graph
                    G = nx.Graph()
                    G.add_nodes_from(nodes)
                    G.add_edges_from(edges)
                    pos = nx.spring_layout(G, seed=42)
                    fig, ax = plt.subplots(figsize=(6, 4))
                    nx.draw_networkx_nodes(G, pos, node_color="#f093fb", node_size=700, alpha=0.8, ax=ax)
                    nx.draw_networkx_edges(G, pos, edge_color="#764ba2", width=2, alpha=0.5, ax=ax)
                    nx.draw_networkx_labels(G, pos, font_color="white", font_weight="bold", font_family="sans-serif", ax=ax)
                    ax.set_axis_off()
                    st.markdown('<div class="mind-map-container">', unsafe_allow_html=True)
                    st.pyplot(fig)
                    st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style='text-align:center; margin-top:3rem; color:rgba(255,255,255,0.6); font-size:0.95rem; letter-spacing:0.03em;'>
        <span>✨ GemmaGlow &copy; {year} &mdash; Crafted with cosmic care ✨</span>
        <br>
        <span style="font-size:0.8em;">Made with Streamlit, Gemini, and a sprinkle of stardust.</span>
    </div>
    """.format(year=datetime.now().year), unsafe_allow_html=True)

if __name__ == "__main__":
    main()

st.markdown("""
<style>
/* Dreamy, ethereal overlays and glows */
.dreamy-glow {
    position: fixed;
    top: -10%;
    left: -10%;
    width: 120vw;
    height: 120vh;
    pointer-events: none;
    z-index: 0;
    background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.12) 0%, rgba(240,147,251,0.10) 40%, transparent 80%),
                radial-gradient(circle at 70% 70%, rgba(102,126,234,0.10) 0%, rgba(76,175,254,0.08) 50%, transparent 90%);
    filter: blur(40px) saturate(1.2);
    opacity: 0.85;
    animation: dreamyFade 18s ease-in-out infinite alternate;
}
@keyframes dreamyFade {
    0% { opacity: 0.8; }
    50% { opacity: 1; }
    100% { opacity: 0.8; }
}

/* Subtle floating nebula clouds */
.dreamy-cloud {
    position: absolute;
    border-radius: 50%;
    pointer-events: none;
    opacity: 0.45;
    filter: blur(30px) brightness(1.2);
    animation: floatCloud 30s ease-in-out infinite alternate;
    z-index: 1;
}
.dreamy-cloud.cloud1 { width: 320px; height: 180px; top: 10%; left: 5%; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); animation-delay: 0s;}
.dreamy-cloud.cloud2 { width: 220px; height: 120px; top: 60%; left: 70%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); animation-delay: 8s;}
.dreamy-cloud.cloud3 { width: 180px; height: 100px; top: 80%; left: 20%; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); animation-delay: 16s;}
.dreamy-cloud.cloud4 { width: 260px; height: 140px; top: 20%; left: 60%; background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); animation-delay: 12s;}
@keyframes floatCloud {
    0% { transform: translateY(0px) scale(1) rotate(0deg);}
    50% { transform: translateY(-30px) scale(1.05) rotate(3deg);}
    100% { transform: translateY(0px) scale(1) rotate(0deg);}
}

/* Glowing border for main container */
.main-container, .feature-card, .result-container, .mind-map-container {
    box-shadow: 0 0 40px 8px rgba(240,147,251,0.12), 0 0 80px 0px rgba(102,126,234,0.10) !important;
    border: 1.5px solid rgba(255,255,255,0.18) !important;
    backdrop-filter: blur(24px) !important;
}

/* Dreamy text glow */
.hero-title, .result-title, .stat-number {
    /* Reduced glow for readability */
    text-shadow: 0 0 3px #f0f0f0, 0 0 10px #f093fb, 0 0 4px #4facfe;
    letter-spacing: 0.1em;
}

/* Floating sparkles */
.dreamy-sparkle {
    position: fixed;
    pointer-events: none;
    z-index: 9999;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: radial-gradient(circle, #fff 0%, #f093fb 60%, transparent 100%);
    opacity: 0.7;
    animation: sparkleFloat 7s linear infinite;
}
@keyframes sparkleFloat {
    0% { transform: translateY(0) scale(1);}
    50% { transform: translateY(-40px) scale(1.2);}
    100% { transform: translateY(0) scale(1);}
}

/* Dreamy aurora overlay */
.dreamy-aurora {
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    pointer-events: none;
    z-index: 0;
    background: linear-gradient(120deg, rgba(255,255,255,0.04) 0%, rgba(240,147,251,0.07) 40%, rgba(76,175,254,0.05) 100%);
    mix-blend-mode: lighten;
    opacity: 0.7;
    animation: auroraMove 22s ease-in-out infinite alternate;
}
@keyframes auroraMove {
    0% { background-position: 0% 50%;}
    100% { background-position: 100% 50%;}
}

/* Dreamy floating particles override for more shimmer */
.floating-particles .particle {
    background: radial-gradient(circle, #fff 0%, #f093fb 80%, transparent 100%);
    opacity: 0.8;
    filter: blur(0.5px) brightness(1.2);
    animation-duration: 18s;
}
</style>
<div class="dreamy-glow"></div>
<div class="dreamy-aurora"></div>
<div class="dreamy-cloud cloud1"></div>
<div class="dreamy-cloud cloud2"></div>
<div class="dreamy-cloud cloud3"></div>
<div class="dreamy-cloud cloud4"></div>
<script>
for(let i=0;i<12;i++){
    let s=document.createElement('div');
    s.className='dreamy-sparkle';
    s.style.left=Math.random()*100+'vw';
    s.style.top=Math.random()*100+'vh';
    s.style.animationDelay=(Math.random()*7)+'s';
    document.body.appendChild(s);
}
</script>
""", unsafe_allow_html=True)
