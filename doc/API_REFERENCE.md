# API Reference - Invoice Compliance & Validation System

## Overview
This document provides a complete reference for all agents, tools, and services available in the Invoice Compliance & Validation System.

---

## Table of Contents
1. [Agents](#agents)
2. [Tools](#tools)
3. [Services](#services)
4. [Data Models](#data-models)

---

## Agents

### 1. Extractor Agent
**Module:** `agents/extractor_agent.py`

Responsible for extracting invoice data from JSON files.

#### Function: `create_extractor_agent()`
```python
agent = create_extractor_agent()
```

**Returns:** ExtractorAgent instance

**Methods:**

#### `run(input_text: str) -> dict | list`
Extracts invoice data from a file path specified in input_text.

**Parameters:**
- `input_text` (str): Text containing file path (e.g., "Extract invoice from data/invoices/invoice_001.json")

**Returns:**
- dict | list: Invoice data from JSON file

**Example:**
```python
extractor = create_extractor_agent()
invoices = extractor.run("Extract invoice from data/invoices/invoice_001.json")
```

---

### 2. Validator Agent
**Module:** `agents/validator_agent.py`

Routes validation requests to appropriate validation tools.

#### Function: `create_validator_agent()`
```python
validator = create_validator_agent()
```

**Returns:** ValidatorAgent instance

**Methods:**

#### `run(input_text: str) -> bool | dict`
Routes validation based on input text keywords.

**Parameters:**
- `input_text` (str): Validation request (e.g., "Validate invoice number INV-2024-0001")

**Returns:**
- bool | dict: Validation result

**Supported Validations:**

| Keyword | Tool Used | Example Input |
|---------|-----------|---------------|
| "invoice number" | validate_invoice_number | "Validate invoice number INV-2024-0001" |
| "duplicate" | check_duplicate_invoice | "Check duplicate invoice INV-2024-0001" |
| "gstin format" OR "validate gstin" | validate_gstin_format | "Validate gstin 27AABCT1234F1ZP" |
| "gstin active" OR "verify gstin" | verify_gstin_active | "Verify gstin 27AABCT1234F1ZP" |
| "state match" OR "match gstin" | match_gstin_state | "Match gstin state 27 vendor state 27" |

**Example:**
```python
validator = create_validator_agent()
result = validator.run("Validate invoice number INV-2024-0001")  # Returns: True/False
```

---

### 3. Resolver Agent
**Module:** `agents/resolver_agent.py`

Aggregates validation results and computes final compliance status.

#### Function: `resolve_results(results: list) -> dict`

**Parameters:**
- `results` (list): List of validation result dictionaries

**Returns:** dict with keys:
- `final_status` (str): "PASS" or "FAIL"
- `confidence` (float): 0.0 to 1.0
- `failed_checks` (list): List of failed validation items

**Result Dictionary Format:**
```python
{
    "final_status": "PASS",           # or "FAIL"
    "confidence": 0.85,                # Percentage of passed checks
    "failed_checks": [                 # Only if failures exist
        {"check": "Invoice ID Format", "status": False},
        {"check": "Duplicate Invoice", "status": False}
    ]
}
```

**Example:**
```python
results = [
    {"check": "Invoice ID Format", "status": True},
    {"check": "Duplicate Invoice", "status": True},
    {"check": "Vendor Validation", "status": False}
]
resolution = resolve_results(results)
# Returns: {"final_status": "FAIL", "confidence": 0.67, "failed_checks": [...]}
```

---

### 4. Reporter Agent
**Module:** `agents/reporter_agent.py`

Generates human-readable compliance reports.

#### Function: `generate_report(invoice: dict, resolution: dict) -> None`

**Parameters:**
- `invoice` (dict): Invoice data dictionary
- `resolution` (dict): Resolution dictionary from resolver_agent

**Output:** Formatted console report

**Example:**
```python
invoice = {
    "invoice_id": "INV-2024-0001",
    "vendor": {"name": "TechSoft Solutions"},
    "invoice_date": "2024-09-15",
    "total_amount": 590000
}
resolution = {
    "final_status": "PASS",
    "confidence": 1.0,
    "failed_checks": []
}
generate_report(invoice, resolution)
```

**Sample Output:**
```
===== COMPLIANCE REPORT =====
Invoice ID     : INV-2024-0001
Vendor         : TechSoft Solutions
Date           : 2024-09-15
Total          : 590000

Final Status   : PASS
Confidence     : 100.0%

[SUCCESS] All checks passed!
```

---

## Tools

### Invoice Tools
**Module:** `tools/invoice_tools.py`

#### 1. `extract_invoice(file_path: str) -> dict | list`

Extracts invoice data from JSON file.

**Parameters:**
- `file_path` (str): Path to JSON invoice file

**Returns:** dict or list of invoice data

**Raises:** FileNotFoundError, json.JSONDecodeError

**Example:**
```python
from tools.invoice_tools import extract_invoice
data = extract_invoice.invoke({"file_path": "data/invoices/invoice_001.json"})
```

---

#### 2. `validate_invoice_number(invoice_number: str) -> bool`

Validates invoice number format: `INV-YYYY-NNNN`

**Parameters:**
- `invoice_number` (str): Invoice number to validate

**Returns:** bool - True if valid format, False otherwise

**Pattern:** `^INV-\d{4}-\d{4}$`

**Valid Examples:**
- INV-2024-0001 ✓
- INV-2023-9999 ✓

**Invalid Examples:**
- INV-24-1 ✗
- inv-2024-0001 ✗ (lowercase)
- INV-2024-00001 ✗ (5 digits)

**Example:**
```python
from tools.invoice_tools import validate_invoice_number
result = validate_invoice_number.invoke({"invoice_number": "INV-2024-0001"})  # True
```

---

#### 3. `check_duplicate_invoice(invoice_number: str) -> bool`

Detects if invoice has been previously processed using StateStore.

**Parameters:**
- `invoice_number` (str): Invoice number to check

**Returns:** bool - True if unique (not duplicate), False if duplicate

**Logic:**
- Checks StateStore for prior processing
- If new: marks as processed and returns True
- If duplicate: returns False

**Example:**
```python
from tools.invoice_tools import check_duplicate_invoice
is_unique = check_duplicate_invoice.invoke({"invoice_number": "INV-2024-0001"})
```

---

### GST Tools
**Module:** `tools/gst_tools.py`

#### 1. `validate_gstin_format(gstin: str) -> bool`

Validates GSTIN (GST Identification Number) structure.

**Parameters:**
- `gstin` (str): GSTIN to validate

**Returns:** bool - True if valid format, False otherwise

**Pattern:** `^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$`

**Format Breakdown:**
- Positions 1-2: State code (2 digits)
- Positions 3-7: Name code (5 uppercase letters)
- Positions 8-11: Registration number (4 digits)
- Position 12: Entity type (1 letter)
- Position 13: Check digit (1-9 or A-Z)
- Position 14: 'Z' (fixed)
- Position 15: Check digit (0-9 or A-Z)

**Valid Example:** `27AABCT1234F1ZP`

**Example:**
```python
from tools.gst_tools import validate_gstin_format
result = validate_gstin_format.invoke({"gstin": "27AABCT1234F1ZP"})  # True
```

---

#### 2. `verify_gstin_active(gstin: str) -> dict | None`

Verifies GSTIN active status using mock GST portal.

**Parameters:**
- `gstin` (str): GSTIN to verify

**Returns:** 
- dict with keys:
  - `active` (bool): True if active, False if inactive
  - `state_code` (str): State code extracted from GSTIN
- None: If GSTIN not found in database

**Mock Database:**
```python
{
    "27AABCT1234F1ZP": {"active": True, "state_code": "27"},
    "29ABCDE1234F1Z5": {"active": False, "state_code": "29"}
}
```

**Example:**
```python
from tools.gst_tools import verify_gstin_active
result = verify_gstin_active.invoke({"gstin": "27AABCT1234F1ZP"})
# Returns: {"active": True, "state_code": "27"}
```

---

#### 3. `match_gstin_state(gstin_state: str, vendor_state: str) -> bool`

Verifies GSTIN state code matches vendor address state.

**Parameters:**
- `gstin_state` (str): State code from GSTIN
- `vendor_state` (str): State code from vendor address

**Returns:** bool - True if states match, False otherwise

**Logic:** Simple string equality check

**Example:**
```python
from tools.gst_tools import match_gstin_state
result = match_gstin_state.invoke({"gstin_state": "27", "vendor_state": "27"})  # True
```

---

## Services

### StateStore
**Module:** `services/state_store.py`

Centralized state management for tracking processed invoices.

#### Methods

##### `__init__()`
Initializes empty invoice registry.

```python
state_store = StateStore()
```

---

##### `is_duplicate(invoice_number: str) -> bool`

Checks if invoice has been previously processed.

**Parameters:**
- `invoice_number` (str): Invoice number to check

**Returns:** bool - True if duplicate, False if new

**Example:**
```python
is_dup = state_store.is_duplicate("INV-2024-0001")
```

---

##### `mark_processed(invoice_number: str) -> None`

Records an invoice as processed.

**Parameters:**
- `invoice_number` (str): Invoice number to mark

**Side Effects:** Updates internal registry

**Example:**
```python
state_store.mark_processed("INV-2024-0001")
```

---

## Data Models

### Invoice Dictionary
```python
{
    "invoice_id": str,              # Unique identifier
    "invoice_number": str,          # Business invoice number
    "invoice_date": str,            # ISO format YYYY-MM-DD
    "vendor": {                     # Vendor information
        "name": str,
        "gstin": str,               # GST ID
        "pan": str,                 # PAN number
        "address": str
    },
    "buyer": {                      # Buyer information
        "name": str,
        "gstin": str,
        "address": str
    },
    "line_items": [                 # Line items
        {
            "description": str,
            "hsn_sac": str,
            "quantity": int,
            "unit": str,
            "rate": float,
            "amount": float
        }
    ],
    "subtotal": float,
    "cgst_rate": float,             # CGST percentage
    "cgst_amount": float,           # CGST amount
    "sgst_rate": float,             # SGST percentage
    "sgst_amount": float,           # SGST amount
    "igst_rate": float,             # IGST percentage
    "igst_amount": float,           # IGST amount
    "total_tax": float,
    "total_amount": float,
    "irn": str,                     # Invoice Reference Number
    "irn_date": str,
    "qr_code_present": bool,
    "payment_terms": str,
    "po_reference": str,            # Purchase Order reference
    "notes": str
}
```

### Validation Result
```python
{
    "check": str,                   # Check name
    "status": bool                  # Pass/Fail
}
```

### Resolution Dictionary
```python
{
    "final_status": str,            # "PASS" or "FAIL"
    "confidence": float,            # 0.0 to 1.0
    "failed_checks": [              # List of failed checks
        {
            "check": str,
            "status": bool
        }
    ]
}
```

---

## Error Handling

### Common Exceptions

| Exception | Cause | Handle |
|-----------|-------|--------|
| FileNotFoundError | Invoice file not found | Check file path |
| json.JSONDecodeError | Invalid JSON format | Validate file format |
| KeyError | Missing required field | Check invoice structure |
| ValueError | Invalid parameter value | Validate input |

---

## Usage Examples

### Complete Workflow
```python
from agents.extractor_agent import create_extractor_agent
from agents.validator_agent import create_validator_agent
from agents.resolver_agent import resolve_results
from agents.reporter_agent import generate_report

# Create agents
extractor = create_extractor_agent()
validator = create_validator_agent()

# Extract invoices
invoices = extractor.run("Extract invoice from data/invoices/invoice_001.json")

# Process first invoice
invoice = invoices[0]
results = []

# Run validations
if "invoice_id" in invoice:
    results.append({
        "check": "Invoice ID Format",
        "status": validator.run(f"Validate invoice number {invoice['invoice_id']}")
    })

if "invoice_id" in invoice:
    results.append({
        "check": "Duplicate Invoice",
        "status": validator.run(f"Check duplicate invoice {invoice['invoice_id']}")
    })

# Resolve and report
resolution = resolve_results(results)
generate_report(invoice, resolution)
```

---

*API Reference Version: 1.0*
*Last Updated: January 2026*
