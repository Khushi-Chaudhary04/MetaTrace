# app/extract_metadata.py

import subprocess
import json
import os

def extract_metadata(file_path):
    """Extract metadata from the file using ExifTool."""
    try:
        # Run ExifTool and get the output in JSON format
        command = ['exiftool', '-j', file_path]  # '-j' returns the result in JSON format
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check for errors in ExifTool execution
        if result.stderr:
            raise Exception(f"Error extracting metadata: {result.stderr}")

        # Return the metadata as a Python object (list of dictionaries)
        metadata = json.loads(result.stdout)
        return metadata

    except Exception as e:
        return {"error": str(e)}
