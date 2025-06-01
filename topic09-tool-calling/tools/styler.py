from typing import Dict

EMOJI_MAP: Dict[str, str] = {
    "Introduction": "🎯",
    "Understanding": "🧠",
    "Overview": "🔍",
    "Basics": "📚",
    "Components": "🔧",
    "Implementation": "⚙️",
    "Practices": "✨",
    "Applications": "💡",
    "Future": "🚀",
    "Comparison": "⚖️",
    "Cases": "📊",
    "Choice": "🎯",
    "Conclusion": "🎬"
}

def style_with_emojis(text: str, heading_level: int = 1) -> str:
    """Add emojis and style to text based on context."""
    # Find matching emoji
    emoji = "💫"  # Default emoji
    for key, value in EMOJI_MAP.items():
        if key in text:
            emoji = value
            break
    
    # Style based on heading level
    if heading_level == 1:
        return f"# {emoji} {text}"
    elif heading_level == 2:
        return f"## {emoji} {text}"
    else:
        return f"{emoji} {text}"

def format_code_block(code: str, language: str = "python") -> str:
    """Format code blocks with proper markdown syntax."""
    return f"```{language}\n{code}\n```"

def format_quote(quote: str) -> str:
    """Format quotes with proper markdown syntax and emoji."""
    return f"> 💭 {quote}"

def format_table(headers: list, rows: list) -> str:
    """Format data into a markdown table."""
    table = "| " + " | ".join(headers) + " |\n"
    table += "|" + "|".join(["---" for _ in headers]) + "|\n"
    
    for row in rows:
        table += "| " + " | ".join(str(cell) for cell in row) + " |\n"
    
    return table 