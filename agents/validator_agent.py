from tools.invoice_tools import (
    validate_invoice_number,
    check_duplicate_invoice
)
from tools.gst_tools import (
    validate_gstin_format,
    verify_gstin_active,
    match_gstin_state
)

def create_validator_agent():
    """
    Creates a validator agent that uses multiple validation tools.
    Returns a callable that can validate invoice data.
    """
    class ValidatorAgent:
        def run(self, input_text):
            """
            Route to appropriate validation tool based on input text
            """
            input_lower = input_text.lower()
            
            # Invoice number validation
            if "invoice number" in input_lower:
                invoice_num = input_text.split()[-1]
                return validate_invoice_number.invoke({"invoice_number": invoice_num})
            
            # Duplicate check
            elif "duplicate" in input_lower:
                invoice_num = input_text.split()[-1]
                return check_duplicate_invoice.invoke({"invoice_number": invoice_num})
            
            # GSTIN format validation
            elif "gstin format" in input_lower or "validate gstin" in input_lower:
                gstin = input_text.split()[-1]
                return validate_gstin_format.invoke({"gstin": gstin})
            
            # GSTIN active status
            elif "gstin active" in input_lower or "verify gstin" in input_lower:
                gstin = input_text.split()[-1]
                return verify_gstin_active.invoke({"gstin": gstin})
            
            # GSTIN state match
            elif "state match" in input_lower or "match gstin" in input_lower:
                parts = input_text.split()
                # Extract state codes
                gstin_state = None
                vendor_state = None
                for i, part in enumerate(parts):
                    if part.isdigit() and len(part) == 2:
                        if gstin_state is None:
                            gstin_state = part
                        else:
                            vendor_state = part
                            break
                if gstin_state and vendor_state:
                    return match_gstin_state.invoke({
                        "gstin_state": gstin_state,
                        "vendor_state": vendor_state
                    })
            
            return False
    
    return ValidatorAgent()
