def generate_report(invoice: dict, resolution: dict):
    print("\n===== COMPLIANCE REPORT =====")
    invoice_id = invoice.get('invoice_id', 'N/A')
    vendor_name = invoice.get('vendor', {}).get('name', 'N/A') if isinstance(invoice.get('vendor'), dict) else invoice.get('vendor', 'N/A')
    invoice_date = invoice.get('invoice_date', 'N/A')
    total_amount = invoice.get('total_amount', 'N/A')
    
    print(f"Invoice ID     : {invoice_id}")
    print(f"Vendor         : {vendor_name}")
    print(f"Date           : {invoice_date}")
    print(f"Total          : {total_amount}")
    print(f"\nFinal Status   : {resolution['final_status']}")
    print(f"Confidence     : {resolution['confidence'] * 100}%")

    if resolution["failed_checks"]:
        print("\nFailed Checks:")
        for f in resolution["failed_checks"]:
            print(f"- {f['check']}")
    else:
        print("\n[SUCCESS] All checks passed!")
