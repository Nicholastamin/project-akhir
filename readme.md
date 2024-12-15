# FOOD SELECTOR
Ini adalah proyek yang bertujuan untuk mendeteksi makanan sehat dan tidak sehat melalui gambar

# CARA KERJA APLIKASI
Web ini menggunakan Flask sebagai backend untuk menangani rute-rute seperti login, register, dan prediksi. Pada rute /login, pengguna diminta memasukkan username dan password, lalu diarahkan ke halaman utama jika berhasil. Di rute /register, pengguna dapat mendaftar dengan memasukkan username dan password, dan jika password cocok, mereka diarahkan ke halaman login. Halaman utama (/) memungkinkan pengguna mengunggah gambar untuk diprediksi oleh model Keras. Gambar yang diunggah diproses, diprediksi menggunakan model yang diload dari file keras_Model.h5, dan hasilnya ditampilkan di halaman result.html. Gambar disimpan sementara di folder uploads dan dihapus setelah prediksi. Semua tampilan menggunakan HTML yang dirender oleh Flask, termasuk formulir login, pendaftaran, dan prediksi.
