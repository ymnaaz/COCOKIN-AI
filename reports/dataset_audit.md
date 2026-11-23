# 5. Laporan Audit Dataset & Notebook AI (`dataset_audit.md`)

**Tanggal Audit:** 23 November 2026  
**Cakupan:** Seluruh dataset dan notebook di `D:\Semester 5\IPPL\COCOKIN-AI` serta `COCOKIN\lib\backend\cocokin_ai_training.py`  
**Status:** Audit Selesai — Ditemukan Masalah Kritis (*Data Leakage*, Konflik Label, dan Batasan Lisensi)

---

## 1. Ringkasan Sumber Data yang Tersedia di `COCOKIN-AI`

Saat ini terdapat **4 sumber data/script** di dalam workspace:

| No | Nama Folder / File | Jumlah File | Target Label | Status Kelayakan untuk Training Personal Color |
|---|---|---|---|---|
| 1 | `personal color.v1i.multiclass/` | **531 foto** (456 train, 50 valid, 25 test) | 4 Musim (`fall`, `spring`, `summer`, `winter`) | ⚠️ **TIDAK LAYAK LANGSUNG** — Mengandung *data leakage* parah (43 foto dasar bocor lintas split) dan **67 dari 93 foto dasar memiliki label konflik**! |
| 2 | `images/` + CSV Splits (`images_train_test_splits` & `individuals_train_test_splits`) | **14.278 foto wajah** & **14.205 foto kulit** | Skala Warna Kulit **1 s/d 10** (Monk Skin Tone) | ✅ **LAYAK UNTUK MODEL SKIN TONE** — Memiliki split berbasis individu (`individuals_train_test_splits`) yang bebas leakage, tetapi **bukan** dataset *Seasonal Personal Color* (Spring/Summer/Autumn/Winter). |
| 3 | `mst-e_data/` (Google & TONL) | **1.515 foto** & 31 video (19 subjek) | Skala Monk Skin Tone (1–10) | ❌ **DILARANG UNTUK TRAINING ML** — Lisensi resmi di `README.md` melarang penggunaan foto untuk melatih model Machine Learning. |
| 4 | `Cocokin_AI_Training.ipynb` & `cocokin_ai_training.py` | **16 foto Unsplash** (notebook) / **Data Acak** (`.py`) | `Warm Autumn`, `Cool Summer`, `Warm Spring`, `Cool Winter` | ⚠️ **HANYA PROTOTIPE KODE** — Mengandung *data leakage* karena augmentasi 15x dilakukan sebelum `train_test_split`. |

---

## 2. Temuan Audit Mendalam per Dataset

### A. Dataset 1: `personal color.v1i.multiclass` (Roboflow)

- **Asal & Lisensi:** Export Roboflow (6 Juni 2022), Lisensi `CC BY 4.0`, ukuran gambar `416x416` (stretch), pre-augmentation Roboflow 3x (*Random brightness -25% to +25%*).
- **Distribusi Kelas pada File `_classes.csv`:**

| Split | `fall` (Autumn) | `spring` | `summer` | `winter` | Total Baris |
|---|---|---|---|---|---|
| **Train** | 137 | 162 | 52 | 105 | **456** |
| **Valid** | 11 | 20 | 7 | 12 | **50** |
| **Test** | 7 | 11 | 3 | 4 | **25** |
| **Total** | **155 (29.2%)** | **193 (36.3%)** | **62 (11.7%)** | **121 (22.8%)** | **531** |

- **Temuan Kritis 1 — Jumlah Foto Unik Sangat Sedikit & Terjadi *Data Leakage* Lintas Split:**
  - Dari 531 file gambar (`imgXX_jpg.rf.<hash>.jpg`), hanya terdapat **93 ID foto dasar (`base_id`) yang unik**.
  - Sebanyak **43 dari 93 foto dasar tersebut muncul di lebih dari satu split** (misalnya versi pertama ada di `train`, versi keduanya ada di `valid` atau `test`).
- **Temuan Kritis 2 — Konflik Label yang Masif (67 dari 93 Prefix Nama File):**
  - Sebanyak **67 dari 93 prefix nama file (`imgXX_jpg`) memiliki label musim yang berbeda-beda** di dalam CSV!
  - Contoh nyata dari hasil pemeriksaan `_classes.csv`:
    - `img25_jpg`: muncul di `train` sebagai `winter` (3x), di `valid` sebagai `fall` (1x), dan di `test` sebagai `spring` (1x).
    - `img13_jpg`: muncul 12 kali di `train` dengan keempat label sekaligus (`winter`, `spring`, `fall`, `summer`).
    - `img100_jpg`: muncul di `train` sebagai `fall` (3x), tetapi di `valid` sebagai `spring` (1x).
  - **Penyebab:** Pembuat dataset di Roboflow menamai ulang gambar dari berbagai folder kelas menggunakan penomoran urut (`img1.jpg`, `img2.jpg`, dst.) sebelum digabung, sehingga beberapa orang berbeda memiliki prefix `img13_jpg`, **ATAU** satu foto yang sama dilabeli secara tidak konsisten, lalu di-augmentasi dan di-split secara acak oleh Roboflow setelah augmentasi.
  - **Tindakan yang Diperlukan:** Perlu dilakukan pengecekan kemiripan visual (*perceptual hash / image similarity*) pada ke-531 gambar untuk memisahkan mana gambar yang benar-benar orang berbeda dengan nama prefix sama, dan mana gambar duplikat/augmentasi dari foto yang sama.

---

### B. Dataset 2: `images/` (Klasifikasi Warna Kulit Kelas 1–10)

- **Asal Data:** Gabungan gambar wajah ter-crop dari dataset publik **LFW**, **FairFace**, dan **CASIA-Face-Africa** yang telah dipetakan ke dalam **10 kelas skala warna kulit (Kelas 1 s/d 10)**.
- **Dua Variasi Gambar yang Tersedia:**
  1. `all_cropped_images_by_class/` (**14.278 gambar** potongan wajah)
  2. `all_cropped_skin_only_images/` (**14.205 gambar** wajah yang sudah di-masking sehingga hanya menyisakan piksel kulit, background hitam)
- **Distribusi Kelas:**

| Kelas (Skala 1–10) | `all_cropped_images_by_class` | `all_cropped_skin_only_images` | Persentase | Kategori Skin Tone COCOKIN (Usulan Pemetaan) |
|---|---|---|---|---|
| **Kelas 1** | 1.298 | 1.298 | 9.1% | **Light** (Kelas 1–3: 77.6%) |
| **Kelas 2** | 5.685 | 5.673 | 39.8% | **Light** |
| **Kelas 3** | 4.104 | 4.086 | 28.7% | **Light** |
| **Kelas 4** | 1.464 | 1.443 | 10.3% | **Medium** (Kelas 4–7: 21.3%) |
| **Kelas 5** | 945 | 938 | 6.6% | **Medium** |
| **Kelas 6** | 454 | 442 | 3.2% | **Medium** |
| **Kelas 7** | 182 | 179 | 1.3% | **Medium** |
| **Kelas 8** | 81 | 81 | 0.6% | **Deep** (Kelas 8–10: 1.0%) |
| **Kelas 9** | 43 | 43 | 0.3% | **Deep** |
| **Kelas 10** | 22 | 22 | 0.2% | **Deep** |
| **Total** | **14.278** | **14.205** | **100%** | — |

- **Ketersediaan Split Bebas Leakage:**
  - Folder `individuals_train_test_splits-20261123T120121Z-1-001` sudah menyediakan `train.csv`, `test.csv`, `holdout_train.csv`, `holdout_val.csv`, serta 5-Fold Stratified K-Fold (`SKF_TRAIN_Fold_1..5.csv`) yang dikelompokkan berdasarkan **identitas orang (`tokens` / `new_tokens`)** sehingga foto dari individu yang sama di LFW atau CASIA-Face-Africa tidak bocor antar split.
- **Kelemahan Dataset 2:**
  - Ketimpangan kelas (*class imbalance*) sangat tinggi: Kelas 2 dan 3 mendominasi (>68%), sedangkan Kelas 8, 9, dan 10 sangat sedikit (total hanya 146 foto).
  - Dataset ini hanya memiliki label **Skin Tone (1–10)**, tidak memiliki label **Undertone** (`Warm`/`Cool`) maupun **Personal Color** (`Spring`/`Summer`/`Autumn`/`Winter`).

---

### C. Dataset 3: `mst-e_data/` (Monk Skin Tone Examples)

- **Isi:** 1.515 foto dan 31 video dari 19 subjek (`subject_0` s/d `subject_18`) beserta detail pencahayaan dan pose di `mst-e_image_details.csv`.
- **Status Lisensi (KRITIS):**
  - Kutipan langsung dari [mst-e_data/mst-e_data/README.md](file:///D:/Semester%205/IPPL/COCOKIN-AI/mst-e_data/mst-e_data/README.md#L7):
    > *"TONL has given permission for these images to be released and used for research or human-annotator-training purposes only. **The images cannot be used to train machine learning models.**"*
- **Kesimpulan Audit:** Dataset `mst-e_data` **wajib dikecualikan dari seluruh proses training Machine Learning**.

---

### D. Notebook `Cocokin_AI_Training.ipynb` & `cocokin_ai_training.py`

1. **`COCOKIN/lib/backend/cocokin_ai_training.py`:**
   - Membangkitkan 1.000 baris angka acak (`np.random.normal`) untuk fitur `[R, G, B, H, S, V, L, a, b]` tanpa membaca gambar sama sekali. Tidak boleh digunakan sebagai model produksi.
2. **`COCOKIN-AI/Cocokin_AI_Training.ipynb`:**
   - Mengunduh 16 foto dari URL Unsplash (4 foto per kelas: `Warm Autumn`, `Cool Summer`, `Warm Spring`, `Cool Winter`).
   - Mengekstrak ROI persegi di tengah wajah menggunakan MediaPipe Face Detection (`roi_x = x + 0.35*bw`, `roi_y = y + 0.4*bh`, lebar `0.3*bw`, tinggi `0.2*bh`) — area tengah wajah (`0.35..0.65` horizontal, `0.4..0.6` vertikal) sebenarnya jatuh tepat di area **hidung dan sekitar lubang hidung/kumis**, bukan pipi murni, sehingga rentan terkena bayangan hidung.
   - **Data Leakage pada Augmentasi (Baris 187–218):**
     - Dari 16 foto asli, setiap baris fitur diduplikasi 15 kali dengan `np.random.normal(0, 2.5)` menjadi 256 baris, **lalu baru di-split** dengan `train_test_split(test_size=0.2)`.
     - Akibatnya, setiap wajah di data `X_test` memiliki ~12 kembaran identik (hanya beda noise ±2.5 piksel) di dalam `X_train`.

---

## 3. Rekomendasi Arsitektur AI & Solusi Dataset untuk COCOKIN

Mengingat kondisi dataset yang ditemukan di atas, berikut adalah rekomendasi arsitektur paling realistis, jujur secara akademis (untuk mata kuliah IPPL & PCD), dan kuat secara teknis:

### Rekomendasi 1: Pisahkan Estimasi **Skin Tone** dan Klasifikasi **Personal Color / Undertone**
1. **Model / Modul 1 — Skin Tone Estimator (`Light`, `Medium`, `Deep` + `skinToneHex`):**
   - Dapat dilatih/divalidasi menggunakan fitur warna kulit (RGB, HSV, CIE-LAB + Individual Typology Angle / ITA) dari dataset **`images/all_cropped_skin_only_images`** menggunakan split resmi di `individuals_train_test_splits` (dengan *class weighting* atau *undersampling* pada kelas 2 & 3 agar seimbang).
   - Rata-rata nilai RGB kulit yang terekstrak dari wajah pengguna juga langsung dikonversi menjadi `skinToneHex` nyata (bukan lagi hex statis `0xFF8C6258`).
2. **Model / Modul 2 — Undertone & Personal Color Classifier (`Warm Spring`, `Cool Summer`, `Warm Autumn`, `Cool Winter`):**
   - Gunakan dataset **`personal color.v1i.multiclass`** **HANYA SETELAH** dilakukan deduplikasi visual (*perceptual hashing*) untuk membuang duplikat augmentasi Roboflow dan melakukan *re-splitting* dari foto unik yang bebas konflik label.
   - Ekstrak fitur warna dari beberapa ROI kulit bersih (pipi kiri, pipi kanan, dahi menggunakan landmark wajah MediaPipe) dalam ruang warna **CIE-LAB (`L*`, `a*`, `b*`) dan HSV**, karena komponen `b*` (biru-kuning), `a*` (hijau-merah), `S` (saturasi), dan `L*` (kecerahan) berkaitan langsung dengan sumbu *Warm vs Cool* dan *Spring/Autumn vs Summer/Winter*.

---

## 4. Hal yang Membutuhkan Keputusan Pengguna (Sebelum Melangkah ke Tahap Berikutnya)

Sesuai **Bagian 37–39** dokumen rencana pengembangan, saya **berhenti di sini (tidak mengubah kode aplikasi dan tidak melakukan training)** dan meminta keputusan/persetujuan Anda untuk 4 hal berikut:

1. **Pembersihan Dataset `personal color.v1i.multiclass`:**
   - Apakah Anda setuju saya membuat script audit/deduplikasi visual (tanpa menghapus file asli, melainkan membuat manifest bersih di `COCOKIN-AI/dataset/manifests/`) untuk memisahkan foto unik dari 531 foto Roboflow dan membuang gambar yang labelnya konflik?
2. **Pemanfaatan Dataset `images/all_cropped_skin_only_images` (Kelas 1–10):**
   - Apakah Anda setuju dataset 10 kelas ini kita pakai untuk melatih modul **Skin Tone (`Light`, `Medium`, `Deep`)** dengan pemetaan: Kelas 1–3 = `Light`, Kelas 4–7 = `Medium`, Kelas 8–10 = `Deep`?
3. **Skema Target Personal Color untuk MVP:**
   - Apakah untuk MVP ini kita fokus pada **4 kelas utama** yang selaras dengan aplikasi saat ini (`Warm Spring`, `Cool Summer`, `Warm Autumn`, `Cool Winter`), sambil melengkapi 2 profil yang belum ada di `AnalysisController` (`Warm Spring` & `Cool Winter`) dan menambah katalog produk di `db.json`?
4. **Jalur Backend yang Akan Diintegrasikan dengan Flutter:**
   - Saat ini `ApiService` di Flutter mengarah ke **Supabase Cloud**, sedangkan `server.dart` menjalankan **Pure Dart Backend (`db.json`)** di `localhost:5000`. Untuk integrasi AI nanti, apakah aplikasi Flutter akan diarahkan ke **Backend Lokal (`server.dart` + Python AI Service)** atau tetap menggunakan **Supabase + Python AI Service**?
