import streamlit as st

def load_css(file_path):
    """Loads a CSS file and injects it into the Streamlit app."""
    try:
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found at {file_path}")

def get_footer():
    """Returns the HTML for the app footer."""
    footer = """
    <div style="text-align: center; padding: 1rem; position: fixed; bottom: 0; width: 100%; background-color: #0D0D0D; color: #F8F8F2;">
        Made with <span style="color: #B3001B;">&#10084;</span> by Ayesha Mughal
    </div>
    """
    return footer 