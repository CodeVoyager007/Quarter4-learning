from typing import Dict, List

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
    """Format code with proper markdown code block syntax."""
    return f"```{language}\n{code}\n```"

def format_quote(quote: str) -> str:
    """Format a quote with proper markdown blockquote syntax."""
    return f"> {quote}"

def format_table(headers: List[str], rows: List[List[str]]) -> str:
    """Format a table with proper markdown table syntax."""
    table_lines = []
    
    # Add headers
    table_lines.append("| " + " | ".join(headers) + " |")
    
    # Add separator
    table_lines.append("| " + " | ".join(["-" * len(header) for header in headers]) + " |")
    
    # Add rows
    for row in rows:
        table_lines.append("| " + " | ".join(row) + " |")
    
    return "\n".join(table_lines) 