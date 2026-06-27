import os
import numpy as np
import cv2
import tensorflow as tf


class UAVPredictor:
    IMG_SIZE = (128, 128)

    def __init__(self, classify_model_path: str, regress_model_path: str):
        self._classify_model = None
        self._regress_model  = None
        self._classify_path  = classify_model_path
        self._regress_path   = regress_model_path
        self._load_models()

    def _load_models(self):
        if os.path.exists(self._classify_path):
            self._classify_model = tf.keras.models.load_model(
                self._classify_path, compile=False
            )
            print(f"[OK] Model klasifikasi loaded: {self._classify_path}")
        else:
            print(f"[!!] TIDAK DITEMUKAN: {self._classify_path}")

        if os.path.exists(self._regress_path):
            self._regress_model = tf.keras.models.load_model(
                self._regress_path, compile=False
            )
            print(f"[OK] Model regresi loaded: {self._regress_path}")
        else:
            print(f"[!!] TIDAK DITEMUKAN: {self._regress_path}")

    def _preprocess(self, image_path: str) -> np.ndarray:
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Gambar tidak dapat dibaca: {image_path}")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, self.IMG_SIZE)
        img = img.astype(np.float32) / 255.0
        img = np.expand_dims(img, axis=0)
        return img

    def predict(self, image_path: str) -> dict:
        if self._classify_model is None:
            return {"success": False, "error": "Model klasifikasi belum di-load."}

        try:
            img = self._preprocess(image_path)
        except ValueError as e:
            return {"success": False, "error": str(e)}

        # ── Klasifikasi ──────────────────────────────────────────
        raw        = self._classify_model.predict(img, verbose=0)
        sigmoid_val = float(raw[0][0])

        # UAV = 1, NON UAV = 0  →  sigmoid >= 0.5 → UAV
        is_uav     = sigmoid_val >= 0.5

        # Confidence = probabilitas kelas yang diprediksi
        # Jika UAV   → confidence = sigmoid_val         (seberapa yakin = UAV)
        # Jika NON UAV → confidence = 1 - sigmoid_val  (seberapa yakin = NON UAV)
        confidence = sigmoid_val if is_uav else (1.0 - sigmoid_val)
        label      = "UAV" if is_uav else "NON UAV"

        print(f"[PREDICT] file={image_path} | sigmoid={sigmoid_val:.6f} | label={label} | conf={confidence*100:.2f}%")

        # ── Regresi jarak (hanya jika UAV) ──────────────────────
        jarak = None
        if is_uav and self._regress_model is not None:
            raw_dist = self._regress_model.predict(img, verbose=0)
            jarak    = round(float(raw_dist[0][0]), 2)
            print(f"[REGRESI] estimasi jarak = {jarak} m")

        return {

    "success": True,

    "label": label,

    "is_uav": is_uav,

    "confidence": round(confidence * 100, 2),

    "sigmoid_raw": round(sigmoid_val, 6),

    "jarak_meter": jarak,

}