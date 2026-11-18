"""
Keuangan Pribadi - pemasukan, pengeluaran, dan kategori.

Jalankan: python keuangan_pribadi.py
"""

from fplib import (average_by, filter_by, group_by, persen, pipe, rupiah, sort_by,
                   sum_by, top_n, where)


def data_transaksi():
    return (
        {"tanggal": "2026-11-01", "jenis": "masuk", "kategori": "uang saku", "ket": "Kiriman orang tua", "jumlah": 1500000},
        {"tanggal": "2026-11-02", "jenis": "keluar", "kategori": "kos", "ket": "Bayar kos", "jumlah": 600000},
        {"tanggal": "2026-11-03", "jenis": "keluar", "kategori": "makan", "ket": "Belanja mingguan", "jumlah": 120000},
        {"tanggal": "2026-11-04", "jenis": "keluar", "kategori": "transport", "ket": "Bensin", "jumlah": 30000},
        {"tanggal": "2026-11-05", "jenis": "masuk", "kategori": "freelance", "ket": "Desain poster", "jumlah": 250000},
        {"tanggal": "2026-11-06", "jenis": "keluar", "kategori": "kuliah", "ket": "Fotokopi modul", "jumlah": 25000},
        {"tanggal": "2026-11-08", "jenis": "keluar", "kategori": "makan", "ket": "Makan di kantin", "jumlah": 85000},
        {"tanggal": "2026-11-09", "jenis": "keluar", "kategori": "hiburan", "ket": "Nonton bioskop", "jumlah": 50000},
        {"tanggal": "2026-11-10", "jenis": "keluar", "kategori": "kuliah", "ket": "Kuota internet", "jumlah": 75000},
        {"tanggal": "2026-11-11", "jenis": "keluar", "kategori": "transport", "ket": "Bensin", "jumlah": 30000},
        {"tanggal": "2026-11-12", "jenis": "keluar", "kategori": "makan", "ket": "Belanja mingguan", "jumlah": 110000},
        {"tanggal": "2026-11-14", "jenis": "masuk", "kategori": "freelance", "ket": "Edit video", "jumlah": 300000},
        {"tanggal": "2026-11-15", "jenis": "keluar", "kategori": "hiburan", "ket": "Langganan musik", "jumlah": 55000},
        {"tanggal": "2026-11-16", "jenis": "keluar", "kategori": "makan", "ket": "Makan di kantin", "jumlah": 90000},
    )


def total_jenis(transaksi, jenis):
    return sum_by(lambda t: t["jumlah"], filter_by(where(jenis=jenis), transaksi))


def ringkasan_kategori(pengeluaran):
    """Total dan porsi tiap kategori pengeluaran, dari yang terbesar."""
    total = sum_by(lambda t: t["jumlah"], pengeluaran)
    return pipe(
        pengeluaran,
        lambda ts: group_by(lambda t: t["kategori"], ts),
        lambda grup: tuple(
            {"kategori": k, "total": sum_by(lambda t: t["jumlah"], isi)}
            for k, isi in grup.items()
        ),
        lambda daftar: tuple({**d, "porsi": persen(d["total"], total)} for d in daftar),
        lambda daftar: sort_by(lambda d: d["total"], daftar, descending=True),
    )


def main():
    transaksi = data_transaksi()
    pemasukan = total_jenis(transaksi, "masuk")
    pengeluaran_total = total_jenis(transaksi, "keluar")

    print("=== RINGKASAN KEUANGAN NOVEMBER 2026 ===")
    print(f" Pemasukan   : {rupiah(pemasukan):>13}")
    print(f" Pengeluaran : {rupiah(pengeluaran_total):>13}")
    print(f" Saldo       : {rupiah(pemasukan - pengeluaran_total):>13}")
    print(f" Uang terpakai {persen(pengeluaran_total, pemasukan)}% dari pemasukan")

    pengeluaran = filter_by(where(jenis="keluar"), transaksi)
    print("\nPengeluaran per kategori:")
    for d in ringkasan_kategori(pengeluaran):
        batang = "#" * round(d["porsi"] / 2)
        print(f" {d['kategori']:<10} {rupiah(d['total']):>11}  {d['porsi']:>5}%  {batang}")

    print(f"\nRata-rata per transaksi pengeluaran: {rupiah(average_by(lambda t: t['jumlah'], pengeluaran))}")

    print("\n3 pengeluaran terbesar:")
    for t in top_n(3, lambda t: t["jumlah"], pengeluaran):
        print(f" - {t['tanggal']}  {t['ket']:<18} {rupiah(t['jumlah']):>10}")

    print("\nRiwayat pemasukan:")
    for t in sort_by(lambda t: t["tanggal"], filter_by(where(jenis="masuk"), transaksi)):
        print(f" + {t['tanggal']}  {t['ket']:<18} {rupiah(t['jumlah']):>10}")


if __name__ == "__main__":
    main()
