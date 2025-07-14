# main.py
import io
import os
import easyocr
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

# --- Configuration ---
# Use an environment variable to set GPU usage, defaulting to False
USE_GPU = os.getenv("USE_GPU", "False").lower() == "true"
# Define the languages you want to support
SUPPORTED_LANGUAGES = ['en']

# --- FastAPI App Initialization ---
app = FastAPI(
    title="EasyOCR API",
    description="Deployable OCR API using EasyOCR and FastAPI",
    version="1.0.0",
)

# --- Model Loading ---
# Load the model once when the application starts
print(f"Loading EasyOCR reader for languages: {SUPPORTED_LANGUAGES} (GPU: {USE_GPU})")
reader = easyocr.Reader(SUPPORTED_LANGUAGES, gpu=USE_GPU)
print("EasyOCR reader loaded successfully.")

# --- API Endpoints ---
@app.get("/", tags=["General"])
def read_root():
    return {"message": "Welcome to the EasyOCR API! Navigate to /docs for documentation."}

@app.post("/ocr", tags=["OCR"], response_description="OCR results")
async def perform_ocr(file: UploadFile = File(...)):
    """Performs OCR on an uploaded image."""
    try:
        contents = await file.read()
        
        # The 'detail=0' gives only text, 'detail=1' gives bounding boxes and confidence
        result = reader.readtext(contents, detail=1)
        
        # Format the response
        response_data = {
            "filename": file.filename,
            "extracted_text": [item[1] for item in result],
            "full_result": [
                {
                    # Convert numpy types to standard Python types for JSON serialization
                    "bounding_box": [list(map(int, point)) for point in item[0]],
                    "text": item[1],
                    "confidence": float(item[2])
                }
                for item in result
            ]
        }
        return JSONResponse(content=response_data)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})