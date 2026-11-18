"""
Pengujian untuk fplib.py.

Jalankan: python -m pytest -v
"""

import copy

import pytest

from fplib import (average_by, count_by, filter_by, group_by, persen, pipe, rupiah,
                   sort_by, sum_by, top_n, update, where)


@pytest.fixture
def data():
    return (
        {"nama": "Es Teh", "kategori": "minuman", "harga": 4000},
        {"nama": "Nasi Goreng", "kategori": "makanan", "harga": 15000},
        {"nama": "Kopi Susu", "kategori": "minuman", "harga": 8000},
        {"nama": "Mie Ayam", "kategori": "makanan", "harga": 13000},
    )


def harga(item):
    return item["harga"]


def kategori(item):
    return item["kategori"]


# ---------- pipe ----------

def test_pipe_menjalankan_fungsi_dari_kiri_ke_kanan():
    assert pipe(3, lambda x: x + 1, lambda x: x * 10) == 40


def test_pipe_tanpa_fungsi_mengembalikan_nilai_awal():
    assert pipe(5) == 5


# ---------- where ----------

def test_where_menghasilkan_fungsi():
    assert callable(where(kategori="minuman"))


def test_where_mencocokkan_semua_kriteria(data):
    cocok = where(kategori="minuman", harga=8000)
    assert [cocok(item) for item in data] == [False, False, True, False]


def test_where_tanpa_kriteria_selalu_true(data):
    assert all(where()(item) for item in data)


# ---------- filter_by ----------

def test_filter_by_mengambil_item_yang_cocok(data):
    hasil = filter_by(where(kategori="makanan"), data)
    assert [item["nama"] for item in hasil] == ["Nasi Goreng", "Mie Ayam"]


def test_filter_by_mengembalikan_tuple(data):
    assert isinstance(filter_by(lambda item: True, data), tuple)


def test_filter_by_tidak_ada_yang_cocok(data):
    assert filter_by(lambda item: item["harga"] > 100000, data) == ()


# ---------- sum_by ----------

def test_sum_by(data):
    assert sum_by(harga, data) == 40000


def test_sum_by_data_kosong():
    assert sum_by(harga, ()) == 0


# ---------- average_by ----------

def test_average_by(data):
    assert average_by(harga, data) == 10000


def test_average_by_data_kosong_tidak_error():
    assert average_by(harga, ()) == 0.0


# ---------- group_by ----------

def test_group_by_mengelompokkan_dan_menjaga_urutan(data):
    hasil = group_by(kategori, data)
    assert list(hasil) == ["minuman", "makanan"]
    assert [item["nama"] for item in hasil["minuman"]] == ["Es Teh", "Kopi Susu"]


def test_group_by_data_kosong():
    assert group_by(kategori, ()) == {}


# ---------- count_by ----------

def test_count_by(data):
    assert count_by(kategori, data) == {"minuman": 2, "makanan": 2}


# ---------- sort_by ----------

def test_sort_by_naik(data):
    assert [harga(item) for item in sort_by(harga, data)] == [4000, 8000, 13000, 15000]


def test_sort_by_turun(data):
    assert [harga(item) for item in sort_by(harga, data, descending=True)] == [15000, 13000, 8000, 4000]


# ---------- top_n ----------

def test_top_n(data):
    assert [item["nama"] for item in top_n(2, harga, data)] == ["Nasi Goreng", "Mie Ayam"]


@pytest.mark.parametrize("n, panjang", [(0, 0), (-1, 0), (10, 4)])
def test_top_n_batas(data, n, panjang):
    assert len(top_n(n, harga, data)) == panjang


# ---------- update ----------

def test_update_mengubah_dan_menambah_field():
    assert update({"a": 1, "b": 2}, b=5, c=3) == {"a": 1, "b": 5, "c": 3}


def test_update_tidak_mengubah_record_asli():
    asli = {"jumlah": 1}
    baru = update(asli, jumlah=2)
    assert asli == {"jumlah": 1}
    assert baru is not asli


# ---------- rupiah ----------

@pytest.mark.parametrize("angka, teks", [
    (0, "Rp0"),
    (500, "Rp500"),
    (15000, "Rp15.000"),
    (1250000, "Rp1.250.000"),
    (-7400, "-Rp7.400"),
])
def test_rupiah(angka, teks):
    assert rupiah(angka) == teks


# ---------- persen ----------

def test_persen():
    assert persen(1, 3) == 33.3
    assert persen(1, 3, digit=2) == 33.33


def test_persen_total_nol_tidak_error():
    assert persen(5, 0) == 0.0


# ---------- sifat fungsional ----------

def test_semua_fungsi_tidak_mengubah_argumen(data):
    salinan = copy.deepcopy(data)
    filter_by(where(kategori="minuman"), data)
    sum_by(harga, data)
    average_by(harga, data)
    group_by(kategori, data)
    count_by(kategori, data)
    sort_by(harga, data)
    top_n(2, harga, data)
    update(data[0], harga=1)
    assert data == salinan


def test_fungsi_murni_hasil_selalu_sama(data):
    assert group_by(kategori, data) == group_by(kategori, data)
    assert sort_by(harga, data) == sort_by(harga, data)
