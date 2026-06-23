from pathlib import Path
from typing import Union

from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError


class EncryptedPdfError(Exception):
    """Raised when an encrypted PDF cannot be opened with a blank password."""


def extract_text(pdf_path: Union[str, Path]) -> str:
    """
    Extract text from a PDF and always close its file handle afterward.
    """
    path = Path(pdf_path)

    with path.open("rb") as pdf_file:
        reader = PdfReader(pdf_file)

        if reader.is_encrypted:
            # PyPDF2 3.0.1 returns 0 when blank-password decryption fails.
            decrypted = reader.decrypt("")

            if decrypted == 0:
                raise EncryptedPdfError(
                    "PDF is encrypted and requires a password."
                )

        try:
            return "\n".join(
                page.extract_text() or ""
                for page in reader.pages
            )
        except PdfReadError:
            raise