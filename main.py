import logging
import shutil
from pathlib import Path

from classifier import classify_text
from pdf_reader import extract_text

BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
CATEGORIES = ("Math", "Science", "English", "Unknown")

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)


def get_unique_destination(category: str, file_name: str) -> Path:
    """
    Prevents overwriting when a file with the same name
    already exists in an output folder.
    """
    category_dir = OUTPUT_DIR / category
    original_path = category_dir / file_name

    if not original_path.exists():
        return original_path

    file_path = Path(file_name)
    counter = 1

    while True:
        new_name = f"{file_path.stem}_{counter}{file_path.suffix}"
        new_path = category_dir / new_name

        if not new_path.exists():
            return new_path

        counter += 1


def process_pdfs():
    INPUT_DIR.mkdir(exist_ok=True)

    for category in CATEGORIES:
        (OUTPUT_DIR / category).mkdir(parents=True, exist_ok=True)

    # Supports names such as document.pdf and document.PDF
    pdf_files = [
        file
        for file in INPUT_DIR.iterdir()
        if file.is_file() and file.suffix.lower() == ".pdf"
    ]

    if not pdf_files:
        logging.info("No PDF files found in input folder.")
        return

    for pdf_file in pdf_files:
        try:
            text = extract_text(pdf_file)
            category = classify_text(text)

            # Empty or scanned PDFs have no extractable text.
            if not text.strip():
                logging.info(f"{pdf_file.name} has no extractable text.")

        except Exception as error:
            # Corrupt/password-protected PDFs are safely sent to Unknown.
            category = "Unknown"
            logging.warning(f"{pdf_file.name}: could not read PDF ({error})")

        destination = get_unique_destination(category, pdf_file.name)

        try:
            shutil.move(str(pdf_file), str(destination))

            if destination.name != pdf_file.name:
                logging.info(
                    f"{pdf_file.name} -> {category} "
                    f"(saved as {destination.name})"
                )
            else:
                logging.info(f"{pdf_file.name} -> {category}")

        except OSError as error:
            logging.error(f"Could not move {pdf_file.name}: {error}")


if __name__ == "__main__":
    process_pdfs()