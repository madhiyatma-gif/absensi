# utils/helpers.py
from datetime import datetime

def format_tanggal(tanggal):
    """
    Mengubah objek datetime/date menjadi string format Indonesia.
    Contoh: 2026-03-30 -> '30 Maret 2026'
    """
    bulan = {
        "01": "Januari", "02": "Februari", "03": "Maret", "04": "April",
        "05": "Mei", "06": "Juni", "07": "Juli", "08": "Agustus",
        "09": "September", "10": "Oktober", "11": "November", "12": "Desember"
    }
    tgl = tanggal.strftime("%d")
    bln = bulan[tanggal.strftime("%m")]
    thn = tanggal.strftime("%Y")
    return f"{tgl} {bln} {thn}"

def validasi_no_hp(no_hp):
    """
    Validasi nomor HP sederhana:
    - hanya angka
    - panjang minimal 10 digit
    """
    if no_hp.isdigit() and len(no_hp) >= 10:
        return True
    return False

def input_int(prompt):
    """
    Fungsi input integer dengan validasi.
    """
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Input harus berupa angka. Coba lagi.")

def garis_pemisah():
    """
    Cetak garis pemisah untuk tampilan menu.
    """
    print("=" * 40)
