from models import Peserta, RiwayatAbsen
from database import session
from sqlalchemy import func

def laporan_bulanan(bulan, tahun):
    hasil = session.query(
        Peserta.nama,
        func.count(RiwayatAbsen.id).label("jumlah")
    ).join(RiwayatAbsen, Peserta.no == RiwayatAbsen.peserta_id)\
     .filter(func.strftime("%m", RiwayatAbsen.tanggal) == str(bulan).zfill(2),
             func.strftime("%Y", RiwayatAbsen.tanggal) == str(tahun))\
     .group_by(Peserta.nama).all()

    for nama, jumlah in hasil:
        print(f"{nama}: {jumlah} kali absen")
