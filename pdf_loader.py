import fitz  # this is PyMuPDF - it helps us read PDF files

def load_pdf(pdf_path):
    """
    This function opens a PDF file and reads all the text from every page.
    Think of it like a person flipping through every page of a book 
    and writing down everything they see.
    """
    
    # Open the PDF file
    document = fitz.open(pdf_path)
    
    # This will hold all the text we find
    all_text = ""
    
    # Go through every single page one by one
    for page_number in range(len(document)):
        
        # Open that specific page
        page = document[page_number]
        
        # Extract all the text from that page
        text = page.get_text()
        
        # Add that page's text to our collection
        all_text += text
    
    # Close the document when we're done
    document.close()
    
    # Send back all the text we collected
    return all_text