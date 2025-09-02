# Dokumentasi Fish Chain Optimization API

## Pengantar

Repository ini berisi dokumentasi komprehensif untuk Fish Chain Optimization API, sistem yang dirancang untuk mengelola rantai pasok ikan dengan fitur-fitur seperti manajemen pengguna, kapal, ikan, dan peran pengguna.

## Struktur Dokumentasi

- [API_DOCUMENTATION.md](file:///Users/ROFI/Develop/proyek/fco_ai/docs/API_DOCUMENTATION.md) - Dokumentasi utama API dengan penjelasan semua endpoint
- [API Schema](http://localhost:8000/api/docs/) - Dokumentasi interaktif yang dihasilkan oleh drf-spectacular

## Fitur Utama API

### 1. Manajemen Pengguna

- Registrasi pengguna dengan berbagai tipe (pemilik kapal, kapten, nelayan, dll.)
- Autentikasi berbasis token
- Manajemen profil pengguna

### 2. Manajemen Kapal

- CRUD (Create, Read, Update, Delete) untuk data kapal
- Impor data massal dari file CSV/Excel
- Template impor yang dapat diunduh
- Validasi nomor registrasi kapal yang unik

### 3. Manajemen Ikan

- Manajemen jenis ikan dan ikan individual
- CRUD untuk data ikan dan jenis ikan
- Impor data massal dari file CSV/Excel
- Template impor yang dapat diunduh

### 4. Manajemen Peran dan Izin

- Sistem peran dan izin berbasis grup
- Manajemen izin untuk setiap peran

## Teknologi yang Digunakan

- **Django** - Framework web Python
- **Django REST Framework** - Toolkit untuk membangun API Web
- **drf-spectacular** - Generator dokumentasi API
- **Pandas** - Library untuk manipulasi data
- **OpenPyXL** - Library untuk membaca/menulis file Excel

## Cara Mengakses Dokumentasi

### Dokumentasi Interaktif

Setelah menjalankan server pengembangan, dokumentasi API interaktif dapat diakses di:

```
http://localhost:8000/api/docs/
```

### Dokumentasi Markdown

Dokumentasi dalam format Markdown tersedia di file [API_DOCUMENTATION.md](file:///Users/ROFI/Develop/proyek/fco_ai/docs/API_DOCUMENTATION.md)

## Penggunaan

1. **Registrasi Pengguna**

   - Gunakan endpoint `/api/users/register/` untuk mendaftarkan pengguna baru

2. **Autentikasi**

   - Gunakan endpoint `/api/users/login/` untuk mendapatkan token autentikasi
   - Sertakan token dalam header `Authorization: Token YOUR_TOKEN` untuk endpoint yang memerlukan autentikasi

3. **Manajemen Data**

   - Gunakan endpoint CRUD yang sesuai untuk mengelola data kapal, ikan, dan jenis ikan

4. **Impor Data Massal**
   - Unduh template menggunakan endpoint template
   - Isi template dengan data Anda
   - Unggah file menggunakan endpoint impor

## Contoh Penggunaan

### Registrasi Pengguna

```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "user_type": "ship_owner",
    "ship_number": "SHIP001",
    "phone_number": "+628123456789"
  }'
```

### Login Pengguna

```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepassword123"
  }'
```

### Membuat Kapal Baru

```bash
curl -X POST http://localhost:8000/api/ships/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MV Oceanic",
    "reg_number": "SHIP001",
    "length": 45.5,
    "width": 8.2,
    "gross_tonnage": 1200.5,
    "year_built": 2010,
    "home_port": "Port of Jakarta",
    "active": true
  }'
```

### Mengimpor Data Kapal

```bash
curl -X POST http://localhost:8000/api/ships/import/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "file=@ship_data.csv"
```

### Mengunduh Template Impor

```bash
curl -X GET http://localhost:8000/api/ships/template/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -o ship_template.csv
```

## Pengembangan Lebih Lanjut

Untuk informasi lebih lanjut tentang pengembangan dan kontribusi terhadap proyek ini, silakan merujuk ke dokumentasi pengembangan dalam repository utama.

## Lisensi

[Lisensi proyek Anda]
