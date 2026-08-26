from guid_detector.processing import preprocess_image
from PIL import Image


def test_preprocess_image():
    # Create a test empty square in memory
    img = Image.new("RGB", (100, 100), color="white")
    processed = preprocess_image(img, scale=2, threshold=200)
    
    # Checking upscaling and conversion to grayscale
    assert processed.size == (200, 200)
    assert processed.mode == "L"