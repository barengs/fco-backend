# Panduan Import Data Wilayah Penangkapan

## Gambaran Umum

Fitur import wilayah penangkapan memungkinkan pengguna untuk mengimpor data wilayah penangkapan secara massal dari file CSV atau Excel. Fitur ini membantu dalam mengelola data wilayah penangkapan dengan lebih efisien, terutama ketika ada banyak data yang perlu dimasukkan sekaligus.

## Format File yang Diterima

Fitur ini mendukung dua format file:

1. **CSV (Comma-Separated Values)**
2. **Excel (.xlsx)**

## Struktur Kolom yang Diperlukan

Berikut adalah kolom-kolom yang harus ada dalam file import:

| Kolom       | Wajib | Deskripsi                                |
| ----------- | ----- | ---------------------------------------- |
| name        | Ya    | Nama wilayah penangkapan                 |
| code        | Ya    | Kode unik untuk wilayah penangkapan      |
| description | Tidak | Deskripsi wilayah penangkapan            |
| coordinates | Tidak | Koordinat wilayah dalam format JSON/text |

## Contoh Format CSV

```csv
name,code,description,coordinates
"Perairan Utara","N001","Wilayah penangkapan di utara","[[106.823, -6.234], [106.825, -6.232]]"
"Perairan Selatan","S001","Wilayah penangkapan di selatan","[[106.820, -6.240], [106.822, -6.238]]"
"Perairan Timur","E001","Wilayah penangkapan di timur","[[106.830, -6.230], [106.832, -6.228]]"
```

## Cara Menggunakan Fitur Import

1. **Siapkan File**: Buat file CSV atau Excel dengan struktur kolom yang sesuai
2. **Akses Endpoint**: Gunakan endpoint POST `/api/regions/import/`
3. **Upload File**: Kirim file melalui form-data dengan key `file`
4. **Proses Import**: Sistem akan memproses file dan memberikan respons tentang hasil import

## Penanganan Data Duplikat

Jika ada data dengan kode yang sama:

- Sistem akan memperbarui data yang sudah ada
- Tidak akan membuat entri baru

## Penanganan Kesalahan

Sistem akan memberikan informasi detail tentang:

- Baris yang mengalami kesalahan
- Jenis kesalahan yang terjadi
- Jumlah data yang berhasil diimport

## Template Import

Anda dapat mengunduh template import dari endpoint:
`GET /api/regions/download-template/`

Template ini berisi contoh format yang benar untuk memudahkan proses import.
