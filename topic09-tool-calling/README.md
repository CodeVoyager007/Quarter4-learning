# 🎯 SyntaxCrafter: The Blog Smith

An AI-powered blog generation tool that creates structured, engaging blog posts from any topic. No external AI APIs required!

## 🎯 Assignment Overview: Understanding Tool Calling / Function Calling

This project demonstrates the practical implementation of tool calling and function calling concepts through an AI-powered blog generation system. It showcases how different tools and functions can be chained together to create a powerful content generation application.

## 🔑 Key Concepts Demonstrated

### 1. Tool Calling Implementation
- **API Integration**: Demonstrates how to properly call and handle external APIs (Wikipedia, DBpedia)
- **Error Handling**: Shows robust error handling in tool calls
- **Asynchronous Operations**: Uses async/await for efficient API calls
- **Tool Chaining**: Combines multiple tools for enhanced content generation

### 2. Function Calling Features
- **Domain Detection**: Smart function calls to identify content domain
- **Content Analysis**: Automated analysis of topic requirements
- **Template Selection**: Dynamic selection of content templates
- **Data Enrichment**: Intelligent gathering and combining of information

### 3. Real-World Application
- Generates professional blog content for any topic
- Handles multiple domains (Technology, Medical, Science, etc.)
- Provides structured, well-formatted output
- Implements proper error recovery

## 🚀 Features

- 📝 Automatically generates well-structured blog posts
- 💡 Smart topic analysis for content customization
- 💻 Adds relevant code examples for technical topics
- 📊 Creates comparison tables when needed
- 🌐 Real Wikipedia content integration
- 🖼️ Topic images when available
- 💭 Inspirational quotes
- 🎨 Beautiful formatting with emojis and markdown
- **Multi-Domain Support**: Generate blogs about:
  - Technology and Programming
  - Medical and Healthcare
  - Science and Research
  - Fitness and Wellness
  - Finance and Investment
  - Business and Entrepreneurship
  - Arts and Creativity
  - Education and Learning
  - Lifestyle and Personal Development
  - Environment and Sustainability

- **Smart Content Generation**:
  - Domain-specific formatting
  - Appropriate content structure
  - Relevant examples and citations
  - Professional styling

- **Modern UI/UX**:
  - Professional dark theme
  - Responsive design
  - Interactive elements
  - Clear visual hierarchy

## 🛠️ Technical Implementation

### Dependencies
```
streamlit==1.32.0
httpx==0.27.0
```

### Project Structure
```
📂 syntaxcrafter/
├── app.py                  # Streamlit interface
├── agent.py               # Blog generation logic
├── tools/
│   ├── outline.py        # Blog outline generator
│   ├── sections.py       # Section content generator
│   └── styler.py         # Formatting and styling
├── requirements.txt      # Project dependencies
└── README.md             # You are here!
```

## 🎯 How It Demonstrates Tool Calling

1. **API Tool Calls**
   - Wikipedia API for main content
   - DBpedia API for additional context
   - Error handling and fallback mechanisms

2. **Content Generation Tools**
   - Topic analysis function calls
   - Template selection tools
   - Content structuring utilities

3. **Formatting Tools**
   - Style application functions
   - Layout management tools
   - Theme handling utilities

## 🚀 Getting Started

1. Clone this repository:
```bash
git clone https://github.com/yourusername/syntaxcrafter.git
cd syntaxcrafter
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the app:
```bash
streamlit run app.py
```

## 💡 Usage Example

1. Enter any topic in the input field
2. The system will:
   - Analyze the topic domain
   - Gather relevant information
   - Generate structured content
   - Apply appropriate styling
   - Provide downloadable output

## 🔍 Key Learning Outcomes

1. **Tool Calling Mastery**
   - Understanding API integration
   - Handling asynchronous operations
   - Managing tool dependencies

2. **Function Calling Expertise**
   - Implementing chainable functions
   - Building robust error handling
   - Creating reusable tools

3. **Practical Application**
   - Real-world implementation
   - Production-ready code
   - User-focused design

## 📚 Related Blog Posts

- [Tool Calling in Agentic AI: Turning Language into Action](https://mughalsyntax.hashnode.dev/tool-calling-in-agentic-ai-turning-language-into-action)


