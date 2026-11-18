"""
Presensi Kelas - kehadiran dan rekap per mahasiswa.

Jalankan: python presensi_kelas.py
"""

from fplib import (average_by, count_by, filter_by, group_by, persen, pipe,
                   sort_by, sum_by, update, where)


def data_mahasiswa():
    return (
        {"nim": "230001", "nama": "Andi"},
        {"nim": "230002", "nama": "Bunga"},
        {"nim": "230003", "nama": "Citra"},
        {"nim": "230004", "nama": "Dimas"},
        {"nim": "230005", "nama": "Eka"},
    )


def data_presensi():
    """H = hadir, I = izin, S = sakit, A = alpa. Satu huruf = satu pertemuan."""
    pola = {
        "230001": "HHHHHHHH",
        "230002": "HHIHHHHH",
        "230003": "HAHHSAHH",
        "230004": "HHHHHAHH",
        "230005": "AAHSHAHI",
    }
    arti = {"H": "hadir", "I": "izin", "S": "sakit", "A": "alpa"}
    return tuple(
        {"nim": nim, "pertemuan": ke + 1, "status": arti[huruf]}
        for nim, baris in pola.items()
        for ke, huruf in enumerate(baris)
    )


def rekap_mahasiswa(presensi, mhs):
    catatan = filter_by(where(nim=mhs["nim"]), presensi)
    jumlah = count_by(lambda r: r["status"], catatan)
    return update(
        mhs,
        hadir=jumlah.get("hadir", 0),
        izin=jumlah.get("izin", 0),
        sakit=jumlah.get("sakit", 0),
        alpa=jumlah.get("alpa", 0),
        persen_hadir=persen(jumlah.get("hadir", 0), len(catatan)),
    )


def rekap_kelas(presensi, mahasiswa):
    return tuple(rekap_mahasiswa(presensi, mhs) for mhs in mahasiswa)


def koreksi_status(presensi, nim, pertemuan, status_baru):
    """Mengembalikan data presensi BARU dengan satu status dikoreksi."""
    return tuple(
        update(r, status=status_baru) if r["nim"] == nim and r["pertemuan"] == pertemuan else r
        for r in presensi
    )


def hadir_per_pertemuan(presensi):
    per_pertemuan = group_by(lambda r: r["pertemuan"], presensi)
    return {ke: len(filter_by(where(status="hadir"), isi)) for ke, isi in per_pertemuan.items()}


def cetak_rekap(rekap):
    print(f" {'NIM':<8}{'Nama':<8}{'H':>3}{'I':>3}{'S':>3}{'A':>3}{'% Hadir':>9}")
    print(" " + "-" * 36)
    for r in rekap:
        print(f" {r['nim']:<8}{r['nama']:<8}{r['hadir']:>3}{r['izin']:>3}{r['sakit']:>3}{r['alpa']:>3}{r['persen_hadir']:>8}%")


def main(batas_minimal=75):
    mahasiswa = data_mahasiswa()
    presensi = data_presensi()

    print("=== REKAP PRESENSI (diurutkan dari kehadiran tertinggi) ===")
    rekap = pipe(
        presensi,
        lambda p: rekap_kelas(p, mahasiswa),
        lambda r: sort_by(lambda x: x["persen_hadir"], r, descending=True),
    )
    cetak_rekap(rekap)

    print(f"\nRata-rata kehadiran kelas : {round(average_by(lambda r: r['persen_hadir'], rekap), 1)}%")
    print(f"Total alpa satu kelas     : {sum_by(lambda r: r['alpa'], rekap)} kali")

    print(f"\nMahasiswa di bawah {batas_minimal}% kehadiran:")
    for r in filter_by(lambda r: r["persen_hadir"] < batas_minimal, rekap):
        print(f" - {r['nama']} ({r['persen_hadir']}%)")

    print("\nJumlah hadir per pertemuan:")
    for ke, jumlah in hadir_per_pertemuan(presensi).items():
        print(f" Pertemuan {ke}: {'#' * jumlah} {jumlah}")

    print("\nKoreksi: Citra pertemuan 2 ternyata izin (surat menyusul).")
    presensi_baru = koreksi_status(presensi, "230003", 2, "izin")
    lama = rekap_mahasiswa(presensi, mahasiswa[2])
    baru = rekap_mahasiswa(presensi_baru, mahasiswa[2])
    print(f" Alpa sebelum koreksi: {lama['alpa']}, sesudah: {baru['alpa']}")
    print(" Data presensi lama tetap utuh, koreksi menghasilkan data baru.")


if __name__ == "__main__":
    main()
