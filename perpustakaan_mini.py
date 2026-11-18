"""
Perpustakaan Mini - katalog, peminjaman, dan denda.

Jalankan: python perpustakaan_mini.py
"""

from datetime import date

from fplib import (count_by, filter_by, group_by, pipe, rupiah, sort_by, sum_by,
                   top_n, update, where)


def data_katalog():
    return (
        {"kode": "B01", "judul": "Laskar Pelangi", "kategori": "novel", "tersedia": True},
        {"kode": "B02", "judul": "Bumi Manusia", "kategori": "novel", "tersedia": True},
        {"kode": "B03", "judul": "Python untuk Pemula", "kategori": "komputer", "tersedia": True},
        {"kode": "B04", "judul": "Struktur Data", "kategori": "komputer", "tersedia": True},
        {"kode": "B05", "judul": "Kalkulus Dasar", "kategori": "matematika", "tersedia": True},
        {"kode": "B06", "judul": "Sejarah Indonesia", "kategori": "sejarah", "tersedia": True},
    )


def data_peminjaman():
    """Riwayat peminjaman. tgl_kembali None berarti buku belum dikembalikan."""
    return (
        {"kode": "B01", "anggota": "Andi", "tgl_pinjam": date(2026, 10, 1), "tgl_kembali": date(2026, 10, 6)},
        {"kode": "B03", "anggota": "Bunga", "tgl_pinjam": date(2026, 10, 3), "tgl_kembali": date(2026, 10, 15)},
        {"kode": "B01", "anggota": "Citra", "tgl_pinjam": date(2026, 10, 10), "tgl_kembali": date(2026, 10, 16)},
        {"kode": "B04", "anggota": "Andi", "tgl_pinjam": date(2026, 10, 20), "tgl_kembali": date(2026, 10, 30)},
        {"kode": "B03", "anggota": "Dimas", "tgl_pinjam": date(2026, 10, 25), "tgl_kembali": date(2026, 10, 31)},
        {"kode": "B01", "anggota": "Bunga", "tgl_pinjam": date(2026, 11, 2), "tgl_kembali": date(2026, 11, 8)},
    )


def hari_terlambat(pinjam, hari_ini, lama_pinjam=7):
    """Hari ini dikirim sebagai argumen, bukan dibaca dari jam, agar fungsi tetap murni."""
    tgl_akhir = pinjam["tgl_kembali"] or hari_ini
    return max(0, (tgl_akhir - pinjam["tgl_pinjam"]).days - lama_pinjam)


def denda(pinjam, hari_ini, tarif_per_hari=1000):
    return hari_terlambat(pinjam, hari_ini) * tarif_per_hari


def ubah_ketersediaan(katalog, kode, tersedia):
    return tuple(update(b, tersedia=tersedia) if b["kode"] == kode else b for b in katalog)


def pinjam_buku(katalog, peminjaman, kode, anggota, tanggal):
    """Mengembalikan pasangan (katalog_baru, peminjaman_baru)."""
    if not filter_by(where(kode=kode, tersedia=True), katalog):
        return katalog, peminjaman
    catatan = {"kode": kode, "anggota": anggota, "tgl_pinjam": tanggal, "tgl_kembali": None}
    return ubah_ketersediaan(katalog, kode, False), peminjaman + (catatan,)


def kembalikan_buku(katalog, peminjaman, kode, tanggal):
    peminjaman_baru = tuple(
        update(p, tgl_kembali=tanggal) if p["kode"] == kode and p["tgl_kembali"] is None else p
        for p in peminjaman
    )
    return ubah_ketersediaan(katalog, kode, True), peminjaman_baru


def judul_buku(katalog, kode):
    return filter_by(where(kode=kode), katalog)[0]["judul"]


def main():
    hari_ini = date(2026, 11, 18)
    katalog = data_katalog()
    peminjaman = data_peminjaman()

    katalog, peminjaman = pinjam_buku(katalog, peminjaman, "B05", "Eka", date(2026, 11, 2))
    katalog, peminjaman = pinjam_buku(katalog, peminjaman, "B02", "Citra", date(2026, 11, 14))
    katalog, peminjaman = pinjam_buku(katalog, peminjaman, "B05", "Dimas", date(2026, 11, 15))  # ditolak
    katalog, peminjaman = kembalikan_buku(katalog, peminjaman, "B02", date(2026, 11, 17))

    print(f"=== KATALOG (per {hari_ini:%d-%m-%Y}) ===")
    for b in sort_by(lambda b: b["judul"], katalog):
        status = "tersedia" if b["tersedia"] else "DIPINJAM"
        print(f" {b['kode']}  {b['judul']:<22} {b['kategori']:<11} {status}")

    print("\nJumlah buku per kategori:")
    for kategori, jumlah in count_by(lambda b: b["kategori"], katalog).items():
        print(f" - {kategori}: {jumlah}")
    print(f"Buku tersedia sekarang: {len(filter_by(where(tersedia=True), katalog))}")

    print("\n=== PEMINJAMAN TERLAMBAT ===")
    terlambat = filter_by(lambda p: hari_terlambat(p, hari_ini) > 0, peminjaman)
    for p in terlambat:
        status = "belum kembali" if p["tgl_kembali"] is None else "sudah kembali"
        print(f" {p['anggota']:<6} {judul_buku(katalog, p['kode']):<22} "
              f"{hari_terlambat(p, hari_ini):>2} hari  {rupiah(denda(p, hari_ini)):>8}  ({status})")

    print("\nTotal denda per anggota:")
    for anggota, daftar in group_by(lambda p: p["anggota"], peminjaman).items():
        total = sum_by(lambda p: denda(p, hari_ini), daftar)
        if total:
            print(f" - {anggota}: {rupiah(total)}")
    print(f"Total denda semua anggota: {rupiah(sum_by(lambda p: denda(p, hari_ini), peminjaman))}")

    print("\nBuku paling sering dipinjam:")
    terpopuler = pipe(
        peminjaman,
        lambda ps: count_by(lambda p: p["kode"], ps),
        lambda hitung: tuple({"kode": k, "kali": v} for k, v in hitung.items()),
        lambda daftar: top_n(3, lambda x: x["kali"], daftar),
    )
    for urutan, item in enumerate(terpopuler, start=1):
        print(f" {urutan}. {judul_buku(katalog, item['kode'])} ({item['kali']} kali)")


if __name__ == "__main__":
    main()
