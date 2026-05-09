import fitz  # PyMuPDF

def extract_text_from_pdf(file_bytes):
    try:
        if not file_bytes:
            raise RuntimeError("Empty file uploaded")

        doc = fitz.open(stream=file_bytes, filetype="pdf")

        if doc.page_count == 0:
            raise RuntimeError("PDF has no pages")

        text = ""

        for page in doc:
            page_text = page.get_text()
            if page_text:
                text += page_text + "\n"

        text = text.strip()

        if not text:
            raise RuntimeError("No readable text found in PDF")

        return text

    except Exception as e:
        raise RuntimeError(f"Invalid or corrupted PDF: {str(e)}")