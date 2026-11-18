"""
fplib.py - Library fungsi umum bergaya fungsional.

Aturan yang dipegang oleh semua fungsi di file ini:
1. Fungsi murni: hasil hanya bergantung pada argumen, tanpa efek samping
   (tidak print, tidak membaca/menulis file, tidak memakai waktu sekarang).
2. Tidak mengubah argumen: data masukan tidak pernah dimodifikasi.
   Hasil selalu berupa objek baru (tuple atau dict baru).
3. Tanpa variabel global.

Data yang diolah berupa kumpulan "record", yaitu dict seperti
{"nama": "Es Teh", "harga": 4000}.
"""

from functools import reduce


def pipe(value, *funcs):
    """Komposisi fungsi: mengalirkan `value` melewati `funcs` dari kiri ke kanan.

    pipe(x, f, g, h) sama dengan h(g(f(x))).
    """
    return reduce(lambda hasil, f: f(hasil), funcs, value)


def where(**kriteria):
    """Membuat predikat yang bernilai True jika record cocok dengan semua kriteria.

    where(status="hadir") menghasilkan sebuah FUNGSI, bukan nilai.
    Contoh: where(status="hadir")({"status": "hadir"}) -> True
    """
    return lambda record: all(record.get(kunci) == nilai for kunci, nilai in kriteria.items())


def filter_by(predikat, items):
    """Mengambil item yang memenuhi predikat. Hasil berupa tuple baru."""
    return tuple(item for item in items if predikat(item))


def sum_by(key_fn, items):
    """Menjumlahkan key_fn(item) untuk semua item. Kumpulan kosong -> 0."""
    return sum(key_fn(item) for item in items)


def average_by(key_fn, items):
    """Rata-rata key_fn(item). Kumpulan kosong -> 0.0 (tidak error)."""
    nilai = tuple(key_fn(item) for item in items)
    return sum(nilai) / len(nilai) if nilai else 0.0


def group_by(key_fn, items):
    """Mengelompokkan item berdasarkan key_fn(item).

    Hasil: dict baru {kunci: tuple item}. Urutan item di tiap kelompok
    sama dengan urutan aslinya.
    """
    def gabung(hasil, item):
        kunci = key_fn(item)
        return {**hasil, kunci: hasil.get(kunci, ()) + (item,)}

    return reduce(gabung, items, {})


def count_by(key_fn, items):
    """Menghitung jumlah item per kunci. Dibangun dari group_by (komposisi)."""
    return {kunci: len(isi) for kunci, isi in group_by(key_fn, items).items()}


def sort_by(key_fn, items, descending=False):
    """Mengurutkan item berdasarkan key_fn(item). Hasil berupa tuple baru."""
    return tuple(sorted(items, key=key_fn, reverse=descending))


def top_n(n, key_fn, items):
    """Mengambil n item dengan nilai key_fn terbesar."""
    return sort_by(key_fn, items, descending=True)[:max(n, 0)]


def update(record, **perubahan):
    """Mengembalikan salinan record dengan field yang diubah/ditambah.

    Record asli tidak berubah. Contoh:
    update({"jumlah": 1}, jumlah=2) -> {"jumlah": 2}
    """
    return {**record, **perubahan}


def rupiah(jumlah):
    """Format angka menjadi teks rupiah. Contoh: rupiah(15000) -> 'Rp15.000'."""
    tanda = "-" if jumlah < 0 else ""
    return f"{tanda}Rp{abs(round(jumlah)):,}".replace(",", ".")


def persen(bagian, total, digit=1):
    """Persentase bagian terhadap total, dibulatkan. Total 0 -> 0.0."""
    return round(bagian / total * 100, digit) if total else 0.0
