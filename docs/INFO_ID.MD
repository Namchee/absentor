# Discord Bot Pencatat Kehadiran Siswa

## Konteks

Membangun sebuah bot Discord untuk mencatat kehadiran siswa pada suatu server Discord dan menyimpan tiap pencatatan pada server tertentu kedalam Google Sheet.

## Latar Belakang

Dikarenakan peristiwa global yang sedang terjadi di dunia saat ini, banyak sekolah dan universitas berpindah ke jalur daring untuk melakukan aktivitas mereka. Salah satu perangkat lunak yang populer digunakan untuk melakukan hal tersebut adalah Discord. Discord adalah suatu perangkat lunak yang berspesialisasi pada bidang komunikasi berbasis teks, gambar, video, dan audio.

Karena pencatatan kehadiran merupakan salah satu aspek yang penting dalam kegiatan belajar-mengajar, pencatatan kehadiran menjadi hal yang penting bagi siswa maupun guru. Untuk saat ini hanya terdapat beberapa cara seorang guru dapat mengkonfirmasi indentitas seseorang didalam server Discord. Pertama dengan face cam, tapi hal ini mengharuskan semua orang pada server tersebut untuk memiliki kamera dan bahkan jika semua orang sudah memiliki kamera pengecakan dengan cara ini akan memakan banyak waktu dan membutuhkan usaha yang cukup lebih besar, terutama pada kelas yang memiliki jumlah murid yang cukup banyak. Kedua adalah dengan suara, untuk cara ini guru harus mengenali suara dari tiap siswa / siswi yang diajar olehnya, hal ini sangat sulit dilakukan kecuali guru yang melakukan pencatatan kehadiran memiliki pendengaran yang sangat bagus.

Kesulitan bagi seseorang untuk mengetahui kebenaran identitas seseorang pada suatu server Discord, dan ketidaktersediaan layanan untuk mencatat kehadiran pada Discord menjadi alasan mengapa proyek ini dimulai.

## Hasil yang Diharapkan

Suatu bot Discord yang dapat membantu mengurangi potensi pemalsuan identitas / pemalsuan kehadiran dan mempermudah proses pencatatan kehadiran para murid secara otomatis.

## Fitur yang Diharapkan

1. Seorang member pada suatu server dengan role tertentu memulai sebuah perintah (_command_) untuk memberi perintah kepada bot untuk mulai melakukan pencatatan kehadiran para murid dalam waktu tertentu.
2. Dalam waktu pencatatan ini para murid dapat menuliskan sebuah perintah yang akan memberi tahu bot tersebut bahwa dia hadir di server tersebut pada saat itu.
3. Bot akan melihat nama dan id unik yang dimiliki tiap murid dan mencatat nama mereka kedalam sheet yang sudah disediakan.

## Limitasi

1. Nama untuk murid pada server Discord harus mengikuti aturan `<nama> - <npm>`. Contoh: `Cristopher - 2017730017` merupakan format yang valid, sedangkan `fariz` bukan merupakan format yang valid dan harus diabaikan

## Teknologi yang Digunakan

1. Python
2. Discord API
