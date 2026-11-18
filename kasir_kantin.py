"""
Kasir Kantin - menu, keranjang, dan total belanja.

Jalankan: python kasir_kantin.py
"""

from fplib import filter_by, group_by, pipe, rupiah, sort_by, sum_by, update, where


def data_menu():
    return (
        {"kode": "M01", "nama": "Nasi Goreng", "kategori": "makanan", "harga": 15000},
        {"kode": "M02", "nama": "Mie Ayam", "kategori": "makanan", "harga": 13000},
        {"kode": "M03", "nama": "Ayam Geprek", "kategori": "makanan", "harga": 17000},
        {"kode": "C01", "nama": "Pisang Goreng", "kategori": "camilan", "harga": 5000},
        {"kode": "C02", "nama": "Cireng", "kategori": "camilan", "harga": 6000},
        {"kode": "D01", "nama": "Es Teh", "kategori": "minuman", "harga": 4000},
        {"kode": "D02", "nama": "Es Jeruk", "kategori": "minuman", "harga": 6000},
        {"kode": "D03", "nama": "Kopi Susu", "kategori": "minuman", "harga": 8000},
    )


def cari_menu(menu, kode):
    hasil = filter_by(where(kode=kode), menu)
    return hasil[0] if hasil else None


def tambah_ke_keranjang(keranjang, menu, kode, jumlah=1):
    """Mengembalikan keranjang BARU. Keranjang lama tidak diubah."""
    if filter_by(where(kode=kode), keranjang):
        return tuple(
            update(item, jumlah=item["jumlah"] + jumlah) if item["kode"] == kode else item
            for item in keranjang
        )
    item_menu = cari_menu(menu, kode)
    if item_menu is None:
        return keranjang
    return keranjang + (update(item_menu, jumlah=jumlah),)


def subtotal(item):
    return item["harga"] * item["jumlah"]


def total_belanja(keranjang):
    return sum_by(subtotal, keranjang)


def diskon(total, batas=50000, persen_diskon=10):
    """Diskon 10% untuk belanja minimal Rp50.000."""
    return total * persen_diskon // 100 if total >= batas else 0


def tampilkan_menu(menu):
    per_kategori = pipe(
        menu,
        lambda m: group_by(lambda item: item["kategori"], m),
        lambda grup: {k: sort_by(lambda item: item["harga"], isi) for k, isi in grup.items()},
    )
    for kategori, daftar in per_kategori.items():
        print(f"\n  [{kategori.upper()}]")
        for item in daftar:
            print(f"   {item['kode']}  {item['nama']:<15} {rupiah(item['harga']):>10}")


def cetak_struk(keranjang):
    total = total_belanja(keranjang)
    potongan = diskon(total)
    print("\n" + "=" * 44)
    print("            STRUK KANTIN KAMPUS")
    print("=" * 44)
    for item in keranjang:
        print(f" {item['nama']:<15} {item['jumlah']:>2} x {rupiah(item['harga']):>8} {rupiah(subtotal(item)):>10}")
    print("-" * 44)
    print(f" {'Total':<30}{rupiah(total):>12}")
    print(f" {'Diskon':<30}{rupiah(-potongan):>12}")
    print(f" {'Bayar':<30}{rupiah(total - potongan):>12}")
    print("=" * 44)


def main():
    menu = data_menu()
    print("=== MENU KANTIN ===")
    tampilkan_menu(menu)

    minuman = filter_by(where(kategori="minuman"), menu)
    print(f"\nAda {len(minuman)} pilihan minuman.")

    keranjang = pipe(
        (),
        lambda k: tambah_ke_keranjang(k, menu, "M01", 2),
        lambda k: tambah_ke_keranjang(k, menu, "D01", 2),
        lambda k: tambah_ke_keranjang(k, menu, "C01", 3),
        lambda k: tambah_ke_keranjang(k, menu, "M03", 1),
        lambda k: tambah_ke_keranjang(k, menu, "D01", 1),
    )
    cetak_struk(keranjang)


if __name__ == "__main__":
    main()
