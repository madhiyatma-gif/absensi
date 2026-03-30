from flask import Flask, request, render_template, Response
import io
from models import Base, Peserta, RiwayatAbsen
from database import engine, session
from datetime import date

app = Flask(__name__)
Base.metadata.create_all(engine)

@app.route("/", methods=["GET", "POST"])
def absen():
    if request.method == "POST":
        nama = request.form["nama"]
        no_hp = request.form["no_hp"]
        keterangan = request.form["keterangan"]

        peserta = session.query(Peserta).filter_by(nama=nama, no_hp=no_hp).first()
        if peserta:
            riwayat = RiwayatAbsen(peserta_id=peserta.no, tanggal=date.today(), keterangan=keterangan)
            session.add(riwayat)
            session.commit()
            return f"{peserta.nama} sudah absen."
        else:
            peserta_baru = Peserta(nama=nama, no_hp=no_hp)
            session.add(peserta_baru)
            session.commit()
            return "Peserta baru ditambahkan."
    return render_template("form_absen.html")

@app.route("/lihat_akun", methods=["GET", "POST"])
def lihat_akun():
    if request.method == "POST":
        nama = request.form["nama"]
        no_hp = request.form["no_hp"]

        peserta = session.query(Peserta).filter_by(nama=nama, no_hp=no_hp).first()
        if peserta:
            return f"ID: {peserta.id}, Password: {peserta.password}"
        else:
            return "Peserta tidak ditemukan."
    return render_template("form_lihat_akun.html")
@app.route("/bulk_update", methods=["GET", "POST"])
def bulk_update():
    if request.method == "POST":
        data = request.form["bulk_data"]
        lines = data.strip().split("\n")
        for line in lines:
            parts = line.split(",")
            if len(parts) == 3:
                no, id_baru, password_baru = parts
                peserta = session.query(Peserta).filter_by(no=int(no)).first()
                if peserta:
                    peserta.id = id_baru.strip()
                    peserta.password = password_baru.strip()
        session.commit()
        return "Update massal berhasil."
    return render_template("form_bulk_update.html")

@app.route("/download_template")
def download_template():
    # Buat CSV template sederhana
    output = io.StringIO()
    output.write("no,id,password\n")
    output.write("1,ID001,pass123\n")
    output.write("2,ID002,pass456\n")
    output.write("3,ID003,pass789\n")
    return Response(output.getvalue(),
                    mimetype="text/csv",
                    headers={"Content-Disposition":"attachment;filename=template.csv"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
