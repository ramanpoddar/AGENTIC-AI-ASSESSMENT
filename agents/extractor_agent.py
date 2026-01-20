from tools.invoice_tools import extract_invoice

def create_extractor_agent():
    """
    Creates an extractor agent that uses the extract_invoice tool.
    Returns a callable that can extract invoice data.
    """
    class ExtractorAgent:
        def run(self, input_text):
            # Parse file path from input
            if "invoice_001.json" in input_text:
                file_path = "data/invoices/invoice_001.json"
            else:
                file_path = input_text.split()[-1]
            result = extract_invoice.invoke({"file_path": file_path})
            # extract_invoice returns a list of invoices, return all of them
            if isinstance(result, list):
                return result
            return result
    
    return ExtractorAgent()
