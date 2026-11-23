# 3. Laporan Audit Alur Analisis (`analysis_flow.md`)

**Tanggal Audit:** 23 November 2026  
**Cakupan:** Alur `KameraPage` → `LoadingPage` → `HasilPage` → `RekomendasiPage`  
**Status:** Audit Selesai

---

## 1. Diagram Alur Aplikasi Saat Ini (Kondisi Nyata di Kode)

```text
[BerandaPage]
   │  (Klik "Mulai Analisis" -> Cek Login di MainMobileShell)
   ↓
[KameraPage] (lib/halaman/kamera_page.dart)
   │  - Menampilkan bingkai oval dengan ilustrasi vektor wajah (Container warna statis)
   │  - Klik tombol kamera / "Pilih foto dari galeri" -> mengubah state _isPreviewStep = true
   │  - Belum memanggil plugin image_picker / camera asli
   │  - Klik "Gunakan Foto & Mulai Analisis →" -> memanggil widget.onCapture()
   ↓
[LoadingPage] (lib/halaman/loading_page.dart)
   │  - Pada initState() memanggil ApiService.analyzeFacePhoto('kamera_wajah.png')
   │  - Tidak menunggu/menyimpan return value dari analyzeFacePhoto
   │  - Menjalankan Timer 900ms untuk animasi progress bar (0.35 -> 0.85)
   │  - Klik "Lihat hasil analisis →" -> memanggil widget.onFinish()
   ↓
[HasilPage] (lib/halaman/hasil_page.dart)
   │  - Menampilkan nilai yang masih di-hardcode di widget UI:
   │      • Skin Tone      : "Medium" (Color 0xFF8C6258)
   │      • Undertone      : "Warm"   (Color 0xFFDEC4A1)
   │      • Personal Color : "Warm Autumn" + 4 kotak warna palet
   │  - Kartu Personal Color di-blur (ImageFilter.blur) hingga user menekan gembok Premium
   │  - Klik "Lihat Rekomendasi Produk →" -> navigasi ke RekomendasiPage
   ↓
[RekomendasiPage] (lib/halaman/rekomendasi_page.dart)
   │  - Memuat produk dari ApiService.fetchProducts() (fallback ke kCatalogProducts)
   │  - Menyediakan filter Kategori (Semua, Complexion, Eye Makeup, Blush, Lip Product)
   │  - Menyediakan filter Budget (Semua Harga, < Rp50rb, Rp50rb - 100rb, > Rp100rb)
   │  - Klik kartu produk -> navigasi ke DetailProdukPage
```

---

## 2. Bagian yang Sudah Berjalan vs Bagian yang Masih Mock/Static

### A. Bagian yang Sudah Berjalan
1. **Navigasi & Proteksi Login (`MainMobileShell`):** Pengguna yang belum login otomatis diarahkan ke `AuthPage` saat mencoba masuk ke halaman kamera atau rekomendasi, lalu diarahkan kembali (`_redirectAfterLogin`) setelah berhasil login.
2. **Mekanisme Gembok Premium (`HasilPage`):** Efek blur pada kartu `Personal Color` dan pembukaan kunci premium saat diketuk sudah berfungsi secara visual.
3. **Filter Kategori & Budget (`RekomendasiPage` & `ProductController`):** Logika penyaringan produk berdasarkan kategori makeup dan rentang harga (`< Rp50rb`, `Rp50rb - 100rb`, `> Rp100rb`) sudah berjalan dengan baik.
4. **Halaman Detail Produk & Tautan E-Commerce (`DetailProdukPage`):** Pemilihan variasi shade (`allShades`), alasan kecocokan (`whyMatch`), serta tautan pencarian ke Shopee dan Tokopedia sudah lengkap.

### B. Bagian yang Masih Mock / Static (Titik Integrasi AI Nantinya)
1. **Pengambilan File Foto (`KameraPage`):**
   - Saat ini belum ada objek `File` / `Uint8List` foto nyata yang diambil dari kamera atau galeri perangkat.
2. **Pemanggilan API Analisis (`LoadingPage` & `ApiService.analyzeFacePhoto`):**
   - `LoadingPage` hanya mengirim string dummy `'kamera_wajah.png'` dan tidak meneruskan objek `AnalysisResultModel` ke `HasilPage`.
   - `ApiService.analyzeFacePhoto` langsung me-return `const AnalysisResultModel(skinTone: 'Medium', undertone: 'Warm', personalColor: 'Warm Autumn')`.
3. **Tampilan Hasil Analisis (`HasilPage`):**
   - Teks `'Medium'`, `'Warm'`, `'Warm Autumn'`, dan 4 warna palet di `HasilPage` masih tertulis langsung (*hardcoded*) di dalam widget tree `HasilPage`, belum membaca dari instance `AnalysisResultModel` yang dinamis.
4. **Filter Produk Berdasarkan Hasil Analisis (`RekomendasiPage`):**
   - Meskipun `ProductController.handleGetProducts` di backend sudah mendukung filter `?undertone=...`, tampilan di `RekomendasiPage` saat ini menampilkan katalog tanpa memfilter berdasarkan `undertone` atau `personalColor` hasil analisis terakhir pengguna.

---

## 3. Rencana Transisi ke Alur AI Nyata (Tanpa Merombak Desain UI)

Ketika model AI dan API AI sudah siap pada Tahap 10–11:
1. `KameraPage` memilih file gambar nyata dan meneruskan path/bytes foto ke `MainMobileShell`.
2. `LoadingPage` mengirim foto tersebut ke endpoint `/api/analyze` (atau service AI `/predict`), menerima objek `AnalysisResultModel` dinamis, lalu menyimpannya di state `MainMobileShell`.
3. `HasilPage` menerima parameter `AnalysisResultModel` tersebut sehingga teks `skinTone`, `undertone`, `personalColor`, dan warna lingkaran/palet berubah secara dinamis mengikuti hasil prediksi AI.
4. `RekomendasiPage` menerima `undertone` / `personalColor` dari hasil analisis untuk mengurutkan atau memfilter produk yang paling cocok.
