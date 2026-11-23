# 🎨 COCOKIN-AI — Personal Color, Skin Tone & Undertone AI Service

Repository khusus pengembangan komponen **Artificial Intelligence (AI)** dan **Pengolahan Citra Digital (PCD)** untuk aplikasi mobile **COCOKIN** ([ymnaaz/COCOKIN](https://github.com/ymnaaz/COCOKIN)).

---

## 📂 Struktur Repository

```text
COCOKIN-AI/
├── RENCANA_PENGEMBANGAN_COCOKIN_AI.md   # Dokumen master rencana pengembangan & arsitektur AI
├── Cocokin_AI_Training.ipynb            # Notebook eksplorasi & eksperimen awal
├── requirements.txt                     # Daftar pustaka Python yang dibutuhkan
│
├── src/                                 # Source code utama AI Engine & REST API
│   ├── skintone_undertone_engine.py     # Ekstraksi fitur kulit (RGB, HSV, CIE-L*a*b*, ITA) & Undertone
│   ├── train_skintone_baseline.py       # Script training & evaluasi model Random Forest Skin Tone
│   ├── predict_skintone_undertone.py    # Kelas CocokinSkinAnalyzer untuk inferensi foto
│   └── ai_server.py                     # HTTP REST API Server (Port 8000: /health, /model-info, /predict)
│
├── models/
│   └── skintone_model.pkl               # Model Random Forest terlatih untuk klasifikasi Skin Tone
│
├── reports/                             # Laporan hasil audit & evaluasi model
│   ├── repository_audit.md
│   ├── backend_audit.md
│   ├── analysis_flow.md
│   ├── product_data_audit.md
│   ├── dataset_audit.md
│   ├── baseline_skintone_report.md
│   └── laporan_hasil_pengerjaan.md
│
├── images_train_test_splits-.../        # Manifest CSV pembagian train/val/test berbasis gambar
└── individuals_train_test_splits-.../   # Manifest CSV pembagian train/val/test berbasis individu (leak-free)
```

---

## 🚀 Cara Menjalankan AI Server

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Jalankan server AI (Port 8000):**
   ```bash
   python src/ai_server.py
   ```

3. **Endpoint yang tersedia:**
   - `GET http://localhost:8000/health` — Cek status server & model
   - `GET http://localhost:8000/model-info` — Informasi fitur dan target prediksi model
   - `POST http://localhost:8000/predict` — Analisis foto wajah (`imageBase64` / `imagePath` / `sampleKey`)
