import streamlit as st
import asyncio
from agent import BlogAgent
from tools.image_generator import ImageGenerator

# Set page config
st.set_page_config(
    page_title="SyntaxCrafter: The Blog Smith",
    page_icon="⚙️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main app styling */
    .main {
        padding: 2rem;
        color: #1a1a1a;
    }
    
    /* Headers */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 2rem !important;
    }
    
    h2 {
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        margin: 2rem 0 1rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 2px solid #f0f0f0 !important;
    }
    
    h3 {
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        margin: 1.5rem 0 1rem !important;
    }
    
    /* Blog content */
    .blog-section {
        margin: 2rem 0;
        padding: 1.5rem;
        background-color: #ffffff;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Tables */
    table {
        width: 100% !important;
        margin: 1.5rem 0 !important;
        border-collapse: collapse !important;
    }
    
    th {
        background-color: #f8f9fa !important;
        padding: 12px !important;
        text-align: left !important;
        border: 1px solid #dee2e6 !important;
        font-weight: 600 !important;
    }
    
    td {
        padding: 12px !important;
        border: 1px solid #dee2e6 !important;
    }
    
    tr:nth-child(even) {
        background-color: #f8f9fa !important;
    }
    
    /* Code blocks */
    pre {
        background-color: #f8f9fa !important;
        padding: 1rem !important;
        border-radius: 4px !important;
        margin: 1rem 0 !important;
        overflow-x: auto !important;
    }
    
    code {
        font-family: 'Consolas', 'Monaco', monospace !important;
        font-size: 0.9rem !important;
    }
    
    /* Blockquotes */
    blockquote {
        border-left: 4px solid #007bff !important;
        margin: 1.5rem 0 !important;
        padding: 1rem !important;
        background-color: #f8f9fa !important;
        font-style: italic !important;
    }
    
    /* Horizontal rules */
    hr {
        margin: 2rem 0 !important;
        border: 0 !important;
        border-top: 1px solid #dee2e6 !important;
    }
    
    /* Links */
    a {
        color: #007bff !important;
        text-decoration: none !important;
    }
    
    a:hover {
        text-decoration: underline !important;
    }
    
    /* Images */
    img {
        max-width: 100% !important;
        height: auto !important;
        border-radius: 4px !important;
        margin: 1rem 0 !important;
    }
    
    /* Lists */
    ul, ol {
        margin: 1rem 0 1rem 1.5rem !important;
    }
    
    li {
        margin-bottom: 0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'blog_content' not in st.session_state:
    st.session_state.blog_content = None

# Header
st.title("🎯 SyntaxCrafter: The Blog Smith")
st.markdown("*Generate professional, well-structured blog posts with AI-powered insights and beautiful images*")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    writing_style = st.selectbox(
        "Writing Style",
        ["Professional", "Casual", "Academic", "Technical"]
    )
    
    content_depth = st.slider(
        "Content Depth",
        min_value=1,
        max_value=5,
        value=3,
        help="1 = Brief overview, 5 = In-depth analysis"
    )
    
    include_code = st.checkbox("Include Code Examples", value=True)
    include_quotes = st.checkbox("Include Quotes", value=True)

# Main content area
topic = st.text_input("🔍 Enter your blog topic", placeholder="e.g., Machine Learning Basics")

if st.button("Generate Blog", type="primary"):
    with st.spinner("🎨 Crafting your blog post..."):
        # Initialize our tools
        blog_agent = BlogAgent()
        image_generator = ImageGenerator()
        
        # Generate blog content
        blog_content = asyncio.run(blog_agent.generate_blog(
            topic=topic,
            style=writing_style.lower(),
            depth=content_depth,
            include_code=include_code,
            include_quotes=include_quotes
        ))
        
        # Enrich with images
        if blog_content:
            blog_content["sections"] = asyncio.run(
                image_generator.get_images_for_blog(blog_content["sections"])
            )
            st.session_state.blog_content = blog_content

# Display generated blog
if st.session_state.blog_content:
    blog = st.session_state.blog_content
    
    # Title and introduction
    st.markdown(f"# {blog['title']}")
    st.markdown(f"*{blog['introduction']}*")
    
    # Display each section with images
    for section in blog['sections']:
        with st.container():
            st.markdown("---")
            st.markdown(f"## {section['title']}")
            
            # Display section image if available
            if section.get('image'):
                st.markdown(
                    image_generator.format_image_markdown(section['image']),
                    unsafe_allow_html=True
                )
            
            st.markdown(section['content'])
            
            # Display code if present
            if section.get('code_example'):
                st.code(section['code_example'], language='python')
            
            # Display quote if present
            if section.get('quote'):
                st.markdown(f"> {section['quote']}")
    
    # Export options
    st.markdown("---")
    st.markdown("### 📥 Export Options")
    
    # Convert blog content to markdown
    markdown_content = f"# {blog['title']}\n\n"
    markdown_content += f"{blog['introduction']}\n\n"
    
    for section in blog['sections']:
        markdown_content += f"## {section['title']}\n\n"
        if section.get('image'):
            markdown_content += image_generator.format_image_markdown(section['image'])
        markdown_content += f"{section['content']}\n\n"
        if section.get('code_example'):
            markdown_content += f"```python\n{section['code_example']}\n```\n\n"
        if section.get('quote'):
            markdown_content += f"> {section['quote']}\n\n"
    
    st.download_button(
        label="Download as Markdown",
        data=markdown_content,
        file_name="blog_post.md",
        mime="text/markdown"
    )