# Project Analisa Data menggunakan Bike Sharing Dataset
Tentang Bike Sharing Dataset
Bike Sharing adalah inovasi dari penyewaan sepeda tradisional yang mengotomatiskan proses mulai dari keanggotaan hingga penyewaan dan pengembalian. Dengan lebih dari 500 program di seluruh dunia dan 500.000 sepeda, sistem ini berkontribusi pada isu lalu lintas, lingkungan, dan kesehatan. Data yang dihasilkan dari sistem ini mencatat detail perjalanan, menjadikannya jaringan sensor virtual untuk memantau mobilitas perkotaan.

Set Data:
Proses penyewaan sepeda dipengaruhi oleh faktor lingkungan dan musiman seperti cuaca, hari dalam seminggu, dan waktu. Set data utama mencakup log historis dua tahun dari sistem Capital Bikeshare di Washington, D.C., pada 2011 dan 2012, yang dapat diakses di Capital Bikeshare. Data ini telah digabungkan berdasarkan jam dan hari, dengan informasi cuaca yang diperoleh dari Free Meteo.

# Informasi Dataset
- instant: indeks record
- dteday: tanggal
- season: musim (1: semi, 2: panas, 3: gugur, 4: dingin)
- yr: tahun (0: 2011, 1: 2012)
- mnth: bulan (1 sampai 12)
- hr: jam (0 sampai 23, hanya di hours.csv)
- holiday: hari libur(0: tidak, 1: ya)
- weekday: hari dalam minggu (0: Minggu, 1: Senin, ..., 6: Sabtu)
- workingday: Apabila hari tersebut bukan akhir pekan atau hari libur, bernilai 1; jika tidak, bernilai 0.
- weathersit:
  - 1: Cerah, Beberapa awan, Sebagian besar awan
  - 2: Kabut + Awan, Kabut + Awan terputus, Kabut + Beberapa awan
  - 3: Salju ringan, Hujan ringan + Petir + Awan terputus, Hujan ringan + Awan terputus
  - 4: Hujan deras + Ice Pallet + Petir + Kabut, Salju + Kabut
- temp: Suhu yang dikonversi dalam Celsius, dihitung dengan \((t - t_{min})/(t_{max} - t_{min})\), dengan \(t_{min} = -8\) dan \(t_{max} = +39\).
- atemp: Suhu yang dirasakan yang dinormalisasi dalam Celsius, dihitung dengan \((t - t_{min})/(t_{max} - t_{min})\), dengan \(t_{min} = -16\) dan \(t_{max} = +50\).
- hum: Kelembaban yang dikonversi, dibagi dengan 100 (maksimum)
- windspeed: Kecepatan angin yang dikonversi, dibagi dengan 67 (maksimum)
- casual: jumlah pengguna kasual
- registered: jumlah pengguna terdaftar
- cnt: jumlah total sepeda sewa, termasuk pengguna kasual dan terdaftar

# Cara menjalankan proyek ini
1. Clone Repositori ini
`https://github.com/agusputrawan/bike-share-analysis.git`
2. Install library yang diperlukan, contoh terdapat dalam requirement.txt
   `pip install -r requirements.txt`
3. Masuk kedalam folder dashboard
   `cd dashboard`
5. Jalankan dengan streamlit
   `streamlit run dashboard.py`
#atau kamu bisa mengunjungi website ini
#[https://bike-share-analysis-mdz8xpzih6dpjstkrhlmhx.streamlit.app/]

