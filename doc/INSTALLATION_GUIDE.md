# Installation Guide - Invoice Compliance & Validation System

## Prerequisites

Before installing the Invoice Compliance & Validation System, ensure you have:

- **Python 3.8 or higher** - [Download here](https://www.python.org/downloads/)
- **pip** - Package manager (usually comes with Python)
- **Virtual Environment** - For dependency isolation (recommended)
- **Groq API Key** - [Get API key](https://console.groq.com/keys)
- **Git** (optional) - For cloning the repository
- **Text Editor/IDE** - VS Code, PyCharm, etc.

### System Requirements

| Component | Requirement |
|-----------|-------------|
| OS | Windows, macOS, or Linux |
| Python | 3.8+ |
| RAM | 2GB minimum |
| Disk Space | 500MB+ |
| Internet | Required (for Groq API calls) |

---

## Step-by-Step Installation

### Step 1: Get the Project

#### Option A: Clone from Git
```bash
git clone https://github.com/ramanpoddar/AGENTIC-AI-ASSESSMENT.git
cd AGENTIC-AI-ASSESSMENT
```

#### Option B: Download ZIP
1. Download the project as ZIP
2. Extract to your desired location
3. Navigate to the project folder

### Step 2: Create Python Virtual Environment

#### On Windows (PowerShell):
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### On Windows (Command Prompt):
```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate.bat
```

#### On macOS/Linux (Bash/Zsh):
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

**Verify Activation:**
You should see `(venv)` prefix in your terminal prompt.

```
(venv) C:\path\to\project>  # Windows
(venv) ~/path/to/project$   # macOS/Linux
```

### Step 3: Upgrade pip

```bash
# Windows
python -m pip install --upgrade pip

# macOS/Linux
python3 -m pip install --upgrade pip
```

### Step 4: Install Dependencies

```bash
# Install from requirements.txt
pip install -r requirements.txt
```

**What gets installed:**
```
groq==0.4.1+              # Groq API client
python-dotenv==1.0.0+     # Environment variable management
langchain==0.1.0+         # Agentic AI framework
langchain-groq==0.1.0+    # LangChain-Groq integration
pydantic==2.0.0+          # Data validation
```

**Installation Progress:**
```
Collecting groq
  Downloading groq-0.4.1.tar.gz
  Installing collected packages: groq, python-dotenv, langchain, langchain-groq, pydantic
Successfully installed groq-0.4.1 python-dotenv-1.0.0 langchain-0.1.0 langchain-groq-0.1.0 pydantic-2.0.0
```

### Step 5: Configure Environment Variables

#### Create .env File

In the project root directory, create a file named `.env`:

```bash
# Windows (PowerShell)
echo "GROQ_API_KEY=your_api_key_here" > .env

# macOS/Linux (Bash)
echo "GROQ_API_KEY=your_api_key_here" > .env
```

#### Edit .env File

Replace `your_api_key_here` with your actual Groq API key:

```
GROQ_API_KEY=gsk_abc123def456ghi789jkl...
```

**Obtaining Groq API Key:**
1. Visit [Groq Console](https://console.groq.com)
2. Sign up or log in
3. Go to API Keys section
4. Create new API key
5. Copy the key
6. Paste into .env file

**Security Note:**
⚠️ Never commit `.env` file to version control!
✓ Add `.env` to `.gitignore`

### Step 6: Verify Installation

#### Test Python Environment
```bash
python --version
# Should output: Python 3.8.x or higher
```

#### Test Groq Connection
```bash
python groq_chat_client.py
```

**Expected Output:**
```
API key working!
```

If you get an error:
- Check if API key is correct in .env
- Verify internet connection
- Ensure .env file is in project root

#### Test Import Dependencies
```bash
python -c "import groq, langchain, pydantic; print('All imports successful!')"
```

### Step 7: Verify Project Structure

```
AGENTIC AI ASSESSMENT/
├── venv/                          # Virtual environment (created in Step 2)
├── agents/
│   ├── __init__.py
│   ├── extractor_agent.py
│   ├── validator_agent.py
│   ├── resolver_agent.py
│   └── reporter_agent.py
├── tools/
│   ├── __init__.py
│   ├── invoice_tools.py
│   └── gst_tools.py
├── services/
│   ├── __init__.py
│   └── state_store.py
├── llm/
│   ├── __init__.py
│   └── groq_llm.py
├── data/
│   └── invoices/
│       └── invoice_001.json
├── doc/
│   ├── README.md
│   ├── System_Architecture_Document.docx
│   ├── API_REFERENCE.md
│   ├── INSTALLATION_GUIDE.md
│   └── DEVELOPMENT_GUIDE.md
├── .env                           # Created in Step 5
├── .gitignore
├── main.py
├── groq_chat_client.py
└── requirements.txt
```

---

## Running the Application

### Basic Run
```bash
# Ensure virtual environment is activated
python main.py
```

**Expected Output:**
```
===== COMPLIANCE REPORT =====
Invoice ID     : INV-2024-0002N
Vendor         : TechSoft Solutions Private Limited
Date           : 2024-09-15
Total          : 590000

Final Status   : PASS
Confidence     : 100.0%

[SUCCESS] All checks passed!
```

### Run with Logging
Create `main_with_logging.py` for debugging:

```python
import logging
from agents.extractor_agent import create_extractor_agent
from agents.validator_agent import create_validator_agent
from agents.resolver_agent import resolve_results
from agents.reporter_agent import generate_report

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

extractor = create_extractor_agent()
validator = create_validator_agent()

logger.info("Starting invoice processing...")

invoices = extractor.run("Extract invoice from data/invoices/invoice_001.json")
logger.info(f"Extracted {len(invoices)} invoices")

for invoice in invoices:
    results = []
    
    if "invoice_id" in invoice:
        logger.info(f"Validating invoice: {invoice['invoice_id']}")
        results.append({
            "check": "Invoice ID Format",
            "status": validator.run(f"Validate invoice number {invoice['invoice_id']}")
        })
    
    resolution = resolve_results(results)
    generate_report(invoice, resolution)
```

---

## Troubleshooting

### Issue 1: "Command not found: python"

**Solution:**
- Add Python to PATH environment variable
- Restart terminal/IDE
- Use `python3` on macOS/Linux if `python` doesn't work

### Issue 2: "ModuleNotFoundError: No module named 'groq'"

**Solution:**
```bash
# Verify virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 3: "GROQ_API_KEY not found"

**Solution:**
- Verify .env file exists in project root
- Check .env file contains correct API key format
- Ensure no extra spaces around equals sign
- Restart Python after creating .env

### Issue 4: "API key working! not showing"

**Solution:**
- Check internet connection
- Verify API key is valid
- Try generating new API key from Groq console
- Check firewall/proxy settings

### Issue 5: "ModuleNotFoundError: No module named 'dotenv'"

**Solution:**
```bash
pip install python-dotenv
```

### Issue 6: Virtual Environment Not Activating

**Windows:**
```powershell
# Try this if Activate.ps1 fails
venv\Scripts\activate.bat

# Or enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**macOS/Linux:**
```bash
# Try explicit python path
./venv/bin/python -c "import sys; print(sys.executable)"
```

---

## Deactivating Virtual Environment

When you're done working:

```bash
# All platforms
deactivate
```

The `(venv)` prefix will disappear from your prompt.

---

## Updating Dependencies

To update all packages to latest versions:

```bash
pip install --upgrade -r requirements.txt
```

To update a specific package:

```bash
pip install --upgrade groq
```

---

## Next Steps

1. ✅ Installation complete!
2. 📖 Read [README.md](README.md) for project overview
3. 🔍 Check [API_REFERENCE.md](API_REFERENCE.md) for available tools
4. 👨‍💻 Review [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md) for coding standards
5. 🏗️ Study [System_Architecture_Document.docx](System_Architecture_Document.docx) for architecture details

---

## Additional Resources

- [Groq Documentation](https://console.groq.com/docs)
- [LangChain Documentation](https://python.langchain.com)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [pip Documentation](https://pip.pypa.io/en/latest/)

---

## Support

If you encounter any issues:
1. Check the Troubleshooting section above
2. Review error messages carefully
3. Verify all prerequisites are installed
4. Check documentation files in `doc/` folder
5. Review logs for detailed error information

---

*Installation Guide Version: 1.0*
*Last Updated: January 2026*
