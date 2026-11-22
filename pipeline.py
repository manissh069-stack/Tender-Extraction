import os
import cv2
import pytesseract
import pdfplumber
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

PDF_PATH = "sample.pdf"
OUTPUT_DIR = "results"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

KEYWORDS = ['टेन्डर', 'बोलपत्र', 'सूचना', 'दरभाउपत्र', 'आह्वान']

def process_pdf():
    print(f"Reading {PDF_PATH}...")
    pdf = pdfplumber.open(PDF_PATH)

    for page_num, page in enumerate(pdf.pages):
        print(f"Processing page {page_num + 1}...")
        
        # Render page to high-res image
        im = page.to_image(resolution=300)
        open_cv_image = cv2.cvtColor(np.array(im.original), cv2.COLOR_RGB2BGR)

        print("  Scanning page for keywords...")
        data = pytesseract.image_to_data(open_cv_image, lang='nep', output_type=pytesseract.Output.DICT)

        for i in range(len(data['text'])):
            word = data['text'][i].strip()
            if not word:
                continue
                
            if any(kw in word for kw in KEYWORDS):
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                print(f"  -> Found keyword '{word}' at X:{x} Y:{y}")
                
                # We will dynamically expand the crop to capture the full tender
                # 1. Start with the keyword's position
                top = max(0, y - 50)           # A little space above the heading
                bottom = min(open_cv_image.shape[0], y + h + 800) # Grab 800 pixels below
                
                # 2. Expand left and right, but try not to bleed into other columns
                # We assume a standard newspaper column is about 600-700 pixels wide at 300 DPI
                left = max(0, x - 100)         
                right = min(open_cv_image.shape[1], x + w + 600) 

                crop = open_cv_image[top:bottom, left:right]
                
                # Save the crop
                filename = f"page{page_num+1}_tender_{word[:5]}.png"
                save_path = os.path.join(IMAGES_DIR, filename)
                cv2.imwrite(save_path, crop)
                print(f"     Saved: {filename}")
                
                # To avoid saving the same tender multiple times if the keyword appears twice,
                # we break after the first find on this page. Remove this if you want multiple.
                break 

    pdf.close()

if __name__ == "__main__":
    process_pdf()