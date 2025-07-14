# main.py (modified for Hugging Face)
import io
import os
import easyocr
import gradio as gr # Import Gradio
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# --- Configuration ---
USE_GPU = os.getenv("USE_GPU", "False").lower() == "true"
SUPPORTED_LANGUAGES = ['en']

# --- Model Loading ---
print(f"Loading EasyOCR reader for languages: {SUPPORTED_LANGUAGES} (GPU: {USE_GPU})")
reader = easyocr.Reader(SUPPORTED_LANGUAGES, gpu=USE_GPU)
print("EasyOCR reader loaded successfully.")

# --- Core OCR Function ---
def ocr_and_draw(image_upload):
    """
    Performs OCR and returns the image with bounding boxes drawn on it.
    """
    # Convert Gradio's image (numpy array) to bytes for easyocr
    image = Image.fromarray(image_upload)
    
    # Draw on a copy of the image
    draw = ImageDraw.Draw(image)
    
    # Perform OCR
    result = reader.readtext(np.array(image))
    
    extracted_text = []
    for (bbox, text, prob) in result:
        extracted_text.append(text)
        
        # Draw bounding box
        top_left = tuple(bbox[0])
        bottom_right = tuple(bbox[2])
        draw.rectangle([top_left, bottom_right], outline="red", width=3)
        
        # You can also draw the text, but it can get messy
        # draw.text(top_left, text, fill="red")
        
    return image, "\n".join(extracted_text)

# --- Gradio Interface Definition ---
description = "A simple web app to perform OCR on an uploaded image using EasyOCR. Upload an image to see the result."
title = "EasyOCR Online"

iface = gr.Interface(
    fn=ocr_and_draw,
    inputs=gr.Image(type="numpy", label="Upload Image"),
    outputs=[
        gr.Image(type="pil", label="Image with Bounding Boxes"),
        gr.Textbox(label="Extracted Text")
    ],
    title=title,
    description=description,
    examples=[["./example.png"]] # You can add an example image to your repo
)

# --- Launch the App ---
# When deploying on Spaces, it will run this automatically.
iface.launch()