# Ringkasan Teknis Fitur Import Wilayah Penangkapan

## Gambaran Umum

Dokumen ini menjelaskan implementasi teknis fitur import data wilayah penangkapan dalam sistem Fish Chain Optimization. Fitur ini memungkinkan pengguna untuk mengimpor data wilayah penangkapan secara massal dari file CSV atau Excel.

## Endpoint API

### 1. Import Data Wilayah Penangkapan

- **URL**: `/api/regions/import/`
- **Method**: POST
- **Autentikasi**: Diperlukan (Bearer Token)
- **Content-Type**: multipart/form-data
- **Parameter**:
  - `file`: File CSV atau Excel yang berisi data wilayah penangkapan

### 2. Download Template Import

- **URL**: `/api/regions/download-template/`
- **Method**: GET
- **Autentikasi**: Diperlukan (Bearer Token)
- **Response**: File CSV template

## Fitur Utama

### 1. Dukungan Format File

- CSV (Comma-Separated Values)
- Excel (.xlsx)

### 2. Validasi Data

- Memeriksa keberadaan kolom yang diperlukan
- Memvalidasi format file
- Menangani data duplikat dengan memperbarui entri yang ada

### 3. Penanganan Kesalahan

- Transaksi atomik (all-or-nothing)
- Laporan kesalahan per baris
- Respons yang informatif tentang hasil import

### 4. Keamanan

- Autentikasi berbasis token diperlukan
- Validasi file yang diupload
- Perlindungan terhadap data yang tidak valid

## Struktur Data

### Kolom yang Diperlukan

1. `name` - Nama wilayah penangkapan
2. `code` - Kode unik wilayah penangkapan

### Kolom Opsional

1. `description` - Deskripsi wilayah
2. `coordinates` - Koordinat wilayah

## Implementasi Teknis

### Teknologi yang Digunakan

- **pandas**: Untuk membaca dan memproses file CSV/Excel
- **Django Transactions**: Untuk memastikan integritas data
- **DRF (Django REST Framework)**: Untuk endpoint API
- **drf-spectacular**: Untuk dokumentasi API

### Alur Proses Import

1. Validasi file yang diupload
2. Membaca file berdasarkan ekstensi
3. Memvalidasi struktur kolom
4. Memproses setiap baris dalam transaksi
5. Menangani data duplikat
6. Memberikan respons dengan hasil import

## Pengujian

Fitur ini telah diuji dengan berbagai skenario:

- File CSV yang valid
- File Excel yang valid
- File tanpa kolom yang diperlukan
- Data dengan entri duplikat
- File dengan format yang tidak didukung

## Dokumentasi

Dokumen terkait:

1. [Panduan Import](IMPORT_GUIDE.md) - Panduan penggunaan untuk pengguna akhir
2. Dokumentasi API di Swagger - Dokumentasi teknis untuk pengembang
