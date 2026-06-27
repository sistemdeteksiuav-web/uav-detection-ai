# UAV Detection AI System

## Struktur Project

```
UAV_AI_WEB/
├── app.py
├── predictor.py
├── requirements.txt
├── model/
│   ├── model_klasifikasi.keras   ← TARUH MODEL KAMU DI SINI
│   └── model_regresi.keras       ← TARUH MODEL KAMU DI SINI
├── templates/
│   └── index.html
└── static/
    ├── css/style.css
    ├── js/script.js
    ├── img/logo.png
    └── upload/                   ← Gambar upload disimpan di sini
```

---

## Cara Menjalankan

### 1. Install dependensi

```bash
pip install -r requirements.txt
```

### 2. Taruh file model

Salin kedua file model ke dalam folder `model/`:
- `model/model_klasifikasi.keras`
- `model/model_regresi.keras`

### 3. Jalankan server

```bash
python app.py
```

### 4. Buka browser

```
http://127.0.0.1:5000
```

---

## Spesifikasi Model yang Didukung

| Model | Input | Output |
|-------|-------|--------|
| Klasifikasi | 128×128×3 | Dense(1, sigmoid) |
| Regresi | 128×128×3 | Dense(1, linear) — meter |

- Sigmoid ≥ 0.5 → **UAV**
- Sigmoid < 0.5 → **NON UAV**
- Model regresi hanya dijalankan jika hasil klasifikasi adalah UAV

---

## Format Gambar yang Didukung

JPG, JPEG, PNG, BMP, WEBP — maksimal 10 MB
