from flask import Flask, request, jsonify
import time
import uuid

app = Flask(__name__)

# In-memory store for access tokens
mock_tokens = {}

@app.route("/auth", methods=["POST"])
def mock_auth():
    api_key = request.headers.get("x-api-key")
    content_type = request.headers.get("Content-Type")

    if not api_key:
        return jsonify({"error": "Missing x-api-key header"}), 400

    if content_type != "application/x-www-form-urlencoded":
        return jsonify({"error": "Invalid Content-Type"}), 400

    form = request.form
    grant_type = form.get("grant_type")

    if grant_type == "refresh_token":
        if not all(k in form for k in ("client_id", "client_secret", "refresh_token")):
            return jsonify({"error": "Missing fields for refresh_token flow"}), 400

    elif grant_type == "password":
        if not all(k in form for k in ("username", "password", "client_id", "client_secret")):
            return jsonify({"error": "Missing fields for password flow"}), 400

    else:
        return jsonify({"error": f"Unsupported grant_type: {grant_type}"}), 400

    # Simulate success
    token = str(uuid.uuid4())
    mock_tokens[token] = time.time()

    return jsonify({
        "access_token": token,
        "token_type": "Bearer",
        "expires_in": 3600
    }), 200

@app.route("/ingestion/v1/documents/upload", methods=["POST"])
def mock_upload():
    auth_header = request.headers.get("Authorization")
    api_key = request.headers.get("x-api-key")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401

    token = auth_header.split()[1]
    if token not in mock_tokens:
        return jsonify({"error": "Invalid or expired token"}), 403

    if "file" not in request.files or "metadata(type:string)" not in request.form:
        return jsonify({"error": "Missing file or metadata"}), 400

    file = request.files["file"]
    metadata = request.form["metadata(type:string)"]

    # Simulate successful upload
    return jsonify({
        "message": "Document upload accepted",
        "jobId": str(uuid.uuid4()),
        "filename": file.filename,
        "metadata": metadata
    }), 202

if __name__ == "__main__":
    app.run(port=5001, debug=True)
