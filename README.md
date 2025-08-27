# University Planner Agent

An intelligent university planning system that uses LangGraph to process user queries, gather data from multiple sources, and generate comprehensive university recommendations with knowledge graph visualization.

## Features

- **Intelligent Query Processing**: LLM-powered user preference extraction
- **Multi-Source Data Gathering**: University data, weather information, course details
- **AI-Powered Recommendations**: Comprehensive university recommendation reports
- **Knowledge Graph Generation**: Interactive visualization of relationships and data
- **Real-time Data Integration**: Tavily API for university and weather data
- **Streamlit Web Interface**: User-friendly interactive interface

## Project Structure

```
university planner/
├── src/
│   ├── agents/
│   │   ├── planner.py      # Extracts user preferences from queries
│   │   ├── gatherer.py     # Gathers data from various sources
│   │   ├── recommender.py  # Generates recommendation reports
│   │   └── formatter.py    # Creates knowledge graphs and final formatting
│   ├── graph/
│   │   ├── state.py        # Defines the shared state structure
│   │   ├── nodes.py        # Registers agent functions as nodes
│   │   ├── edges.py        # Defines the workflow connections
│   │   └── runner.py       # Custom runner for step-by-step execution
│   └── utils/
│       └── tools.py        # External API calls and data functions
├── data── ipeds_data.db       # Pre-converted IPEDS database
├── streamlit_app.py        # Main web interface
├── requirements.txt        # Python dependencies
└── data.json              # Generated knowledge graph (auto-created)
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the root directory:

```bash
# Required for LLM functionality
GROQ_API_KEY=your_groq_api_key_here

# Required for real-time data gathering
TAVILY_API_KEY=your_tavily_api_key_here
```

### 3. Data Sources

The system uses a **RAG (Retrieval-Augmented Generation)** approach combining:

- **IPEDS Database**: Structured university data (enrollment, tuition, acceptance rates)
- **Tavily Search API**: Real-time web search for additional context and current information
- **Weather Data**: Current weather conditions for university locations

This provides the best of both worlds - accurate structured data plus current real-time information!

### 4. API Keys

**Groq API Key**: 
- Sign up at [Groq](https://console.groq.com/)
- Get your API key from the console
- Add to `.env` file

**Tavily API Key**:
- Sign up at [Tavily](https://tavily.com/)
- Get your API key
- Add to `.env` file

## How to Use

1. **Start the Application**:
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Enter Your Query**: 
   - Example: "I want to study Computer Science in California with a high budget"
   - Example: "I'm looking for Mathematics programs in the United States"

3. **View Results**:
   - **Left Panel**: University recommendations and detailed report
   - **Right Panel**: Interactive knowledge graph visualization

## Data Sources

- **University Data**: College Scorecard API (with IPEDS fallback)
- **Weather Data**: OpenWeather One Call API 3.0
- **Course Information**: University website scraping (mock data)
- **Location Data**: Geocoding services

## Knowledge Graph Export

The system automatically generates and saves a knowledge graph to `data.json` containing:
- University entities and attributes
- Academic programs and majors
- Location and weather information
- Relationships between entities

## Troubleshooting

- **LLM Not Available**: If `GROQ_API_KEY` is not set, the system falls back to template-based responses
- **Weather Data**: Ensure `OPENWEATHER_API_KEY` is set for location-based weather information
- **IPEDS Data**: If `.accdb` files are not available, the system uses mock university data

## Current Status

✅ **Working Features**:
- Complete workflow from query to recommendation
- LLM-powered preference extraction using DeepSeek model
- Real IPEDS database integration with 7 universities
- Comprehensive recommendation reports (11,000+ characters)
- Interactive knowledge graph visualization
- Weather integration with OpenWeather API
- Streamlit interface with step-by-step progress tracking
- Automatic data export to `data.json`

✅ **Real Data Integration**:
- **Universities**: Harvard, MIT, Stanford, UC Berkeley, Columbia, UT Austin, Texas A&M
- **Data Sources**: Institution info, admissions, enrollment, tuition, room & board
- **States Covered**: California, Massachusetts, New York, Texas

The system is fully functional with real IPEDS data and ready to use! 🎓✨
