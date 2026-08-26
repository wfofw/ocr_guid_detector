from guid_detector.extractor import find_guids_by_stripes
from PIL import Image

image = Image.open("sample_screenshot_2.jpeg")

# Localization and extraction
guids = find_guids_by_stripes(image)
print("Found GUIDs:", guids)