from flask import Flask, request, render_template_string
from models import Base
from database import engine
from services.absen_service import absen
from services.operator_service import update_operator
from reports.laporan import laporan_bulanan

app = Flask(__name__)

# Inisialisasi database
Base.metadata.create_all(engine)

@app.route("/")
def home():
    return """
    <h2>Sistem Absensi</h2>
    <ul>
      <li><a href='/form_absen'>Form Absen</a></li>
      <li><a href='/form_update'>Update ID & Password</a></li>
      <li><a href='/form_laporan'>Laporan Bulanan</a></li>
    </ul>
    """

@app.route("/form_absen")
def form_absen():
    return """
    <h3>Form Absensi</h3>
    <form method="post" action="/absen">
      Nama: <input type="text" name="nama"><br>
      No HP: <input type="text" name="no_hp"><br>
      Keterangan: <input type="text" name="keterangan"><br>
      <input type="submit" value="Absen">
    </form>
    """

@app.route("/absen", methods=["POST"])
def absen_route():
    nama = request.form["nama"]
    no_hp = request.form["no_hp"]
    keterangan = request.form["keterangan"]
    absen(nama, no_hp, keterangan)
    return "<p>Absensi berhasil!</p><a href='/'>Kembali</a>"

@app.route("/form_update")
def form_update():
    return """
    <h3>Update ID & Password</h3>
    <form method="post" action="/update">
      Nomor urut peserta: <input type="number" name="no"><br>
      ID baru: <input type="text" name="id"><br>
      Password baru: <input type="text" name="password"><br>
      <input type="submit" value="Update">
    </form>
    """

@app.route("/update", methods=["POST"])
def update_route():
    no = int(request.form["no"])
    id_baru = request.form["id"]
    password_baru = request.form["password"]
    update_operator(no, id_baru, password_baru)
    return "<p>ID & Password berhasil diupdate!</p><a href='/'>Kembali</a>"

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
    hasil = laporan_bulanan(bulan, tahun)
    return render_template_string("<h3>Laporan Bulanan</h3><pre>{{hasil}}</pre>", hasil=hasil)

if __name__ == "__main__":
    app.run(debug=True)
