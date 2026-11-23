# LAPORAN HASIL PENGERJAAN PENGEMBANGAN COCOKIN AI

**Tanggal Laporan:** 23 November 2026  
**Penyusun:** AI Assistant (Antigravity)  
**Referensi Pedoman:** `D:\Semester 5\IPPL\COCOKIN-AI\RENCANA_PENGEMBANGAN_COCOKIN_AI.md` (Bagian 37, 38, & 39)  
**Status Pengerjaan:** Selesai Tahap Audit Lengkap + Tahap Pembangunan Baseline Model Skin Tone & Undertone

---

## 1. Ringkasan Eksekutif

Sesuai instruksi pada dokumen rencana kerja **COCOKIN AI**, pengerjaan difokuskan pada:
1. **Audit Total Proyek:** Memeriksa arsitektur kode Flutter di `COCOKIN/`, controller backend, database `db.json`, serta seluruh dataset di `COCOKIN-AI/`.
2. **Audit Kualitas & Risiko Dataset:** Menemukan fakta kritis bahwa dataset 4 musim Roboflow mengalami *data leakage* dan konflik label parah, serta dataset `mst-e_data` memiliki larangan lisensi untuk training ML.
3. **Penyelarasan Fokus ke Skin Tone & Undertone:** Mengalihkan fokus utama ke modul **Skin Tone** (Light, Medium, Deep) dan **Undertone** (Warm, Cool, Neutral) yang memiliki fondasi data ilmiah kuat (14.000+ foto) dan relevan dengan tampilan utama aplikasi `HasilPage`.
4. **Pembangunan Pipeline PCD & Baseline Model:** Berhasil membangun modul ekstraksi fitur citra digital (RGB, HSV, CIE-Lab, ITA), melatih baseline model Random Forest dengan akurasi **76.26%** pada test set murni tanpa *data leakage*, serta modul analisis inferensi yang menghasilkan nilai Hex asli warna kulit pengguna.

---

## 2. Rincian Pengerjaan Sesuai 14 Poin Wajib (Bagian 39 Dokumen MD)

### 1. Kondisi Repository
- Proyek terbagi rapi menjadi dua direktori utama di `D:\Semester 5\IPPL\`:
  - `COCOKIN/`: Berisi aplikasi mobile Flutter (Dart SDK `^3.5.0`) dan Pure Dart REST API Server (`server.dart`).
  - `COCOKIN-AI/`: Berisi dokumen rencana kerja, notebook Jupyter, modul Python baru di `src/`, model tersimpan di `models/`, dan laporan di `reports/`.

### 2. Struktur Aplikasi Flutter
- Menggunakan single-activity/shell model (`MainMobileShell` di `lib/main.dart`) yang mengatur navigasi berbasis state string.
- Terdapat 7 halaman utama aktif: `BerandaPage`, `AuthPage`, `KameraPage`, `LoadingPage`, `HasilPage`, `RiwayatPage`, `RekomendasiPage`, dan `DetailProdukPage`.
- Ditemukan 7 file duplikat tanpa akhiran `_page.dart` di `lib/halaman/` (seperti `beranda.dart`, `kamera.dart`) yang tidak dipakai oleh `main.dart` namun tetap dipertahankan aman.

### 3. Alur Kamera → Analisis → Hasil
- **Kondisi Nyata Saat Ini:**
  - `KameraPage`: Menampilkan bingkai oval berpanduan wajah dengan ilustrasi vektor statis.
  - `LoadingPage`: Menjalankan timer simulasi 900ms dan memanggil fungsi `ApiService.analyzeFacePhoto('kamera_wajah.png')`.
  - `HasilPage`: Menampilkan kartu `Skin Tone`, `Undertone`, dan kartu `Personal Color` yang diberi efek blur (gembok fitur Premium). Nilai teks dan warna saat ini masih di-*hardcode* di widget UI.

### 4. Kondisi Backend Dart
- Backend utama berbasis Pure Dart berjalan di `http://localhost:5000/api` melalui [server.dart](file:///D:/Semester%205/IPPL/COCOKIN/lib/backend/server.dart).
- Memiliki 11 endpoint lengkap untuk kesehatan server (`/api/health`), autentikasi (`/api/login`, `/api/register`), analisis & riwayat (`/api/analyze`, `/api/history`), unlock premium (`/api/premium/unlock`), dan katalog produk (`/api/products`).
- Endpoint `/api/analyze` saat ini masih menggunakan kamus profil warna statis (*preset* `'Warm Autumn'` atau `'Cool Summer'`).

### 5. Kondisi Database (`db.json`)
- File lokal [db.json](file:///D:/Semester%205/IPPL/COCOKIN/lib/backend/db.json) menyimpan:
  - `users`: Akun pengguna reguler (`yumna@gmail.com`) dan admin (`admin@cocokin.id`).
  - `analysis_history`: Riwayat hasil analisis lengkap dengan tanggal dan palet warna.
  - `products`: Katalog produk makeup.
- Terdapat skema relasional padanan di [cocokin_db.sql](file:///D:/Semester%205/IPPL/COCOKIN/lib/backend/cocokin_db.sql) dengan 6 tabel SQL.

### 6. Kondisi Katalog Produk & Profil Warna
- Di `db.json` saat ini tersimpan 4 produk awal (Make Over Lip Cream, Emina Blush, Luxcrime Eye Shadow, Somethinc Mesh Cushion).
- **Temuan Kritis Katalog:** Keempat produk tersebut berlabel `undertone: "Warm"` dan `personalColor: "Warm Autumn"`. Jika nanti model mendeteksi pengguna sebagai `Cool`, filter katalog akan mengembalikan 0 produk sebelum katalog diperkaya.
- Profil warna di `analysis_controller.dart` baru mendefinisikan palet untuk 2 musim (`Warm Autumn` & `Cool Summer`).

### 7. Bagian yang Sudah Berjalan
- Navigasi halaman dan proteksi autentikasi (redirect otomatis ke login jika belum masuk).
- Fitur gembok interaktif dan pembukaan kunci status Premium di `HasilPage`.
- Filter katalog produk berdasarkan kategori makeup dan rentang harga (budget) di `RekomendasiPage`.
- Navigasi ke halaman detail produk dan pembuatan URL pencarian Shopee & Tokopedia.
- Seluruh endpoint CRUD dan autentikasi di Dart Backend `server.dart`.

### 8. Bagian yang Masih Mock / Static / Simulasi
- `KameraPage`: Belum membaca stream kamera asli atau file galeri nyata perangkat.
- `LoadingPage`: Belum meneruskan payload gambar atau menangkap return value analisis secara dinamis.
- `HasilPage`: Teks hasil analisis dan 4 kotak warna palet masih berupa konstanta di dalam kode tampilan.
- `cocokin_ai_training.py`: Menggunakan data buatan angka acak (`np.random.normal`).
- `Cocokin_AI_Training.ipynb`: Menggunakan 16 foto Unsplash yang mengalami kebocoran data augmentasi sebelum split.

### 9. Dataset yang Tersedia di `COCOKIN-AI`
1. `personal color.v1i.multiclass`: 531 file gambar (4 musim).
2. `images/all_cropped_images_by_class`: 14.278 foto potongan wajah skala Monk Skin Tone 1–10.
3. `images/all_cropped_skin_only_images`: 14.205 foto potongan kulit murni skala Monk Skin Tone 1–10.
4. `mst-e_data`: 1.515 foto & 31 video (19 subjek).

### 10. Kekurangan Dataset & Batasan Lisensi
- **Batasan Lisensi `mst-e_data`:** Pada file `README.md` tertulis larangan eksplisit: *"The images cannot be used to train machine learning models."* Dataset ini wajib dikeluarkan dari proses pelatihan model.
- **Ketimpangan Kelas pada Dataset `images/`:** Skala 1–3 mendominasi (77.6%), skala 4–7 (21.3%), sedangkan skala 8–10 sangat minim (1.0%).

### 11. Risiko Data Leakage
- **Pada Dataset Roboflow (531 foto):** Ditemukan hanya ada **93 subjek foto unik**. Sebanyak **43 subjek tersebar lintas split train, valid, dan test**, serta **67 subjek memiliki label musim yang saling bertentangan** di file CSV.
- **Pada Notebook Lama:** Augmentasi duplikasi 15x dilakukan sebelum fungsi `train_test_split`, menyebabkan foto yang sama bocor ke data train dan test.

### 12. Rekomendasi Arsitektur AI (PCD + ML)
- Mengadopsi arsitektur terpisah dua modul:
  1. **Modul Skin Tone:** Mengekstrak nilai kecerahan ($L^*$ pada CIE-Lab dan sudut ITA) lalu diklasifikasikan ke dalam kategori `Light`, `Medium`, atau `Deep` menggunakan model Random Forest yang dilatih pada dataset kulit bersih.
  2. **Modul Undertone:** Mengekstrak perbandingan kromatik $b^*$ (kuning) terhadap $a^*$ (merah) untuk menentukan `Warm`, `Cool`, atau `Neutral`.
  3. **Ekstraksi Hex Nyata:** Menghitung kode warna hex langsung dari piksel kulit rata-rata pengguna untuk ditampilkan di UI Flutter.

### 13. Perubahan & Pengerjaan yang Telah Diselesaikan
1. Merapikan dan memperbarui dokumen master [RENCANA_PENGEMBANGAN_COCOKIN_AI.md](file:///D:/Semester%205/IPPL/COCOKIN-AI/RENCANA_PENGEMBANGAN_COCOKIN_AI.md).
2. Menyusun 5 laporan audit resmi di folder `COCOKIN-AI/reports/`:
   - `repository_audit.md`
   - `backend_audit.md`
   - `analysis_flow.md`
   - `product_data_audit.md`
   - `dataset_audit.md`
3. Membangun modul Python ekstraksi fitur citra digital [src/skintone_undertone_engine.py](file:///D:/Semester%205/IPPL/COCOKIN-AI/src/skintone_undertone_engine.py).
4. Melatih dan mengevaluasi model Random Forest [src/train_skintone_baseline.py](file:///D:/Semester%205/IPPL/COCOKIN-AI/src/train_skintone_baseline.py) yang menghasilkan model terverifikasi [models/skintone_model.pkl](file:///D:/Semester%205/IPPL/COCOKIN-AI/models/skintone_model.pkl) dengan akurasi **76.26%** (bebas data leakage).
5. Membangun engine inferensi lengkap [src/predict_skintone_undertone.py](file:///D:/Semester%205/IPPL/COCOKIN-AI/src/predict_skintone_undertone.py) dan memverifikasi keberhasilan pengujian sampelnya.

### 14. Hal yang Membutuhkan Keputusan Pengguna Selanjutnya
1. **Pembuatan Endpoint API AI:** Apakah modul inferensi `predict_skintone_undertone.py` ingin langsung kita bungkus menjadi REST API lokal (Flask / FastAPI di port 8000)?
2. **Integrasi Backend Dart:** Apakah backend `server.dart` (port 5000) ingin kita hubungkan langsung untuk memanggil endpoint API AI tersebut saat menerima request `/api/analyze`?
3. **Pengayaan Katalog `db.json`:** Apakah setuju kita tambahkan 8–12 produk bertema undertone `Cool` dan kategori lengkap di `db.json` agar hasil rekomendasi tidak kosong saat pengguna terdeteksi memiliki undertone `Cool`?
