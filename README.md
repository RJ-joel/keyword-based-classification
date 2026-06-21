# PDF Document Ingestion & Categorization

## Overview

This Python application:

1. Reads PDF files from the input folder.
2. Extracts text from each PDF.
3. Converts text to lowercase.
4. Counts predefined category keywords.
5. Determines the document category.
6. Moves the PDF into the appropriate output folder.
7. Logs processing results.

## Categories

### Math
- equation
- algebra
- geometry
- fraction
- integer
- variable

### Science
- plant
- photosynthesis
- atom
- force
- energy
- gravity

### English
- grammar
- noun
- verb
- pronoun
- sentence
- adjective

## Folder Structure

project/

├── input/

├── output/

│ ├── Math/

│ ├── Science/

│ ├── English/

│ └── Unknown/

├── main.py

├── classifier.py

├── pdf_reader.py

├── requirements.txt

└── README.md

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Example Output

```text
math_ch1.pdf -> Math
science_intro.pdf -> Science
grammar_notes.pdf -> English
abc.pdf -> Unknown
```