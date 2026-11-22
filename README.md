# Nepali Tender Extractor

An automated pipeline designed to scan Nepali newspaper PDFs, detect tender notices using Nepali OCR, and crop them for use in a mobile application.

## Features
- **PDF to Image Conversion:** Renders high-resolution images from newspaper PDFs.
- **Keyword Detection:** Uses Tesseract OCR (Nepali language pack) to scan the page for keywords like "टेन्डर", "बोलपत्र", and "सूचना".
- **Smart Cropping:** Uses OpenCV and Tesseract's layout data to crop the exact region surrounding the tender notice.

## Tech Stack
- Python
- OpenCV (Image processing)
- PyTesseract (Nepali OCR)
- pdfplumber (PDF extraction)

## Setup Instructions
1. Clone the repository.
2. Create a virtual environment and install requirements: `pip install -r requirements.txt`
3. Ensure Tesseract OCR is installed with the Nepali language pack.
4. Place a newspaper PDF named `sample.pdf` in the root folder.
5. Run `python pipeline.py`.
