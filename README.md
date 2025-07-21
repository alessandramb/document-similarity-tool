# Document Similarity Tool

## Features
- Compare PDF and DOCX documents across folders
- Group documents by parent folder names
- Generate interactive HTML dashboard
- Export CSV reports with similarity scores
- Supports parallel processing for large collections

## Installation
pip install .

For development:
pip install -e ".[dev]"

## Usage
Basic command:
docsim folder1 folder2 [options]

Options:
--threshold FLOAT  Set similarity threshold (0.0-1.0, default: 0.85)
--csv FILE         Specify CSV output file
--html FILE        Specify HTML dashboard file
--workers INT      Set number of parallel processes

Example:
docsim ./assignments/2023 ./assignments/2024 --threshold 0.9

## Supported Folder Structure
The tool processes this structure:
submissions_root/
├── participant_1/
│   ├── doc1.pdf
│   └── doc2.docx
└── participant_2/
    └── submission.pdf

## Development Commands
make install-dev  # Install dev dependencies
make test        # Run tests
make lint        # Run linters
make format      # Format code
make clean       # Remove temporary files

## Dependencies
Core:
- pymupdf, python-docx, scikit-learn
- pdf2image, pytesseract, reportlab

Development:
- pytest, black, flake8, mypy

## License
MIT License
