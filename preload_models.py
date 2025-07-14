# preload_models.py
import easyocr

# This script is run during the Docker build process.
# It initializes the reader, which triggers the download of the
# pre-trained models for the specified languages.
print("Pre-loading EasyOCR models...")
reader = easyocr.Reader(['en'], gpu=False)
print("Models have been downloaded and cached.")