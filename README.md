# Dashboard Restoran

Mini project Web Application Development untuk mengelola persediaan bahan baku dapur. Frontend memakai Vue 3 dan backend memakai FastAPI dengan penyimpanan JSON lokal.

## Teknologi dan struktur

- `dashboard-vue/`: Vue 3, Vite, JavaScript, dan CSS native.
- `backend-fastapi/`: FastAPI, Pydantic, dan `bahan_baku.json`.

## Cara Menjalankan project

Buka dua terminal dari folder root project.

Terminal 1 - backend:

```powershell
cd backend-fastapi
venv\Scripts\activate.bat

python -m pip install -r requirements.txt
python -m uvicorn --version
python -m uvicorn main:app --reload
```

Terminal 2 - frontend:

```powershell
cd dashboard-vue
npm install
npm run dev
```

Buka frontend di `http://localhost:5173`. Dokumentasi interaktif API tersedia di `http://127.0.0.1:8000/docs`.

## Endpoint API

| Method | Endpoint | Kegunaan |
| --- | --- | --- |
| GET | `/` | Cek backend |
| GET | `/bahan` | Ambil seluruh bahan |
| POST | `/bahan` | Tambah bahan baru |
| PATCH | `/bahan/{id}` | Ubah angka stok saja |
| DELETE | `/bahan/{id}` | Hapus bahan |

Setiap POST, PATCH, atau DELETE menulis ulang seluruh data ke `backend-fastapi/bahan_baku.json`. Karena itu perubahan tetap ada ketika backend direstart; ini bukan database.

## Aturan stok

- `0`: **Stok Habis**
- `1-3`: **Menipis**
- `>= 4`: **Aman**

Ambang tersebut sengaja disederhanakan untuk tugas. Pada aplikasi nyata setiap bahan dan satuan dapat mempunyai batas aman yang berbeda. Tile **Total Satuan Stok** dan grafik kategori adalah jumlah angka stok lintas satuan (misalnya kg, liter, botol), sehingga hanya indikator ringkas dan bukan ukuran fisik tunggal.

## Demo singkat

1. Pastikan kedua server berjalan, lalu cek 24 data awal serta empat tile.
2. Cari nama bahan atau kategori, lalu uji tombol A-Z dan Z-A.
3. Tambahkan bahan melalui form, ubah stoknya melalui `Edit Stok`, lalu hapus data percobaan.
4. Lihat perubahan pada `/docs` dan `bahan_baku.json`; restart backend untuk memeriksa persistensi.
