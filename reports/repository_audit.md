# 1. Laporan Audit Repository (`repository_audit.md`)

**Tanggal Audit:** 23 November 2026  
**Cakupan:** Direktori `D:\Semester 5\IPPL\COCOKIN` & `D:\Semester 5\IPPL\COCOKIN-AI`  
**Status:** Audit Selesai — Tidak ada perubahan kode aplikasi yang dilakukan

---

## 1. Kondisi Umum Workspace

Proyek COCOKIN saat ini terbagi ke dalam dua folder utama di `D:\Semester 5\IPPL\`:

1. **`COCOKIN/`** — Repository aplikasi utama berbasis **Flutter** beserta **Pure Dart REST API Server** dan skema database lokal/cloud.
2. **`COCOKIN-AI/`** — Workspace khusus pengembangan AI yang berisi notebook pelatihan model (`Cocokin_AI_Training.ipynb`), dokumen rencana pengembangan (`RENCANA_PENGEMBANGAN_COCOKIN_AI.md`), serta beberapa kumpulan dataset citra wajah dan warna kulit.

---

## 2. Struktur Aplikasi Flutter (`COCOKIN/`)

Berdasarkan `pubspec.yaml` dan struktur `lib/`, proyek menggunakan **Dart SDK `^3.5.0`** dan **Flutter Material 3** tanpa ketergantungan package eksternal yang berat (murni menggunakan `flutter/material.dart`, `dart:io`, `dart:convert`).

### Peta File di `COCOKIN/lib/`:

| Path File | Status | Keterangan |
|---|---|---|
| [main.dart](file:///D:/Semester%205/IPPL/COCOKIN/lib/main.dart) | Aktif | Entry point aplikasi Flutter (`CocokinApp` & `MainMobileShell`), mengatur state navigasi antar halaman dan tema warna (`CocokinColors`). |
| [halaman/beranda_page.dart](file:///D:/Semester%205/IPPL/COCOKIN/lib/halaman/beranda_page.dart) | Aktif | Halaman utama (Landing Page) dengan tab Beranda, Cara Kerja, dan Tentang. |
| [halaman/auth_page.dart](file:///D:/Semester%205/IPPL/COCOKIN/lib/halaman/auth_page.dart) | Aktif | Halaman Masuk (`login`) dan Daftar (`daftar`) pengguna maupun admin. |
| [halaman/kamera_page.dart](file:///D:/Semester%205/IPPL/COCOKIN/lib/halaman/kamera_page.dart) | Aktif (UI Simulasi) | Halaman ambil foto wajah dengan panduan bingkai oval. |
| [halaman/loading_page.dart](file:///D:/Semester%205/IPPL/COCOKIN/lib/halaman/loading_page.dart) | Aktif | Halaman loading transisi saat analisis warna kulit berlangsung. |
| [halaman/hasil_page.dart](file:///D:/Semester%205/IPPL/COCOKIN/lib/halaman/hasil_page.dart) | Aktif | Menampilkan hasil `Skin Tone`, `Undertone`, serta kartu `Personal Color` & palet warna (dengan fitur gembok/blur Premium). |
| [halaman/riwayat_page.dart](file:///D:/Semester%205/IPPL/COCOKIN/lib/halaman/riwayat_page.dart) | Aktif | Menampilkan daftar riwayat hasil analisis pengguna. |
| [halaman/rekomendasi_page.dart](file:///D:/Semester%205/IPPL/COCOKIN/lib/halaman/rekomendasi_page.dart) | Aktif | Menampilkan rekomendasi produk makeup dengan filter kategori dan rentang harga (budget), serta panel Admin CRUD produk. |
| [halaman/detail_produk_page.dart](file:///D:/Semester%205/IPPL/COCOKIN/lib/halaman/detail_produk_page.dart) | Aktif | Menampilkan detail produk, daftar shade, alasan kecocokan (`whyMatch`), dan tombol tautan ke Shopee & Tokopedia. |
| [services/api_service.dart](file:///D:/Semester%205/IPPL/COCOKIN/lib/services/api_service.dart) | Aktif | Kelas service HTTP yang menghubungkan Flutter ke Supabase REST API (dengan fallback data lokal). |
| [models/product_model.dart](file:///D:/Semester%205/IPPL/COCOKIN/lib/models/product_model.dart) | Aktif | Definisi model `ProductModel` dan `AnalysisResultModel`. |
| [backend/server.dart](file:///D:/Semester%205/IPPL/COCOKIN/lib/backend/server.dart) | Aktif (Standalone) | Server REST API Pure Dart (`http://localhost:5000/api`). |
| [backend/database_helper.dart](file:///D:/Semester%205/IPPL/COCOKIN/lib/backend/database_helper.dart) | Aktif | Helper pembaca/penulis database lokal [db.json](file:///D:/Semester%205/IPPL/COCOKIN/lib/backend/db.json). |
| [backend/auth_controller.dart](file:///D:/Semester%205/IPPL/COCOKIN/lib/backend/auth_controller.dart) | Aktif | Controller autentikasi pada Dart Backend. |
| [backend/analysis_controller.dart](file:///D:/Semester%205/IPPL/COCOKIN/lib/backend/analysis_controller.dart) | Aktif (Preset) | Controller analisis warna kulit, riwayat, dan unlock premium pada Dart Backend. |
| [backend/product_controller.dart](file:///D:/Semester%205/IPPL/COCOKIN/lib/backend/product_controller.dart) | Aktif | Controller katalog produk, filter kategori/undertone/budget, dan CRUD produk pada Dart Backend. |
| [backend/cocokin_db.sql](file:///D:/Semester%205/IPPL/COCOKIN/lib/backend/cocokin_db.sql) | Referensi Skema | Skema DDL SQL untuk 6 tabel (`pengguna`, `analisis_wajah`, `produk`, `shade`, `rekomendasi`, `langganan_premium`). |
| [backend/cocokin_ai_training.py](file:///D:/Semester%205/IPPL/COCOKIN/lib/backend/cocokin_ai_training.py) | Script Simulasi | Script Python pelatihan Random Forest menggunakan data angka acak (`np.random.normal`). |

### Temuan File Duplikat di `COCOKIN/lib/halaman/`
Terdapat 7 file tanpa akhiran `_page.dart` di dalam `lib/halaman/` yang **tidak di-import oleh `main.dart`**:
- `auth.dart`, `beranda.dart`, `detail_produk.dart`, `hasil.dart`, `kamera.dart`, `loading.dart`, `rekomendasi.dart`.
- File yang aktif digunakan oleh `main.dart` adalah versi dengan akhiran **`_page.dart`**. File duplikat ini dibiarkan utuh sesuai aturan keamanan (tidak dihapus tanpa persetujuan).

---

## 3. Struktur Workspace AI (`COCOKIN-AI/`)

| Path / Folder | Isi & Fungsi |
|---|---|
| [Cocokin_AI_Training.ipynb](file:///D:/Semester%205/IPPL/COCOKIN-AI/Cocokin_AI_Training.ipynb) | Notebook prototype ekstraksi fitur kulit (OpenCV + MediaPipe, RGB/HSV/LAB) dan klasifikasi Random Forest menggunakan 16 foto dari Unsplash. |
| `personal color.v1i.multiclass/` | Dataset Roboflow (531 gambar, 4 kelas: `fall`, `spring`, `summer`, `winter`) yang terbagi dalam `train/` (456), `valid/` (50), dan `test/` (25). |
| `images/` | Dataset klasifikasi warna kulit 10 kelas (skala Monk Skin Tone 1–10), terdiri dari `all_cropped_images_by_class` (14.278 foto) dan `all_cropped_skin_only_images` (14.205 foto). |
| `images_train_test_splits-.../` | File CSV pembagian train/val/test dan 5-fold cross-validation berbasis gambar untuk dataset `images/`. |
| `individuals_train_test_splits-.../` | File CSV pembagian train/val/test dan 5-fold cross-validation berbasis individu (`person_id`) untuk mencegah *data leakage* pada dataset `images/`. |
| `mst-e_data/` | Dataset Monk Skin Tone Examples (Google & TONL, 19 subjek, 1.515 foto). Memiliki larangan lisensi untuk digunakan sebagai data training ML. |
