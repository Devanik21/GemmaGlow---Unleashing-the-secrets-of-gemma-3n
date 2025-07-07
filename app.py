import streamlit as st
import google.generativeai as genai
import re
import time
import json
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from textblob import TextBlob
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import base64
from io import BytesIO

# Configure page
st.set_page_config(
    page_title="GemmaGlow ✨",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for magical UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;600;700&display=swap');
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    }
    
    .main-header h1 {
        color: white;
        font-family: 'Quicksand', sans-serif;
        font-size: 3rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin: 0;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    
    .emotion-happy { background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); }
    .emotion-sad { background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); }
    .emotion-angry { background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%); }
    .emotion-excited { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
    .emotion-calm { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
    .emotion-neutral { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    
    .theme-dreamy { background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); }
    .theme-neon { background: linear-gradient(135deg, #08fdd8 0%, #9d50bb 100%); }
    .theme-solar { background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%); }
    
    .sparkle {
        position: absolute;
        width: 4px;
        height: 4px;
        background: white;
        border-radius: 50%;
        animation: sparkle 2s infinite;
    }
    
    @keyframes sparkle {
        0% { opacity: 0; transform: scale(0); }
        50% { opacity: 1; transform: scale(1); }
        100% { opacity: 0; transform: scale(0); }
    }
    
    .stTextInput input {
        border-radius: 15px;
        border: 2px solid rgba(255,255,255,0.3);
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    }
    
    .stButton button {
        border-radius: 15px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# Initialize Gemini API
@st.cache_resource
def init_gemini():
    try:
        genai.configure(api_key=st.secrets["gemini_api_key"])
        return genai.GenerativeModel('gemini-pro')
    except Exception as e:
        st.error(f"Error initializing Gemini: {e}")
        return None

model = init_gemini()

# Emotion detection function
def detect_emotion(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    if polarity > 0.3:
        return "happy", "😊"
    elif polarity < -0.3:
        return "sad", "😢"
    elif subjectivity > 0.7:
        return "excited", "🤩"
    elif polarity < -0.1 and subjectivity > 0.5:
        return "angry", "😠"
    elif abs(polarity) < 0.1 and subjectivity < 0.3:
        return "calm", "😌"
    else:
        return "neutral", "😐"

# Generate AI response
def generate_response(prompt, context=""):
    if not model:
        return "Gemini API not available. Please check your API key."
    
    try:
        full_prompt = f"{context}\n\n{prompt}" if context else prompt
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Main app header
st.markdown("""
<div class="main-header">
    <h1>💎 GemmaGlow</h1>
    <p>The Multifaceted AI Companion ✨</p>
</div>
""", unsafe_allow_html=True)

# Theme selector
theme = st.sidebar.selectbox(
    "🎨 Choose Theme",
    ["Dreamy", "NeonByte", "SolarBurst"]
)

# Apply theme
theme_class = f"theme-{theme.lower()}"
if theme == "NeonByte":
    theme_class = "theme-neon"
elif theme == "SolarBurst":
    theme_class = "theme-solar"

# Sidebar navigation
st.sidebar.markdown("### 🌟 Features")
feature = st.sidebar.radio(
    "Select a feature:",
    ["MoodSync", "QuickThink", "CreateSpark", "DebateBot", "MultiLingua", "PromptCraft", "ThoughtLoop"]
)

# Feature 1: MoodSync - Emotion Analysis
if feature == "MoodSync":
    st.markdown("## 🌸 MoodSync - Emotion Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_input = st.text_area(
            "Share your thoughts or feelings:",
            placeholder="Tell me how you're feeling today...",
            height=100
        )
        
        if st.button("🔍 Analyze Mood"):
            if user_input:
                with st.spinner("Analyzing your emotions..."):
                    emotion, emoji = detect_emotion(user_input)
                    
                    # Generate empathic response
                    empathy_prompt = f"""
                    The user wrote: "{user_input}"
                    Their detected emotion is: {emotion}
                    
                    Provide a warm, empathetic response that acknowledges their feelings and offers gentle support or encouragement. Be understanding and compassionate.
                    """
                    
                    ai_response = generate_response(empathy_prompt)
                    
                    # Display results
                    st.markdown(f'<div class="feature-card emotion-{emotion}">', unsafe_allow_html=True)
                    st.markdown(f"### {emoji} Detected Emotion: {emotion.title()}")
                    st.markdown(f"**AI Response:** {ai_response}")
                    
                    # Suggested action
                    if emotion == "sad":
                        suggestion = "How about taking a gentle walk or listening to uplifting music? 🎵"
                    elif emotion == "angry":
                        suggestion = "Try some deep breathing exercises or physical activity to release tension 🧘‍♀️"
                    elif emotion == "excited":
                        suggestion = "Channel that energy into something creative or share your excitement with someone! 🎨"
                    elif emotion == "calm":
                        suggestion = "Perfect time for reflection or planning something meaningful 📝"
                    else:
                        suggestion = "Take a moment to check in with yourself and practice self-care 💚"
                    
                    st.markdown(f"**💡 Suggested Action:** {suggestion}")
                    st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🎭 Emotion Guide")
        st.markdown("""
        - 😊 **Happy**: Positive, upbeat
        - 😢 **Sad**: Melancholic, down
        - 😠 **Angry**: Frustrated, upset
        - 🤩 **Excited**: Enthusiastic, energetic
        - 😌 **Calm**: Peaceful, balanced
        - 😐 **Neutral**: Balanced, neutral
        """)

# Feature 2: QuickThink - Summarizer & Explainer
elif feature == "QuickThink":
    st.markdown("## 📚 QuickThink - Smart Summarizer")
    
    text_input = st.text_area(
        "Paste your text here:",
        placeholder="Enter long text, article, or notes...",
        height=150
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Summarize"):
            if text_input:
                with st.spinner("Summarizing..."):
                    summary = generate_response(f"Provide a concise summary of this text: {text_input}")
                    st.markdown("### 📋 Summary")
                    st.markdown(f'<div class="feature-card">{summary}</div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("🔍 Explain Simply"):
            if text_input:
                level = st.selectbox("Explanation level:", ["Like I'm 5", "Like I'm 15", "Like I'm a Pro"])
                with st.spinner("Explaining..."):
                    explain_prompt = f"Explain this text {level.lower()}: {text_input}"
                    explanation = generate_response(explain_prompt)
                    st.markdown("### 💡 Explanation")
                    st.markdown(f'<div class="feature-card">{explanation}</div>', unsafe_allow_html=True)
    
    with col3:
        if st.button("🎨 Create Metaphor"):
            if text_input:
                with st.spinner("Creating metaphor..."):
                    metaphor = generate_response(f"Create a creative metaphor to explain this concept: {text_input}")
                    st.markdown("### 🌟 Metaphor")
                    st.markdown(f'<div class="feature-card">{metaphor}</div>', unsafe_allow_html=True)

# Feature 3: CreateSpark - Creative Writer
elif feature == "CreateSpark":
    st.markdown("## ✨ CreateSpark - Creative Writer")
    
    prompt_input = st.text_input(
        "Enter your creative prompt:",
        placeholder="A mysterious forest at midnight..."
    )
    
    mood = st.selectbox(
        "Choose mood:",
        ["Dreamy", "Deep", "Chaotic", "Romantic", "Mysterious", "Uplifting"]
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🪷 Generate Poem"):
            if prompt_input:
                with st.spinner("Crafting poetry..."):
                    poem_prompt = f"Write a {mood.lower()} poem about: {prompt_input}"
                    poem = generate_response(poem_prompt)
                    st.markdown("### 🪷 Your Poem")
                    st.markdown(f'<div class="feature-card">{poem}</div>', unsafe_allow_html=True)
        
        if st.button("📘 Write Microfiction"):
            if prompt_input:
                with st.spinner("Writing story..."):
                    fiction_prompt = f"Write a {mood.lower()} microfiction (under 100 words) about: {prompt_input}"
                    fiction = generate_response(fiction_prompt)
                    st.markdown("### 📘 Microfiction")
                    st.markdown(f'<div class="feature-card">{fiction}</div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("🎨 Visual Art Prompt"):
            if prompt_input:
                with st.spinner("Creating visual prompt..."):
                    visual_prompt = f"Create a detailed visual art prompt with {mood.lower()} mood for: {prompt_input}"
                    visual = generate_response(visual_prompt)
                    st.markdown("### 🎨 Visual Prompt")
                    st.markdown(f'<div class="feature-card">{visual}</div>', unsafe_allow_html=True)
        
        if st.button("💬 Tweet-sized Idea"):
            if prompt_input:
                with st.spinner("Generating idea..."):
                    tweet_prompt = f"Create a {mood.lower()} tweet-sized idea (under 280 characters) about: {prompt_input}"
                    tweet = generate_response(tweet_prompt)
                    st.markdown("### 💬 Tweet Idea")
                    st.markdown(f'<div class="feature-card">{tweet}</div>', unsafe_allow_html=True)

# Feature 4: DebateBot - AI Thinks Like Opposites
elif feature == "DebateBot":
    st.markdown("## 🔍 DebateBot - Multiple Perspectives")
    
    topic = st.text_input(
        "Enter debate topic:",
        placeholder="Is artificial intelligence dangerous?"
    )
    
    persona = st.selectbox(
        "Choose AI persona:",
        ["Socrates", "Feynman", "Tsundere", "Philosopher", "Scientist", "Optimist", "Pessimist"]
    )
    
    if st.button("🎭 Generate Debate"):
        if topic:
            with st.spinner("Generating perspectives..."):
                col1, col2 = st.columns(2)
                
                with col1:
                    pro_prompt = f"As {persona}, argue FOR this position: {topic}. Be thoughtful and provide strong reasoning."
                    pro_response = generate_response(pro_prompt)
                    st.markdown("### ✅ Pro Argument")
                    st.markdown(f'<div class="feature-card">{pro_response}</div>', unsafe_allow_html=True)
                
                with col2:
                    con_prompt = f"As {persona}, argue AGAINST this position: {topic}. Be thoughtful and provide strong reasoning."
                    con_response = generate_response(con_prompt)
                    st.markdown("### ❌ Con Argument")
                    st.markdown(f'<div class="feature-card">{con_response}</div>', unsafe_allow_html=True)
                
                # Synthesis
                synthesis_prompt = f"Provide a balanced synthesis of these two perspectives on: {topic}"
                synthesis = generate_response(synthesis_prompt)
                st.markdown("### 🤝 Synthesis")
                st.markdown(f'<div class="feature-card">{synthesis}</div>', unsafe_allow_html=True)

# Feature 5: MultiLingua - Translate + Emotion
elif feature == "MultiLingua":
    st.markdown("## 🌐 MultiLingua - Emotional Translation")
    
    text_to_translate = st.text_area(
        "Enter text to translate:",
        placeholder="Hello, how are you feeling today?",
        height=100
    )
    
    target_lang = st.selectbox(
        "Target language:",
        ["Spanish", "French", "German", "Italian", "Japanese", "Korean", "Chinese", "Portuguese", "Russian"]
    )
    
    if st.button("🔄 Translate with Emotion"):
        if text_to_translate:
            with st.spinner("Translating and analyzing..."):
                col1, col2 = st.columns(2)
                
                with col1:
                    # Original emotion
                    orig_emotion, orig_emoji = detect_emotion(text_to_translate)
                    st.markdown("### 📝 Original Text")
                    st.markdown(f'<div class="feature-card emotion-{orig_emotion}">', unsafe_allow_html=True)
                    st.markdown(f"**Text:** {text_to_translate}")
                    st.markdown(f"**Emotion:** {orig_emoji} {orig_emotion.title()}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    # Translation
                    translate_prompt = f"Translate this text to {target_lang}, maintaining the emotional tone and cultural context: {text_to_translate}"
                    translation = generate_response(translate_prompt)
                    
                    # Analyze translated emotion
                    trans_emotion, trans_emoji = detect_emotion(translation)
                    
                    st.markdown("### 🌍 Translation")
                    st.markdown(f'<div class="feature-card emotion-{trans_emotion}">', unsafe_allow_html=True)
                    st.markdown(f"**Translation:** {translation}")
                    st.markdown(f"**Emotion:** {trans_emoji} {trans_emotion.title()}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Cultural notes
                cultural_prompt = f"Provide cultural context and nuances for translating '{text_to_translate}' to {target_lang}"
                cultural_notes = generate_response(cultural_prompt)
                st.markdown("### 🎭 Cultural Context")
                st.markdown(f'<div class="feature-card">{cultural_notes}</div>', unsafe_allow_html=True)

# Feature 6: PromptCraft - Prompt Rewriting
elif feature == "PromptCraft":
    st.markdown("## 🌱 PromptCraft - Prompt Enhancement")
    
    original_prompt = st.text_area(
        "Enter your prompt:",
        placeholder="Write a story about a robot...",
        height=100
    )
    
    if st.button("✨ Enhance Prompt"):
        if original_prompt:
            with st.spinner("Crafting enhanced prompts..."):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    poetic_prompt = f"Rewrite this prompt in a poetic, beautiful style: {original_prompt}"
                    poetic = generate_response(poetic_prompt)
                    st.markdown("### 🎭 Poetic Style")
                    st.markdown(f'<div class="feature-card">{poetic}</div>', unsafe_allow_html=True)
                
                with col2:
                    visual_prompt = f"Rewrite this prompt with rich visual imagery and cinematic details: {original_prompt}"
                    visual = generate_response(visual_prompt)
                    st.markdown("### 🎨 Visual Style")
                    st.markdown(f'<div class="feature-card">{visual}</div>', unsafe_allow_html=True)
                
                with col3:
                    technical_prompt = f"Rewrite this prompt with technical precision and detailed specifications: {original_prompt}"
                    technical = generate_response(technical_prompt)
                    st.markdown("### 🔧 Technical Style")
                    st.markdown(f'<div class="feature-card">{technical}</div>', unsafe_allow_html=True)

# Feature 7: ThoughtLoop - Mind Map Generator
elif feature == "ThoughtLoop":
    st.markdown("## 💭 ThoughtLoop - Mind Map Generator")
    
    thought_input = st.text_area(
        "Enter your thoughts or topic:",
        placeholder="Artificial intelligence and creativity...",
        height=100
    )
    
    if st.button("🧠 Generate Mind Map"):
        if thought_input:
            with st.spinner("Mapping your thoughts..."):
                # Generate related concepts
                concepts_prompt = f"Generate 8-10 related concepts, themes, or ideas connected to: {thought_input}. List them as comma-separated values."
                concepts_response = generate_response(concepts_prompt)
                
                # Parse concepts
                concepts = [c.strip() for c in concepts_response.split(',')]
                
                # Create network graph
                G = nx.Graph()
                G.add_node(thought_input[:30] + "..." if len(thought_input) > 30 else thought_input)
                
                for concept in concepts[:8]:  # Limit to 8 concepts
                    concept_clean = concept.strip('- ').strip()
                    if concept_clean:
                        G.add_node(concept_clean)
                        G.add_edge(thought_input[:30] + "..." if len(thought_input) > 30 else thought_input, concept_clean)
                
                # Create layout
                pos = nx.spring_layout(G, k=3, iterations=50)
                
                # Plot with matplotlib
                plt.figure(figsize=(12, 8))
                plt.style.use('dark_background')
                
                # Draw nodes
                nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                                     node_size=3000, alpha=0.9)
                
                # Draw edges
                nx.draw_networkx_edges(G, pos, edge_color='white', 
                                     alpha=0.6, width=2)
                
                # Draw labels
                nx.draw_networkx_labels(G, pos, font_size=8, font_color='black', 
                                      font_weight='bold')
                
                plt.title("🧠 Your Thought Map", color='white', fontsize=16, pad=20)
                plt.axis('off')
                plt.tight_layout()
                
                # Display plot
                st.pyplot(plt.gcf())
                
                # Generate insights
                insights_prompt = f"Analyze the connections between these concepts: {', '.join(concepts)}. What interesting patterns or insights emerge?"
                insights = generate_response(insights_prompt)
                
                st.markdown("### 💡 Insights")
                st.markdown(f'<div class="feature-card">{insights}</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.7); padding: 2rem;">
    <p>✨ Made with love using Gemini AI ✨</p>
    <p>🌟 Explore the magic of AI creativity 🌟</p>
</div>
""", unsafe_allow_html=True)
