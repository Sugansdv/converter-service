from flask import Flask, request, send_file
import subprocess
import os
import uuid

app = Flask(__name__)

UPLOAD_DIR = "files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route("/convert", methods=["POST"])
def convert():
    file = request.files["file"]
    output_format = request.form.get("format")

    uid = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_DIR, uid + "_" + file.filename)
    file.save(input_path)

    subprocess.run([
        "soffice",
        "--headless",
        "--convert-to", output_format,
        "--outdir", UPLOAD_DIR,
        input_path
    ])

    base = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(UPLOAD_DIR, f"{base}.{output_format}")

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
