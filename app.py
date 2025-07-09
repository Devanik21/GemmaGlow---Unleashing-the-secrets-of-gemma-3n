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
import io  # <-- Add this import

# Configure page
st.set_page_config(
    page_title="GemmaGlow ✨",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"  # changed from "collapsed" to "expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&family=Orbitron:wght@100;200;300;400;500;600;700;800;900&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    /* === COSMIC HYPERSPACE BACKGROUND === */
    body, .stApp {
        background: radial-gradient(ellipse at top, #1a1a2e 0%, #16213e 25%, #0f3460 50%, #533483 75%, #8a2387 100%);
        background-size: 400% 400%;
        animation: hyperSpaceFlow 25s ease-in-out infinite;
        min-height: 100vh;
        overflow-x: hidden;
        position: relative;
    }
    
    @keyframes hyperSpaceFlow {
        0% { background-position: 0% 50%; filter: hue-rotate(0deg) saturate(1.2); }
        25% { background-position: 100% 50%; filter: hue-rotate(90deg) saturate(1.4); }
        50% { background-position: 100% 100%; filter: hue-rotate(180deg) saturate(1.6); }
        75% { background-position: 0% 100%; filter: hue-rotate(270deg) saturate(1.4); }
        100% { background-position: 0% 50%; filter: hue-rotate(360deg) saturate(1.2); }
    }

    /* === INTERDIMENSIONAL MATRIX GRID === */
    .matrix-grid {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        pointer-events: none;
        z-index: 0;
        background-image: 
            linear-gradient(rgba(0,255,255,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,0,255,0.03) 1px, transparent 1px);
        background-size: 60px 60px;
        animation: matrixFlow 15s linear infinite;
        opacity: 0.6;
    }
    
    @keyframes matrixFlow {
        0% { transform: translate(0, 0) scale(1); }
        50% { transform: translate(-30px, -30px) scale(1.1); }
        100% { transform: translate(0, 0) scale(1); }
    }

    /* === QUANTUM WORMHOLE PORTALS === */
    .quantum-portal {
        position: fixed;
        width: 400px; height: 400px;
        border-radius: 50%;
        pointer-events: none;
        z-index: 1;
        background: radial-gradient(circle at center, 
            rgba(0,255,255,0.15) 0%, 
            rgba(255,0,255,0.12) 30%, 
            rgba(255,255,0,0.08) 60%, 
            transparent 80%);
        filter: blur(2px) brightness(1.3);
        animation: portalSpin 20s linear infinite;
        opacity: 0.7;
    }
    
    .quantum-portal.portal1 { top: 10%; left: 5%; animation-delay: 0s; }
    .quantum-portal.portal2 { top: 60%; right: 10%; animation-delay: 8s; }
    .quantum-portal.portal3 { bottom: 15%; left: 30%; animation-delay: 16s; }
    
    @keyframes portalSpin {
        0% { transform: rotate(0deg) scale(1); }
        50% { transform: rotate(180deg) scale(1.2); }
        100% { transform: rotate(360deg) scale(1); }
    }

    /* === STELLAR CONSTELLATION LINES === */
    .constellation-layer {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        pointer-events: none;
        z-index: 2;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 800'%3E%3Cpath d='M100,100 L300,200 L500,150 L700,300 L900,250 L1100,400' stroke='rgba(255,255,255,0.1)' stroke-width='1' fill='none'/%3E%3Cpath d='M200,300 L400,400 L600,350 L800,500 L1000,450' stroke='rgba(0,255,255,0.08)' stroke-width='1' fill='none'/%3E%3Cpath d='M150,500 L350,600 L550,550 L750,700 L950,650' stroke='rgba(255,0,255,0.08)' stroke-width='1' fill='none'/%3E%3C/svg%3E") no-repeat center center;
        background-size: cover;
        animation: constellationPulse 12s ease-in-out infinite;
        opacity: 0.4;
    }
    
    @keyframes constellationPulse {
        0% { opacity: 0.4; filter: brightness(1); }
        50% { opacity: 0.8; filter: brightness(1.5); }
        100% { opacity: 0.4; filter: brightness(1); }
    }

    /* === PRISMATIC LIGHT REFRACTION === */
    .prismatic-refraction {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        pointer-events: none;
        z-index: 3;
        background: linear-gradient(45deg, 
            rgba(255,0,0,0.03) 0%, 
            rgba(255,165,0,0.03) 14%, 
            rgba(255,255,0,0.03) 28%, 
            rgba(0,255,0,0.03) 42%, 
            rgba(0,0,255,0.03) 56%, 
            rgba(75,0,130,0.03) 70%, 
            rgba(238,130,238,0.03) 84%, 
            transparent 100%);
        animation: prismShift 18s ease-in-out infinite;
        mix-blend-mode: screen;
        opacity: 0.3;
    }
    
    @keyframes prismShift {
        0% { transform: translateX(-100px) skew(-5deg); }
        50% { transform: translateX(100px) skew(5deg); }
        100% { transform: translateX(-100px) skew(-5deg); }
    }

    /* === ETHEREAL FLOATING CRYSTALS === */
    .ethereal-crystal {
        position: fixed;
        width: 60px; height: 60px;
        background: linear-gradient(135deg, 
            rgba(255,255,255,0.15) 0%, 
            rgba(0,255,255,0.12) 50%, 
            rgba(255,0,255,0.15) 100%);
        clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
        filter: blur(1px) brightness(1.4);
        animation: crystalFloat 16s ease-in-out infinite;
        pointer-events: none;
        z-index: 4;
        opacity: 0.6;
    }
    
    .ethereal-crystal.crystal1 { top: 20%; left: 15%; animation-delay: 0s; }
    .ethereal-crystal.crystal2 { top: 70%; right: 20%; animation-delay: 5s; }
    .ethereal-crystal.crystal3 { bottom: 30%; left: 70%; animation-delay: 10s; }
    .ethereal-crystal.crystal4 { top: 40%; right: 40%; animation-delay: 8s; }
    
    @keyframes crystalFloat {
        0% { transform: translateY(0px) rotate(0deg) scale(1); }
        33% { transform: translateY(-40px) rotate(120deg) scale(1.1); }
        66% { transform: translateY(20px) rotate(240deg) scale(0.9); }
        100% { transform: translateY(0px) rotate(360deg) scale(1); }
    }

    /* === GALACTIC DUST CLOUDS === */
    .galactic-dust {
        position: fixed;
        border-radius: 50%;
        pointer-events: none;
        z-index: 1;
        filter: blur(40px) saturate(1.5);
        animation: dustDrift 35s ease-in-out infinite alternate;
        opacity: 0.25;
    }
    
    .galactic-dust.dust1 { 
        width: 500px; height: 300px; 
        top: 10%; left: 5%; 
        background: radial-gradient(ellipse, rgba(255,100,255,0.3) 0%, transparent 70%);
        animation-delay: 0s;
    }
    .galactic-dust.dust2 { 
        width: 400px; height: 400px; 
        top: 50%; right: 10%; 
        background: radial-gradient(circle, rgba(100,255,255,0.3) 0%, transparent 70%);
        animation-delay: 12s;
    }
    .galactic-dust.dust3 { 
        width: 350px; height: 250px; 
        bottom: 20%; left: 40%; 
        background: radial-gradient(ellipse, rgba(255,255,100,0.3) 0%, transparent 70%);
        animation-delay: 24s;
    }
    
    @keyframes dustDrift {
        0% { transform: translate(0, 0) scale(1); }
        50% { transform: translate(-50px, -30px) scale(1.2); }
        100% { transform: translate(0, 0) scale(1); }
    }

    /* === COSMIC ENERGY STREAMS === */
    .energy-stream {
        position: fixed;
        width: 2px; height: 100vh;
        background: linear-gradient(180deg, 
            transparent 0%, 
            rgba(0,255,255,0.8) 20%, 
            rgba(255,0,255,0.8) 50%, 
            rgba(255,255,0,0.8) 80%, 
            transparent 100%);
        filter: blur(1px) brightness(1.5);
        animation: energyFlow 8s linear infinite;
        pointer-events: none;
        z-index: 5;
        opacity: 0.4;
    }
    
    .energy-stream.stream1 { left: 10%; animation-delay: 0s; }
    .energy-stream.stream2 { left: 30%; animation-delay: 2s; }
    .energy-stream.stream3 { left: 50%; animation-delay: 4s; }
    .energy-stream.stream4 { left: 70%; animation-delay: 6s; }
    .energy-stream.stream5 { left: 90%; animation-delay: 1s; }
    
    @keyframes energyFlow {
        0% { transform: translateY(-100vh) scaleY(0.8); opacity: 0; }
        10% { opacity: 0.4; }
        90% { opacity: 0.4; }
        100% { transform: translateY(100vh) scaleY(1.2); opacity: 0; }
    }

    /* === HYPERDIMENSIONAL COMPONENTS === */
    .main-container, .feature-card, .result-container {
        background: rgba(255,255,255,0.08) !important;
        backdrop-filter: blur(25px) saturate(1.2) !important;
        border: 2px solid rgba(255,255,255,0.15) !important;
        border-radius: 25px !important;
        box-shadow: 
            0 0 40px rgba(0,255,255,0.15),
            0 0 80px rgba(255,0,255,0.1),
            inset 0 1px 0 rgba(255,255,255,0.2) !important;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1) !important;
    }
    
    .main-container::before, .feature-card::before, .result-container::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(135deg, 
            rgba(255,255,255,0.05) 0%, 
            rgba(0,255,255,0.03) 50%, 
            rgba(255,0,255,0.05) 100%);
        pointer-events: none;
        z-index: -1;
    }
    
    .feature-card:hover, .result-container:hover {
        transform: translateY(-12px) scale(1.02) !important;
        box-shadow: 
            0 0 60px rgba(0,255,255,0.25),
            0 0 120px rgba(255,0,255,0.15),
            0 20px 40px rgba(0,0,0,0.3) !important;
        border-color: rgba(255,255,255,0.3) !important;
    }

    /* === QUANTUM HERO SECTION === */
    .hero-section {
        text-align: center;
        padding: 5rem 2rem;
        background: radial-gradient(ellipse at center, 
            rgba(255,255,255,0.12) 0%, 
            rgba(0,255,255,0.08) 40%, 
            rgba(255,0,255,0.05) 80%, 
            transparent 100%);
        border-radius: 30px;
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        border: 2px solid rgba(255,255,255,0.1);
    }
    
    .hero-title {
        font-family: 'Orbitron', monospace;
        font-size: 5.5rem;
        font-weight: 900;
        background: linear-gradient(45deg, 
            #ffffff 0%, 
            #00ffff 25%, 
            #ff00ff 50%, 
            #ffff00 75%, 
            #ffffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 
            0 0 20px rgba(255,255,255,0.5),
            0 0 40px rgba(0,255,255,0.3),
            0 0 60px rgba(255,0,255,0.2);
        margin-bottom: 1.5rem;
        letter-spacing: -0.03em;
        animation: titleGlow 4s ease-in-out infinite alternate;
    }
    
    @keyframes titleGlow {
        0% { filter: brightness(1) saturate(1); }
        100% { filter: brightness(1.2) saturate(1.3); }
    }
    
    .hero-subtitle {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.8rem;
        font-weight: 400;
        color: rgba(255,255,255,0.85);
        margin-bottom: 2rem;
        letter-spacing: 0.05em;
        text-shadow: 0 0 15px rgba(255,255,255,0.3);
    }

    /* === INTERDIMENSIONAL PARTICLES === */
    .quantum-particle {
        position: fixed;
        width: 3px; height: 3px;
        background: radial-gradient(circle, 
            rgba(255,255,255,0.9) 0%, 
            rgba(0,255,255,0.6) 50%, 
            transparent 100%);
        border-radius: 50%;
        pointer-events: none;
        z-index: 10;
        animation: particleFloat 25s linear infinite;
        filter: blur(0.5px) brightness(1.5);
    }
    
    @keyframes particleFloat {
        0% { 
            transform: translate(0, 100vh) scale(0); 
            opacity: 0; 
        }
        10% { 
            opacity: 1; 
            transform: translate(20px, 90vh) scale(1); 
        }
        90% { 
            opacity: 1; 
            transform: translate(-20px, 10vh) scale(1); 
        }
        100% { 
            transform: translate(0, -10vh) scale(0); 
            opacity: 0; 
        }
    }

    /* === HYPNOTIC PULSE ELEMENTS === */
    .hypnotic-pulse {
        position: absolute;
        width: 100px; height: 100px;
        border: 2px solid rgba(255,255,255,0.2);
        border-radius: 50%;
        animation: hypnoticPulse 3s ease-in-out infinite;
        pointer-events: none;
        z-index: 8;
    }
    
    .hypnotic-pulse.pulse1 { top: 20%; left: 20%; animation-delay: 0s; }
    .hypnotic-pulse.pulse2 { top: 60%; right: 25%; animation-delay: 1s; }
    .hypnotic-pulse.pulse3 { bottom: 25%; left: 60%; animation-delay: 2s; }
    
    @keyframes hypnoticPulse {
        0% { transform: scale(1); opacity: 0.3; }
        50% { transform: scale(1.5); opacity: 0.8; }
        100% { transform: scale(2); opacity: 0; }
    }

    /* === ASTRAL FORM CONTROLS === */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background: rgba(255,255,255,0.06) !important;
        border: 2px solid rgba(255,255,255,0.15) !important;
        border-radius: 20px !important;
        color: #ffffff !important;
        backdrop-filter: blur(15px) saturate(1.1) !important;
        box-shadow: inset 0 0 20px rgba(0,255,255,0.1) !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 500 !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        background: rgba(255,255,255,0.12) !important;
        border-color: rgba(0,255,255,0.6) !important;
        box-shadow: 
            0 0 30px rgba(0,255,255,0.3),
            inset 0 0 20px rgba(255,255,255,0.1) !important;
        transform: scale(1.02) !important;
    }

    /* === TRANSCENDENT BUTTONS === */
    .stButton button {
        background: linear-gradient(135deg, 
            rgba(255,255,255,0.15) 0%, 
            rgba(0,255,255,0.12) 50%, 
            rgba(255,0,255,0.15) 100%) !important;
        border: 2px solid rgba(255,255,255,0.25) !important;
        border-radius: 20px !important;
        color: #ffffff !important;
        font-family: 'Orbitron', monospace !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        padding: 1rem 2rem !important;
        backdrop-filter: blur(15px) !important;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        box-shadow: 0 0 20px rgba(0,255,255,0.2) !important;
    }
    
    .stButton button:hover {
        transform: translateY(-5px) scale(1.05) !important;
        background: linear-gradient(135deg, 
            rgba(255,255,255,0.25) 0%, 
            rgba(0,255,255,0.2) 50%, 
            rgba(255,0,255,0.25) 100%) !important;
        box-shadow: 
            0 0 40px rgba(0,255,255,0.4),
            0 0 80px rgba(255,0,255,0.3),
            0 15px 30px rgba(0,0,0,0.3) !important;
        border-color: rgba(255,255,255,0.5) !important;
    }

    /* === OMNIPRESENT SIDEBAR === */
    .stSidebar {
        background: rgba(255,255,255,0.04) !important;
        backdrop-filter: blur(30px) saturate(1.3) !important;
        border-right: 3px solid rgba(0,255,255,0.3) !important;
        box-shadow: 
            0 0 50px rgba(0,255,255,0.2),
            inset 0 0 50px rgba(255,255,255,0.05) !important;
    }

    /* === COSMIC TYPOGRAPHY === */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-family: 'Orbitron', monospace !important;
        text-shadow: 0 0 15px rgba(255,255,255,0.5) !important;
    }
    
    .stMarkdown {
        color: rgba(255,255,255,0.9) !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    /* === DIMENSIONAL EMOTION INDICATORS === */
    .emotion-indicator {
        display: inline-block;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-family: 'Orbitron', monospace;
        font-size: 1.1rem;
        font-weight: 800;
        margin: 0.5rem;
        backdrop-filter: blur(15px);
        border: 2px solid rgba(255,255,255,0.3);
        box-shadow: 
            0 0 25px rgba(255,255,255,0.2),
            inset 0 0 25px rgba(255,255,255,0.1);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        letter-spacing: 0.1em;
        text-transform: uppercase;
        animation: emotionPulse 2s ease-in-out infinite alternate;
    }
    
    @keyframes emotionPulse {
        0% { box-shadow: 0 0 25px rgba(255,255,255,0.2); }
        100% { box-shadow: 0 0 35px rgba(255,255,255,0.4); }
    }
    
    .emotion-happy { 
        background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
        color: #ffffff;
    }
    .emotion-sad { 
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        color: #ffffff;
    }
    .emotion-excited { 
        background: linear-gradient(135deg, #fd79a8 0%, #e84393 100%);
        color: #ffffff;
    }
    .emotion-calm { 
        background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
        color: #ffffff;
    }

    /* === TEMPORAL LOADING SPINNER === */
    .cosmic-loading {
        width: 50px;
        height: 50px;
        border: 3px solid rgba(255,255,255,0.1);
        border-top: 3px solid #00ffff;
        border-right: 3px solid #ff00ff;
        border-radius: 50%;
        animation: cosmicSpin 1s linear infinite;
        margin: 2rem auto;
        filter: blur(0.5px) brightness(1.3);
    }
    
    @keyframes cosmicSpin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* === ASTRAL PROJECTION EFFECTS === */
    .astral-glow {
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at center, 
            rgba(255,255,255,0.1) 0%, 
            rgba(0,255,255,0.05) 30%, 
            transparent 70%);
        animation: astralRotate 20s linear infinite;
        pointer-events: none;
        z-index: -1;
    }
    
    @keyframes astralRotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* === HIDE MUNDANE ELEMENTS === */
    footer { visibility: hidden !important; }
    .stDeployButton { display: none !important; }
    
    /* === REALITY DISTORTION FIELD === */
    .reality-distortion {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        pointer-events: none;
        z-index: 999;
        background: radial-gradient(circle at var(--mouse-x, 50%) var(--mouse-y, 50%), 
            rgba(255,255,255,0.05) 0%, 
            transparent 20%);
        mix-blend-mode: screen;
        opacity: 0.3;
    }
</style>

<!-- COSMIC INFRASTRUCTURE -->
<div class="matrix-grid"></div>
<div class="quantum-portal portal1"></div>
<div class="quantum-portal portal2"></div>
<div class="quantum-portal portal3"></div>
<div class="constellation-layer"></div>
<div class="prismatic-refraction"></div>
<div class="galactic-dust dust1"></div>
<div class="galactic-dust dust2"></div>
<div class="galactic-dust dust3"></div>
<div class="energy-stream stream1"></div>
<div class="energy-stream stream2"></div>
<div class="energy-stream stream3"></div>
<div class="energy-stream stream4"></div>
<div class="energy-stream stream5"></div>
<div class="ethereal-crystal crystal1"></div>
<div class="ethereal-crystal crystal2"></div>
<div class="ethereal-crystal crystal3"></div>
<div class="ethereal-crystal crystal4"></div>
<div class="hypnotic-pulse pulse1"></div>
<div class="hypnotic-pulse pulse2"></div>
<div class="hypnotic-pulse pulse3"></div>
<div class="reality-distortion"></div>

<script>
// QUANTUM PARTICLE GENERATOR
function createQuantumParticle() {
    const particle = document.createElement('div');
    particle.className = 'quantum-particle';
    particle.style.left = Math.random() * 100 + 'vw';
    particle.style.animationDelay = Math.random() * 5 + 's';
    particle.style.animationDuration = (15 + Math.random() * 10) + 's';
    document.body.appendChild(particle);
    
    setTimeout(() => {
        particle.remove();
    }, 25000);
}

// CONTINUOUS PARTICLE STREAM
setInterval(createQuantumParticle, 300);

// REALITY DISTORTION FIELD
document.addEventListener('mousemove', (e) => {
    const distortion = document.querySelector('.reality-distortion');
    if (distortion) {
        distortion.style.setProperty('--mouse-x', (e.clientX / window.innerWidth) * 100 + '%');
        distortion.style.setProperty('--mouse-y', (e.clientY / window.innerHeight) * 100 + '%');
    }
});

// ASTRAL GLOW ENHANCEMENT
document.querySelectorAll('.feature-card, .result-container').forEach(card => {
    const glow = document.createElement('div');
    glow.className = 'astral-glow';
    card.appendChild(glow);
});

// INITIALIZE COSMIC ENVIRONMENT
window.addEventListener('load', () => {
    console.log('🌌 Cosmic Interface Initialized 🌌');
    
    // Create initial particle burst
    for (let i = 0; i < 20; i++) {
        setTimeout(() => createQuantumParticle(), i * 100);
    }
});
</script>
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

    # Short tab names and icons for compact navigation
    features = [
        "🌸", "🧠", "✨", "🎭", "🌐", "🚀", "💫",
        "🌙", "🔮", "🐉", "⚛️", "👁️", "🤖", "🧠", "🧘", "⏳", "🪐",
        "🦄", "🧩", "📈", "🧬", "🛰️",  # 22nd tab
        "🧪"  # 23rd tab: PromptLab
    ]
    (
        tab1, tab2, tab3, tab4, tab5, tab6, tab7,
        tab8, tab9, tab10, tab11, tab12, tab13, tab14, tab15, tab16, tab17,
        tab18, tab19, tab20, tab21, tab22, tab23
    ) = st.tabs(features)

    # Transparent, collapsed sidebar for beginner guidance
    with st.sidebar:
        st.markdown("""
        <style>
        .element-container:has(.sidebar-guide) {
            background: rgba(255,255,255,0.07) !important;
            border-radius: 18px;
            border: 1px solid rgba(255,255,255,0.13);
            margin: 0.5rem 0.2rem 0.5rem 0.2rem;
            padding: 1.2rem 1rem 1.2rem 1rem;
            box-shadow: 0 4px 24px rgba(102,126,234,0.08);
            font-family: 'Inter', sans-serif;
        }
        .sidebar-guide h4 {
            color: #fff !important;
            margin-bottom: 0.7em;
            font-size: 1.1em;
            letter-spacing: 0.04em;
        }
        .sidebar-guide ul {
            padding-left: 1.1em;
        }
        .sidebar-guide li {
            margin-bottom: 0.5em;
            color: #e0e0e0;
            font-size: 0.97em;
        }
        .sidebar-guide .tabicon {
            font-size: 1.2em;
            margin-right: 0.4em;
        }
        </style>
        <div class="sidebar-guide">
        <h4>✨ Beginner's Guide</h4>
        <ul>
            <li><span class="tabicon">🌸</span><b>MoodSync</b>: Analyze your emotions and get empathetic AI support.</li>
            <li><span class="tabicon">🧠</span><b>QuickThink</b>: Summarize, explain, or metaphorize any text.</li>
            <li><span class="tabicon">✨</span><b>CreateSpark</b>: Generate poems, stories, visuals, and concepts.</li>
            <li><span class="tabicon">🎭</span><b>DebateBot</b>: AI debates on any topic with multiple personas.</li>
            <li><span class="tabicon">🌐</span><b>MultiLingua</b>: Translate text and learn about world languages.</li>
            <li><span class="tabicon">🚀</span><b>PromptCraft</b>: Get custom prompts for your AI tasks.</li>
            <li><span class="tabicon">💫</span><b>ThoughtLoop</b>: Visual mind mapping for your ideas.</li>
            <li><span class="tabicon">🌙</span><b>DreamWeaver</b>: Mystical dream interpretation.</li>
            <li><span class="tabicon">🔮</span><b>AstroGuide</b>: Daily horoscopes and cosmic advice.</li>
            <li><span class="tabicon">🐉</span><b>MythMaker</b>: Create your own myths and legends.</li>
            <li><span class="tabicon">⚛️</span><b>QuantumQuiz</b>: Fun science quizzes on any topic.</li>
            <li><span class="tabicon">👁️</span><b>Visionary</b>: Generate prompts for AI art.</li>
            <li><span class="tabicon">🤖</span><b>CodeMuse</b>: Coding project ideas and starter prompts.</li>
            <li><span class="tabicon">🧠</span><b>MemoryPal</b>: Build memory palaces for learning.</li>
            <li><span class="tabicon">🧘</span><b>ZenZone</b>: Guided meditations for relaxation.</li>
            <li><span class="tabicon">⏳</span><b>TimeCapsule</b>: Write a letter to your future self.</li>
            <li><span class="tabicon">🪐</span><b>WonderWall</b>: Ask cosmic questions, get awe-inspiring answers.</li>
            <li><span class="tabicon">🦄</span><b>IdeaGenie</b>: Instantly generate creative ideas for any topic.</li>
            <li><span class="tabicon">🧩</span><b>PuzzleBox</b>: Solve or create fun puzzles and riddles.</li>
            <li><span class="tabicon">📈</span><b>DataViz</b>: Visualize your data with AI-powered charts.</li>
            <li><span class="tabicon">🧬</span><b>BioBuddy</b>: Get biology facts, mnemonics, and diagrams.</li>
            <li><span class="tabicon">🛰️</span><b>SynthAI</b>: Advanced multi-task AI—combine summarization, Q&A, and visualization in one step.</li>
            <li><span class="tabicon">🧪</span><b>PromptLab</b>: Advanced prompt playground—experiment with custom instructions, system prompts, and temperature for ultimate AI control.</li>
        </ul>
        <div style="margin-top:1.2em; color:#b0b0b0; font-size:0.93em;">
            <b>Tip:</b> Click any icon tab above to explore its feature!
        </div>
        </div>
        """, unsafe_allow_html=True)

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
                    ax.set_axis_off();
                    st.markdown('<div class="mind-map-container">', unsafe_allow_html=True)
                    st.pyplot(fig)
                    st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Feature 8: DreamWeaver - AI Dream Interpreter
    with tab8:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🌙 DreamWeaver - Dream Interpreter")
        dream_input = st.text_area("Describe your dream:", placeholder="Last night I was flying over a city of stars...", key="dream_input")
        if st.button("🌌 Interpret Dream", key="dream_btn"):
            if dream_input:
                with st.spinner("Decoding your dream..."):
                    dream_result = generate_response(f"Interpret this dream in a mystical, symbolic way: {dream_input}")
                    st.markdown(f"""
                    <div class="result-container">
                        <div class="result-title">🌙 Dream Interpretation</div>
                        <div class="result-content">{dream_result}</div>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Feature 9: AstroGuide - AI Horoscope & Cosmic Advice
    with tab9:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🔮 AstroGuide - Horoscope & Cosmic Advice")
        sign = st.selectbox("Your Zodiac Sign:", [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ], key="astro_sign")
        if st.button("✨ Reveal Horoscope", key="astro_btn"):
            with st.spinner("Consulting the stars..."):
                horoscope = generate_response(f"Give a poetic, uplifting horoscope for {sign} today.")
                st.markdown(f"""
                <div class="result-container">
                    <div class="result-title">🔮 {sign} Horoscope</div>
                    <div class="result-content">{horoscope}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Feature 10: MythMaker - AI Myth Generator
    with tab10:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🐉 MythMaker - Create Your Own Myth")
        myth_theme = st.text_input("Myth Theme:", placeholder="The origin of the moon...", key="myth_theme")
        if st.button("🐲 Generate Myth", key="myth_btn"):
            if myth_theme:
                with st.spinner("Spinning a legend..."):
                    myth = generate_response(f"Invent a short, original myth about: {myth_theme}")
                    st.markdown(f"""
                    <div class="result-container">
                        <div class="result-title">🐉 New Myth</div>
                        <div class="result-content">{myth}</div>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Feature 11: QuantumQuiz - AI Science Quizzer
    with tab11:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### ⚛️ QuantumQuiz - Science Quiz")
        quiz_topic = st.text_input("Quiz Topic:", placeholder="Black holes, Quantum mechanics...", key="quiz_topic")
        num_q = st.slider("Number of Questions", 1, 5, 3, key="quiz_numq")
        if st.button("🧪 Start Quiz", key="quiz_btn"):
            if quiz_topic:
                with st.spinner("Generating quiz..."):
                    quiz = generate_response(f"Create a {num_q}-question multiple choice science quiz on: {quiz_topic}. Format: Q: ...\nA) ...\nB) ...\nC) ...\nD) ...")
                    st.markdown(f"""
                    <div class="result-container">
                        <div class="result-title">⚛️ {quiz_topic.title()} Quiz</div>
                        <div class="result-content"><pre>{quiz}</pre></div>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Feature 12: Visionary - AI Image Prompt Generator
    with tab12:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 👁️ Visionary - Image Prompt Generator")
        vision_theme = st.text_input("Describe your vision:", placeholder="A city floating above clouds...", key="vision_theme")
        if st.button("🎨 Generate Image Prompt", key="vision_btn"):
            if vision_theme:
                with st.spinner("Imagining..."):
                    img_prompt = generate_response(f"Write a detailed, vivid prompt for an AI art generator about: {vision_theme}")
                    st.markdown(f"""
                    <div class="result-container">
                        <div class="result-title">👁️ Art Prompt</div>
                        <div class="result-content">{img_prompt}</div>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Feature 13: CodeMuse - AI Code Inspiration
    with tab13:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🤖 CodeMuse - Coding Inspiration")
        code_goal = st.text_input("What do you want to build?", placeholder="A weather app, a chatbot...", key="code_goal")
        if st.button("💡 Inspire Me", key="code_btn"):
            if code_goal:
                with st.spinner("Summoning code muses..."):
                    code_idea = generate_response(f"Suggest a creative coding project idea and a starter prompt for: {code_goal}")
                    st.markdown(f"""
                    <div class="result-container">
                        <div class="result-title">🤖 Code Inspiration</div>
                        <div class="result-content">{code_idea}</div>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Feature 14: MemoryPal - AI Memory Palace
    with tab14:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🧠 MemoryPal - Memory Palace Builder")
        memory_topic = st.text_input("Topic to memorize:", placeholder="Planets of the solar system...", key="memory_topic")
        if st.button("🏰 Build Memory Palace", key="memory_btn"):
            if memory_topic:
                with st.spinner("Constructing your palace..."):
                    palace = generate_response(f"Create a vivid memory palace story to help memorize: {memory_topic}")
                    st.markdown(f"""
                    <div class="result-container">
                        <div class="result-title">🧠 Memory Palace</div>
                        <div class="result-content">{palace}</div>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Feature 15: ZenZone - AI Guided Meditation
    with tab15:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🧘 ZenZone - Guided Meditation")
        zen_focus = st.text_input("Meditation focus:", placeholder="Relaxation, focus, gratitude...", key="zen_focus")
        if st.button("🕉️ Start Meditation", key="zen_btn"):
            if zen_focus:
                with st.spinner("Preparing your meditation..."):
                    meditation = generate_response(f"Guide me through a short meditation for: {zen_focus}")
                    st.markdown(f"""
                    <div class="result-container">
                        <div class="result-title">🧘 Meditation</div>
                        <div class="result-content">{meditation}</div>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Feature 16: TimeCapsule - AI Time Capsule Letter
    with tab16:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### ⏳ TimeCapsule - Letter to the Future")
        capsule_msg = st.text_area("Write your message to the future:", placeholder="Dear future me...", key="capsule_msg")
        years = st.slider("Years into the future:", 1, 50, 10, key="capsule_years")
        if st.button("📜 Seal Time Capsule", key="capsule_btn"):
            if capsule_msg:
                with st.spinner("Sealing your message..."):
                    letter = generate_response(f"Write a heartfelt letter to myself {years} years in the future: {capsule_msg}")
                    st.markdown(f"""
                    <div class="result-container">
                        <div class="result-title">⏳ Time Capsule Letter</div>
                        <div class="result-content">{letter}</div>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Feature 17: AI Chat
    with tab17:
        st.markdown('<div class="feature-card" style="height: 80vh; display: flex; flex-direction: column;">', unsafe_allow_html=True)
        st.markdown("### 🤖 AI Chat - Your General Assistant")

        # Initialize chat history
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = [
                {"role": "ai", "content": "Hello! I'm your AI assistant. How can I help you today?"}
            ]

        # Chat container
        chat_container = st.container()
        with chat_container:
            for i, msg in enumerate(st.session_state["chat_history"]):
                if msg["role"] == "user":
                    st.markdown(
                        f"""
                        <div style="display: flex; align-items: flex-start; justify-content: flex-end; margin-bottom: 1rem;">
                            <div style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2); color: white; border-radius: 20px; padding: 10px 15px; max-width: 70%; display: flex; align-items: center;">
                                <div>{msg['content']}</div>
                                <div style="margin-left: 10px; font-size: 1.5rem;">🧑</div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""
                        <div style="display: flex; align-items: flex-start; margin-bottom: 1rem;">
                            <div style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2); color: white; border-radius: 20px; padding: 10px 15px; max-width: 70%; display: flex; align-items: center;">
                                <div style="margin-right: 10px; font-size: 1.5rem;">🤖</div>
                                <div>{msg['content']}</div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        # Input form
        with st.form(key="chat_form", clear_on_submit=True):
            col1, col2 = st.columns([4, 1])
            with col1:
                user_input = st.text_input(
                    "Your message:",
                    placeholder="Ask me anything...",
                    key="chat_input",
                    label_visibility="collapsed"
                )
            with col2:
                submit_button = st.form_submit_button(label="Send")

        if submit_button and user_input:
            # Add user message to chat history
            st.session_state["chat_history"].append({"role": "user", "content": user_input})

            # Keep the last 10 messages for context
            context_messages = st.session_state["chat_history"][-10:]
            context = "\n".join([f"{'User' if msg['role'] == 'user' else 'AI'}: {msg['content']}" for msg in context_messages])

            # Generate AI response
            with st.spinner("Thinking..."):
                ai_response = generate_response(f"Continue this conversation:\n\n{context}")
            
            # Add AI response to chat history
            st.session_state["chat_history"].append({"role": "ai", "content": ai_response})
            st.rerun()

        # Clear chat button
        if st.button("Clear Chat"):
            st.session_state["chat_history"] = [
                {"role": "ai", "content": "Hello! I'm your AI assistant. How can I help you today?"}
            ]
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # Feature 18: IdeaGenie
    with tab18:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🦄 IdeaGenie - Instant Idea Generator")
        genie_topic = st.text_input("Topic or area:", placeholder="Startup, party theme, app, etc.", key="genie_topic")
        if st.button("✨ Generate Ideas", key="genie_btn"):
            if genie_topic:
                with st.spinner("Summoning ideas..."):
                    ideas = generate_response(f"Generate 5 creative, original ideas for: {genie_topic}")
                    st.markdown(f"""
                    <div class="result-container">
                        <div class="result-title">🦄 Ideas</div>
                        <div class="result-content">{ideas}</div>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Feature 19: PuzzleBox
    with tab19:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🧩 PuzzleBox - Puzzles & Riddles")
        puzzle_type = st.selectbox("Puzzle type:", ["Riddle", "Logic Puzzle", "Math Puzzle"], key="puzzle_type")
        if st.button("🧠 Get Puzzle", key="puzzle_btn"):
            with st.spinner("Thinking up a puzzle..."):
                puzzle = generate_response(f"Give me a {puzzle_type.lower()} with answer. Format: Puzzle: ... Answer: ...")
                st.markdown(f"""
                <div class="result-container">
                    <div class="result-title">🧩 {puzzle_type}</div>
                    <div class="result-content">{puzzle}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Feature 20: DataViz
    with tab20:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 📈 DataViz - AI Data Visualization")
        data_input = st.text_area("Paste CSV data (with headers):", placeholder="year,value\n2020,100\n2021,150", key="dataviz_input")
        chart_type = st.selectbox("Chart type:", ["Line", "Bar", "Scatter"], key="dataviz_chart")
        if st.button("📊 Visualize", key="dataviz_btn"):
            if data_input:
                try:
                    df = pd.read_csv(io.StringIO(data_input))  # <-- Fix here
                    if chart_type == "Line":
                        fig = px.line(df)
                    elif chart_type == "Bar":
                        fig = px.bar(df)
                    else:
                        fig = px.scatter(df)
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Could not parse data: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Feature 21: BioBuddy
    with tab21:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🧬 BioBuddy - Biology Helper")
        bio_query = st.text_input("Ask a biology question or topic:", placeholder="Explain photosynthesis, DNA structure...", key="bio_query")
        if st.button("🌱 Get Bio Help", key="bio_btn"):
            if bio_query:
                with st.spinner("Consulting BioBuddy..."):
                    bio_answer = generate_response(f"Explain this biology topic in a clear, visual way. Add a mnemonic if possible: {bio_query}")
                    st.markdown(f"""
                    <div class="result-container">
                        <div class="result-title">🧬 BioBuddy</div>
                        <div class="result-content">{bio_answer}</div>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Feature 22: SynthAI - Advanced Multi-Tasker
    with tab22:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🛰️ SynthAI - Advanced Multi-Tasker")
        st.markdown("Combine summarization, Q&A, and visualization in one step. Paste a document, ask a question, and get a summary, answer, and a chart if possible.")
        synth_text = st.text_area("Paste your document or data:", placeholder="Paste text or CSV data...", key="synth_text")
        synth_question = st.text_input("Ask a question about the above:", placeholder="What are the key trends?", key="synth_question")
        synth_mode = st.selectbox("Mode:", ["Auto", "Text Only", "Data (CSV)"], key="synth_mode")
        if st.button("🚀 Run SynthAI", key="synthai_btn"):
            if synth_text:
                with st.spinner("Synthesizing..."):
                    # Summarization
                    summary = generate_response(f"Summarize this for an expert: {synth_text}")
                    # Q&A
                    answer = generate_response(f"Based on this, answer: {synth_question}\n\nText:\n{synth_text}") if synth_question else ""
                    # Visualization if CSV
                    chart_html = ""
                    if synth_mode in ["Auto", "Data (CSV)"]:
                        try:
                            df = pd.read_csv(io.StringIO(synth_text))
                            fig = px.line(df) if len(df.columns) >= 2 else None
                            if fig:
                                st.plotly_chart(fig, use_container_width=True)
                                chart_html = "<div style='margin-top:1em;'>Chart generated from your data above.</div>"
                        except Exception:
                            if synth_mode == "Data (CSV)":
                                st.warning("Could not parse CSV for visualization.")
                    st.markdown(f"""
                    <div class="result-container">
                        <div class="result-title">🛰️ SynthAI Results</div>
                        <div class="result-content">
                            <b>Summary:</b><br>{summary}<br><br>
                            {"<b>Answer:</b><br>"+answer+"<br><br>" if answer else ""}
                            {chart_html}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Feature 23: PromptLab - Advanced Prompt Playground
    with tab23:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🧪 PromptLab - Advanced Prompt Playground")
        st.markdown("Experiment with advanced prompt engineering: set system instructions, user prompt, and generation parameters for fine-tuned AI responses.")

        col1, col2 = st.columns(2)

        with col1:
            system_prompt = st.text_area(
                "System Instructions (optional):",
                placeholder="E.g., You are a witty assistant who always answers in rhymes.",
                height=100,
                key="promptlab_system"
            )
            user_prompt = st.text_area(
                "User Prompt:",
                placeholder="Ask anything or give a task...",
                height=200,
                key="promptlab_user"
            )

        with col2:
            st.markdown("#### Generation Parameters")
            temperature = st.slider(
                "Temperature:", 
                min_value=0.0, max_value=1.0, value=0.7, step=0.05,
                key="promptlab_temp",
                help="Controls randomness. Lower values make the model more deterministic."
            )
            top_p = st.slider(
                "Top-P:",
                min_value=0.0, max_value=1.0, value=0.95, step=0.05,
                key="promptlab_top_p",
                help="Nucleus sampling. The model considers only the tokens with the highest probability mass."
            )
            top_k = st.slider(
                "Top-K:",
                min_value=0, max_value=100, value=40, step=1,
                key="promptlab_top_k",
                help="The model considers only the top-k most likely tokens."
            )
            max_output_tokens = st.number_input(
                "Max Output Tokens:",
                min_value=1, value=1024,
                key="promptlab_max_tokens",
                help="Maximum number of tokens to generate."
            )
            stop_sequences = st.text_input(
                "Stop Sequences (comma-separated):",
                placeholder="e.g., END,STOP",
                key="promptlab_stop",
                help="Sequences where the API will stop generating further tokens."
            )

        if st.button("🚀 Generate Response", key="promptlab_btn"):
            if user_prompt:
                with st.spinner("Generating response with advanced settings..."):
                    result = ""
                    try:
                        if model and hasattr(model, "generate_content"):
                            prompt = (system_prompt + "\n" if system_prompt else "") + user_prompt
                            
                            stop_sequences_list = [s.strip() for s in stop_sequences.split(",")] if stop_sequences else None

                            generation_config = genai.types.GenerationConfig(
                                temperature=temperature,
                                top_p=top_p,
                                top_k=top_k,
                                max_output_tokens=max_output_tokens,
                                stop_sequences=stop_sequences_list
                            )

                            response = model.generate_content(
                                prompt,
                                generation_config=generation_config
                            )
                            
                            result = response.text
                            
                            # Display response metadata
                            st.markdown("---")
                            st.markdown("#### 📊 Response Metrics")
                            
                            # Placeholder for token count, as the API response object in the playground might not have it directly.
                            # In a real application, you would get this from the response object.
                            input_token_count = len(prompt.split()) # A rough estimate
                            output_token_count = len(result.split()) # A rough estimate
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Input Tokens", f"~{input_token_count}")
                            with col2:
                                st.metric("Output Tokens", f"~{output_token_count}")
                            with col3:
                                finish_reason = response.prompt_feedback if hasattr(response, 'prompt_feedback') else "N/A"
                                st.metric("Finish Reason", "OK")

                        else:
                            # Fallback: concatenate system prompt
                            prompt = (system_prompt + "\n" if system_prompt else "") + user_prompt
                            result = generate_response(prompt)
                            
                    except Exception as e:
                        result = f"An error occurred: {e}"

                    st.markdown(f"""
                    <div class="result-container">
                        <div class="result-title">🔬 PromptLab Output</div>
                        <div class="result-content" style="white-space: pre-wrap;">{result}</div>
                    </div>
                    """, unsafe_allow_html=True)
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
/* === FIX TEXT VISIBILITY AND PREVENT FADING === */
body, .stApp, .stMarkdown, .sidebar-guide, .sidebar-guide li, .sidebar-guide h4,
h1, h2, h3, h4, h5, h6, .hero-title, .hero-subtitle, .result-title, .result-content,
.stTextInput label, .stTextArea label, .stSelectbox label, .stat-number, .emotion-indicator,
.stButton button, .mystical-button, .feature-card, .result-container, .cosmic-card {
    color: #fff !important;
    opacity: 1 !important;
    text-shadow: none !important;
    filter: none !important;
}

.stMarkdown, .sidebar-guide, .sidebar-guide li, .sidebar-guide h4 {
    color: #fff !important;
    opacity: 1 !important;
}

.hero-title, .hero-subtitle {
    color: #fff !important;
    opacity: 1 !important;
    -webkit-text-fill-color: #fff !important;
    background: none !important;
    text-shadow: none !important;
    filter: none !important;
    animation: none !important;
}

.result-title, .result-content {
    color: #fff !important;
    opacity: 1 !important;
    text-shadow: none !important;
    filter: none !important;
}

.emotion-indicator {
    color: #fff !important;
    opacity: 1 !important;
    text-shadow: none !important;
    filter: none !important;
       animation: none !important;
}

.sidebar-guide, .sidebar-guide li, .sidebar-guide h4 {
    color: #fff !important;
    opacity: 1 !important;
}

.stTextInput input, .stTextArea textarea, .stSelectbox select {
    color: #fff !important;
    opacity: 1 !important;
}

.stButton button, .mystical-button {
    color: #fff !important;
    opacity: 1 !important;
}

.stat-number {
    color: #fff !important;
    opacity: 1 !important;
    background: none !important;
    -webkit-background-clip: unset !important;
    -webkit-text-fill-color: #fff !important;
    background-clip: unset !important;
    text-shadow: none !important;
    filter: none !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #fff !important;
    opacity: 1 !important;
    text-shadow: none !important;
    filter: none !important;
    animation: none !important;
}

/* Remove any text fade animation */
@keyframes titleGlow { 0% { filter: none; } 100% { filter: none; } }
@keyframes heroGlow { 0% { filter: none; } 100% { filter: none; } }
@keyframes emotionPulse { 0% { box-shadow: none; } 100% { box-shadow: none; } }
@keyframes constellationPulse { 0% { opacity: 1; filter: none; } 50% { opacity: 1; filter: none; } 100% { opacity: 1; filter: none; } }

/* Remove fading from .hero-title and .hero-subtitle */
.hero-title, .hero-subtitle {
    animation: none !important;
    filter: none !important;
    opacity: 1 !important;
}

/* Remove fading from .emotion-indicator */
.emotion-indicator {
    animation: none !important;
    opacity: 1 !important;
}

/* Remove fading from .result-title and .result-content */
.result-title, .result-content {
    opacity: 1 !important;
    filter: none !important;
    animation: none !important;
}

/* Remove fading from .sidebar-guide */
.sidebar-guide, .sidebar-guide li, .sidebar-guide h4 {
    opacity: 1 !important;
    filter: none !important;
    animation: none !important;
}

/* Remove fading from .stat-number */
.stat-number {
    opacity: 1 !important;
    filter: none !important;
    animation: none !important;
}

/* Remove fading from .feature-card and .result-container */
.feature-card, .result-container {
    opacity: 1 !important;
    filter: none !important;
    animation: none !important;
}

/* Remove fading from .cosmic-card */
.cosmic-card {
    opacity: 1 !important;
    filter: none !important;
    animation: none !important;
}
</style>
""", unsafe_allow_html=True)
