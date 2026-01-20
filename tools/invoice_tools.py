import json
import re
from langchain.tools import tool
from services.state_store import StateStore

state_store = StateStore()

@tool
def extract_invoice(file_path: str) -> dict:
    """Extract invoice data from JSON file"""
    with open(file_path, "r") as f:
        return json.load(f)

@tool
def validate_invoice_number(invoice_number: str) -> bool:
    """Validate invoice number format: INV-YYYY-NNNN"""
    return bool(re.match(r"^INV-\d{4}-\d{4}$", invoice_number))

@tool
def check_duplicate_invoice(invoice_number: str) -> bool:
    """Detect duplicate invoices across vendors"""
    if state_store.is_duplicate(invoice_number):
        return False
    state_store.mark_processed(invoice_number)
    return True
