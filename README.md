# Module Extraction AI Agent for Product Documentation

A full-stack Generative AI application that extracts structured product modules and submodules from SaaS product documentation. Built for Pulsegen.io, a GenAI-first startup focused on revolutionizing Product Management for global SaaS companies.

APPLICATION LINK- https://cherrys0710-pulsegen-task-streamlit-app-fsuc4m.streamlit.app/

## Problem Statement

Product Managers often need to quickly understand the structure and capabilities of SaaS products by analyzing their documentation. Manually extracting modules, submodules, and their relationships is time-consuming and error-prone. This tool automates that process using AI to infer product structure from documentation.

## Why This Matters for Product Management

- **Speed**: Instantly extract product structure from documentation instead of hours of manual analysis
- **Consistency**: AI-driven extraction ensures consistent module identification and naming
- **Scalability**: Analyze multiple documentation sources simultaneously
- **Intelligence**: LLM reasoning identifies logical groupings that might be missed in manual review
- **Structured Output**: Machine-readable JSON format enables further analysis and integration

## System Architecture

### Frontend (React + Vite)
- **Location**: `frontend/`
- **Port**: 3000
- **Features**:
  - Multi-URL input with validation
  - Real-time extraction status
  - Structured module display with descriptions and submodules
  - JSON export functionality

### Backend (FastAPI)
- **Location**: `backend/`
- **Port**: 8000
- **API Endpoint**: `POST /extract`
- **Services**:
  - **Crawler**: Crawls documentation sites, extracts clean text, handles internal links
  - **Extractor**: Uses LLM to infer modules and submodules from content

### Data Flow
1. User submits documentation URLs via frontend
2. Backend crawls each URL, extracting clean text content
3. Content is processed and sent to LLM with structured prompt
4. LLM returns JSON with modules, descriptions, and submodules
5. Results displayed in frontend with copy-to-clipboard functionality

## AI Approach

### LLM Usage
- **Model**: Configurable (default: `gpt-4o-mini`)
- **Temperature**: 0.3 (low for consistency)
- **Prompt Engineering**:
  - Explicit JSON structure requirements
  - PM-focused language and reasoning
  - Anti-hallucination instructions
  - Content-based extraction only

### Content Processing
- **Crawling**: Respects robots.txt, limits depth and pages
- **Cleaning**: Removes navigation, scripts, styles, headers/footers
- **Truncation**: Token-aware content limits to stay within API constraints

## Assumptions and Limitations

### Assumptions
- Documentation is publicly accessible (no authentication required)
- Documentation follows standard web structure (HTML)
- LLM has sufficient context to infer module structure
- Documentation URLs are valid and reachable

### Limitations
- **Authentication**: Cannot crawl protected documentation
- **Scale**: Limited to ~50 pages per URL to manage costs and time
- **Language**: Optimized for English documentation
- **Structure**: Relies on LLM inference - may miss subtle relationships
- **Rate Limits**: Subject to LLM API rate limits
- **Content Quality**: Output quality depends on documentation clarity

## Prerequisites

- Python 3.10+
- Node.js 18+
- OpenAI API key (or compatible API)

## Installation

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend
npm install
```

### Environment Configuration

1. Copy `.env.example` to `.env` in the project root:
```bash
cp .env.example .env
```

2. Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-key-here
```

## Running Locally

### Quick Start (Recommended)

Use the provided startup scripts:

**Terminal 1 - Backend:**
```bash
./start-backend.sh
```

**Terminal 2 - Frontend:**
```bash
./start-frontend.sh
```

### Manual Start

**Start Backend:**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend will run on `http://localhost:8000`

**Start Frontend:**

```bash
cd frontend
npm install  # First time only
npm run dev
```

Frontend will run on `http://localhost:3000`

### Important Notes

1. **Both servers must be running** - The frontend needs the backend API to function
2. **Environment Setup** - Make sure you have a `.env` file with your `OPENAI_API_KEY`:
   ```bash
   cp .env.example .env
   # Edit .env and add your API key
   ```
3. **Access the app** - Open `http://localhost:3000` in your browser once both servers are running

### Usage

1. Open `http://localhost:3000` in your browser
2. Enter one or more documentation URLs
3. Click "Extract Modules"
4. View extracted modules, descriptions, and submodules
5. Copy JSON to clipboard if needed

## Example Output

```json
[
  {
    "module": "User Management",
    "description": "Core functionality for managing user accounts, authentication, and access control",
    "submodules": {
      "Authentication": "User login, signup, and session management",
      "User Profiles": "User information, preferences, and settings",
      "Access Control": "Role-based permissions and security policies"
    }
  },
  {
    "module": "Analytics & Reporting",
    "description": "Tools for tracking usage, generating reports, and analyzing product metrics",
    "submodules": {
      "Usage Analytics": "Track feature usage and user engagement",
      "Custom Reports": "Create and schedule custom reports",
      "Data Export": "Export analytics data in various formats"
    }
  }
]
```

## Project Structure

```
pulsegen.io/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── services/
│   │   ├── crawler.py          # Documentation crawling logic
│   │   └── extractor.py        # LLM-based module extraction
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main application component
│   │   ├── components/
│   │   │   ├── URLInput.jsx    # URL input form
│   │   │   └── ResultsDisplay.jsx  # Results display
│   │   └── main.jsx            # Entry point
│   ├── package.json
│   └── vite.config.js
├── .env.example                # Environment template
├── .gitignore
└── README.md
```

## Code Quality Principles

- **Modularity**: Clear separation between crawling, extraction, and API layers
- **Error Handling**: Graceful failures with informative error messages
- **Type Safety**: Pydantic models for request/response validation
- **Clean Code**: Well-named functions, minimal comments, single responsibility
- **Security**: No hardcoded secrets, environment variable usage

## Future Enhancements

- Support for authenticated documentation
- Caching of crawled content
- Batch processing for multiple products
- Export to various formats (CSV, Markdown)
- Module relationship visualization
- Confidence scores for extracted modules

## Alignment with Pulsegen Mission

This tool embodies Pulsegen's GenAI-first approach to Product Management:
- **Intelligence**: Uses AI to extract insights that would take hours manually
- **Practicality**: Solves a real PM pain point with a focused solution
- **Speed**: Enables rapid product analysis and competitive intelligence
- **Structure**: Provides machine-readable output for further analysis

## License

Internal tool for Pulsegen.io

