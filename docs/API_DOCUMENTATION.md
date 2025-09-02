# Dokumentasi API Fish Chain Optimization

## Pengantar

Selamat datang di dokumentasi API untuk sistem Fish Chain Optimization. API ini menyediakan berbagai fitur untuk mengelola data dalam rantai pasok ikan, termasuk manajemen pengguna, kapal, ikan, dan peran pengguna.

Dokumentasi ini menjelaskan cara menggunakan setiap endpoint API yang tersedia, parameter yang diperlukan, dan format respons yang diharapkan.

## Autentikasi

Sebagian besar endpoint dalam API ini memerlukan autentikasi. Pengguna harus login terlebih dahulu untuk mendapatkan token autentikasi, kemudian menyertakan token tersebut dalam header setiap permintaan.

### Mendapatkan Token

Untuk mendapatkan token autentikasi, gunakan endpoint login:

```
POST /api/users/login/
```

Setelah berhasil login, sertakan token dalam header permintaan:

```
Authorization: Token YOUR_TOKEN_HERE
```

## Struktur API

API ini terorganisir dalam beberapa kelompok utama:

1. **Manajemen Pengguna** - Pendaftaran, login, dan manajemen profil pengguna
2. **Manajemen Kapal** - CRUD dan impor data kapal
3. **Manajemen Ikan** - CRUD dan impor data ikan dan jenis ikan
4. **Manajemen Peran** - Pengaturan peran dan izin pengguna

## 1. Manajemen Pengguna

### Registrasi Pengguna

```
POST /api/users/register/
```

Mendaftarkan pengguna baru ke dalam sistem.

### Login Pengguna

```
POST /api/users/login/
```

Melakukan autentikasi pengguna dan menghasilkan token.

### Logout Pengguna

```
POST /api/users/logout/
```

Menghapus token autentikasi pengguna.

### Profil Pengguna

```
GET /api/users/profile/
```

Mendapatkan informasi profil pengguna yang sedang login.

### Update Profil

```
PUT /api/users/profile/
```

Memperbarui informasi profil pengguna.

## 2. Manajemen Kapal

### Daftar dan Buat Kapal

```
GET /api/ships/
POST /api/ships/
```

Mendapatkan daftar semua kapal atau membuat kapal baru.

### Detail, Update, dan Hapus Kapal

```
GET /api/ships/{id}/
PUT /api/ships/{id}/
PATCH /api/ships/{id}/
DELETE /api/ships/{id}/
```

Mengelola kapal berdasarkan ID.

### Impor Data Kapal

```
POST /api/ships/import/
```

Mengimpor data kapal dari file CSV atau Excel.

### Unduh Template Kapal

```
GET /api/ships/template/
```

Mengunduh template CSV untuk impor data kapal.

## 3. Manajemen Ikan

### Jenis Ikan

#### Daftar dan Buat Jenis Ikan

```
GET /api/fishs/species/
POST /api/fishs/species/
```

Mendapatkan daftar semua jenis ikan atau membuat jenis ikan baru.

#### Detail, Update, dan Hapus Jenis Ikan

```
GET /api/fishs/species/{id}/
PUT /api/fishs/species/{id}/
PATCH /api/fishs/species/{id}/
DELETE /api/fishs/species/{id}/
```

Mengelola jenis ikan berdasarkan ID.

#### Impor Data Jenis Ikan

```
POST /api/fishs/species/import/
```

Mengimpor data jenis ikan dari file CSV atau Excel.

#### Unduh Template Jenis Ikan

```
GET /api/fishs/species/template/
```

Mengunduh template CSV untuk impor data jenis ikan.

### Ikan

#### Daftar dan Buat Ikan

```
GET /api/fishs/fish/
POST /api/fishs/fish/
```

Mendapatkan daftar semua ikan atau membuat ikan baru.

#### Detail, Update, dan Hapus Ikan

```
GET /api/fishs/fish/{id}/
PUT /api/fishs/fish/{id}/
PATCH /api/fishs/fish/{id}/
DELETE /api/fishs/fish/{id}/
```

Mengelola ikan berdasarkan ID.

#### Impor Data Ikan

```
POST /api/fishs/fish/import/
```

Mengimpor data ikan dari file CSV atau Excel.

#### Unduh Template Ikan

```
GET /api/fishs/fish/template/
```

Mengunduh template CSV untuk impor data ikan.

## 4. Manajemen Peran

### Daftar dan Buat Peran

```
GET /api/roles/
POST /api/roles/
```

Mendapatkan daftar semua peran atau membuat peran baru.

### Detail, Update, dan Hapus Peran

```
GET /api/roles/{id}/
PUT /api/roles/{id}/
PATCH /api/roles/{id}/
DELETE /api/roles/{id}/
```

Mengelola peran berdasarkan ID.

### Izin Peran

```
GET /api/roles/{id}/permissions/
POST /api/roles/{id}/permissions/
DELETE /api/roles/{id}/permissions/{permission_id}/
```

Mengelola izin untuk peran tertentu.

## Format Data

### Tanggal dan Waktu

Tanggal dan waktu dalam API ini menggunakan format ISO 8601:

```
YYYY-MM-DDTHH:MM:SS.sssZ
```

### Angka Desimal

Angka desimal menggunakan titik (.) sebagai pemisah desimal:

```
123.45
```

## Penanganan Error

API ini menggunakan kode status HTTP standar untuk menunjukkan keberhasilan atau kegagalan operasi:

- `200 OK` - Permintaan berhasil
- `201 Created` - Sumber daya baru berhasil dibuat
- `204 No Content` - Permintaan berhasil tanpa konten respons
- `206 Partial Content` - Sebagian dari permintaan berhasil (untuk impor dengan error sebagian)
- `400 Bad Request` - Permintaan tidak valid
- `401 Unauthorized` - Autentikasi diperlukan
- `403 Forbidden` - Akses ditolak
- `404 Not Found` - Sumber daya tidak ditemukan
- `500 Internal Server Error` - Kesalahan server

## Impor Data Massal

Fitur impor data massal mendukung file dalam format:

- CSV (.csv)
- Excel (.xlsx, .xls)

### Fitur Impor

- Transaksi atomik (semua berhasil atau semua gagal)
- Laporan error per baris
- Update otomatis untuk data yang sudah ada
- Validasi data

### Template Impor

Gunakan endpoint template untuk mengunduh file template yang sesuai:

- `/api/ships/template/` - Template untuk data kapal
- `/api/fishs/species/template/` - Template untuk data jenis ikan
- `/api/fishs/fish/template/` - Template untuk data ikan

## Best Practices

1. **Gunakan Token dengan Benar** - Selalu sertakan token autentikasi dalam header permintaan
2. **Validasi Data** - Pastikan data yang dikirim sesuai dengan format yang diharapkan
3. **Tangani Error dengan Baik** - Periksa kode status dan pesan error dalam respons
4. **Gunakan Template Impor** - Gunakan template yang disediakan untuk impor data massal
5. **Backup Data** - Lakukan backup data sebelum melakukan impor massal

## Dukungan

Jika Anda mengalami masalah dengan API ini, silakan hubungi tim pengembang atau periksa dokumentasi untuk informasi lebih lanjut.
