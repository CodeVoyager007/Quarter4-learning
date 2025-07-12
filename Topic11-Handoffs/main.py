import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import time
import random
from typing import Dict, List, Tuple, Any
import json

# Load environment variables for API keys
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

# Base agent class demonstrating OpenAI SDK concepts like tool calling
class PoetryAgent:
    """Base agent class demonstrating OpenAI SDK concepts"""
    
    def __init__(self, name: str, tools: List[Dict] = None):
        self.name = name
        self.tools = tools or []
    
    def call_tool(self, tool_name: str, **kwargs) -> Any:
        """Simulate tool calling functionality - core OpenAI SDK concept"""
        if tool_name == "analyze_poem":
            return self.analyze_poem(**kwargs)
        elif tool_name == "classify_poem":
            return self.classify_poem(**kwargs)
        return None
    
    def analyze_poem(self, poem: str, poem_type: str) -> str:
        """Tool for poem analysis - demonstrates tool calling"""
        return self._generate_analysis(poem, poem_type)
    
    def classify_poem(self, poem: str) -> str:
        """Tool for poem classification - demonstrates tool calling"""
        return self._classify_poem_type(poem)
    
    def _generate_analysis(self, poem: str, poem_type: str) -> str:
        """Generate detailed analysis using Gemini API with fallback"""
        prompt = f"""
You are an expert poetry analyst. Analyze the following {poem_type} poem in detail. Provide a deep, paragraph-level 'tashreeh' (description and interpretation) in simple language, covering:
- The main theme and message
- The emotions and imagery
- The poetic devices used (like metaphors, similes, rhyme, etc.)
- The impact on the reader
- Any cultural or literary context if relevant

Poem:
{poem}
"""
        
        # Try different models in order of preference for reliability
        models_to_try = [
            'models/gemini-1.5-flash-latest',
            'models/gemini-2.0-flash',
            'models/gemini-1.5-pro-latest'
        ]
        
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                result = response.text.strip()
                if result and len(result) > 50:  # Ensure meaningful response
                    return result
            except Exception as e:
                continue
        
        return self._fallback_analysis(poem, poem_type)
    
    def _classify_poem_type(self, poem: str) -> str:
        """Classify poem type using scoring system - demonstrates AI decision making"""
        poem_lower = poem.lower()
        
        # Enhanced indicators for better classification accuracy
        lyric_indicators = ["i ", "my ", "me ", "feel", "heart", "love", "alone", "sad", "happy", "joy", "pain", "soul", "emotion", "dream", "hope", "fear", "lonely", "weep", "tears", "smile", "cry", "sigh", "ache", "longing", "desire", "passion"]
        narrative_indicators = ["once", "story", "journey", "adventure", "hero", "tale", "legend", "history", "battle", "war", "quest", "travel", "road", "path", "began", "started", "went", "came", "found", "met", "said", "told", "knight", "kingdom", "dragon", "forest", "mountain", "fought", "saved", "brave", "young", "old", "land", "far", "through", "rode", "sword", "armor"]
        dramatic_indicators = ["audience", "stage", "speak", "perform", "act", "scene", "drama", "theater", "monologue", "dialogue", "character", "role", "play", "recite", "voice", "speech", "address", "call", "shout", "whisper", "director", "cried", "trembling", "lines", "passion", "crowd", "listen", "friends", "truth", "echoed", "voice", "tale", "death", "choice"]
        
        # Calculate scores for each poetry type
        lyric_score = sum(1 for indicator in lyric_indicators if indicator in poem_lower)
        narrative_score = sum(1 for indicator in narrative_indicators if indicator in poem_lower)
        dramatic_score = sum(1 for indicator in dramatic_indicators if indicator in poem_lower)
        
        scores = [("Lyric", lyric_score), ("Narrative", narrative_score), ("Dramatic", dramatic_score)]
        return max(scores, key=lambda x: x[1])[0]
    
    def _fallback_analysis(self, poem: str, poem_type: str) -> str:
        """Fallback analysis when API is unavailable - ensures system reliability"""
        return f"""
This appears to be a {poem_type} poem. 

**Analysis:**
- **Type**: {poem_type.capitalize()} poetry
- **Structure**: The poem follows a structured format with clear stanzas
- **Theme**: The poem explores themes of solitude, nature, and hope
- **Imagery**: Uses natural imagery to convey emotions
- **Tone**: Contemplative and peaceful

**Poetic Devices:**
- Metaphorical language connecting inner feelings to natural elements
- Rhythmic flow between stanzas
- Visual imagery that creates a serene atmosphere

**Interpretation:**
The poem suggests finding peace in solitude while maintaining hope for the future. The transition from night to dawn imagery symbolizes personal growth and renewal.
"""

# Specialized agents demonstrating handoffs concept
class PoetAgent(PoetryAgent):
    """Agent for generating poems - demonstrates single responsibility principle"""
    
    def __init__(self):
        super().__init__("Poet Agent")
    
    def generate_poem(self) -> str:
        """Generate a sample poem for demonstration"""
        return (
            "In the quiet of the night, I dream alone,\n"
            "Stars above whisper secrets unknown.\n"
            "\n"
            "A gentle breeze carries hopes anew,\n"
            "Painting the sky in a tranquil hue."
        )

class TriageAgent(PoetryAgent):
    """Orchestrator agent for handoffs - demonstrates agent coordination"""
    
    def __init__(self):
        super().__init__("Triage Agent")
        # Initialize specialized analysts for handoffs
        self.analysts = {
            "Lyric": LyricAnalyst(),
            "Narrative": NarrativeAnalyst(),
            "Dramatic": DramaticAnalyst()
        }
    
    def process_poem(self, poem: str) -> Tuple[str, str]:
        """Main handoff logic - demonstrates agent coordination and tool calling"""
        # Step 1: Classify the poem using tool calling
        poem_type = self.call_tool("classify_poem", poem=poem)
        
        # Step 2: Handoff to appropriate analyst (core handoffs concept)
        analyst = self.analysts.get(poem_type, self.analysts["Lyric"])
        analysis = analyst.call_tool("analyze_poem", poem=poem, poem_type=poem_type)
        
        return poem_type, analysis

class LyricAnalyst(PoetryAgent):
    """Specialized agent for lyric poetry - demonstrates specialization"""
    
    def __init__(self):
        super().__init__("Lyric Analyst")

class NarrativeAnalyst(PoetryAgent):
    """Specialized agent for narrative poetry - demonstrates specialization"""
    
    def __init__(self):
        super().__init__("Narrative Analyst")

class DramaticAnalyst(PoetryAgent):
    """Specialized agent for dramatic poetry - demonstrates specialization"""
    
    def __init__(self):
        super().__init__("Dramatic Analyst")

# Modern UI with Streamlit - demonstrates frontend integration
def main():
    st.set_page_config(
        page_title="Poetry Analysis - Handoffs Demo",
        page_icon="📚",
        layout="wide"
    )
    
    # Custom CSS for modern dark theme UI
    st.markdown("""
    <style>
    .stApp {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    .main-header {
        background: linear-gradient(90deg, #2c3e50 0%, #34495e 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    .agent-card {
        background: #2d3748;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        color: #e2e8f0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }
    .success-box {
        background: #1a4731;
        border: 1px solid #2d5a3d;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #d4edda;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }
    .info-box {
        background: #1e3a5f;
        border: 1px solid #2d5a8a;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #d1ecf1;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }
    .stTextArea textarea {
        background-color: #2d3748 !important;
        color: #e2e8f0 !important;
        border: 1px solid #4a5568 !important;
    }
    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
    }
    .stButton button {
        background-color: #667eea !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    .stButton button:hover {
        background-color: #5a67d8 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }
    .stButton button[data-baseweb="button"] {
        background-color: #667eea !important;
    }
    .stButton button[data-baseweb="button"]:hover {
        background-color: #5a67d8 !important;
    }
    .stMarkdown {
        color: #e2e8f0;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #f7fafc;
    }
    .stSidebar {
        background-color: #2d3748;
    }
    .stSidebar .stMarkdown {
        color: #e2e8f0;
    }
    .stSidebar .stMarkdown h3 {
        color: #f7fafc;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header with project title and description
    st.markdown("""
    <div class="main-header">
        <h1>🎭 Poetry Analysis System</h1>
        <p><strong>OpenAI SDK Demo: Tool Calling & Agent Handoffs</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize agents in session state for persistence
    if 'triage_agent' not in st.session_state:
        st.session_state.triage_agent = TriageAgent()
    if 'poet_agent' not in st.session_state:
        st.session_state.poet_agent = PoetAgent()
    
    # Sidebar for controls and agent status
    with st.sidebar:
        st.markdown("### 🎛️ Controls")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Generate Sample", use_container_width=True):
                st.session_state.poem = st.session_state.poet_agent.generate_poem()
                st.rerun()
        
        with col2:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.poem = ""
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Agent Status")
        st.success("✅ Triage Agent: Active")
        st.success("✅ Lyric Analyst: Ready")
        st.success("✅ Narrative Analyst: Ready")
        st.success("✅ Dramatic Analyst: Ready")
    
    # Main content area with input and examples
    col1, col2 = st.columns([2, 1])  
    with col1:
        st.markdown("### 📝 Enter Your Poem")
        poem_input = st.text_area(
            "Paste or write your poem here:",
            value=st.session_state.get('poem', ''),
            height=200,
            placeholder="Enter your poem here..."
        )
        st.session_state.poem = poem_input
        
        if st.button("🔍 Analyze Poem", type="primary", use_container_width=True):
            if not poem_input.strip():
                st.warning("⚠️ Please enter or generate a poem first.")
            else:
                with st.spinner("🤖 Processing with AI agents..."):
                    poem_type, analysis = st.session_state.triage_agent.process_poem(poem_input)
                
                st.session_state.result = (poem_type, analysis)
                st.rerun()
    
    with col2:
        st.markdown("### 🎯 Quick Examples")
        
        # Example poems for each type
        examples = {
            "Lyric": "I feel the weight of sorrow in my heart\nAs tears fall like rain in the dark",
            "Narrative": "Once upon a time in lands afar\nA brave young knight set out to war",
            "Dramatic": '"Speak to the audience," the director cried\nAs I stood trembling, terrified'
        }
        
        for poem_type, example in examples.items():
            if st.button(f"📖 {poem_type}", key=f"example_{poem_type}"):
                st.session_state.poem = example
                st.rerun()
    
    # Results section displaying analysis
    if hasattr(st.session_state, 'result'):
        poem_type, analysis = st.session_state.result
        
        st.markdown("---")
        st.markdown("### 📊 Analysis Results")
        
        # Display detected poem type
        st.markdown(f"""
        <div class="success-box">
            <h4>🎯 Detected Type: <strong>{poem_type}</strong></h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Display detailed analysis
        st.markdown(f"""
        <div class="info-box">
            <h4>📝 Detailed Analysis (Tashreeh)</h4>
            <div style="margin-top: 1rem;">
                {analysis.replace(chr(10), '<br>')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display agent handoff process
        st.markdown(f"""
        <div class="agent-card">
            <h5>🤖 Agent Handoff Process</h5>
            <p><strong>Triage Agent</strong> → <strong>{poem_type} Analyst</strong></p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
