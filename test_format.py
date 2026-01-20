import json

with open('data/invoices/invoice_001.json') as f:
    data = json.load(f)
    for i in range(3):
        inv = data[i]
        print(f"Invoice {i+1}:")
        print(f"  invoice_id: {inv.get('invoice_id')}")
        print(f"  invoice_number: {inv.get('invoice_number')}")
        print()
