import pytesseract
from PIL import Image
from typing import Tuple
from log_config import logger

# Define the path to your Tesseract executable (change this if needed)
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'


# Open the image file
def read_image(path: str) -> Tuple[bool, float]:
    image = Image.open(path)

    # Perform OCR to extract text from the image
    text: str = pytesseract.image_to_string(image)

    lines: list = text.splitlines()

    target_line = None
    for line in lines:
        if line.strip().endswith('South African Rand'):
            target_line = line
    exchange_rate: float = 0.0
    found: bool = False
    # Print the extracted text
    if target_line:
        try:
            transformed_to_float = float(target_line[:5].strip())
            exchange_rate: float = transformed_to_float
            found: bool = True
            logger.info('Exchange rate successfully extracted.')
        except ValueError:
            logger.error("Value not found.")
    else:
        logger.info("Line ending with 'South African Rand' not found.")
    return found, exchange_rate
