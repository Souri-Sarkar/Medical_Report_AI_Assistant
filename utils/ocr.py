import easyocr
from PIL import Image
import numpy as np

# Initialize OCR model once
reader = easyocr.Reader(['en'], gpu=False)


def extract_text_from_image(image):
    """
    Extract text from an image using EasyOCR.
    """

    image = np.array(image)

    results = reader.readtext(image)

    text = ""

    for result in results:
        text += result[1]
        text += "\n"

    return text