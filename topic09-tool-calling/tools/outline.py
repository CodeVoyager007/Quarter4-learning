from typing import List

def generate_outline(topic: str) -> List[str]:
    """Generate a blog outline based on the topic."""
    # Basic outline structure
    outline = ["Introduction"]
    
    # Add topic-specific sections
    keywords = topic.lower().split()
    
    if any(word in keywords for word in ["tool", "function", "api"]):
        outline.extend([
            "Understanding the Basics",
            "Key Components",
            "Implementation Details",
            "Best Practices"
        ])
    elif any(word in keywords for word in ["compare", "vs", "versus"]):
        outline.extend([
            "Overview",
            "Detailed Comparison",
            "Use Cases",
            "Making the Right Choice"
        ])
    else:
        outline.extend([
            "Background",
            "Main Concepts",
            "Practical Applications",
            "Future Perspectives"
        ])
    
    outline.append("Conclusion")
    return outline 