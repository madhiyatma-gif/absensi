from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey

Base = declarative_base()

class Peserta(Base):
    __tablename__ = "peserta"
    no = Column(Integer, primary_key=True, autoincrement=True)
    nama = Column(String(100))
    no_hp = Column(String(20))
    id = Column(String(50))
    password = Column(String(50))

class RiwayatAbsen(Base):
    __tablename__ = "riwayat_absen"
    id = Column(Integer, primary_key=True, autoincrement=True)
    peserta_id = Column(Integer, ForeignKey("peserta.no"))
    tanggal = Column(Date)
    keterangan = Column(String(255))
