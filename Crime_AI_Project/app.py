from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os

from modules.face_match import compare_uploaded_image
from modules.hotspot import (
    get_hotspots,
    check_location,
    get_statistics
)
from modules.legal_ai import suggest_lawyer
from modules.prediction import predict_crime
from report_generator import generate_report


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)


ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


@app.route("/")
def home():
    return render_template("index.html")


# ---------------------------------------------------------
# IMAGE / FACE VERIFICATION DEMO
# ---------------------------------------------------------

@app.route("/scan", methods=["POST"])
def scan():

    if "file" not in request.files:

        return jsonify({
            "status": "ERROR",
            "message": "No image uploaded."
        }), 400

    file = request.files["file"]

    if file.filename == "":

        return jsonify({
            "status": "ERROR",
            "message": "Please select an image."
        }), 400

    if not allowed_file(file.filename):

        return jsonify({
            "status": "ERROR",
            "message": "Unsupported image format."
        }), 400

    filename = secure_filename(
        file.filename
    )

    path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(path)

    result = compare_uploaded_image(
        path
    )

    return jsonify(result)

# ---------------------------------------------------------
# LOCATION
# ---------------------------------------------------------

@app.route("/api/location", methods=["POST"])
def location():

    try:

        data = request.get_json()

        lat = float(data["lat"])
        lon = float(data["lon"])

        result = check_location(lat, lon)

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "status": "ERROR",
            "message": str(e)
        }), 400


# ---------------------------------------------------------
# HOTSPOTS
# ---------------------------------------------------------

@app.route("/api/hotspots")
def hotspots():

    try:

        result = get_hotspots()

        return jsonify({
            "status": "OK",
            "hotspots": result
        })

    except Exception as e:

        return jsonify({
            "status": "ERROR",
            "message": str(e)
        }), 500


# ---------------------------------------------------------
# STATISTICS
# ---------------------------------------------------------

@app.route("/api/statistics")
def statistics():

    try:

        return jsonify(get_statistics())

    except Exception as e:

        return jsonify({
            "status": "ERROR",
            "message": str(e)
        }), 500


# ---------------------------------------------------------
# CRIME PREDICTION
# ---------------------------------------------------------

@app.route("/api/predict", methods=["POST"])
def prediction():

    try:

        data = request.get_json()

        lat = float(data["lat"])
        lon = float(data["lon"])

        result = predict_crime(lat, lon)

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "status": "ERROR",
            "message": str(e)
        }), 400


# ---------------------------------------------------------
# LEGAL AI
# ---------------------------------------------------------

@app.route("/api/legal", methods=["POST"])
def legal():

    try:

        data = request.get_json()

        case_text = data.get("case", "").strip()

        result = suggest_lawyer(case_text)

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "status": "ERROR",
            "message": str(e)
        }), 400


# ---------------------------------------------------------
# PDF REPORT
# ---------------------------------------------------------

@app.route("/pdf")
def pdf():

    report_path = generate_report()

    return send_file(
        report_path,
        as_attachment=True,
        download_name="Crime_AI_Report.pdf"
    )


# ---------------------------------------------------------
# RUN
# ---------------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )