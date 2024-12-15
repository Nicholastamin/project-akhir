from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from utils import load_keras_model, load_class_names, predict_class
import os

# Inisialisasi Flask
app = Flask(__name__)
app.secret_key = "your_secret_key"

# Konfigurasi Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Model Database untuk User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Path ke model dan label
MODEL_PATH = "models/keras_Model.h5"
LABELS_PATH = "labels.txt"

# Folder untuk upload gambar
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Muat model dan label
model = load_keras_model(MODEL_PATH)
class_names = load_class_names(LABELS_PATH)

# ROUTES
@app.route("/login", methods=["GET", "POST"])
def login():
    """Halaman Login"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Validasi user
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session["username"] = username
            return redirect(url_for("index"))
        else:
            return "Username atau password salah", 401
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Halaman Register"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if password != confirm_password:
            return "Password tidak cocok", 400
        # Cek jika username sudah ada
        if User.query.filter_by(username=username).first():
            return "Username sudah terdaftar", 400
        # Tambahkan user baru ke database
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    """Logout User"""
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/")
def index():
    """Halaman utama"""
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    """Endpoint untuk melakukan prediksi"""
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    # Simpan file sementara
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Lakukan prediksi
    class_name, confidence_score = predict_class(model, class_names, file_path)

    # Hapus file setelah digunakan
    os.remove(file_path)

    # Tampilkan hasil
    return render_template("result.html", class_name=class_name, confidence_score=confidence_score)

if __name__ == "__main__":
    # Buat tabel jika belum ada
    with app.app_context():
        db.create_all()
    app.run(debug=True)