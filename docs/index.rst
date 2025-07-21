Document Similarity Tool Documentation
=====================================

Repository Structure
--------------------

::

    document-similarity-tool/
    ├── Makefile
    ├── pyproject.toml
    ├── README.md
    ├── similarity_dashboard.html
    ├── similarity_results.csv
    ├── src/
    │   ├── docsim/
    │   └── docsim.egg-info/
    └── tests/
        ├── __init__.py
        ├── test_file_handling.py
        └── test_similarity.py

Package Description
-------------------

The Document Similarity Tool compares textual content between PDF and DOCX documents across folders.

Key Features
------------

- Compare documents within and between two folders
- Group documents by subfolder (author)
- Generate HTML dashboard with interactive results
- Create CSV reports

Installation
------------

.. code-block:: bash

    pip install .

For development:

.. code-block:: bash

    pip install -e ".[dev]"

Usage
-----

Basic command:

.. code-block:: bash

    docsim folder1 folder2 [options]

Options:

- ``--threshold FLOAT`` - Similarity threshold (0.0-1.0, default: 0.85)
- ``--csv FILE`` - Output CSV filename
- ``--html FILE`` - Output HTML dashboard filename
- ``--workers INT`` - Number of parallel processes

Example:

.. code-block:: bash

    docsim ./theses ./papers --threshold 0.9 --csv my_results.csv

Development
-----------

Makefile targets:

.. code-block:: bash

    make install-dev   # Install development dependencies
    make test         # Run tests
    make lint         # Run linters
    make format       # Format code
    make clean        # Remove temporary files
    make all          # Run all checks

Testing:

.. code-block:: bash

    pytest --cov=docsim tests/

File Descriptions
-----------------

pyproject.toml
~~~~~~~~~~~~~~
Package configuration with dependencies and build settings.

Makefile
~~~~~~~~
Automation of development tasks (testing, linting, formatting).

src/docsim/
~~~~~~~~~~~
Main package containing:

- core.py: Main comparison logic
- file_handling.py: Document processing
- similarity.py: Similarity calculations
- visualization.py: Report generation
- cli.py: Command line interface

tests/
~~~~~~
Unit tests for package functionality.

Folder Structure Processing
Folder Structure Processing
---------------------------

The tool is designed to work with hierarchical folder structures containing document files.

Supported Structure
------------------

The expected folder structure is:

.. code-block:: none

    submissions_root/
    ├── group_1/
    │   ├── participant_identifier_1/
    │   │   ├── document1.pdf
    │   │   ├── document2.docx
    │   │   └── notes.txt (ignored)
    │   └── participant_identifier_2/
    │       └── submission.pdf
    └── group_2/
        └── participant_identifier_3/
            ├── file_a.pdf
            └── file_b.docx

Example Structures
-----------------

Minimal structure:

.. code-block:: none

    submissions_root/
    └── participant_1/
        └── submission.pdf

Multiple groups:

.. code-block:: none

    course_work/
    ├── physics_lab/
    │   └── student_01/
    │       ├── report.pdf
    │       └── appendix.docx
    └── math_project/
        └── student_02/
            └── solution.pdf
            
File Handling
~~~~~~~~~~~~

1. Directory Scanning:
   - Processes all subdirectories recursively
   - Only analyzes .pdf and .docx files
   - Skips other file types and empty directories

2. Participant Identification:
   - Extracts identifiers from folder names
   - Supports common naming patterns:
     * name_id
     * lastname_firstname
     * identifier_additionalinfo

3. Content Processing:
   - Combines all PDF/DOCX files per participant
   - Removes identifiers from extracted text
   - Normalizes whitespace and formatting

Technical Implementation
~~~~~~~~~~~~~~~~~~~~~~~

Key functions in file_handling.py:

1. find_files():
   - Uses os.walk() for directory traversal
   - Case-insensitive file extension check
   - Returns list of absolute file paths

2. group_files_by_subfolder():
   - Groups files by immediate parent directory
   - Special cases handled:
     - __MACOSX folders ignored
     - Hidden files (starting with .) skipped
     - Handles nested submission folders

3. Text extraction:
   - PDF: PyMuPDF (fitz) with Tesseract OCR fallback
   - DOCX: python-docx library
   - All text converted to UTF-8 encoding

Example Structures
~~~~~~~~~~~~~~~~~

Minimal structure:
submissions_root/
    ├── group_1/
    │   ├── participant_identifier_1/
    │   │   ├── document1.pdf
    │   │   ├── document2.docx
    │   │   └── notes.txt (ignored)
    │   └── participant_identifier_2/
    │       └── submission.pdf
    └── group_2/
        └── participant_identifier_3/
            ├── file_a.pdf
            └── file_b.docx


Output Files
------------

similarity_dashboard.html
~~~~~~~~~~~~~~~~~~~~~~~~~
Interactive HTML dashboard showing similarity results.

similarity_results.csv
~~~~~~~~~~~~~~~~~~~~~~
CSV file containing detailed similarity comparisons.

Dependencies
------------

Core:

- pymupdf
- python-docx
- scikit-learn
- pdf2image
- pytesseract
- reportlab
- tqdm

Development:

- pytest
- black
- flake8
- mypy
- isort

License
-------
MIT License

Acknowledgements
----------------
This project was developed with assistance from AI tools.