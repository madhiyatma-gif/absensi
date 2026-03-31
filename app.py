from flask import Flask, request, render_template, Response
import io
from models import Base, Peserta, RiwayatAbsen
from database import engine, session
from datetime import date

app = Flask(__name__)
Base.metadata.create_all(engine)

# ------------------ MENU UTAMA ------------------
@app.route("/peserta")
def home_peserta():
    return """
    <h2>Menu Peserta</h2>
    <ul>
      <li><a href='/form_absen'>Form Absen</a></li>
      <li><a href='/lihat_akun'>Lihat Akun</a></li>
    </ul>
    """

@app.route("/operator")
def home_operator():
    return """
    <h2>Menu Operator</h2>
    <ul>
      <li><a href='/bulk_update'>Bulk Update ID & Password</a></li>
      <li><a href='/download_template'>Download Template CSV</a></li>
      <li><a href='/form_laporan'>Laporan Bulanan</a></li>
      <li><a href='/daftar_peserta'>Daftar Peserta Lengkap</a></li>
    </ul>
    """

# ------------------ PESERTA ------------------
@app.route("/form_absen", methods=["GET", "POST"])
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

# ------------------ OPERATOR ------------------
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
    output = io.StringIO()
    output.write("no,id,password\n")
    output.write("1,ID001,pass123\n")
    output.write("2,ID002,pass456\n")
    output.write("3,ID003,pass789\n")
    return Response(output.getvalue(),
                    mimetype="text/csv",
                    headers={"Content-Disposition":"attachment;filename=template.csv"})

@app.route("/form_laporan")
def form_laporan():
    return """
    <h3>Laporan Bulanan</h3>
    <form method="get" action="/laporan">
      Bulan (1-12): <input type="number" name="bulan"><br>
      Tahun (YYYY): <input type="number" name="tahun"><br>
      <input type="submit" value="Lihat Laporan">
    </form>
    """

@app.route("/laporan")
def laporan_route():
    bulan = int(request.args.get("bulan"))
    tahun = int(request.args.get("tahun"))
    return f"Laporan bulan {bulan} tahun {tahun} (data akan ditampilkan di sini)."

@app.route("/daftar_peserta")
def daftar_peserta():
    peserta_list = session.query(Peserta).all()
    html = "<h2>Daftar Peserta & Riwayat Absen</h2><table border='1'>"
    html += "<tr><th>No</th><th>Nama</th><th>No HP</th><th>ID</th><th>Password</th><th>Riwayat Absen</th></tr>"
    for p in peserta_list:
        # Ambil semua riwayat absen peserta ini
        riwayat_list = session.query(RiwayatAbsen).filter_by(peserta_id=p.no).all()
        riwayat_str = "<ul>"
        for r in riwayat_list:
            riwayat_str += f"<li>{r.tanggal} - {r.keterangan}</li>"
        riwayat_str += "</ul>"

        html += f"<tr><td>{p.no}</td><td>{p.nama}</td><td>{p.no_hp}</td><td>{p.id}</td><td>{p.password}</td><td>{riwayat_str}</td></tr>"
    html += "</table>"
    return html

# ------------------ RUN ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
