from models import Peserta
from database import session

def update_operator(no, id, password):
    peserta = session.query(Peserta).filter_by(no=no).first()
    if peserta:
        peserta.id = id
        peserta.password = password
        session.commit()
        print("ID & Password diperbarui.")
