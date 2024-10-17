# pdf_ingestion.py
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import List, Dict
import fitz  # PyMuPDF
import pdfplumber
import os

app = FastAPI()

# Create a directory to store uploaded PDFs.
UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, change as needed for production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are allowed"}
    
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}

def extract_text_from_pdf(pdf_path: str) -> List[Dict[str, str]]:
    """
    Extracts text from each page of the PDF and returns it along with page numbers.
    Uses pdfplumber for high accuracy in extracting text.
    """
    extracted_pages = []

    try:
        # Using pdfplumber for text extraction with better handling of layout.
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""  # Extract text or set to empty if none found.
                extracted_pages.append({
                    "page_number": page_num,
                    "text": text.strip()  # Strip leading/trailing whitespace.
                })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading PDF: {str(e)}")
    
    return {"filename": file.filename, "size": len(contents), "message": "Upload successful"}



if __name__ == "__main__":
    import uvicorn
    # Start the FastAPI server for local development.
    uvicorn.run(app, host="0.0.0.0", port=8000)
