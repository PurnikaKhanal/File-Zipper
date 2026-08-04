import os
from flask import Flask, request, jsonify, send_from_directory, render_template
from huffman_compress import compress
from huffman_decompress import decompress

app = Flask(__name__)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/compress", methods=["POST"])
def api_compress():
    f = request.files.get("file")
    if not f:
        return jsonify({"success": False, "error": "No file uploaded"}), 400

    in_path = os.path.join(UPLOAD_DIR, f.filename)
    f.save(in_path)

    out_name = f.filename + ".huf"
    out_path = os.path.join(OUTPUT_DIR, out_name)

    result = compress(in_path, out_path)
    if not result.get("success"):
        return jsonify({"success": False, "error": result.get("error")}), 500

    return jsonify({
        "success": True,
        "original_size": result["original_size"],
        "compressed_size": result["compressed_size"],
        "output_file": out_name
    })

@app.route("/api/decompress", methods=["POST"])
def api_decompress():
    f = request.files.get("file")
    if not f:
        return jsonify({"success": False, "error": "No file uploaded"}), 400
    if not f.filename.lower().endswith(".huf"):
        return jsonify({"success": False, "error": "Invalid file type for decompression"}), 400

    in_path = os.path.join(UPLOAD_DIR, f.filename)
    f.save(in_path)

    out_name = f.filename.replace(".huf", "_recovered.txt")
    out_path = os.path.join(OUTPUT_DIR, out_name)

    result = decompress(in_path, out_path)
    if not result.get("success"):
        return jsonify({"success": False, "error": result.get("error")}), 500

    return jsonify({
        "success": True,
        "original_size": result["original_size"],
        "recovered_size": os.path.getsize(out_path),
        "output_file": out_name
    })

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
