import streamlit as st
import asyncio
from agent import BlogAgent

# Configure Streamlit page with dark theme
st.set_page_config(
    page_title="✨ SyntaxCrafter: The Blog Smith",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize the blog agent
@st.cache_resource
def get_agent():
    return BlogAgent()

# Custom CSS with enhanced dark theme
st.markdown("""
<style>
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #1a1f2c, #121620) !important;
        color: #c8d1e0 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Primary Heading (h1) styling */
    h1 {
        background: linear-gradient(120deg, #3b82f6, #60a5fa) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        text-align: center !important;
        margin-bottom: 2rem !important;
        padding: 2rem 0 !important;
        text-shadow: 0 0 30px rgba(59, 130, 246, 0.5) !important;
        letter-spacing: -0.5px !important;
    }
    
    /* Secondary Heading (h2) styling */
    h2 {
        color: #10b981 !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        margin: 2rem 0 1.5rem !important;
        border-bottom: 2px solid rgba(16, 185, 129, 0.2) !important;
        padding-bottom: 0.5rem !important;
        letter-spacing: -0.3px !important;
    }
    
    /* Tertiary Heading (h3) styling */
    h3 {
        color: #818cf8 !important;
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        margin: 1.5rem 0 1rem !important;
        letter-spacing: -0.2px !important;
    }
    
    /* Description box styling */
    .description-box {
        background: rgba(30, 41, 59, 0.5) !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
        border-radius: 12px !important;
        padding: 2rem !important;
        margin: 2rem 0 !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Blog content styling */
    .blog-content {
        background: rgba(30, 41, 59, 0.7) !important;
        padding: 3rem !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
        margin: 2rem 0 !important;
    }
    
    .blog-content p {
        color: #c8d1e0 !important;
        line-height: 1.8 !important;
        font-size: 1.1rem !important;
        margin-bottom: 1.2rem !important;
    }
    
    /* Code block styling */
    .blog-content code {
        background: #1e293b !important;
        color: #60a5fa !important;
        padding: 0.2rem 0.4rem !important;
        border-radius: 4px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.9rem !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
    }
    
    .blog-content pre {
        background: #1e293b !important;
        padding: 1.5rem !important;
        border-radius: 8px !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Table styling */
    table {
        width: 100% !important;
        border-collapse: separate !important;
        border-spacing: 0 !important;
        margin: 1.5rem 0 !important;
        background: rgba(30, 41, 59, 0.5) !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }
    
    th {
        background: rgba(59, 130, 246, 0.1) !important;
        color: #60a5fa !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        text-align: left !important;
        border-bottom: 2px solid rgba(59, 130, 246, 0.2) !important;
    }
    
    td {
        padding: 1rem !important;
        color: #c8d1e0 !important;
        border-bottom: 1px solid rgba(59, 130, 246, 0.1) !important;
    }
    
    tr:hover {
        background: rgba(59, 130, 246, 0.05) !important;
    }
    
    /* List styling */
    .blog-content ul, .blog-content ol {
        color: #c8d1e0 !important;
        margin: 1.2rem 0 1.2rem 1.5rem !important;
    }
    
    .blog-content li {
        margin-bottom: 0.8rem !important;
        line-height: 1.6 !important;
    }
    
    .blog-content li::marker {
        color: #60a5fa !important;
    }
    
    /* Input field styling */
    .stTextInput input {
        background: rgba(30, 41, 59, 0.5) !important;
        border: 2px solid rgba(59, 130, 246, 0.2) !important;
        border-radius: 8px !important;
        color: #c8d1e0 !important;
        padding: 1rem !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #3b82f6, #60a5fa) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Blockquote styling */
    blockquote {
        border-left: 4px solid #3b82f6 !important;
        margin: 1.5rem 0 !important;
        padding: 1rem 1.5rem !important;
        background: rgba(59, 130, 246, 0.1) !important;
        border-radius: 0 8px 8px 0 !important;
        color: #c8d1e0 !important;
        font-style: italic !important;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-color: #3b82f6 transparent transparent transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.title("✨ SyntaxCrafter: The Blog Smith")

st.markdown("""
<div class="description-box">
    <h3 style="color: #818cf8; margin-bottom: 1.5rem; font-size: 2rem;">Transform Any Topic into an Engaging Blog Post!</h3>
    <p style="font-size: 1.2rem; color: #c8d1e0; margin-bottom: 2rem;">
        Generate detailed, well-structured blog posts on any topic - from technology to health, science to lifestyle, and everything in between! Our AI-powered tool creates professional content tailored to your subject matter.
    </p>
    <div style="margin-top: 2rem;">
        <p style="font-weight: 600; color: #60a5fa; font-size: 1.3rem; margin-bottom: 1rem;">Try these diverse topics:</p>
        <div style="display: flex; flex-wrap: wrap; gap: 1rem; justify-content: center;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; width: 100%; text-align: center;">
                <div style="background: rgba(30, 41, 59, 0.7); padding: 1rem; border-radius: 8px; border: 1px solid rgba(59, 130, 246, 0.2);">
                    <span style="color: #60a5fa;">💻 Technology</span>
                    <div style="color: #c8d1e0; font-size: 0.9rem; margin-top: 0.5rem;">Machine Learning in Healthcare</div>
                </div>
                <div style="background: rgba(30, 41, 59, 0.7); padding: 1rem; border-radius: 8px; border: 1px solid rgba(59, 130, 246, 0.2);">
                    <span style="color: #60a5fa;">🔬 Science</span>
                    <div style="color: #c8d1e0; font-size: 0.9rem; margin-top: 0.5rem;">Black Holes and Dark Matter</div>
                </div>
                <div style="background: rgba(30, 41, 59, 0.7); padding: 1rem; border-radius: 8px; border: 1px solid rgba(59, 130, 246, 0.2);">
                    <span style="color: #60a5fa;">💪 Fitness</span>
                    <div style="color: #c8d1e0; font-size: 0.9rem; margin-top: 0.5rem;">HIIT vs Traditional Cardio</div>
                </div>
                <div style="background: rgba(30, 41, 59, 0.7); padding: 1rem; border-radius: 8px; border: 1px solid rgba(59, 130, 246, 0.2);">
                    <span style="color: #60a5fa;">💰 Finance</span>
                    <div style="color: #c8d1e0; font-size: 0.9rem; margin-top: 0.5rem;">Cryptocurrency Investment Strategies</div>
                </div>
                <div style="background: rgba(30, 41, 59, 0.7); padding: 1rem; border-radius: 8px; border: 1px solid rgba(59, 130, 246, 0.2);">
                    <span style="color: #60a5fa;">🎨 Arts</span>
                    <div style="color: #c8d1e0; font-size: 0.9rem; margin-top: 0.5rem;">Digital Art Revolution</div>
                </div>
                <div style="background: rgba(30, 41, 59, 0.7); padding: 1rem; border-radius: 8px; border: 1px solid rgba(59, 130, 246, 0.2);">
                    <span style="color: #60a5fa;">🌿 Environment</span>
                    <div style="color: #c8d1e0; font-size: 0.9rem; margin-top: 0.5rem;">Sustainable Living Guide</div>
                </div>
                <div style="background: rgba(30, 41, 59, 0.7); padding: 1rem; border-radius: 8px; border: 1px solid rgba(59, 130, 246, 0.2);">
                    <span style="color: #60a5fa;">🏥 Medical</span>
                    <div style="color: #c8d1e0; font-size: 0.9rem; margin-top: 0.5rem;">Understanding Immunotherapy</div>
                </div>
                <div style="background: rgba(30, 41, 59, 0.7); padding: 1rem; border-radius: 8px; border: 1px solid rgba(59, 130, 246, 0.2);">
                    <span style="color: #60a5fa;">🎓 Education</span>
                    <div style="color: #c8d1e0; font-size: 0.9rem; margin-top: 0.5rem;">Future of Online Learning</div>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Get or create agent
agent = get_agent()

# Input field for topic
topic = st.text_input("✍️ Enter your blog topic:", placeholder="e.g., Space Tourism, Mindful Living, or Quantum Computing")

async def generate_blog_async(topic):
    return await agent.generate_blog(topic)

if topic:
    with st.spinner("🎨 Crafting your cyberpunk masterpiece..."):
        try:
            # Generate blog content
            blog_content = asyncio.run(generate_blog_async(topic))
            
            # Display the blog
            st.markdown('<div class="blog-content">', unsafe_allow_html=True)
            st.markdown(blog_content)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Add download button with enhanced styling
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    label="📥 Download Your Masterpiece",
                    data=blog_content,
                    file_name=f"{topic.replace(' ', '_').lower()}_blog.md",
                    mime="text/markdown"
                )
            
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}\n\nPlease try a different topic.")
            
# Footer
st.markdown("""
<footer>
    <p>Crafted with 💚 by SyntaxCrafter Team</p>
    <a href="https://github.com/yourusername/syntaxcrafter" target="_blank">
        View on GitHub
    </a>
</footer>
""", unsafe_allow_html=True)
