import streamlit as st
import asyncio
from agent import BlogAgent
from tools.image_generator import ImageGenerator

# Set page config
st.set_page_config(
    page_title="SyntaxCrafter: The Blog Smith",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stTextInput > div > div > input {
        padding: 1rem;
    }
    .blog-section {
        margin: 2rem 0;
        padding: 1rem;
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0.05);
    }
    .section-image {
        width: 100%;
        border-radius: 10px;
        margin: 1rem 0;
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