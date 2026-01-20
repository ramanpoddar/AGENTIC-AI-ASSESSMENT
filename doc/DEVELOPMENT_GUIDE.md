# Development Guide - Invoice Compliance & Validation System

## Table of Contents
1. [Project Structure](#project-structure)
2. [Coding Standards](#coding-standards)
3. [Development Workflow](#development-workflow)
4. [Adding New Features](#adding-new-features)
5. [Testing Guidelines](#testing-guidelines)
6. [Debugging Tips](#debugging-tips)
7. [Best Practices](#best-practices)

---

## Project Structure

### Directory Layout
```
AGENTIC AI ASSESSMENT/
├── agents/                    # Agent implementations
│   ├── __init__.py
│   ├── extractor_agent.py    # Invoice extraction
│   ├── validator_agent.py    # Validation routing
│   ├── resolver_agent.py     # Result aggregation
│   └── reporter_agent.py     # Report generation
├── tools/                     # Tool definitions
│   ├── __init__.py
│   ├── invoice_tools.py      # Invoice-specific tools
│   └── gst_tools.py          # GST/GSTIN validation tools
├── services/                  # Shared services
│   ├── __init__.py
│   └── state_store.py        # State management
├── llm/                       # LLM integration
│   ├── __init__.py
│   └── groq_llm.py           # Groq service
├── data/                      # Data directory
│   └── invoices/             # Sample invoices
├── doc/                       # Documentation
├── main.py                    # Entry point
├── groq_chat_client.py       # API test
├── requirements.txt           # Dependencies
└── .env                       # Configuration
```

### Module Responsibilities

| Module | Responsibility | Key Files |
|--------|-----------------|-----------|
| agents/ | Agent orchestration | *_agent.py |
| tools/ | Business logic tools | *_tools.py |
| services/ | Shared utilities | state_store.py |
| llm/ | LLM service integration | groq_llm.py |
| data/ | Data storage | invoice files |

---

## Coding Standards

### Python Style Guide
Follow PEP 8 conventions:

```python
# Imports: grouped and sorted
import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Union

# Constants: UPPER_CASE
INVOICE_PATTERN = r"^INV-\d{4}-\d{4}$"
MAX_RETRIES = 3

# Classes: PascalCase
class ExtractorAgent:
    pass

# Functions/Methods: snake_case
def validate_invoice_number():
    pass

# Variables: snake_case
processed_invoices = []

# Line length: Max 100 characters
# Indentation: 4 spaces
# Blank lines: 2 between classes, 1 between methods
```

### Docstring Format
Use Google-style docstrings:

```python
def validate_invoice_number(invoice_number: str) -> bool:
    """Validate invoice number format: INV-YYYY-NNNN.
    
    Checks if the provided invoice number matches the expected format
    using regex pattern matching.
    
    Args:
        invoice_number (str): The invoice number to validate.
        
    Returns:
        bool: True if valid format, False otherwise.
        
    Raises:
        ValueError: If invoice_number is not a string.
        
    Example:
        >>> validate_invoice_number("INV-2024-0001")
        True
        >>> validate_invoice_number("INV-24-1")
        False
    """
    if not isinstance(invoice_number, str):
        raise ValueError("invoice_number must be a string")
    
    return bool(re.match(r"^INV-\d{4}-\d{4}$", invoice_number))
```

### Type Hints
Always use type hints for function parameters and returns:

```python
from typing import Dict, List, Optional, Union, Any

def process_invoice(
    invoice_id: str,
    data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """Process a single invoice."""
    pass

def extract_invoices(file_path: str) -> Union[Dict, List]:
    """Extract invoice(s) from file."""
    pass
```

### Error Handling
Use specific exceptions and proper error messages:

```python
import logging

logger = logging.getLogger(__name__)

def load_invoice(file_path: str) -> dict:
    """Load invoice from file with error handling."""
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        logger.info(f"Successfully loaded invoice from {file_path}")
        return data
    except FileNotFoundError:
        logger.error(f"Invoice file not found: {file_path}")
        raise FileNotFoundError(f"Cannot find invoice at {file_path}")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {file_path}: {str(e)}")
        raise ValueError(f"Invalid JSON format in {file_path}")
    except Exception as e:
        logger.error(f"Unexpected error loading {file_path}: {str(e)}")
        raise
```

---

## Development Workflow

### 1. Setup Development Environment
```bash
# Clone repository
git clone https://github.com/ramanpoddar/AGENTIC-AI-ASSESSMENT.git
cd AGENTIC-AI-ASSESSMENT

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or ./venv/Scripts/activate on Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "GROQ_API_KEY=your_key" > .env
```

### 2. Create Feature Branch
```bash
# Create new branch for feature
git checkout -b feature/new-validation-tool

# Or for fixes
git checkout -b fix/duplicate-detection-issue
```

### 3. Development
```bash
# Edit files
# Test changes
python main.py

# Run specific agent
python -c "from agents.validator_agent import create_validator_agent; ..."
```

### 4. Commit Changes
```bash
# Stage changes
git add .

# Commit with clear message
git commit -m "feat: Add new GSTIN validation tool"
# or
git commit -m "fix: Resolve duplicate detection bug"

# Push branch
git push origin feature/new-validation-tool
```

### 5. Create Pull Request
- Go to GitHub
- Create PR with description
- Request review
- Merge after approval

---

## Adding New Features

### Example: Add New Invoice Validation Tool

#### Step 1: Create Tool Function
**File:** `tools/invoice_tools.py`

```python
@tool
def validate_invoice_date(invoice_date: str) -> bool:
    """Validate invoice date is not in future.
    
    Args:
        invoice_date (str): Invoice date in YYYY-MM-DD format.
        
    Returns:
        bool: True if valid (not in future), False otherwise.
    """
    from datetime import datetime
    
    try:
        invoice_dt = datetime.strptime(invoice_date, "%Y-%m-%d")
        today = datetime.now()
        return invoice_dt <= today
    except ValueError:
        return False
```

#### Step 2: Register Tool in Validator Agent
**File:** `agents/validator_agent.py`

```python
from tools.invoice_tools import (
    validate_invoice_number,
    check_duplicate_invoice,
    validate_invoice_date  # Add import
)

def create_validator_agent():
    class ValidatorAgent:
        def run(self, input_text):
            input_lower = input_text.lower()
            
            # Existing validations...
            
            # Add new validation
            elif "invoice date" in input_lower or "validate date" in input_lower:
                date = input_text.split()[-1]
                return validate_invoice_date.invoke({"invoice_date": date})
            
            return False
    
    return ValidatorAgent()
```

#### Step 3: Use in Main
**File:** `main.py`

```python
# In the validation loop
if "invoice_date" in invoice:
    results.append({
        "check": "Invoice Date Valid",
        "status": validator.run(
            f"Validate invoice date {invoice['invoice_date']}"
        )
    })
```

#### Step 4: Test
```bash
python main.py
# Check output includes new validation
```

---

## Testing Guidelines

### Unit Testing Example

**File:** `test_invoice_tools.py`

```python
import unittest
from tools.invoice_tools import validate_invoice_number

class TestInvoiceTools(unittest.TestCase):
    
    def test_valid_invoice_number(self):
        """Test valid invoice number format."""
        result = validate_invoice_number.invoke({
            "invoice_number": "INV-2024-0001"
        })
        self.assertTrue(result)
    
    def test_invalid_invoice_number_format(self):
        """Test invalid format."""
        result = validate_invoice_number.invoke({
            "invoice_number": "INV-24-1"
        })
        self.assertFalse(result)
    
    def test_invalid_invoice_number_case(self):
        """Test case sensitivity."""
        result = validate_invoice_number.invoke({
            "invoice_number": "inv-2024-0001"
        })
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
```

### Run Tests
```bash
python -m unittest test_invoice_tools.py
```

### Integration Testing
```bash
# Test full workflow
python main.py

# Test specific agent
python -c "
from agents.extractor_agent import create_extractor_agent
agent = create_extractor_agent()
result = agent.run('Extract invoice from data/invoices/invoice_001.json')
print(f'Extracted {len(result)} invoices')
"
```

---

## Debugging Tips

### 1. Add Print Statements
```python
def validate_invoice_number(invoice_number: str) -> bool:
    print(f"DEBUG: Validating invoice: {invoice_number}")
    pattern = r"^INV-\d{4}-\d{4}$"
    result = bool(re.match(pattern, invoice_number))
    print(f"DEBUG: Validation result: {result}")
    return result
```

### 2. Use Logging
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def process_invoice(invoice):
    logger.debug(f"Processing invoice: {invoice.get('invoice_id')}")
    logger.info("Starting validation")
    logger.warning("Duplicate invoice detected")
    logger.error("Failed to process invoice")
```

### 3. Use Debugger
```python
import pdb

def complex_function(data):
    pdb.set_trace()  # Execution pauses here
    # Now you can inspect variables, step through code
    result = process(data)
    return result
```

### 4. Test Individual Components
```bash
# Test agent
python -c "from agents.extractor_agent import create_extractor_agent; print(create_extractor_agent())"

# Test tool
python -c "from tools.invoice_tools import validate_invoice_number; print(validate_invoice_number.invoke({'invoice_number': 'INV-2024-0001'}))"

# Test service
python -c "from services.state_store import StateStore; s = StateStore(); print(s.is_duplicate('INV-2024-0001'))"
```

### 5. Check Environment
```bash
# Verify API key
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GROQ_API_KEY'))"

# Check imports
python -c "import groq, langchain, pydantic; print('OK')"

# Verify data files
ls -la data/invoices/
```

---

## Best Practices

### ✅ DO

- **Use type hints** for all functions
- **Write docstrings** for all functions and classes
- **Handle exceptions** explicitly
- **Use logging** for debugging
- **Keep functions small** and focused
- **Follow PEP 8** conventions
- **Test before committing**
- **Use descriptive variable names**
- **Comment complex logic**
- **Keep dependencies updated**

### ❌ DON'T

- **Don't use bare `except:`** - be specific
- **Don't have functions > 50 lines** - break them up
- **Don't commit `.env` file** - use `.gitignore`
- **Don't use `print()` for logging** - use logging module
- **Don't hardcode values** - use constants/config
- **Don't ignore warnings** - fix them
- **Don't commit commented code** - delete or document
- **Don't make massive commits** - keep them focused
- **Don't skip documentation** - write clear docstrings
- **Don't test manually only** - automate tests

### Code Review Checklist

Before pushing code:
- ✅ Follows PEP 8 style guide
- ✅ Has type hints
- ✅ Has docstrings
- ✅ No unused imports
- ✅ Proper error handling
- ✅ Uses logging appropriately
- ✅ Passes all tests
- ✅ No hardcoded values
- ✅ No .env or secrets
- ✅ Clear commit message

---

## Common Patterns

### Agent Pattern
```python
def create_custom_agent():
    """Create an agent for specific task."""
    class CustomAgent:
        def __init__(self):
            self.state = {}
        
        def run(self, input_text):
            """Execute agent logic."""
            # Parse input
            # Execute business logic
            # Return result
            return result
    
    return CustomAgent()
```

### Tool Pattern
```python
from langchain.tools import tool

@tool
def my_custom_tool(param: str) -> bool:
    """Tool description.
    
    Args:
        param: Input parameter
        
    Returns:
        bool: Result
    """
    # Implementation
    return result

# Usage
result = my_custom_tool.invoke({"param": "value"})
```

### Service Pattern
```python
class MyService:
    """Shared service for common functionality."""
    
    def __init__(self):
        self.state = {}
    
    def method_one(self, param):
        """Do something."""
        pass
    
    def method_two(self, param):
        """Do something else."""
        pass

# Usage
service = MyService()
service.method_one("value")
```

---

## Performance Tips

### Profile Code
```python
import cProfile
import pstats

cProfile.run('main()', 'output.prof')
stats = pstats.Stats('output.prof')
stats.sort_stats('cumulative')
stats.print_stats(10)
```

### Optimize Hot Paths
```python
# Slow: Regex compiled each time
for invoice in invoices:
    if re.match(r"^INV-\d{4}-\d{4}$", invoice['id']):
        pass

# Fast: Compile once
import re
pattern = re.compile(r"^INV-\d{4}-\d{4}$")
for invoice in invoices:
    if pattern.match(invoice['id']):
        pass
```

### Cache Results
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_vendor_info(vendor_id):
    # Expensive operation - cached
    return fetch_from_db(vendor_id)
```

---

## Resources

- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Real Python Best Practices](https://realpython.com/courses/)
- [Python Documentation](https://docs.python.org/3/)
- [LangChain Docs](https://python.langchain.com)
- [Groq API Docs](https://console.groq.com/docs)

---

*Development Guide Version: 1.0*
*Last Updated: January 2026*
