import os
import shutil
import json
import datetime
import logging

ALLOWED_EXTENSIONS = {"pdf", "html", "htm", "txt", "doc", "docx", "xls", "xlsx", "ppt", "pptx",
                      "msg", "eml", "csv", "xlsb", "xlsm", "one", "tsv", "ods"}
MAX_FILE_SIZE_MB = 150
INVALID_CHARS = {'/', '\\', ','}

def is_valid_filename(filename):
    if len(filename) > 255:
        return False, "Filename exceeds 255 characters"
    if any(char in filename for char in INVALID_CHARS):
        return False, "Filename contains invalid characters"
    if filename.count('.') != 1:
        return False, "Filename must contain only one dot (no double extensions)"
    return True, ""

def is_valid_file(file_path):
    filename = os.path.basename(file_path)
    ext = filename.split('.')[-1].lower()
    size_mb = os.path.getsize(file_path) / (1024 * 1024)

    if ext not in ALLOWED_EXTENSIONS:
        return False, "File extension not permitted"
    if size_mb > MAX_FILE_SIZE_MB:
        return False, "File size exceeds 150MB"

    valid_name, msg = is_valid_filename(filename)
    if not valid_name:
        return False, msg

    return True, ""

def build_metadata(filename, username):
    title = os.path.splitext(filename)[0]
    today = datetime.datetime.utcnow().isoformat() + "Z"
    return json.dumps({
        "title": title,
        "companies": [{
            "value": "",
            "operation": "ADD",
            "identifier": "",
            "salience": "PRIMARY"
        }],
        "customTags": [
            {
                "name": "",
                "visibility": "PUBLIC",
                "operation": "ADD"
            },
            {
                "name": "",
                "visibility": "PRIVATE",
                "operation": "ADD"
            }
        ],
        "shareInfo": {
            "mode": "DEFAULT"
        },
        "docAuthors": [
            {
                "authorName": username,
                "operation": "ADD"
            }
        ],
        "documentOwner": username,
        "createdTimestamp": today,
        "sourceType": "Internal Research",
        "documentUrl": ""
    })


def move_to_archive(file_path, archive_folder, failed=False):
    subfolder = "failed" if failed else "uploaded"
    target_dir = os.path.join(archive_folder, subfolder)
    os.makedirs(target_dir, exist_ok=True)
    shutil.move(file_path, os.path.join(target_dir, os.path.basename(file_path)))
    logging.info(f"Moved file to archive: {file_path} -> {target_dir}")
