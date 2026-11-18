# fplib: Satu Library, Lima Aplikasi

Tugas kelompok mata kuliah Pemrograman Fungsional, Informatika UMM.

`fplib.py` adalah library berisi 12 fungsi umum bergaya fungsional. Kelima aplikasi di repositori ini meng-import library tersebut, dan setiap fungsi dipakai oleh minimal 3 aplikasi.

**Anggota kelompok**

| Nama | NIM |
| --- | --- |
| Erik Putra Hernanda (ketua) | 202310370311250 |
| Ahmad Sultan Amanda Putra | 202310370311239 |

## Struktur repositori

```
fplib.py              library fungsi umum
test_fplib.py         pengujian library dengan pytest
kasir_kantin.py       aplikasi 1: menu, keranjang, total belanja
presensi_kelas.py     aplikasi 2: kehadiran, rekap per mahasiswa
perpustakaan_mini.py  aplikasi 3: katalog, peminjaman, denda
keuangan_pribadi.py   aplikasi 4: pemasukan, pengeluaran, kategori
nilai_mahasiswa.py    aplikasi 5: komponen nilai, nilai akhir, peringkat
requirements.txt      dependensi (hanya pytest)
```

## Cara menjalankan

Butuh Python 3.8 atau lebih baru.

```bash
pip install -r requirements.txt

python kasir_kantin.py
python presensi_kelas.py
python perpustakaan_mini.py
python keuangan_pribadi.py
python nilai_mahasiswa.py

python -m pytest -v
```

## Prinsip fungsional

Semua fungsi di `fplib.py` memegang tiga aturan:

1. **Fungsi murni.** Hasil hanya bergantung pada argumen, tanpa efek samping. Contohnya, aplikasi perpustakaan mengirim tanggal hari ini sebagai argumen, bukan membaca jam di dalam fungsi.
2. **Tidak mengubah argumen.** Hasil selalu berupa objek baru (`tuple` atau `dict` baru).
3. **Tanpa variabel global.**

## Daftar fungsi

| Fungsi | Kegunaan | Contoh |
| --- | --- | --- |
| `pipe(value, *funcs)` | Mengalirkan nilai melewati beberapa fungsi, kiri ke kanan | `pipe(3, f, g)` sama dengan `g(f(3))` |
| `where(**kriteria)` | Membuat fungsi predikat dari kriteria | `where(status="hadir")` |
| `filter_by(predikat, items)` | Mengambil item yang memenuhi predikat | `filter_by(where(kategori="minuman"), menu)` |
| `sum_by(key_fn, items)` | Menjumlahkan nilai dari tiap item | `sum_by(lambda t: t["jumlah"], transaksi)` |
| `average_by(key_fn, items)` | Rata-rata nilai dari tiap item (kosong = 0) | `average_by(lambda m: m["akhir"], kelas)` |
| `group_by(key_fn, items)` | Mengelompokkan item ke dict `{kunci: tuple}` | `group_by(lambda b: b["kategori"], katalog)` |
| `count_by(key_fn, items)` | Menghitung jumlah item per kunci | `count_by(lambda r: r["status"], presensi)` |
| `sort_by(key_fn, items, descending=False)` | Mengurutkan item | `sort_by(lambda m: m["harga"], menu)` |
| `top_n(n, key_fn, items)` | Mengambil n item dengan nilai terbesar | `top_n(3, lambda t: t["jumlah"], pengeluaran)` |
| `update(record, **perubahan)` | Salinan record dengan field yang diubah | `update(item, jumlah=2)` |
| `rupiah(jumlah)` | Format angka ke rupiah | `rupiah(15000)` menghasilkan `"Rp15.000"` |
| `persen(bagian, total, digit=1)` | Persentase dengan pembulatan (total 0 = 0) | `persen(1, 3)` menghasilkan `33.3` |

## Matriks fungsi × aplikasi

| Fungsi | Kasir | Presensi | Perpustakaan | Keuangan | Nilai | Jumlah |
| --- | :-: | :-: | :-: | :-: | :-: | :-: |
| `pipe` | ✓ | ✓ | ✓ | ✓ | ✓ | 5 |
| `where` | ✓ | ✓ | ✓ | ✓ | ✓ | 5 |
| `filter_by` | ✓ | ✓ | ✓ | ✓ | ✓ | 5 |
| `sum_by` | ✓ | ✓ | ✓ | ✓ | ✓ | 5 |
| `sort_by` | ✓ | ✓ | ✓ | ✓ | ✓ | 5 |
| `group_by` | ✓ | ✓ | ✓ | ✓ |  | 4 |
| `update` | ✓ | ✓ | ✓ |  | ✓ | 4 |
| `average_by` |  | ✓ |  | ✓ | ✓ | 3 |
| `count_by` |  | ✓ | ✓ |  | ✓ | 3 |
| `top_n` |  |  | ✓ | ✓ | ✓ | 3 |
| `rupiah` | ✓ |  | ✓ | ✓ |  | 3 |
| `persen` |  | ✓ |  | ✓ | ✓ | 3 |

Nomor baris tiap pemanggilan ada di laporan.

## Pengujian

`test_fplib.py` berisi 32 tes: tiap fungsi diuji untuk kasus normal dan kasus batas (data kosong, total nol, n negatif), ditambah tes bahwa fungsi tidak mengubah argumennya.

## Catatan

Kode dan dokumentasi disusun dengan bantuan Claude (AI dari Anthropic). Seluruh aplikasi sudah dijalankan dan semua tes lulus.
