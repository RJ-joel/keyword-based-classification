import logging
import os
import shutil
from pathlib import Path

from PyPDF2.errors import PdfReadError

from classifier import classify_text
from pdf_reader import EncryptedPdfError, extract_text

BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
CATEGORIES = ("Math", "Science", "English", "Unknown")

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


def reserve_unique_destination(category: str, source_file: Path) -> Path:
    """
    Atomically reserve a unique output filename.

    O_CREAT | O_EXCL ensures that two program instances cannot reserve
    the same filename.
    """
    output_folder = OUTPUT_DIR / category
    output_folder.mkdir(parents=True, exist_ok=True)

    counter = 0

    while True:
        if counter == 0:
            filename = source_file.name
        else:
            filename = (
                f"{source_file.stem}_{counter}{source_file.suffix}"
            )

        destination = output_folder / filename

        try:
            file_descriptor = os.open(
                destination,
                os.O_CREAT | os.O_EXCL | os.O_WRONLY,
            )
        except FileExistsError:
            counter += 1
            continue

        os.close(file_descriptor)
        return destination


def move_to_reserved_destination(
    source_file: Path,
    destination: Path,
) -> None:
    """
    Copy to the atomically reserved file, then remove the source.

    This avoids filename collisions even when multiple processes run
    at the same time.
    """
    try:
        shutil.copy2(source_file, destination)
        source_file.unlink()
    except OSError:
        # Remove the empty/reserved destination if transfer failed.
        if destination.exists():
            destination.unlink()
        raise


def process_pdf(pdf_file: Path) -> None:
    try:
        extracted_text = extract_text(pdf_file)
        category = classify_text(extracted_text)

        if not extracted_text.strip():
            logger.info("%s has no extractable text.", pdf_file.name)

    except (PdfReadError, EncryptedPdfError) as error:
        # Known PDF-specific problems are safely routed to Unknown.
        category = "Unknown"
        logger.warning("%s: %s", pdf_file.name, error)

    except OSError as error:
        # Example: unreadable file or insufficient file permissions.
        logger.error("Could not read %s: %s", pdf_file.name, error)
        return

    destination = reserve_unique_destination(category, pdf_file)

    try:
        move_to_reserved_destination(pdf_file, destination)
    except OSError:
        logger.exception("Could not move %s", pdf_file.name)
        return

    if destination.name == pdf_file.name:
        logger.info("%s -> %s", pdf_file.name, category)
    else:
        logger.info(
            "%s -> %s (saved as %s)",
            pdf_file.name,
            category,
            destination.name,
        )


def main() -> None:
    INPUT_DIR.mkdir(exist_ok=True)

    pdf_files = [
        file
        for file in INPUT_DIR.iterdir()
        if file.is_file() and file.suffix.lower() == ".pdf"
    ]

    if not pdf_files:
        logger.info("No PDF files found in input folder.")
        return

    for pdf_file in pdf_files:
        process_pdf(pdf_file)


if __name__ == "__main__":
    main()