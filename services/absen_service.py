from datetime import date
from models import Peserta, RiwayatAbsen
from database import session

def absen(nama, no_hp, keterangan):
    peserta = session.query(Peserta).filter_by(nama=nama, no_hp=no_hp).first()
    if peserta:
        riwayat = RiwayatAbsen(peserta_id=peserta.no, tanggal=date.today(), keterangan=keterangan)
        session.add(riwayat)
        session.commit()
        total = session.query(RiwayatAbsen).filter_by(peserta_id=peserta.no).count()
        print(f"{peserta.nama} sudah absen {total} kali.")
    else:
        peserta_baru = Peserta(nama=nama, no_hp=no_hp)
        session.add(peserta_baru)
        session.commit()
        print("Peserta baru ditambahkan.")
