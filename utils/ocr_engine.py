import easyocr
import numpy as np

reader = easyocr.Reader(
    ['en'],
    gpu=False
)


def run_ocr(image):

    image = np.array(image)

    results = reader.readtext(
        image,
        detail=1
    )

    return results