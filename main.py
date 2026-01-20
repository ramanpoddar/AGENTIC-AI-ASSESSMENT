from agents.extractor_agent import create_extractor_agent
from agents.validator_agent import create_validator_agent
from agents.resolver_agent import resolve_results
from agents.reporter_agent import generate_report

extractor = create_extractor_agent()
validator = create_validator_agent()

# Extract all invoices
invoices = extractor.run(
    "Extract invoice from data/invoices/invoice_001.json"
)

# Process each invoice
for invoice in invoices:
    results = []
    
    # Validate invoice ID format (INV-YYYY-NNNN)
    if "invoice_id" in invoice:
        results.append({
            "check": "Invoice ID Format",
            "status": validator.run(
                f"Validate invoice number {invoice['invoice_id']}"
            )
        })
    
    # Check duplicate
    if "invoice_id" in invoice:
        results.append({
            "check": "Duplicate Invoice",
            "status": validator.run(
                f"Check duplicate invoice {invoice['invoice_id']}"
            )
        })
    
    # Validate vendor info
    if "vendor" in invoice:
        results.append({
            "check": "Vendor Validation",
            "status": len(invoice['vendor']) > 0
        })
    
    # Validate total amount
    if "total_amount" in invoice:
        results.append({
            "check": "Total Amount Valid",
            "status": invoice['total_amount'] > 0
        })
    
    resolution = resolve_results(results)
    generate_report(invoice, resolution)
