# 4. Laporan Audit Data Produk & Recommendation Engine (`product_data_audit.md`)

**Tanggal Audit:** 23 November 2026  
**Cakupan:** `COCOKIN/lib/backend/db.json`, `product_controller.dart`, `rekomendasi_page.dart`, dan `cocokin_db.sql`  
**Status:** Audit Selesai

---

## 1. Kondisi Katalog Produk Saat Ini

Katalog produk disimpan di tiga tempat dengan struktur yang serupa:
1. **[lib/backend/db.json](file:///D:/Semester%205/IPPL/COCOKIN/lib/backend/db.json)** (Database JSON untuk Pure Dart Backend)
2. **`kCatalogProducts` di [lib/halaman/rekomendasi_page.dart](file:///D:/Semester%205/IPPL/COCOKIN/lib/halaman/rekomendasi_page.dart#L5-L91)** (Fallback katalog di aplikasi Flutter)
3. **[lib/backend/cocokin_db.sql](file:///D:/Semester%205/IPPL/COCOKIN/lib/backend/cocokin_db.sql)** (Seeder SQL untuk tabel `produk` dan `shade`)

### Daftar Produk di `db.json` Saat Ini:

| ID | Brand & Nama Produk | Kategori (`category`) | Shade Utama (`shade`) | Harga (`price`) | Undertone | Personal Color | Jumlah `allShades` |
|---|---|---|---|---|---|---|---|
| `prod-1` | **Make Over** — Lip Cream | `Lip Product` | Warm Teracotta | Rp45.000 | `Warm` | `Warm Autumn` | 3 shade (Warm Teracotta, Caramel Nude, Dusty Rose) |
| `prod-2` | **Emina** — Blush | `Blush` | Peach Sun | Rp55.000 | `Warm` | `Warm Autumn` | 2 shade (Peach Sun, Soft Mauve) |
| `prod-3` | **Luxcrime** — Eye Shadow | `Eye Makeup` | Brown | Rp125.000 | `Warm` | `Warm Autumn` | 2 shade (Brown Earth, Cool Taupe) |
| `prod-4` | **Somethinc** — Mesh Cushion | `Complexion` | W02 Warm Sand | Rp145.000 | `Warm` | `Warm Autumn` | 2 shade (W02 Warm Sand, C01 Cool Ivory) |

---

## 2. Analisis Cakupan & Kekurangan Katalog Produk

1. **Ketimpangan Kelas `undertone` dan `personalColor`:**
   - Keempat produk utama di `db.json` saat ini **semuanya berlabel `undertone: "Warm"` dan `personalColor: "Warm Autumn"`**.
   - Walaupun di dalam array `allShades` sudah tersimpan opsi shade bertema sejuk (seperti *Dusty Rose*, *Soft Mauve*, *Cool Taupe*, dan *C01 Cool Ivory*), belum ada entri produk mandiri di `db.json` yang berlabel:
     - `undertone: "Cool"` (`Cool Summer`, `Cool Winter`)
     - `undertone: "Warm"` dengan season Spring (`Warm Spring`)
     - `undertone: "Neutral"`
   - **Dampak:** Jika model AI memprediksi pengguna sebagai **`Cool Summer`** atau **`Cool Winter`**, lalu `ProductController.handleGetProducts` memfilter dengan `undertone=Cool`, maka hasil produk yang dikembalikan akan **kosong (0 produk)**.

2. **Cakupan Rentang Harga (Budget Filter):**
   - `< Rp50.000`: 1 produk (`prod-1` — Rp45.000)
   - `Rp50.000 – Rp100.000`: 1 produk (`prod-2` — Rp55.000)
   - `> Rp100.000`: 2 produk (`prod-3` — Rp125.000, `prod-4` — Rp145.000)
   - Jika dikombinasikan dengan filter kategori + undertone, banyak kombinasi filter yang akan menghasilkan list kosong jika jumlah produk belum ditambah.

---

## 3. Kondisi Recommendation Engine Saat Ini

Logika rekomendasi saat ini terbagi di dua controller Dart:

1. **Pemetaan Personal Color → Palet Warna ([analysis_controller.dart](file:///D:/Semester%205/IPPL/COCOKIN/lib/backend/analysis_controller.dart#L11-L42)):**
   - Menggunakan dictionary `_colorProfiles`.
   - Baru mencakup **`Warm Autumn`** (`skinTone: Medium`, `undertone: Warm`) dan **`Cool Summer`** (`skinTone: Light`, `undertone: Cool`).
   - Belum memiliki profil untuk **`Warm Spring`**, **`Cool Winter`**, atau kombinasi `skinTone` lainnya (misalnya `Deep`).

2. **Penyaringan Produk ([product_controller.dart](file:///D:/Semester%205/IPPL/COCOKIN/lib/backend/product_controller.dart#L12-L45)):**
   - Menyaring berdasarkan `category`, `undertone`, `minPrice`, dan `maxPrice`.
   - Belum menyaring atau memberi skor prioritas berdasarkan `personalColor` dan `skinTone` (terutama untuk kategori `Complexion` seperti Cushion/Foundation yang sangat bergantung pada `skinTone`: Light/Medium/Deep).

---

## 4. Rekomendasi Perbaikan Data Produk (Tahap 8 & 9 Nanti)

1. Tambahkan minimal **12–16 produk terkurasi** di `db.json` sehingga setiap kategori (`Lip Product`, `Blush`, `Eye Makeup`, `Complexion`) memiliki perwakilan untuk **`Warm Autumn`**, **`Warm Spring`**, **`Cool Summer`**, dan **`Cool Winter`** di berbagai rentang harga.
2. Lengkapi `_colorProfiles` di `AnalysisController` agar mencakup minimal ke-4 musim utama (`Warm Spring`, `Cool Summer`, `Warm Autumn`, `Cool Winter`) serta mendukung `skinTone` dinamis (`Light`, `Medium`, `Deep`) dari hasil ekstraksi AI.
