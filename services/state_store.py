class StateStore:
    def __init__(self):
        self.invoice_numbers = set()

    def is_duplicate(self, invoice_number: str) -> bool:
        return invoice_number in self.invoice_numbers

    def mark_processed(self, invoice_number: str):
        self.invoice_numbers.add(invoice_number)
