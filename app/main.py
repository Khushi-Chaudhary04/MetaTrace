from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import subprocess
import os
from pathlib import Path
import shutil

app = FastAPI()

# Directory to store uploaded files temporarily
UPLOAD_DIR = Path("uploads")

# Ensure the upload directory exists
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Function to extract metadata using ExifTool
def extract_metadata(file_path: str):
    try:
        # Call ExifTool to extract metadata
        result = subprocess.run(
            ["exiftool", "-json", file_path],
            capture_output=True,
            text=True,
            check=True,
        )
        # Parse the JSON output from ExifTool
        metadata = jsonable_encoder(result.stdout)
        return metadata
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail="Error extracting metadata")

# Endpoint to upload a file and extract metadata
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Get the file name and create a temporary path
    file_path = UPLOAD_DIR / file.filename
    
    try:
        # Save the uploaded file
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Extract metadata from the saved file
        metadata = extract_metadata(file_path)
        
        # Clean up the file after processing (optional)
        os.remove(file_path)
        
        # Return the extracted metadata
        return JSONResponse(content=metadata, status_code=200)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Basic test route to verify the server is running
@app.get("/")
def read_root():
        return {"message": "MetaTrace - Metadata Forensics Tool is running!"}
