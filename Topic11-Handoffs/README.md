# Poetry Analysis System - OpenAI SDK Demo

## 📚 Overview

This project demonstrates core OpenAI SDK concepts including **Tool Calling** and **Agent Handoffs** through a poetry analysis system. The application uses a multi-agent architecture to classify and analyze different types of poetry.

## 🏗️ Architecture

### Core Concepts Demonstrated

1. **Tool Calling**: Agents can call specific tools for different tasks
2. **Agent Handoffs**: Orchestration between specialized agents
3. **Fallback Systems**: Reliability when APIs are unavailable

## 🤖 Agent System

### Base Agent Class

We created a base `PoetryAgent` class that serves as the foundation for all agents. This class includes:

**Key Components:**
- **Agent Identity**: Each agent has a unique name for identification
- **Tool Registry**: A list of available tools the agent can call

**Why We Used This:**
- **Reusability**: All agents inherit from the same base class
- **Consistency**: Ensures all agents follow the same patterns
- **Extensibility**: Easy to add new agents or tools

### Tool Calling Implementation

We implemented a tool calling system that allows agents to execute specific functions. The system includes:

**Available Tools:**
- **Poem Analysis**: Generates detailed literary analysis
- **Poem Classification**: Determines poetry type using AI scoring

**Why We Used This:**
- **Modularity**: Each tool has a single, well-defined purpose
- **Flexibility**: Agents can call different tools as needed
- **OpenAI SDK Pattern**: Follows the standard tool calling approach

## 🎭 Specialized Agents

### 1. Poet Agent

**Purpose**: Generates sample poems for demonstration
**Responsibility**: Single responsibility principle - only generates content

**Why We Used This:**
- **Demonstration**: Provides ready-to-use examples
- **Single Responsibility**: Shows clean agent design
- **User Experience**: Gives users starting points

### 2. Triage Agent

**Purpose**: Orchestrates handoffs between specialized analysts
**Key Function**: Coordinates the entire analysis process

**Handoffs Process:**
1. **Classification**: Determines poetry type using scoring
2. **Agent Selection**: Chooses appropriate specialized analyst
3. **Analysis**: Delegates to specialized analyst
4. **History Tracking**: Records each step in conversation

**Why We Used This:**
- **Orchestration**: Demonstrates agent coordination
- **Decision Making**: Shows intelligent routing
- **Scalability**: Easy to add new poetry types

### 3. Specialized Analysts

**Purpose**: Provide specialized analysis for each poetry type

- **Lyric Analyst**: Analyzes personal, emotional poetry
- **Narrative Analyst**: Analyzes storytelling poetry
- **Dramatic Analyst**: Analyzes performance-oriented poetry

**Why We Used This:**
- **Specialization**: Each analyst focuses on specific poetry types
- **Accuracy**: Better analysis through focused expertise
- **Modularity**: Easy to add new specialized analysts

## 🧠 Classification System

### Poetry Type Detection

We implemented an AI-powered classification system that uses:

**Classification Indicators:**
- **Lyric Indicators**: Personal pronouns, emotions, feelings
- **Narrative Indicators**: Storytelling words, past tense, characters
- **Dramatic Indicators**: Performance words, dialogue, audience

**Scoring System:**
- **Word Matching**: Counts relevant words in the poem
- **Score Calculation**: Determines the most likely poetry type
- **Decision Making**: Returns the type with highest score

**Why We Used This:**
- **Accuracy**: Better classification through multiple indicators
- **Transparency**: Clear reasoning for classification decisions
- **Extensibility**: Easy to add new indicators or poetry types

## 🔧 Analysis System

### AI-Powered Analysis

We use Gemini API for generating detailed poetry analysis with:

**Analysis Features:**
- **Multi-Model Support**: Tries different models for reliability
- **Structured Prompts**: Consistent analysis format
- **Comprehensive Coverage**: Theme, emotions, devices, impact

**Model Selection Strategy:**
1. **Flash Models**: Faster, less quota intensive
2. **Pro Models**: Higher quality, more quota intensive
3. **Fallback**: Manual analysis when all models fail

**Why We Used This:**
- **Reliability**: Multiple fallback options
- **Cost Efficiency**: Uses cheaper models first
- **Quality**: Ensures analysis even when APIs fail

## 🎨 UI Components

### Environment Variables

We use environment variables for:
- **API Key Management**: Secure storage of API keys
- **Configuration**: Easy deployment across environments
- **Security**: Prevents hardcoding sensitive data

### Session State Management

We use Streamlit's session state for:
- **Agent Persistence**: Maintains agent instances across interactions
- **State Management**: Preserves user input and results
- **Performance**: Avoids recreating agents on each interaction

### UI Layout

We designed a modern dark theme interface with:
- **Header**: Project title and description
- **Sidebar**: Controls and agent status
- **Main Area**: Input and examples
- **Results**: Analysis display

**Why We Used This:**
- **User Experience**: Professional, modern interface
- **Accessibility**: Clear visual hierarchy
- **Functionality**: Easy to use and understand

## 🚀 Usage Examples

### Example 1: Lyric Poetry
**Input**: "I feel the weight of sorrow in my heart"
**Classification**: Lyric (high score on personal emotion indicators)
**Analysis**: Detailed emotional and personal interpretation

### Example 2: Narrative Poetry
**Input**: "Once upon a time in lands afar"
**Classification**: Narrative (high score on storytelling indicators)
**Analysis**: Detailed story and character interpretation

### Example 3: Dramatic Poetry
**Input**: '"Speak to the audience," the director cried'
**Classification**: Dramatic (high score on performance indicators)
**Analysis**: Detailed performance and dialogue interpretation

## 🔄 Handoffs Flow

1. **User Input**: Poem entered in UI
2. **Triage Agent**: Receives poem and calls classification tool
3. **Classification**: Determines poetry type using scoring system
4. **Agent Selection**: Chooses appropriate specialized analyst
5. **Handoff**: Passes poem to selected analyst
6. **Analysis**: Calls analysis tool on specialized analyst
7. **Result**: Returns detailed analysis to user

**Why This Flow:**
- **Efficiency**: Each agent focuses on its specialty
- **Accuracy**: Specialized analysis for each poetry type
- **Scalability**: Easy to add new poetry types or analysts

## 🛠️ Technical Implementation

### Dependencies

We chose these technologies for specific reasons:

- **Streamlit**: Rapid web UI development with Python
- **Google Generative AI**: Reliable text generation with fallback options
- **Python-dotenv**: Secure environment variable management

### Key Functions

- **Main Function**: Application entry point and UI setup
- **Process Poem**: Core handoffs logic and coordination
- **Call Tool**: Tool calling implementation

### Error Handling

We implemented comprehensive error handling for:
- **API Failures**: Automatic fallback to manual analysis
- **Model Unavailable**: Tries multiple models in sequence
- **Rate Limits**: Implements retry logic with delays

**Why This Approach:**
- **Reliability**: System works even when external APIs fail
- **User Experience**: No broken functionality
- **Robustness**: Handles various failure scenarios

## 📊 Performance Features

- **Multi-Model Fallback**: Ensures reliability
- **Session Persistence**: Maintains state across interactions
- **Responsive UI**: Dark theme with modern styling
- **Real-time Status**: Agent status indicators

## 🎯 Learning Objectives

This project demonstrates:
1. **Tool Calling**: How agents can call specific functions
2. **Agent Handoffs**: Orchestrating multiple specialized agents
3. **Fallback Systems**: Ensuring reliability when APIs fail
4. **Modern UI**: Professional web interface with Streamlit

## 🚀 Running the Application

```bash
# Install dependencies
uv add -r requirements.txt 

# Run the application
streamlit run main.py
```

The application will be available at `http://localhost:8501`
