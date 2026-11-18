"""
Nilai Mahasiswa - komponen nilai, nilai akhir, dan peringkat.

Jalankan: python nilai_mahasiswa.py
"""

from fplib import (average_by, count_by, filter_by, persen, pipe, sort_by, sum_by,
                   top_n, update, where)


def data_bobot():
    """Bobot tiap komponen nilai. Totalnya harus 1.0."""
    return {"tugas": 0.20, "kuis": 0.15, "uts": 0.30, "uas": 0.35}


def data_mahasiswa():
    return (
        {"nim": "230001", "nama": "Andi", "nilai": {"tugas": 85, "kuis": 80, "uts": 78, "uas": 82}},
        {"nim": "230002", "nama": "Bunga", "nilai": {"tugas": 92, "kuis": 88, "uts": 90, "uas": 87}},
        {"nim": "230003", "nama": "Citra", "nilai": {"tugas": 70, "kuis": 65, "uts": 60, "uas": 58}},
        {"nim": "230004", "nama": "Dimas", "nilai": {"tugas": 88, "kuis": 75, "uts": 82, "uas": 79}},
        {"nim": "230005", "nama": "Eka", "nilai": {"tugas": 60, "kuis": 45, "uts": 50, "uas": 48}},
        {"nim": "230006", "nama": "Fajar", "nilai": {"tugas": 78, "kuis": 85, "uts": 74, "uas": 80}},
    )


def nilai_akhir(nilai, bobot):
    """Jumlah dari nilai tiap komponen dikali bobotnya."""
    return round(sum_by(lambda komponen: nilai[komponen] * bobot[komponen], bobot), 2)


def nilai_huruf(angka):
    """Konversi angka ke huruf. Skala ini contoh, sesuaikan dengan aturan kampus."""
    skala = ((85, "A"), (80, "A-"), (75, "B+"), (70, "B"), (65, "B-"),
             (60, "C+"), (55, "C"), (40, "D"))
    cocok = filter_by(lambda batas: angka >= batas[0], skala)
    return cocok[0][1] if cocok else "E"


def lengkapi(mhs, bobot, batas_lulus=55):
    akhir = nilai_akhir(mhs["nilai"], bobot)
    return update(mhs, akhir=akhir, huruf=nilai_huruf(akhir), lulus=akhir >= batas_lulus)


def beri_peringkat(daftar):
    urut = sort_by(lambda m: m["akhir"], daftar, descending=True)
    return tuple(update(m, peringkat=ke) for ke, m in enumerate(urut, start=1))


def main():
    bobot = data_bobot()
    hasil = pipe(
        data_mahasiswa(),
        lambda daftar: tuple(lengkapi(m, bobot) for m in daftar),
        beri_peringkat,
    )

    print("=== DAFTAR NILAI ===")
    print(" Bobot: " + ", ".join(f"{k} {round(v * 100)}%" for k, v in bobot.items()))
    print(f"\n {'#':<3}{'NIM':<8}{'Nama':<7}{'Tgs':>4}{'Kuis':>5}{'UTS':>4}{'UAS':>4}{'Akhir':>7}{'Huruf':>6}  Status")
    print(" " + "-" * 56)
    for m in hasil:
        n = m["nilai"]
        status = "Lulus" if m["lulus"] else "Tidak lulus"
        print(f" {m['peringkat']:<3}{m['nim']:<8}{m['nama']:<7}{n['tugas']:>4}{n['kuis']:>5}{n['uts']:>4}"
              f"{n['uas']:>4}{m['akhir']:>7}{m['huruf']:>6}  {status}")

    print(f"\nRata-rata kelas: {round(average_by(lambda m: m['akhir'], hasil), 2)}")
    jumlah_lulus = len(filter_by(where(lulus=True), hasil))
    print(f"Kelulusan      : {jumlah_lulus} dari {len(hasil)} mahasiswa ({persen(jumlah_lulus, len(hasil))}%)")

    print("\nSebaran nilai huruf:")
    for huruf, jumlah in sort_by(lambda x: x[0], count_by(lambda m: m["huruf"], hasil).items()):
        print(f" {huruf:<3}{'#' * jumlah} {jumlah}")

    print("\n3 besar:")
    for m in top_n(3, lambda m: m["akhir"], hasil):
        print(f" {m['peringkat']}. {m['nama']} ({m['akhir']})")


if __name__ == "__main__":
    main()
