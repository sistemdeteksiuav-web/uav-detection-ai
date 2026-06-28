import os
import uuid

from flask import Flask, render_template, request, jsonify

from predictor import UAVPredictor

# =====================================================
# FLASK
# =====================================================

app = Flask(__name__)

# =====================================================
# FOLDER UPLOAD
# =====================================================

UPLOAD_FOLDER = "static/upload"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Maksimal ukuran upload 16 MB
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

# =====================================================
# LOAD MODEL (HANYA SEKALI SAAT SERVER BERJALAN)
# =====================================================

predictor = UAVPredictor(
    classify_model_path="model/model_klasifikasi.h5",
    regress_model_path="model/model_regresi.h5"
)

# =====================================================
# HALAMAN UTAMA
# =====================================================

@app.route("/")
def index():
    return render_template("index.html")

# =====================================================
# PREDIKSI
# =====================================================

@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return jsonify({
            "success": False,
            "message": "Tidak ada gambar yang dipilih."
        })

    file = request.files["image"]

    if file.filename == "":
        return jsonify({
            "success": False,
            "message": "Nama file kosong."
        })

    # Membuat nama file unik
    filename = f"{uuid.uuid4().hex}.jpg"

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    try:

        hasil = predictor.predict(filepath)

        return jsonify({
            "success": hasil["success"],
            "label": hasil["label"],
            "confidence": hasil["confidence"],
            "distance": hasil["jarak_meter"]
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        })

# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":

    import os

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )