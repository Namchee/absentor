# Absentor

Sebuah _chatbot_ sederhana untuk melakukan otomatisasi absensi mahasiswa untuk platform [Discord](https://discordapp.com/download)

## Tech Stack

1. Python 3.x.x (disarankan 3.8.x)

## Instalasi

1. Clone repository ini
2. Masuk ke _root directory_ dari project ini, kemudian buatlah _virtual environment_ python dengan perintah `virtualenv <nama folder>` (namanya bebas, tapi isi saja dengan `venv`)
3. Jalankan perintah `pip install -r requirements.txt`
4. Sebelum _running_ program, pastikan bahwa `virtualenv` juga sedang _running_. Cara manualnya dengan menjalankan perintah `venv/Scripts/Activate` atau bila menggunakan IDE, pastikan bahwa IDE anda mendeteksi `virtualenv` tersebut dan menggunakan interpreter yang ada didalamnya. (Visual Studio Code: F1 -> Python: Select Interpreter -> pilih `<nama folder>` yang telah anda buat dalam langkah 2)
5. Copy file `.env` dan `credentials.json` yang anda miliki ke _root_ folder dari project ini
6. Jalankan aplikasi dengan mengetikkan perintah `py main.py`

## FAQ

1. Tolong!!! Saya nyangkut di langkah X!

    Pastikan anda:
    - Bisa me-_run_ Python dengan lancar
    - Mengikuti langkah-langkah yang ada diatas dengan benar

2. Saya ingin menambahkan _dependency_ untuk project ini!

    Silahkan saja, selama _dependency_ tersebut benar-benar dipakai. Untuk menambahkan _dependency_,
    cukup `pip install <dependency>` seperti biasa KEMUDIAN jalankan perintah `pip freeze > requirements.txt`. langkah tersebut berguna untuk meng-_update_ `requirements.txt` sehingga memasukkan _dependency_ yang baru anda tambahkan.

## Catatan Tambahan

1. Sebisa mungkin, gunakan _named import_ pada saat meng-import _dependency_
2. Tambahkan _file_ baru yang anda butuhkan pada folder `src` :exclamation:
3. Nama _file_ harus merupakan sebuah `kebab-case`. Tata cara penamaan lain seperti `PascalCase`, `snake_case`, maupun `camelCase` akan ditolak :exclamation:
4. Sebisa mungkin, gunakan `snake_case` dalam menamakan _variable_ atau _method_
5. Sebisa mungkin, berikan komentar pada kode yang anda buat (itu ngapain)
6. Jelaskan _commit message_ anda sejelas mungkin, bila perlu gunakan _conventional commit_
7. Apabila anda yakin mengenai pekerjaan anda, mohon _update_ `README.MD` dengan menambahkan nama anda sendiri
8. :exclamation: JANGAN IKUT MENG-COMMIT TOKEN DAN CREDENTIALS :exclamation:

Melanggar ketentuan tersebut dapat mengakibatkan _pull request_ anda tertolak :exclamation:

## Kontributor

1. Cristopher 'Namchee' - [GitHub](https://github.com/namchee)

PS: Penambahan kontributor hanya akan dilakukan bila anda melakukan _meaningful commit_ pada project ini
