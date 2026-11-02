# ConveyorJam Watch — Panduan Bahasa Indonesia

**Day 29/100 • Computer Vision • Manufaktur • Prototipe penelitian**

## Deskripsi sebenarnya

Sistem menggunakan model YOLOv8s yang dilatih untuk mendeteksi **area conveyor**, ByteTrack untuk mengikuti prediksi pada video, dan aturan ambang pergerakan centroid/dwell untuk mengeluarkan **indikasi potensi anomali yang belum diverifikasi**. Proyek ini **belum** memiliki label kejadian macet nyata, sehingga **belum terbukti mendeteksi kemacetan conveyor**.

## Before → Now → Next

| Tahap | Status |
|---|---|
| Before | Pengumpulan dan audit data conveyor berlabel |
| Now | YOLOv8n dan YOLOv8s dilatih, YOLOv8s dipilih dengan validation mAP50:95; aplikasi FastAPI + React dan pengujian GPU lokal |
| Next | Data negatif, split video independen, pengukuran gerak material, anotasi jam asli, pengujian eksternal, keamanan deployment |

## Metrik asli

Total 2.474 gambar: train 2.283, validasi 96, test 95. Model YOLOv8s pada test sumber: mAP50:95 **0,9847654346**, mAP50 **0,995**, precision **1,0**, recall **1,0**. Semua gambar pengujian sumber memuat conveyor; independensi asal video **belum diverifikasi**. Angka ini **bukan akurasi deteksi jam**.

## Jalankan

Dari root repo (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r backend\requirements.txt
.\.venv\Scripts\python -m uvicorn app.main:app --app-dir backend --reload --port 8000
```

Terminal lain:

```powershell
cd frontend
npm ci
npm run dev
```

Akses `http://127.0.0.1:5173` dan `http://127.0.0.1:8000/docs`. Model harus tersedia lokal di `models/champion/conveyorjam_champion.pt`. FFmpeg dibutuhkan untuk video H.264 yang dapat diputar di browser.

## Batasan penting

Sinyal potential jam belum punya ground truth; stop normal juga bisa terdeteksi. Perbandingan citra dari satu video belum menjamin independensi. Folder `assets/examples/images/` adalah pratinjau beranotasi, bukan foto mentah. Kode berlisensi MIT; lisensi sumber gambar/video dan hak distribusi checkpoint masih perlu diverifikasi.

## Dokumen lengkap

Baca [README utama](../../README.md), [AGENTS](../../AGENTS.md), [metodologi riset](../RESEARCH_AND_DATA.md), [API](../API_AND_OPERATIONS.md), [keamanan](../QUALITY_SECURITY_DEPLOYMENT.md), [FAQ](../FAQ_AND_TROUBLESHOOTING.md) dan [asal data/lisensi](../DATASET_PROVENANCE_AND_LICENSES.md).
