import logging
import shutil
from pathlib import Path

from classifier import classify_text
from pdf_reader import extract_text

BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)


def process_pdfs():
    for category in ("Math", "Science", "English", "Unknown"):
        (OUTPUT_DIR / category).mkdir(parents=True, exist_ok=True)

    pdf_files = list(INPUT_DIR.glob("*.pdf"))

    if not pdf_files:
        logging.info("No PDF files found in input folder.")
        return

    for pdf_file in pdf_files:
        try:
            text = extract_text(pdf_file)
            category = classify_text(text)

            destination = OUTPUT_DIR / category / pdf_file.name
            shutil.move(str(pdf_file), str(destination))

            logging.info(f"{pdf_file.name} -> {category}")

        except Exception as error:
            logging.error(f"Failed to process {pdf_file.name}: {error}")


if __name__ == "__main__":
    process_pdfs()