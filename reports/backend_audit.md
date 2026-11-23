# 2. Laporan Audit Backend & Database (`backend_audit.md`)

**Tanggal Audit:** 23 November 2026  
**Cakupan:** `COCOKIN/lib/backend/` dan `COCOKIN/lib/services/api_service.dart`  
**Status:** Audit Selesai

---

## 1. Arsitektur Backend Saat Ini (Dual-Mode: Pure Dart Server & Supabase REST)

Dari pemeriksaan kode, aplikasi COCOKIN memiliki **dua jalur backend** yang sudah dibangun:

1. **Pure Dart REST API Server ([lib/backend/server.dart](file:///D:/Semester%205/IPPL/COCOKIN/lib/backend/server.dart))**
   - Berjalan di `http://localhost:5000/api` dan menyimpan data secara persisten ke file lokal [lib/backend/db.json](file:///D:/Semester%205/IPPL/COCOKIN/lib/backend/db.json) menggunakan [database_helper.dart](file:///D:/Semester%205/IPPL/COCOKIN/lib/backend/database_helper.dart).
2. **Supabase Cloud REST Client ([lib/services/api_service.dart](file:///D:/Semester%205/IPPL/COCOKIN/lib/services/api_service.dart))**
   - Aplikasi Flutter (`api_service.dart`) saat ini dikonfigurasi memanggil endpoint Supabase PostgreSQL (`https://izgfxqikndcuhrepcjjd.supabase.co/rest/v1`) untuk login, register, riwayat, unlock premium, dan katalog produk (dengan fallback ke `kCatalogProducts` lokal jika offline), namun **khusus fungsi `analyzeFacePhoto()` masih mengembalikan objek statis `AnalysisResultModel` (`Warm Autumn`) tanpa memanggil HTTP endpoint**.

---

## 2. Daftar Endpoint di `server.dart` (Pure Dart Backend)

Seluruh endpoint berikut sudah terimplementasi dengan lengkap di [server.dart](file:///D:/Semester%205/IPPL/COCOKIN/lib/backend/server.dart):

| Method | Endpoint | Controller & Method | Status Implementasi |
|---|---|---|---|
| `GET` | `/api/health` | `server.dart` | **Berjalan** — Mengembalikan status server dan jumlah `users`, `products`, `history`. |
| `POST` | `/api/login` | `AuthController.handleLogin` | **Berjalan** — Validasi email & password terhadap `db.json`. |
| `POST` | `/api/register` | `AuthController.handleRegister` | **Berjalan** — Menambah user baru ke `db.json`. |
| `POST` | `/api/analyze` | `AnalysisController.handleAnalyzePhoto` | **Mock/Preset** — Memvalidasi ekstensi file (`.png`, `.jpg`, `.jpeg`, `.webp`), lalu mengambil profil warna statis berdasarkan parameter `preset` (`'Warm Autumn'` atau `'Cool Summer'`) dan menyimpannya ke `analysis_history`. |
| `POST` | `/api/history` | `AnalysisController.handleSaveHistory` | **Berjalan** — Menyimpan hasil analisis ke `analysis_history` di `db.json`. |
| `GET` | `/api/history` | `AnalysisController.handleGetHistory` | **Berjalan** — Mengambil daftar riwayat analisis (mendukung filter `?email=...`). |
| `DELETE` | `/api/history` | `AnalysisController.handleDeleteHistory` | **Berjalan** — Menghapus item riwayat berdasarkan `?id=...`. |
| `POST` | `/api/premium/unlock` | `AnalysisController.handleUnlockPremium` | **Berjalan** — Mengubah `isPremium = true` pada akun pengguna di `db.json`. |
| `GET` | `/api/products` | `ProductController.handleGetProducts` | **Berjalan** — Mendukung filter `?category=...&undertone=...&minPrice=...&maxPrice=...`. |
| `POST` | `/api/products` | `ProductController.handleCreateProduct` | **Berjalan** — Admin menambah produk & shade baru ke `db.json`. |
| `DELETE` | `/api/products` | `ProductController.handleDeleteProduct` | **Berjalan** — Admin menghapus produk berdasarkan `?id=...`. |

---

## 3. Kondisi Database (`db.json` vs `cocokin_db.sql`)

### A. Database Lokal [db.json](file:///D:/Semester%205/IPPL/COCOKIN/lib/backend/db.json)
Berisi 3 tabel/koleksi JSON utama:
1. **`users`** (2 akun awal: `yumna@gmail.com` [role: `user`, `isPremium: false`] dan `admin@cocokin.id` [role: `admin`, `isPremium: true`]).
2. **`analysis_history`** (1 riwayat awal milik `yumna@gmail.com` dengan hasil `skinTone: Medium`, `undertone: Warm`, `personalColor: Warm Autumn`, beserta 4 warna `palette`).
3. **`products`** (4 produk awal: Make Over Lip Cream, Emina Blush, Luxcrime Eye Shadow, Somethinc Mesh Cushion).

### B. Skema Relasional [cocokin_db.sql](file:///D:/Semester%205/IPPL/COCOKIN/lib/backend/cocokin_db.sql)
Merupakan skema SQL (6 tabel: `pengguna`, `analisis_wajah`, `produk`, `shade`, `rekomendasi`, `langganan_premium`) yang selaras dengan tabel-tabel yang dipanggil oleh `ApiService` ke Supabase (`pengguna`, `analisis_wajah`, `produk`, `shade`).

---

## 4. Celah Integrasi Backend yang Perlu Diperhatikan

1. **Belum Ada Pemanggilan dari Backend ke AI Service:**
   - `AnalysisController.handleAnalyzePhoto` di [analysis_controller.dart](file:///D:/Semester%205/IPPL/COCOKIN/lib/backend/analysis_controller.dart#L45-L91) hanya membaca string nama file (`body['image']`) dan memilih dictionary `_colorProfiles[preset]`, belum membaca byte gambar atau meneruskannya ke service AI Python.
2. **Profil Warna di `AnalysisController._colorProfiles` Baru Memiliki 2 Kelas:**
   - Saat ini `_colorProfiles` hanya mendefinisikan **`Warm Autumn`** dan **`Cool Summer`**.
   - Kelas **`Warm Spring`** dan **`Cool Winter`** (atau 12 seasonal subtypes) belum memiliki definisi `skinToneHex`, `undertoneHex`, `summary`, dan `palette` di dalam `_colorProfiles`.
3. **Inkonsistensi Parameter di `HasilPage` vs `ApiService`:**
   - Di [hasil_page.dart](file:///D:/Semester%205/IPPL/COCOKIN/lib/halaman/hasil_page.dart#L25-L37), `_handleUnlockPremium()` memanggil `ApiService.unlockPremium('yumna@gmail.com')` (mengirim `String` email) dan `_handleSaveResult()` mengirim parameter `email: 'yumna@gmail.com'`, sedangkan definisi di [api_service.dart](file:///D:/Semester%205/IPPL/COCOKIN/lib/services/api_service.dart#L168-L228) meminta `int userId`. Hal ini penting untuk diselaraskan saat tahap integrasi Flutter nanti.
