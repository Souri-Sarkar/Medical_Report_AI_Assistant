from PIL import Image


def load_image(uploaded_file):
    """
    Open uploaded image.
    """

    return Image.open(uploaded_file)