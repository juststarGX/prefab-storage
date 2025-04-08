
from flask import Flask, request, jsonify, send_file
import os, zipfile, uuid, shutil

app = Flask(__name__)
UPLOAD_DIR = "uploaded_zips"
EXTRACT_DIR = "unpacked"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(EXTRACT_DIR, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("zip")
    if not file or not file.filename.endswith(".zip"):
        return jsonify({"error": "Invalid file"}), 400

    serial = str(uuid.uuid4())
    zip_path = os.path.join(UPLOAD_DIR, f"{serial}.zip")
    extract_path = os.path.join(EXTRACT_DIR, serial)

    file.save(zip_path)
    os.makedirs(extract_path, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    return jsonify({
        "serial": serial,
        "message": "Uploaded and unpacked",
        "download_url": f"/download/{serial}"
    })

@app.route("/download/<serial>", methods=["GET"])
def download(serial):
    zip_path = os.path.join(UPLOAD_DIR, f"{serial}.zip")
    if not os.path.exists(zip_path):
        return jsonify({"error": "Not found"}), 404
    return send_file(zip_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
