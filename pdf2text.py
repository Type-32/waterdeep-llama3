import os
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import tempfile


def extract_text_from_pdf_ocr(pdf_path, dpi=300):
    text = ""
    temp_dir = "training_data/.temp"
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Convert PDF to list of images
        pages = convert_from_path(pdf_path, dpi)

        for i, page in enumerate(pages):
            # if i > 10:
            #     break
            print(f"Processing page {i + 1}/{len(pages)}...")

            # Save the image as PNG instead of JPEG
            image_path = os.path.join(temp_dir, f"temp_page_{i}.png")
            page.save(image_path, "PNG")

            try:
                # Perform OCR on the image
                text += pytesseract.image_to_string(Image.open(image_path))
                text += "\n\n"  # Add separation between pages
            except pytesseract.TesseractError as e:
                print(f"Error on page {i + 1}: {str(e)}")
                # Optionally, you can try to process the image at a lower resolution
                try:
                    resized_image = page.resize((page.width // 2, page.height // 2))
                    text += pytesseract.image_to_string(resized_image)
                    text += "\n\n"
                except Exception as e2:
                    print(f"Error processing resized image on page {i + 1}: {str(e2)}")

            # Remove the temporary image
            os.remove(image_path)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return text


# Example usage
pdf_path = "training_data/dnd5e_rulebook.pdf"
extracted_text = extract_text_from_pdf_ocr(pdf_path)

# Save the extracted text to a file
with open("extracted_text.txt", "w", encoding="utf-8") as text_file:
    text_file.write(extracted_text)

print("Text extraction complete. Saved to 'extracted_text.txt'")
print("First 500 characters of extracted text:")
print(extracted_text[:500])