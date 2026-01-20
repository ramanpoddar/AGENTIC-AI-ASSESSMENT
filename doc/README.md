# Invoice Compliance & Validation System - Documentation

This folder contains comprehensive documentation for the Invoice Compliance & Validation System project.

## Documents

### 1. System Architecture Document
**File:** `System_Architecture_Document.docx`

A detailed Word document covering:
- Executive summary and key objectives
- System overview and characteristics
- High-level architecture diagram
- Complete component descriptions
- Data flow workflows
- Technology stack and dependencies
- Module structure and organization
- Agent architecture and responsibilities
- Tools and utilities documentation
- State management system
- API integration details
- Deployment considerations and future enhancements

---

## Quick Reference

### Project Structure
```
AGENTIC AI ASSESSMENT/
├── agents/
│   ├── extractor_agent.py
│   ├── validator_agent.py
│   ├── resolver_agent.py
│   └── reporter_agent.py
├── tools/
│   ├── invoice_tools.py
│   └── gst_tools.py
├── services/
│   └── state_store.py
├── llm/
│   └── groq_llm.py
├── data/
│   └── invoices/
│       └── invoice_001.json
├── doc/
│   ├── README.md (this file)
│   ├── System_Architecture_Document.docx
│   ├── API_REFERENCE.md
│   ├── INSTALLATION_GUIDE.md
│   └── DEVELOPMENT_GUIDE.md
├── main.py
├── groq_chat_client.py
└── requirements.txt
```

### Key Technologies
- **Python 3.8+**
- **Groq API** (Llama-3.3-70B model)
- **LangChain** (Agentic AI framework)
- **LangChain-Groq** (API integration)
- **Pydantic** (Data validation)
- **python-dotenv** (Environment management)

### Core Components
1. **Extractor Agent** - Invoice data extraction
2. **Validator Agent** - Multi-criteria validation
3. **Resolver Agent** - Result aggregation
4. **Reporter Agent** - Report generation

### Main Validations
- Invoice ID format (INV-YYYY-NNNN)
- Duplicate invoice detection
- Vendor information validation
- Total amount validation
- GSTIN format validation
- GSTIN active status verification
- GSTIN state code matching

---

## Setup & Usage

### Installation
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your Groq API key
echo GROQ_API_KEY=your_api_key_here > .env
```

### Running the System
```bash
python main.py
```

---

## Document Guide

| Document | Purpose | Audience |
|----------|---------|----------|
| System_Architecture_Document.docx | Complete architectural overview | Architects, Leads, Developers |
| API_REFERENCE.md | Tool and function documentation | Developers |
| INSTALLATION_GUIDE.md | Setup and deployment steps | DevOps, Developers |
| DEVELOPMENT_GUIDE.md | Development guidelines | Developers |

---

## Getting Started

1. **Read** the System_Architecture_Document.docx for overall understanding
2. **Follow** INSTALLATION_GUIDE.md to set up the environment
3. **Review** API_REFERENCE.md for available tools
4. **Check** DEVELOPMENT_GUIDE.md for coding standards

---

## Support

For detailed information on any component, refer to:
- Architecture Document: High-level design decisions
- API Reference: Function signatures and parameters
- Installation Guide: Environment setup
- Development Guide: Coding practices and standards

---

*Last Updated: January 2026*
*System Version: 1.0*
