# COCOKIN AI — Rencana Pengembangan, Data Training, dan Integrasi Aplikasi

**Dokumen kerja untuk pengembangan COCOKIN**  
**Tanggal:** 23 November 2026  
**Basis:** Repository `COCOKIN` (Flutter & Dart Backend) + Workspace `COCOKIN-AI` (Dataset & Eksperimen AI)  
**Status:** Rencana pengembangan — belum melakukan training final atau perubahan kode aplikasi

---

## 0. Tujuan dokumen

Dokumen ini menjadi acuan kerja untuk mengembangkan **COCOKIN** dari aplikasi mobile Personal Color Analysis dan rekomendasi makeup menjadi aplikasi yang memiliki komponen AI yang benar-benar dapat melakukan analisis warna kulit (*skin tone*) dan warna personal (*personal color*) dari foto pengguna.

Dokumen ini dibuat dengan prinsip:

1. Memahami aplikasi dan struktur yang sudah ada di folder `COCOKIN` dan `COCOKIN-AI` sebelum mengubah kode.
2. Mengumpulkan dan mengaudit data yang sudah ada di `COCOKIN-AI` sebelum melakukan training model final.
3. Memisahkan **model AI**, **database produk (`db.json`)**, dan **recommendation engine**.
4. Tidak menganggap hasil analisis preset/simulasi saat ini sebagai hasil model AI sebelum model benar-benar tersedia dan dievaluasi.
5. Menjaga agar fitur lama di aplikasi Flutter tetap berjalan selama pengembangan AI.
6. Membuat setiap tahap dapat diuji dan dikembalikan jika terjadi masalah.

---

# 1. Gambaran COCOKIN

## 1.1 Deskripsi aplikasi

**COCOKIN** adalah aplikasi mobile **Personal Color Analysis & Rekomendasi Makeup**.

Tujuan utama aplikasi:

> Membantu pengguna mengetahui *skin tone*, *undertone*, dan *personal color* berdasarkan foto wajah, kemudian memberikan rekomendasi palet warna dan produk makeup yang sesuai dengan hasil analisis serta mempertimbangkan budget pengguna.

Repository aplikasi saat ini menggunakan Flutter dengan backend Pure Dart REST API dan sudah memiliki alur utama:

```text
Beranda
   ↓
Masuk / Daftar
   ↓
Ambil Foto Wajah
   ↓
Proses Analisis
   ↓
Hasil Analisis (Skin Tone, Undertone, Personal Color & Palet)
   ↓
Rekomendasi Makeup (Filter Kategori & Budget)
   ↓
Detail Produk & Pilihan Shade
   ↓
Tautan E-Commerce (Shopee & Tokopedia)
```

Aplikasi juga memiliki riwayat hasil analisis (`analysis_history`), fitur buka kunci **Cocokin Premium**, dan halaman **Admin CRUD Produk**.

---

# 2. Kondisi workspace dan aplikasi saat ini

Saat ini ruang kerja (*workspace*) terbagi menjadi **dua direktori utama** di `D:\Semester 5\IPPL\`:

1. **`COCOKIN/`** — Repository utama aplikasi Flutter dan Pure Dart REST API Backend.
2. **`COCOKIN-AI/`** — Workspace khusus eksperimen Machine Learning, notebook training, dan kumpulan dataset.

## 2.1 Struktur folder `COCOKIN/` (Aplikasi & Backend)

```text
COCOKIN/
├── lib/
│   ├── main.dart
│   │
│   ├── halaman/
│   │   ├── beranda_page.dart        (serta beranda.dart)
│   │   ├── auth_page.dart           (serta auth.dart)
│   │   ├── kamera_page.dart         (serta kamera.dart)
│   │   ├── loading_page.dart        (serta loading.dart)
│   │   ├── hasil_page.dart          (serta hasil.dart)
│   │   ├── riwayat_page.dart
│   │   ├── rekomendasi_page.dart    (serta rekomendasi.dart)
│   │   └── detail_produk_page.dart  (serta detail_produk.dart)
│   │
│   ├── backend/
│   │   ├── server.dart
│   │   ├── database_helper.dart
│   │   ├── auth_controller.dart
│   │   ├── analysis_controller.dart
│   │   ├── product_controller.dart
│   │   ├── db.json
│   │   ├── cocokin_db.sql
│   │   └── cocokin_ai_training.py
│   │
│   ├── services/
│   │   └── api_service.dart
│   │
│   └── models/
│       └── product_model.dart
│
├── test/
└── pubspec.yaml
```

## 2.2 Struktur folder `COCOKIN-AI/` (Dataset & Eksperimen AI)

```text
COCOKIN-AI/
├── Cocokin_AI_Training.ipynb
├── personal color.v1i.multiclass/
│   ├── train/ (+ _classes.csv)
│   ├── valid/ (+ _classes.csv)
│   ├── test/  (+ _classes.csv)
│   ├── README.dataset.txt
│   └── README.roboflow.txt
├── images/
│   └── images/
│       ├── all_cropped_images_by_class/ (Kelas 1 s/d 10)
│       └── all_cropped_skin_only_images/ (Kelas 1 s/d 10)
├── images_train_test_splits-20261123T120118Z-1-001/
├── individuals_train_test_splits-20261123T120121Z-1-001/
└── mst-e_data/
```

## 2.3 Fungsi utama komponen aplikasi

| Komponen | Fungsi |
|---|---|
| `kamera_page.dart` | Mengambil/memilih foto wajah pengguna |
| `loading_page.dart` | Menampilkan proses analisis warna kulit |
| `hasil_page.dart` | Menampilkan hasil analisis (`skinTone`, `undertone`, `personalColor`, `palette`) |
| `riwayat_page.dart` | Menyimpan dan menampilkan riwayat analisis pengguna |
| `rekomendasi_page.dart` | Menampilkan rekomendasi produk makeup + filter kategori & budget |
| `detail_produk_page.dart` | Menampilkan detail produk, daftar shade (`allShades`), alasan cocok (`whyMatch`), dan tautan Shopee/Tokopedia |
| `server.dart` | HTTP Server Pure Dart (`http://localhost:5000/api`) |
| `auth_controller.dart` | Login dan registrasi pengguna & admin |
| `analysis_controller.dart` | Endpoint `/api/analyze` (saat ini masih berbasis preset `Warm Autumn` & `Cool Summer`), `/api/history`, dan `/api/premium/unlock` |
| `product_controller.dart` | Endpoint `/api/products` untuk katalog, filter kategori/undertone/budget, dan Admin CRUD produk |
| `db.json` | Penyimpanan JSON lokal untuk `users`, `analysis_history`, dan `products` |
| `api_service.dart` | Komunikasi aplikasi Flutter dengan backend Dart |
| `product_model.dart` | Model data `ProductModel` dan `AnalysisResultModel` |

**Catatan penting:** Struktur aplikasi Flutter dan Dart backend yang sudah ada harus dipertahankan sebagai fondasi. Pengembangan AI di `COCOKIN-AI` sebaiknya dihubungkan sebagai service/endpoint inferensi yang dipanggil oleh backend atau aplikasi, bukan merombak seluruh aplikasi.

---

# 3. Target pengembangan COCOKIN

Target arsitektur yang disarankan:

```text
                 ┌───────────────────┐
                 │    Foto Wajah     │
                 │   dari COCOKIN    │
                 └─────────┬─────────┘
                           ↓
                 ┌───────────────────┐
                 │ Image Preprocess  │
                 │ & Face Validation │
                 └─────────┬─────────┘
                           ↓
                 ┌───────────────────┐
                 │ AI Personal Color │
                 │  & Skin Analysis  │
                 └─────────┬─────────┘
                           ↓
      ┌────────────────────┼────────────────────┐
      ↓                    ↓                    ↓
  Skin Tone            Undertone            Season /
  (Light/Medium/       (Warm/Cool/          Subtype
   Deep + Hex)          Neutral + Hex)      (Personal Color)
      │                    │                    │
      └────────────────────┼────────────────────┘
                           ↓
                ┌────────────────────┐
                │ Recommendation     │
                │ Engine & Palette   │
                └─────────┬──────────┘
                          ↓
                ┌────────────────────┐
                │ Product Database   │
                │ (db.json)          │
                └─────────┬──────────┘
                          ↓
                ┌────────────────────┐
                │ Budget & Category  │
                │ Filter             │
                └─────────┬──────────┘
                          ↓
                ┌────────────────────┐
                │ Produk + Shade +   │
                │ Shopee/Tokopedia   │
                └────────────────────┘
```

---

# 4. Pembagian komponen AI

COCOKIN sebaiknya **tidak menggunakan satu model untuk semuanya**.

Pisahkan menjadi:

## A. Computer Vision / AI Model

Tugas:

> Mengubah foto wajah menjadi prediksi *skin tone*, *undertone*, dan *personal color*.

Contoh:

```text
Foto
→ face detection & skin ROI segmentation
→ skin/color feature extraction (RGB, HSV, CIE-LAB)
→ model
→ skinTone (Light/Medium/Deep) + skinToneHex
→ undertone (Warm/Cool/Neutral) + undertoneHex
→ season / personalColor
```

## B. Recommendation Engine

Tugas:

> Mengubah hasil personal color dan undertone menjadi palet warna referensi dan aturan rekomendasi makeup.

Contoh:

```text
Warm Autumn (Undertone: Warm, Skin Tone: Medium)
→ palet warna referensi (Deep Espresso, Warm Caramel, dll.)
→ filter produk dengan undertone/personalColor yang sesuai
→ filter kategori (Lip Product, Blush, Eye Makeup, Complexion)
```

Recommendation engine tidak harus menggunakan machine learning.

Untuk versi saat ini dan MVP, **rule-based recommendation** seperti yang sudah ada di `analysis_controller.dart` dan `product_controller.dart` lebih mudah dijelaskan, diuji, dan dikontrol.

## C. Product Database

Tugas:

> Menyimpan produk makeup yang dapat direkomendasikan di `db.json` (atau database SQL ke depannya).

Database ini bukan dataset training utama.

---

# 5. Target prediksi AI

Sebelum melatih model final, target output harus selaras dengan `AnalysisResultModel` di Flutter (`lib/models/product_model.dart`) dan `analysis_history` di `db.json`.

## 5.1 Skin Tone (Kedalaman Warna Kulit)

Untuk mendukung UI aplikasi saat ini (`skinTone` dan `skinToneHex`):

```text
Light  (atau Fair)
Medium
Deep
```

*(Opsional: Dapat dipetakan dari skala Monk Skin Tone 1–10 yang ada pada dataset `images/` di `COCOKIN-AI`, misalnya MST 1–3 = Light, MST 4–7 = Medium, MST 8–10 = Deep).*

## 5.2 Undertone

Minimal:

```text
Warm
Cool
Neutral
```

## 5.3 Seasonal Color (4 Musim Utama)

Empat kategori utama (sesuai dengan dataset `personal color.v1i.multiclass` yang memiliki label `spring`, `summer`, `fall`/`autumn`, `winter`):

```text
Spring
Summer
Autumn (Fall)
Winter
```

## 5.4 Subtype (Personal Color)

Di aplikasi COCOKIN saat ini, label `personalColor` yang digunakan pada profil warna dan katalog produk menggunakan format kombinasi *Undertone + Season* (4 kelas utama):

```text
Warm Spring
Cool Summer
Warm Autumn
Cool Winter
```

Jika dataset dan kualitas label memungkinkan pengembangan lebih lanjut, barulah diperluas ke 12-season:

```text
Light Spring, Warm Spring, Bright Spring
Light Summer, Cool Summer, Soft Summer
Soft Autumn, Warm Autumn, Deep Autumn
Deep Winter, Cool Winter, Bright Winter
```

### Catatan

Jangan langsung memaksakan model 12 kelas jika jumlah dan kualitas data belum cukup.

Tahap pengembangan yang lebih aman dan sesuai dengan kondisi aplikasi saat ini:

```text
Tahap A:
Skin Tone (Light / Medium / Deep) & Undertone (Warm / Cool / Neutral)

Tahap B:
4 Season / 4 Main Personal Colors (Warm Spring, Cool Summer, Warm Autumn, Cool Winter)

Tahap C:
12 Seasonal Subtypes (jika dataset memadai)
```

Jika hasil evaluasi tahap sebelumnya buruk, jangan melanjutkan ke tahap yang lebih kompleks sebelum penyebabnya dipahami.

---

# 6. DATA YANG HARUS DIKUMPULKAN DAN DIAUDIT

## 6.1 Dataset utama: foto wajah berlabel

Setiap data untuk training personal color minimal harus memiliki:

```text
image
skin_tone (opsional/terpisah)
undertone
season
personal_color
```

Contoh:

| image_id | skin_tone | undertone | season | personal_color |
|---|---|---|---|---|
| IMG001 | Medium | Warm | Autumn | Warm Autumn |
| IMG002 | Light | Cool | Summer | Cool Summer |
| IMG003 | Deep | Cool | Winter | Cool Winter |

**Foto tanpa label personal color yang valid tidak boleh langsung dianggap sebagai data training berlabel.**

## 6.2 Kondisi awal dataset di folder `COCOKIN-AI/` saat ini

Saat ini di dalam folder `COCOKIN-AI/` terdapat beberapa sumber data yang **wajib diaudit terlebih dahulu**:

1. **`personal color.v1i.multiclass/`** (Roboflow, 531 foto: 456 train, 50 valid, 25 test)
   - Berisi label 4 musim (`fall`, `spring`, `summer`, `winter`).
   - **Catatan Audit:** Dataset ini telah mengalami *pre-augmentation* (3 versi brightness per foto sumber) dari Roboflow. Perlu diperiksa potensi *data leakage* (foto sumber yang sama masuk ke train dan valid/test) serta konsistensi labelnya.
2. **`images/` + `images_train_test_splits` + `individuals_train_test_splits`**
   - Berisi potongan wajah (`all_cropped_images_by_class`) dan potongan kulit (`all_cropped_skin_only_images`) dari LFW, FairFace, dan CASIA-Face-Africa yang dikelompokkan ke dalam **Kelas 1 s/d 10** (skala kedalaman warna kulit / *Skin Tone*).
   - **Catatan Audit:** Dataset ini cocok untuk melatih atau memvalidasi komponen **Skin Tone (Light/Medium/Deep)**, tetapi **bukan** label *Seasonal Personal Color* (Spring/Summer/Autumn/Winter).
3. **`mst-e_data/`** (Monk Skin Tone Examples - Google & TONL, 19 subjek, 1515 foto)
   - **Catatan Audit & Lisensi:** Berdasarkan `mst-e_data/README.md`, dataset ini dilisensikan hanya untuk riset atau pelatihan annotator manusia (*"The images cannot be used to train machine learning models"*). Oleh karena itu, `mst-e_data` **tidak boleh digunakan sebagai data training ML**, maksimal hanya sebagai referensi kalibrasi visual.
4. **Script Simulasi & Sampel Web (`Cocokin_AI_Training.ipynb` & `cocokin_ai_training.py`)**
   - `cocokin_ai_training.py` menggunakan data angka acak (`np.random.normal`), sedangkan `Cocokin_AI_Training.ipynb` mengunduh 16 foto Unsplash dan melakukan augmentasi noise sebelum `train_test_split`.
   - **Catatan Audit:** Hanya boleh dianggap sebagai *proof-of-concept* kode pipeline awal, bukan model final yang valid.

---

# 7. Standar pengambilan foto

Agar model tidak belajar dari pencahayaan atau filter, foto harus memiliki standar.

## Wajib

- wajah terlihat jelas
- wajah menghadap kamera
- tidak blur
- tidak menggunakan filter
- tidak menggunakan beauty effect
- pencahayaan relatif netral
- tidak terlalu gelap atau terlalu terang
- wajah tidak tertutup masker
- wajah tidak tertutup rambut secara berlebihan
- resolusi cukup
- makeup seminimal mungkin atau dicatat dengan jelas

## Sangat disarankan

- background sederhana
- white balance relatif netral
- ekspresi natural
- jarak kamera konsisten
- tidak menggunakan lampu berwarna
- hindari foto dengan color grading

---

# 8. Metadata dataset

Selain foto dan label, simpan metadata.

Contoh struktur:

```csv
image_id,image_path,undertone,season,personal_color,skin_depth,lighting,makeup,filter,glasses,source
IMG001,images/IMG001.jpg,WARM,AUTUMN,WARM_AUTUMN,MEDIUM,NATURAL,NONE,NO,NO,SELF_COLLECTED
```

Metadata yang disarankan:

| Field | Kegunaan |
|---|---|
| `image_id` | ID unik |
| `image_path` | Lokasi foto |
| `undertone` | Label undertone |
| `season` | Label season |
| `personal_color` | Label final |
| `skin_depth` | Label kedalaman warna kulit (`LIGHT`/`MEDIUM`/`DEEP` atau skala 1–10) |
| `lighting` | Audit bias |
| `makeup` | Audit kualitas |
| `filter` | Memastikan tidak ada filter |
| `glasses` | Audit occlusion |
| `source` | Mengetahui sumber data |

Metadata tidak semuanya harus menjadi input model.

---

# 9. Data fitur warna

Jika pipeline menggunakan computer vision berbasis fitur warna (seperti yang sudah diinisiasi di `Cocokin_AI_Training.ipynb`), ekstrak fitur warna dari ROI kulit wajah.

## 9.1 RGB

```text
skin_r
skin_g
skin_b
```

## 9.2 HSV

```text
skin_h
skin_s
skin_v
```

## 9.3 LAB (CIE-L\*a\*b\*)

```text
skin_l  (Luminance -> indikator kuat untuk Skin Tone: Light/Medium/Deep)
skin_a  (Green–Red component)
skin_b  (Blue–Yellow component -> indikator kuat untuk Undertone: Cool vs Warm)
```

LAB sangat disarankan digunakan sebagai representasi warna utama karena memisahkan pencahayaan (`L*`) dari komponen kromatik warna (`a*` dan `b*`).

## 9.4 Sampling beberapa area

Jangan hanya mengambil satu pixel atau crop persegi tengah yang berisiko mengenai mata/mulut/rambut.

Gunakan landmark wajah (misalnya MediaPipe Face Mesh / Face Detection) atau mask kulit untuk mengambil area kulit yang relatif bersih:

```text
forehead
left_cheek
right_cheek
jaw
```

Kemudian gunakan statistik seperti:

```text
mean
median
standard deviation
```

Contoh:

```text
forehead_lab
left_cheek_lab
right_cheek_lab
jaw_lab

→ aggregate color features
→ model
```

---

# 10. Fitur tambahan yang dapat dieksplorasi

Jika dataset memungkinkan:

### Skin

- brightness
- saturation
- hue
- LAB (`L*`, `a*`, `b*`)
- RGB
- HSV
- ITA (Individual Typology Angle) dari nilai `L*` dan `b*` untuk estimasi *skin tone*

### Hair

- warna rambut
- brightness
- saturation

### Eyes

- warna mata
- brightness
- saturation

### Contrast

- skin vs hair
- skin vs eyes
- overall facial contrast

**Jangan menambahkan fitur hanya karena tersedia.** Setiap fitur harus diuji apakah benar membantu prediksi.

---

# 11. Sumber data training

Prioritas sumber data:

## Prioritas 1 — Data yang dikumpulkan sendiri

Paling ideal untuk COCOKIN jika dapat dilakukan dengan izin responden.

Contoh:

```text
Foto wajah
+
hasil personal color dari color analyst / annotator terlatih
```

Kelebihan:

- format foto dapat dikontrol
- kondisi pencahayaan dapat distandarkan
- label dapat disesuaikan dengan skema COCOKIN
- metadata dapat dikumpulkan sejak awal

## Prioritas 2 — Dataset publik

Boleh digunakan jika:

1. **lisensinya mengizinkan untuk training ML** (contoh: perhatikan larangan training ML pada `mst-e_data`)
2. sumber jelas
3. label dapat dipetakan dengan benar ke skema COCOKIN
4. kualitas foto sesuai dan bebas dari *data leakage* antar split
5. penggunaannya sesuai ketentuan dataset

**Jangan mengambil foto dari internet secara acak lalu menganggap labelnya benar.**

---

# 12. Kualitas label lebih penting daripada sekadar jumlah foto

Dataset yang ideal:

```text
Foto bagus
+
label terpercaya
+
kelas seimbang
+
variasi pengguna
+
variasi kondisi yang terkontrol
```

Bukan:

```text
100.000 foto random
+
label tidak jelas
```

Untuk personal color, kesalahan label dapat membuat model belajar definisi yang tidak konsisten.

---

# 13. Jumlah data yang disarankan

Angka berikut adalah target perencanaan, bukan angka minimum ilmiah yang mutlak.

## Prototype awal

```text
500–1.000 foto
```

Cocok untuk:

- menguji pipeline
- preprocessing
- baseline
- menemukan masalah dataset

## Eksperimen utama

```text
2.000–5.000 foto
```

Lebih layak untuk eksperimen klasifikasi dengan beberapa kelas jika distribusinya cukup seimbang.

## Dataset lebih serius

```text
10.000+ foto
```

Dapat dipertimbangkan setelah pipeline dan labeling terbukti.

**Jangan mengejar jumlah besar sebelum kualitas label dan distribusi kelas aman.**

---

# 14. Distribusi kelas

Jika menggunakan 4 kelas utama (Spring, Summer, Autumn, Winter) atau 12 subtype, usahakan distribusi tidak terlalu timpang.

Contoh target eksperimen 4 kelas (pilot):

```text
Warm Spring       250
Cool Summer       250
Warm Autumn       250
Cool Winter       250
```

Total: `1.000 foto`

Contoh target eksperimen 12 subtype:

```text
Light Spring      250    |  Light Summer      250
Warm Spring       250    |  Cool Summer       250
Bright Spring     250    |  Soft Summer       250

Soft Autumn       250    |  Deep Winter       250
Warm Autumn       250    |  Cool Winter       250
Deep Autumn       250    |  Bright Winter     250
```

Total: `3.000 foto`

Ini hanya contoh target. Jika distribusi nyata tidak seimbang, dokumentasikan ketidakseimbangan tersebut dan gunakan strategi yang sesuai (seperti `class_weight` atau *stratified split*) daripada memalsukan keseimbangan dataset.

---

# 15. Train / Validation / Test

Gunakan pembagian data yang jelas.

Titik awal:

```text
70–80%  Train
10–15%  Validation
10–15%  Test
```

## Aturan sangat penting

1. **Foto orang yang sama tidak boleh tersebar ke train dan test** (sebagaimana diterapkan pada `individuals_train_test_splits` di `COCOKIN-AI`).

```text
Person A
├── photo_01 → Train
├── photo_02 → Test   ❌ (Data Leakage!)
```

Lebih benar:

```text
Person A
├── photo_01 → Train
├── photo_02 → Train
└── photo_03 → Train
```

2. **Jangan melakukan augmentasi sebelum `train_test_split`**.
   - Pada `Cocokin_AI_Training.ipynb` saat ini, setiap foto diekstrak fiturnya lalu diduplikasi 15x dengan noise **sebelum** di-split menggunakan `train_test_split`. Hal ini menyebabkan salinan fitur dari foto yang sama masuk ke Train sekaligus Test, sehingga akurasi terlihat tinggi secara semu (*data leakage*).
   - Perbaikan wajib: **Lakukan split foto/individu terlebih dahulu**, baru lakukan augmentasi hanya pada data `Train`.

---

# 16. Data augmentation

Augmentasi hanya dilakukan pada **train set**.

Contoh yang mungkin digunakan:

- horizontal flip jika sesuai
- crop ringan
- brightness ringan
- contrast ringan
- resize
- sedikit perubahan exposure

Hindari augmentasi yang mengubah warna secara ekstrem karena target COCOKIN justru berhubungan dengan warna.

Contoh yang harus dihindari:

```text
Mengubah hue secara ekstrem
Mengubah warna kulit secara drastis
Color filter
Brightness adjustment yang terlalu ekstrem (misal ±25% jika mengubah rona kulit dari Light ke Deep)
```

Karena dapat merusak label personal color dan skin tone.

---

# 17. Audit dataset sebelum training

Sebelum model dilatih, wajib dilakukan:

### File audit

- jumlah file di masing-masing folder `COCOKIN-AI`
- file rusak
- format & resolusi
- lisensi penggunaan (terutama `mst-e_data`, `personal color.v1i.multiclass`, dan dataset `images`)

### Label audit

- seluruh kelas
- jumlah per kelas
- label kosong / tidak dikenal
- **label konflik** (contoh: di `personal color.v1i.multiclass`, periksa apakah foto dasar dengan prefix sama seperti `img27_jpg...` memiliki label berbeda akibat kesalahan anotasi di Roboflow)

### Duplicate & Leakage audit

- exact duplicate
- near duplicate / hasil pre-augmentation Roboflow yang tersebar lintas split (`train`, `valid`, `test`)
- foto orang yang sama lintas split

### Bias audit

Periksa:

- pencahayaan
- kamera
- background
- makeup & filter
- distribusi skin depth

---

# 18. Dataset manifest

Buat satu manifest utama yang bersih.

Contoh:

```csv
image_id,image_path,person_id,source,split,undertone,season,personal_color,skin_depth,lighting,makeup,filter
IMG001,images/IMG001.jpg,P001,self,train,WARM,AUTUMN,WARM_AUTUMN,MEDIUM,NATURAL,NONE,NO
IMG002,images/IMG002.jpg,P002,self,validation,COOL,WINTER,DEEP_WINTER,MEDIUM,NATURAL,NONE,NO
```

`person_id` sangat disarankan agar split berdasarkan individu dapat dilakukan.

---

# 19. Model AI yang disarankan

Jangan langsung memilih model berdasarkan popularitas. Mulai dari baseline sederhana.

## Opsi A — Feature-based baseline (Sesuai pendekatan awal di `Cocokin_AI_Training.ipynb`)

```text
Foto
→ face/skin ROI extraction (OpenCV / MediaPipe)
→ RGB / HSV / CIE-LAB statistical features
→ classifier
→ skin tone & personal color
```

Model yang dapat diuji:

- Logistic Regression
- Random Forest (sudah diinisiasi di notebook)
- XGBoost / LightGBM
- SVM

Kelebihan:

- mudah dijelaskan untuk mata kuliah IPPL & PCD (Pengolahan Citra Digital)
- cepat dilatih
- cocok untuk baseline
- membantu mengetahui apakah fitur warna kulit memang informatif

## Opsi B — Transfer Learning

Jika dataset foto cukup dan bebas leakage:

```text
Image
→ pretrained CNN
→ fine-tuning
→ personal color
```

Model ringan yang dapat dievaluasi:

- MobileNetV2 / MobileNetV3
- EfficientNet-B0
- model vision ringan lainnya

Jangan melatih CNN besar dari nol tanpa alasan.

---

# 20. Arsitektur yang lebih direkomendasikan untuk COCOKIN

Daripada langsung memprediksi banyak kelas sekaligus dari piksel mentah tanpa struktur, pertimbangkan pipeline bertahap:

```text
Foto
 ↓
Face validation & Skin ROI segmentation
 ↓
Color feature extraction (RGB, HSV, CIE-LAB)
 ↓
 ├──→ Skin Tone Estimation (Light / Medium / Deep + Hex)
 └──→ Undertone & Season Classification (Warm/Cool + Spring/Summer/Autumn/Winter)
 ↓
Personal Color & Palette
```

Namun arsitektur final harus ditentukan berdasarkan hasil eksperimen pada data yang sudah dibersihkan.

---

# 21. Evaluasi model

Jangan hanya melihat accuracy.

Untuk klasifikasi gunakan:

- Accuracy
- Precision
- Recall
- F1-score
- Macro F1
- Confusion Matrix

Perhatikan khususnya:

```text
kelas mana yang paling sering tertukar?
```

Misalnya:

```text
Warm Autumn ↔ Warm Spring
Cool Summer ↔ Cool Winter
```

Kesalahan seperti ini lebih informatif daripada satu angka accuracy.

---

# 22. Confidence dan format output AI

Model harus memiliki perilaku jika hasilnya tidak meyakinkan (atau jika tidak ada wajah yang terdeteksi pada foto).

Contoh:

```text
wajah tidak terdeteksi / confidence rendah (< threshold)
→ "Foto belum cukup jelas untuk dianalisis. Pastikan wajah terlihat jelas dengan pencahayaan netral."

confidence tinggi
→ tampilkan hasil analisis & simpan ke riwayat
```

Agar langsung kompatibel dengan `AnalysisController` (`lib/backend/analysis_controller.dart`) dan `AnalysisResultModel` (`lib/models/product_model.dart`), output AI Service sebaiknya menyediakan informasi berikut:

```json
{
  "status": "success",
  "model_version": "0.1.0",
  "skinTone": "Medium",
  "skinToneHex": 4287390296,
  "undertone": "Warm",
  "undertoneHex": 4292790433,
  "season": "Autumn",
  "personalColor": "Warm Autumn",
  "confidence": 0.84
}
```

Contoh di atas hanya format kontrak data, bukan hasil model nyata.

---

# 23. Recommendation Engine

Setelah AI menghasilkan prediksi (misalnya `Warm Autumn` dengan undertone `Warm` dan skin tone `Medium`), jangan meminta model AI untuk mengarang produk.

Gunakan alur yang sudah ada di backend COCOKIN:

```text
Personal Color & Undertone
↓
Color Profile & Palette Rules (di AnalysisController)
↓
Product Database (db.json)
↓
Category, Undertone & Personal Color Matching (di ProductController)
↓
Budget Filter (minPrice & maxPrice)
↓
Recommendation List ke Flutter
```

---

# 24. Data produk makeup (`db.json`)

Di dalam `COCOKIN/lib/backend/db.json` dan `lib/models/product_model.dart`, skema produk yang sudah berjalan saat ini adalah:

| Field di `db.json` | Tipe | Contoh |
|---|---|---|
| `id` | `String` | `"prod-1"` |
| `name` | `String` | `"Lip Cream"` |
| `brand` | `String` | `"Make Over"` |
| `shade` | `String` | `"Warm Teracotta"` |
| `shadeHex` | `int` | `4290143051` (`0xFFB6634B`) |
| `price` | `int` | `45000` |
| `priceLabel` | `String` | `"Rp45.000"` |
| `category` | `String` | `"Lip Product"` (`"Blush"`, `"Eye Makeup"`, `"Complexion"`) |
| `type` | `String` | `"lip"` (`"blush"`, `"eyeshadow"`, `"cushion"`) |
| `undertone` | `String` | `"Warm"` (`"Cool"`, `"Neutral"`) |
| `personalColor` | `String` | `"Warm Autumn"` (`"Cool Summer"`, dll.) |
| `description` | `String` | `"Lip cream bertekstur velvet lembut..."` |
| `whyMatch` | `String` | `"Shade Warm Teracotta selaras dengan undertone Warm..."` |
| `allShades` | `List<Map>` | `[{"name": "Warm Teracotta", "hex": 4290143051}, ...]` |
| `shopeeUrl` | `String` | `"https://shopee.co.id/..."` |
| `tokopediaUrl` | `String` | `"https://www.tokopedia.com/..."` |

Skema di atas **sudah sangat baik dan lengkap**, sehingga tidak perlu diubah secara drastis—cukup diperkaya jumlah katalog produknya agar mencakup semua hasil `personalColor` dan `undertone`.

---

# 25. Cara memperoleh data produk

Untuk MVP, database produk di `db.json` dibuat secara terkurasi.

Pilihan:

### Manual / Melalui Fitur Admin COCOKIN

Admin memasukkan produk melalui endpoint `POST /api/products` yang sudah tersedia di `product_controller.dart`:

```text
brand, name, category, shade, shadeHex, price, undertone, personalColor, description, whyMatch, shopeeUrl, tokopediaUrl
```

Kelebihan:

- mudah dan sudah terimplementasi di aplikasi
- dapat dikontrol
- cocok untuk dataset katalog MVP

**Jangan membuat AI mengarang nama produk, harga, shade, atau link e-commerce.**

---

# 26. AI dan produk harus dipisahkan

Arsitektur yang disarankan:

```text
AI Model (Python Service)
    ↓
"Warm Autumn" (Skin Tone: Medium, Undertone: Warm)
    ↓
Recommendation Engine (Dart Backend)
    ↓
Product Database (db.json)
    ↓
"Make Over Lip Cream - Shade Warm Teracotta (Rp45.000)"
    ↓
Shopee / Tokopedia Link
```

AI menentukan **hasil analisis wajah**.

Database menentukan **produk apa yang tersedia**.

Recommendation engine menentukan **produk mana yang cocok dan masuk budget**.

---

# 27. Database aplikasi

Saat ini repository `COCOKIN` menggunakan `lib/backend/db.json` (dengan referensi skema SQL di `lib/backend/cocokin_db.sql`) untuk menyimpan:

- `users` (akun pengguna, role admin/user, status `isPremium`)
- `analysis_history` (riwayat analisis warna kulit pengguna)
- `products` (katalog produk makeup beserta shade dan link e-commerce)

Pengembangan AI tidak perlu mengganti `db.json`.

Tahap integrasi:

```text
Flutter (kamera_page / loading_page)
   ↓
Dart Backend (POST /api/analyze di server.dart)
   ↓
Python AI Service (POST /predict)
   ↓
AI Result (skinTone, undertone, personalColor, confidence)
   ↓
Dart Backend (simpan ke analysis_history di db.json & ambil profil palet)
   ↓
Flutter (hasil_page → rekomendasi_page)
```

**Jangan menjadikan perpindahan database sebagai syarat agar model AI dapat mulai dikembangkan.**

---

# 28. API AI

Karena backend utama COCOKIN ditulis menggunakan **Pure Dart** (`lib/backend/server.dart` di port `5000`), sedangkan pipeline pengolahan citra dan machine learning menggunakan **Python** (OpenCV, MediaPipe, Scikit-Learn), cara integrasi paling bersih adalah menjalankan Python AI sebagai microservice lokal (misalnya dengan FastAPI atau Flask di port `8000`) atau memanggilnya dari Dart Backend.

Contoh endpoint Python AI Service:

```text
GET  /health
GET  /model-info
POST /predict
```

Input `POST /predict`:

```text
image (file multipart / base64 / image path)
```

Output `POST /predict`:

```json
{
  "status": "success",
  "model_version": "0.1.0",
  "skinTone": "Medium",
  "skinToneHex": 4287390296,
  "undertone": "Warm",
  "undertoneHex": 4292790433,
  "season": "Autumn",
  "personalColor": "Warm Autumn",
  "confidence": 0.81
}
```

Dengan demikian, `AnalysisController.handleAnalyzePhoto` di `COCOKIN/lib/backend/analysis_controller.dart` nantinya cukup meneruskan foto ke service AI ini (dengan fallback ke preset jika service AI sedang mati saat mode testing UI).

---

# 29. Struktur folder pengembangan yang disarankan

Pertahankan pemisahan dua folder yang sudah kamu buat di `D:\Semester 5\IPPL\`, dan rapikan struktur di dalam `COCOKIN-AI/` tanpa merusak `COCOKIN/`:

```text
D:\Semester 5\IPPL\
│
├── COCOKIN/                              # [TETAP] Aplikasi Flutter & Dart Backend
│   ├── lib/
│   │   ├── halaman/
│   │   ├── backend/
│   │   ├── services/
│   │   └── models/
│   ├── test/
│   └── pubspec.yaml
│
└── COCOKIN-AI/                           # [WORKSPACE AI] Dataset, Training & AI API
    ├── RENCANA_PENGEMBANGAN_COCOKIN_AI.md
    ├── Cocokin_AI_Training.ipynb
    │
    ├── personal color.v1i.multiclass/    # Dataset Raw 1 (Roboflow 4-season)
    ├── images/                           # Dataset Raw 2 (Cropped faces/skin 1-10)
    ├── images_train_test_splits.../      # Split CSV untuk dataset images
    ├── individuals_train_test_splits.../ # Split CSV per individu untuk dataset images
    ├── mst-e_data/                       # Referensi MST-E (NON-TRAINING / Kalibrasi)
    │
    ├── dataset/                          # [DISARANKAN] Hasil kurasi & manifest bersih
    │   ├── processed/
    │   └── manifests/
    │
    ├── reports/                          # [DISARANKAN] Laporan hasil audit & evaluasi
    ├── models/                           # [DISARANKAN] Penyimpanan model (.pkl / .onnx)
    ├── src/                              # [DISARANKAN] Kode modular Python
    │   ├── preprocessing/
    │   ├── features/
    │   ├── training/
    │   ├── evaluation/
    │   └── api/
    └── requirements.txt
```

Dataset asli bersifat read-only dan tidak dimasukkan ke repository Git jika ukurannya besar atau lisensinya tidak mengizinkan.

---

# 30. Aturan keamanan pengembangan

AI agent/IDE yang mengerjakan COCOKIN wajib:

1. Jangan menghapus file tanpa persetujuan.
2. Jangan mengganti struktur Flutter di `COCOKIN/` secara besar-besaran.
3. Jangan menghapus `COCOKIN/lib/backend/db.json`.
4. Jangan mengubah credential.
5. Jangan mengubah `.env` tanpa persetujuan.
6. Jangan melakukan push/commit otomatis jika tidak diminta.
7. Jangan mengunggah foto pengguna ke layanan eksternal tanpa kebutuhan dan persetujuan.
8. Dataset asli di `COCOKIN-AI/` bersifat read-only.
9. Hasil preprocessing disimpan sebagai data turunan.
10. Jangan melakukan training model final sebelum audit data selesai.
11. Jangan mengklaim model sudah akurat sebelum evaluasi yang bebas *data leakage*.
12. Jangan mengarang hasil personal color.
13. Jangan mengarang produk, harga, shade, atau link e-commerce.
14. Setiap eksperimen harus dapat direproduksi.

---

# 31. Roadmap pengerjaan

## Tahap 0 — Audit repository `COCOKIN` & `COCOKIN-AI`

Tujuan:

> Memahami kode COCOKIN dan aset di COCOKIN-AI sebelum AI diintegrasikan.

Tugas:

- cek struktur project `COCOKIN` dan `COCOKIN-AI`
- cek Flutter/Dart version
- cek endpoint backend di `server.dart`
- cek model data di `product_model.dart`
- cek format `db.json`
- cek alur `kamera_page.dart` → `loading_page.dart` → `hasil_page.dart`
- cek cara riwayat dan produk disimpan
- identifikasi bagian yang saat ini masih mock/preset (`analysis_controller.dart`, `cocokin_ai_training.py`)

Output:

```text
reports/repository_audit.md
```

---

## Tahap 1 — Audit data training di `COCOKIN-AI`

Tujuan:

> Menentukan dataset mana di `COCOKIN-AI` yang benar-benar valid dan boleh dipakai untuk training personal color maupun skin tone.

Tugas:

- audit `personal color.v1i.multiclass` (jumlah foto unik sebelum augmentasi Roboflow, cek kebocoran data antar train/valid/test, cek konflik label di `_classes.csv`)
- audit `images/` dan CSV split-nya (`images_train_test_splits` & `individuals_train_test_splits`) untuk memahami pemetaan kelas 1–10
- audit lisensi `mst-e_data` (konfirmasi larangan penggunaan untuk training ML)
- audit pipeline di `Cocokin_AI_Training.ipynb` (identifikasi masalah *data leakage* akibat augmentasi sebelum split)

Output:

```text
reports/dataset_audit.md
reports/class_distribution.csv
reports/data_quality.md
```

**STOP setelah tahap ini dan review hasil.**

---

## Tahap 2 — Definisi label COCOKIN

Tentukan secara final pemetaan antara dataset dan output aplikasi:

```text
Skin Tone:
Light / Medium / Deep (dipetakan dari nilai L* / ITA atau kelas MST 1-10)

Undertone:
Warm / Cool / Neutral

Season:
Spring / Summer / Autumn (Fall) / Winter

Personal Color (Output ke Aplikasi):
Warm Spring / Cool Summer / Warm Autumn / Cool Winter (atau 12 seasonal colors)
```

Jangan training sebelum definisi dan pemetaan label ini disetujui.

---

## Tahap 3 — Pembersihan & Penyiapan Dataset (Data Cleaning & Splitting)

Berdasarkan hasil audit:

- bersihkan duplikasi dan *data leakage* pada dataset
- pastikan foto dari individu/sumber yang sama tidak bocor antara `train`, `validation`, dan `test`
- buat manifest CSV yang bersih

---

## Tahap 4 — Preprocessing & Feature Extraction

Pipeline:

```text
Raw Image
↓
Validate
↓
Face Detection (MediaPipe / OpenCV)
↓
Skin ROI Extraction (pipi, dahi, dagu — hindari mata/bibir/rambut)
↓
Quality Check
↓
Color Feature Extraction (RGB, HSV, CIE-LAB)
↓
Processed Dataset (Train / Val / Test terpisah)
```

Jangan menimpa raw image.

---

## Tahap 5 — Baseline Model

Buat baseline sederhana yang bebas *data leakage*:

```text
Color Features (hanya augmentasi di Train set)
→ classifier (Random Forest / SVM / XGBoost / Logistic Regression)
→ undertone / season / skin tone
```

Bandingkan beberapa model pada Validation dan Test set murni.

Output:

```text
reports/baseline_results.csv
reports/baseline_report.md
```

---

## Tahap 6 — Deep Learning / Transfer Learning (Opsional / Pembanding)

Jika baseline berbasis fitur warna belum cukup:

```text
Image
→ pretrained model (MobileNet / EfficientNet)
→ fine-tuning
→ prediction
```

Eksperimen dicatat lengkap (dataset version, hyperparameters, seed, epochs, metrics).

---

## Tahap 7 — Evaluasi

Evaluasi pada Test Set yang tidak pernah dilihat model:

- accuracy
- precision, recall, F1, Macro F1
- confusion matrix
- per-class performance
- confidence threshold
- failure cases

---

## Tahap 8 — Penyelarasan Recommendation Engine & Profil Palet

Pastikan setiap kelas `personalColor` yang dihasilkan model AI memiliki:

- profil palet warna di `AnalysisController._colorProfiles` (`lib/backend/analysis_controller.dart`)
- aturan pencocokan ke katalog produk di `ProductController` (`lib/backend/product_controller.dart`)

*(Saat ini `_colorProfiles` baru memiliki `'Warm Autumn'` dan `'Cool Summer'`; perlu dilengkapi untuk `'Warm Spring'` dan `'Cool Winter'` atau kelas lainnya).*

---

## Tahap 9 — Pengayaan Product Database (`db.json`)

Periksa katalog `products` di `COCOKIN/lib/backend/db.json` agar setiap kategori (`Lip Product`, `Blush`, `Eye Makeup`, `Complexion`) memiliki produk untuk seluruh variasi `undertone` dan `personalColor`.

---

## Tahap 10 — AI API (Python Service)

Buat service Python ringan (FastAPI/Flask) yang memuat model `.pkl` terlatih:

```text
GET  /health
GET  /model-info
POST /predict
```

---

## Tahap 11 — Integrasi dengan Dart Backend & Flutter

Hubungkan alur pengiriman foto:

```text
kamera_page.dart
↓
kirim foto ke backend / AI API
↓
prediksi skinTone, undertone, personalColor
↓
simpan ke analysis_history di db.json
↓
hasil_page.dart
↓
rekomendasi_page.dart
```

Jangan mengubah UI Flutter lebih banyak dari yang dibutuhkan.

---

## Tahap 12 — Pengujian end-to-end

Test:

- **Case 1:** Foto wajah valid → prediksi AI → tampil di `hasil_page` → rekomendasi produk sesuai di `rekomendasi_page`.
- **Case 2:** Foto blur / tidak ada wajah → ditolak dengan pesan yang ramah.
- **Case 3:** Foto terlalu gelap → ditolak / peringatan pencahayaan.
- **Case 4:** Confidence rendah → minta foto ulang.
- **Case 5:** Filter budget tidak menemukan produk → fallback message.

---

# 32. Kriteria keberhasilan

COCOKIN dianggap siap untuk demo AI jika:

- [ ] Foto asli pengguna dapat dikirim dari Flutter (bukan sekadar mengirim nama string `'kamera_wajah.png'` atau preset).
- [ ] AI Service dapat menerima dan memproses foto wajah.
- [ ] Preprocessing saat inferensi konsisten dengan saat training.
- [ ] Model menghasilkan `skinTone`, `undertone`, dan `personalColor` beserta `confidence`.
- [ ] Model telah diuji pada test set tanpa *data leakage*.
- [ ] `AnalysisController` memiliki palet warna untuk seluruh kelas `personalColor` yang didukung model.
- [ ] Recommendation engine menggunakan hasil model untuk menyaring produk.
- [ ] Produk berasal dari `db.json` nyata.
- [ ] Filter kategori dan budget bekerja.
- [ ] Detail produk, shade, dan link Shopee/Tokopedia tampil dengan benar.
- [ ] Hasil analisis tersimpan ke `analysis_history`.
- [ ] Error handling tersedia jika wajah tidak terdeteksi atau foto kurang jelas.

---

# 33. Kriteria kualitas dataset

Dataset di `COCOKIN-AI` dianggap cukup untuk masuk training final jika:

- [ ] setiap gambar memiliki ID dan path yang jelas
- [ ] label konsisten (konflik label pada dataset Roboflow sudah dibersihkan)
- [ ] definisi pemetaan label terdokumentasi
- [ ] distribusi kelas diketahui
- [ ] duplikasi dan pre-augmentation lintas split sudah dibersihkan
- [ ] foto orang yang sama tidak bocor antar split (`train`, `valid`, `test`)
- [ ] augmentasi hanya dilakukan pada `train` set setelah proses splitting
- [ ] foto blur/rusak ditangani
- [ ] sumber data dan lisensi penggunaan diperiksa (tidak memakai `mst-e_data` untuk training ML)

---

# 34. Hal yang TIDAK boleh dilakukan

Jangan:

```text
Foto random dari Google / Unsplash (16 foto)
→ tebak personal color sendiri
→ augmentasi noise 15x sebelum train_test_split
→ klaim akurasi tinggi sebagai model final
```

Jangan:

```text
Menggunakan dataset yang melarang training ML (seperti mst-e_data) untuk melatih model
```

Jangan:

```text
Tidak ada label
→ anggap Neutral
```

Jangan:

```text
Foto dasar yang sama (misal hasil augmentasi Roboflow)
→ masuk ke train sekaligus valid/test
```

Jangan:

```text
AI prediction
→ AI mengarang produk
```

Jangan:

```text
Accuracy tinggi
→ langsung menyimpulkan aplikasi siap digunakan tanpa mengecek data leakage & confusion matrix
```

---

# 35. Batasan COCOKIN

COCOKIN harus menyatakan bahwa hasil merupakan **estimasi berbasis foto**, bukan penilaian profesional yang absolut.

Hasil dapat dipengaruhi oleh:

- pencahayaan
- kamera
- white balance
- makeup
- filter
- kualitas foto
- kondisi kulit
- warna rambut
- warna background

Jika foto tidak memenuhi syarat:

```text
"Foto belum cukup jelas untuk dianalisis.
Silakan ambil foto ulang dengan pencahayaan yang lebih netral."
```

---

# 36. Prioritas pengerjaan

Jika waktu terbatas, gunakan prioritas berikut:

## PRIORITAS 1 ⭐⭐⭐⭐⭐
Audit & pembersihan dataset di `COCOKIN-AI` + penyelarasan sistem label.

## PRIORITAS 2 ⭐⭐⭐⭐⭐
Perbaikan pipeline training baseline model personal color & skin tone (bebas *data leakage*).

## PRIORITAS 3 ⭐⭐⭐⭐⭐
Evaluasi model (Confusion Matrix & F1-score per kelas).

## PRIORITAS 4 ⭐⭐⭐⭐
Melengkapi profil warna di `AnalysisController` (`Warm Spring`, `Cool Winter`, dll.) & produk di `db.json`.

## PRIORITAS 5 ⭐⭐⭐⭐
Pembuatan Python AI API (`/predict`).

## PRIORITAS 6 ⭐⭐⭐
Integrasi Flutter (`kamera_page`) → Dart Backend (`/api/analyze`) → Python AI API.

## PRIORITAS 7 ⭐⭐
Optimasi model dan pengujian end-to-end.

---

# 37. Instruksi untuk AI Coding Agent

Jika dokumen ini diberikan kepada Antigravity/Coding Agent, **jangan langsung mengubah aplikasi atau melatih model final**.

Mulai dari:

### STEP 1
Audit repository `COCOKIN` (Flutter & Dart Backend).

### STEP 2
Audit struktur backend (`server.dart`, controllers) dan database (`db.json`).

### STEP 3
Audit seluruh dataset dan notebook yang tersedia di `COCOKIN-AI`.

### STEP 4
Buat laporan audit lengkap di folder `COCOKIN-AI/reports/`.

### STEP 5
Berhenti dan minta persetujuan sebelum:

- mengubah struktur folder
- membersihkan/memodifikasi dataset
- membuat atau melatih ulang model
- mengubah `db.json`
- mengubah API di `server.dart`
- mengubah kode UI Flutter

---

# 38. Tugas pertama yang harus dikerjakan Agent

> **KERJAKAN HANYA AUDIT. JANGAN TRAINING. JANGAN MENGUBAH APLIKASI.**

Checklist:

1. Baca dokumen ini.
2. Audit struktur repository `COCOKIN` dan `COCOKIN-AI`.
3. Identifikasi halaman Flutter yang berhubungan dengan analisis.
4. Identifikasi `AnalysisController` dan `ProductController`.
5. Identifikasi model data `AnalysisResultModel` dan `ProductModel`.
6. Identifikasi struktur `db.json` dan `cocokin_db.sql`.
7. Identifikasi katalog produk saat ini dan kelas `personalColor` apa saja yang belum memiliki produk/palet.
8. Identifikasi alur kamera (`kamera_page.dart`) hingga hasil (`hasil_page.dart`).
9. Identifikasi seluruh endpoint REST API di `server.dart`.
10. Identifikasi bagian analisis yang saat ini masih mock/static/simulasi (`analysis_controller.dart`, `cocokin_ai_training.py`, `Cocokin_AI_Training.ipynb`).
11. Audit seluruh dataset di `COCOKIN-AI` (`personal color.v1i.multiclass`, `images`, splits CSV, dan `mst-e_data`).
12. Buat laporan di `COCOKIN-AI/reports/`.
13. Berhenti.

Output:

```text
COCOKIN-AI/reports/
├── repository_audit.md
├── backend_audit.md
├── analysis_flow.md
├── product_data_audit.md
└── dataset_audit.md
```

---

# 39. Format laporan Agent

Agent wajib melaporkan:

```text
1. Kondisi repository (COCOKIN & COCOKIN-AI)
2. Struktur aplikasi Flutter
3. Alur kamera → analisis → hasil
4. Kondisi backend Dart
5. Kondisi database (db.json)
6. Kondisi katalog produk & profil warna
7. Bagian yang sudah berjalan
8. Bagian yang masih mock/static/simulasi
9. Dataset yang tersedia di COCOKIN-AI
10. Kekurangan dataset & batasan lisensi
11. Temuan risiko data leakage (di notebook & dataset Roboflow)
12. Rekomendasi arsitektur AI
13. Perubahan yang disarankan
14. Hal yang membutuhkan keputusan pengguna
```

**Agent harus berhenti setelah laporan audit selesai.**

---

# 40. Roadmap final COCOKIN

```text
                 COCOKIN AI ROADMAP

           WORKSPACE (COCOKIN & COCOKIN-AI)
                         │
                         ↓
                 AUDIT EXISTING APP
                         │
                         ↓
              AUDIT EXISTING DATASETS
                         │
                         ↓
                DEFINE LABEL SYSTEM
        (Skin Tone + Undertone + Personal Color)
                         │
                         ↓
            DATA CLEANING & DEDUPLICATION
                         │
                         ↓
             LEAK-FREE DATA SPLITTING
                         │
                         ↓
          BASELINE ML (RGB/HSV/LAB Features)
                         │
                         ↓
                  MODEL EVALUATION
                         │
                    ┌────┴────┐
                    │         │
                  GOOD       BAD
                    │         │
                    ↓         ↓
             Continue      Improve
                    │      Dataset/
                    │       Model
                    ↓         │
             AI INFERENCE ←───┘
                    │
                    ↓
       COMPLETE PROFILES & PRODUCT DB (db.json)
                    │
                    ↓
              PYTHON AI API
                    │
                    ↓
        DART BACKEND & FLUTTER INTEGRATION
                    │
                    ↓
              END-TO-END TEST
                    │
                    ↓
                COCOKIN MVP
```

---

# 41. Kesimpulan

Pengembangan AI COCOKIN dimulai dari **mengaudit dan membersihkan dataset personal color serta skin tone yang sudah ada di `COCOKIN-AI`**, lalu mengintegrasikannya ke arsitektur aplikasi Flutter dan Dart Backend di `COCOKIN` yang fondasinya sudah terbangun dengan baik.

Pembagian tanggung jawab:

```text
AI MODEL (di COCOKIN-AI)
→ menentukan skin tone, undertone, dan personal color dari foto wajah

RECOMMENDATION ENGINE (di AnalysisController & ProductController)
→ menentukan palet warna referensi dan menyaring karakter warna makeup yang cocok

PRODUCT DATABASE (db.json)
→ menyediakan produk dan shade nyata

BUDGET FILTER
→ menyaring produk berdasarkan rentang harga pengguna

E-COMMERCE LINK
→ mengarahkan pengguna ke Shopee & Tokopedia
```

---

## Status awal

```text
Repository audit       : SIAP DIDOKUMENTASIKAN KE REPORTS/
Dataset audit          : DATASET SUDAH ADA DI COCOKIN-AI, PERLU AUDIT MENDALAM
Label definition       : PERLU PENYELARASAN (4 Musim Roboflow vs Subtype Aplikasi + Skin Tone 1-10)
Baseline prototype     : SUDAH ADA KONSEP DI NOTEBOOK (PERLU PERBAIKAN DATA LEAKAGE)
Training final         : BELUM
Evaluation             : BELUM
Recommendation engine  : SUDAH ADA DI DART BACKEND (PERLU DILENGKAPI PROFIL WARNANYA)
Product database       : SUDAH ADA DI db.json
AI API                 : BELUM
Flutter integration    : SUDAH ADA FONDASI BACKEND/API
```

**Next recommended action: Jalankan audit resmi untuk menghasilkan 5 dokumen laporan di `COCOKIN-AI/reports/` sesuai Bagian 38 sebelum melakukan perubahan kode atau training.**
