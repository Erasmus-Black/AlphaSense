# AlphaSense Document Upload Tool

This script automates the upload of documents to the AlphaSense ingestion API.

---

## Requirements

- Python 3.8+
- Install dependencies:
  ```bash
  pip install requests pyyaml 

## Usage

- Place files to upload in the DocumentUpload/upload folder.

- Run the script:

  ```bash
  python DocumentUpload/ingest_upload.py

- Logs will be written to upload.log

## Test Server (Optional)

- You can test against a local Flask server running the mock endpoint:

  ```bash
  python AlphaSenseFlask/mock_server.py

If using Python flask ensure UPLOAD_URL in ingest_upload.py is pointing to the UPLOAD_URL

UPLOAD_URL = "http://localhost:5001/ingestion/v1/documents/upload"

## Notes

- Only files with valid extensions and sizes will be uploaded.
- Metadata is generated per file.
- Uploaded and failed files are moved into DocumentUpload/processed folders.
