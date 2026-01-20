import re
from langchain.tools import tool

MOCK_GST_PORTAL = {
    "27ABCDE1234F1Z5": {"active": True, "state_code": "27"},
    "29ABCDE1234F1Z5": {"active": False, "state_code": "29"}
}

@tool
def validate_gstin_format(gstin: str) -> bool:
    """Validate GSTIN structure"""
    pattern = r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$"
    return bool(re.match(pattern, gstin))

@tool
def verify_gstin_active(gstin: str) -> dict:
    """Verify GSTIN active status (mock GST portal)"""
    return MOCK_GST_PORTAL.get(gstin)

@tool
def match_gstin_state(gstin_state: str, vendor_state: str) -> bool:
    """Match GSTIN state code with vendor address"""
    return gstin_state == vendor_state
