from PyPDF2 import PdfReader


def extract_text(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)

    # Try opening PDFs that have an empty password.
    if reader.is_encrypted:
        if reader.decrypt("") == 0:
            raise ValueError("PDF is encrypted and requires a password")

    return "\n".join(
        page.extract_text() or ""
        for page in reader.pages
    )