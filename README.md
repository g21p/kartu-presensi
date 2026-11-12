# Pembuat Kartu Presensi Siswa

Web untuk membuat kartu presensi (1–5 kartu per lembar F4 215 × 330 mm) lalu mengunduhnya sebagai PDF. Bisa dibuka di PC maupun HP.

## Pasang di GitHub Pages
1. Buat repository baru di GitHub, lalu unggah **seluruh isi** folder ini (index.html, folder `assets`, `data`, `qr`, `template`, `tools`).
2. Buka **Settings → Pages**, pada *Build and deployment* pilih **Deploy from a branch**, branch `main`, folder `/ (root)`, lalu **Save**.
3. Setelah 1–2 menit, web bisa dibuka di `https://<nama-akun>.github.io/<nama-repo>/`.

> Jangan membuka `index.html` dengan klik ganda dari komputer; data tidak akan termuat. Selalu buka lewat alamat GitHub Pages (atau server lokal).

## Isi folder
| Folder | Isi |
|---|---|
| `template/kartu-1.svg` … `kartu-5.svg` | Template asli untuk 1–5 kartu per lembar (dari 29.svg … 25.svg), dipakai untuk pratinjau |
| `template/kartu-1.pdf` … `kartu-5.pdf` | Versi vektor dari template yang sama, dipakai saat membuat PDF (hasil tajam & warna sesuai) |
| `data/siswa.json` | Data siswa (No Induk, nama, kelas) |
| `qr/<ID>.png` | QR tiap siswa, ID = No Induk tanpa titik (2627.1.001 → 26271001) |
| `assets/` | Font Montserrat Bold dan pustaka pdf-lib (tidak perlu internet tambahan) |
| `tools/buat_data.py` | Skrip untuk memperbarui data & QR |

## Memperbarui data siswa / QR (mis. tahun ajaran baru)
```
pip install openpyxl
python tools/buat_data.py Data_Siswa.xlsx folder_hasil_qr
```
Excel harus punya kolom `No Induk`, `NAMA SISWA`, `KELAS`. File QR bernama `<ID>_<Nama>.png`. Setelah itu unggah ulang folder `data` dan `qr` ke GitHub.

## Mengganti desain template
Ganti file SVG di `template/` dengan SVG baru berukuran sama (935.25 × 612 pt, posisi kartu, teks “Nama Siswa”, “Kelas”, dan kotak QR di tempat yang sama), lalu buat ulang versi PDF-nya:
```
python tools/siapkan_template.py template/kartu-1.svg template/kartu-2.svg template/kartu-3.svg template/kartu-4.svg template/kartu-5.svg
```
(butuh `rsvg-convert`, Pillow, numpy). Jika posisi berubah, sesuaikan angka di bagian *Tata letak* pada `index.html`.

## Mencetak
Cetak di kertas F4/Folio dengan skala 100% (“Actual size”), jangan “Fit to page”.
