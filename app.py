from flask import Flask, request, send_file, jsonify
import subprocess
import os
import uuid

app = Flask(__name__)

UPLOAD_DIR = "files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route("/")
def home():
    return "LibreOffice Converter Running"


@app.route("/convert", methods=["POST"])
def convert():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        output_format = request.form.get("format")

        if not output_format:
            return jsonify({"error": "No format provided"}), 400

        uid = str(uuid.uuid4())
        input_filename = uid + "_" + file.filename
        input_path = os.path.join(UPLOAD_DIR, input_filename)

        file.save(input_path)

        # Run LibreOffice
        process = subprocess.run(
            [
                "soffice",
                "--headless",
                "--convert-to", output_format,
                "--outdir", UPLOAD_DIR,
                input_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if process.returncode != 0:
            return jsonify({
                "error": "Conversion failed",
                "details": process.stderr.decode()
            }), 500

        base = os.path.splitext(input_filename)[0]
        output_path = os.path.join(UPLOAD_DIR, f"{base}.{output_format}")

        if not os.path.exists(output_path):
            return jsonify({"error": "Output file not created"}), 500

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
