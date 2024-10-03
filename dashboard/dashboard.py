import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

# Memasukkan file CSV
file_path = "dashboard/main_data.csv"
day_df = pd.read_csv(file_path)

# Konversi kolom 'tanggal' menjadi datetime
day_df['tanggal'] = pd.to_datetime(day_df['tanggal'])

# Filter Sidebar= untuk memelih tanggal
st.sidebar.header("Filter Data")
min_date = day_df['tanggal'].min()
max_date = day_df['tanggal'].max()
date_filter = st.sidebar.date_input("Pilih Tanggal", min_date)

with st.sidebar:
    # Menambahkan logo
    st.image("dashboard/Bike_rental.jpg")

# Filter data berdasarkan tanggal 
filtered_data = day_df[day_df['tanggal'] == pd.to_datetime(date_filter)]

# Judul
st.title("Dashboard Penyewaan Sepeda:sparkles:")

# Menampilkan total pengguna 
total_casual_users = filtered_data['user_kasual'].sum()
total_registered_users = filtered_data['user_terdaftar'].sum()
total_users = filtered_data['user_total'].sum()

st.header("Informasi Pengguna Hari Ini")
st.write(f"Total Pengguna Kasual: {total_casual_users}")
st.write(f"Total Pengguna Terdaftar: {total_registered_users}")
st.write(f"Total Pengguna: {total_users}")

# Visualisasi Jumlah Pengguna Kasual dan Terdaftar per Hari
st.header("Jumlah Pengguna Kasual dan Terdaftar per Hari")
plt.figure(figsize=(10, 6))
sns.lineplot(data=day_df, x='tanggal', y='user_kasual', label='Pengguna Kasual')
sns.lineplot(data=day_df, x='tanggal', y='user_terdaftar', label='Pengguna Terdaftar')
plt.title('Jumlah Pengguna Kasual dan Terdaftar per Hari')
plt.xlabel('Tanggal')
plt.ylabel('Jumlah Pengguna')
plt.xticks(rotation=45)
plt.legend()
st.pyplot(plt)

# Visualisasi Suhu dan Jumlah Penyewaan
st.header("Visualisasi Suhu dan Jumlah Penyewaan")
plt.figure(figsize=(10, 6))
sns.scatterplot(data=day_df, x='temperatur', y='user_total')
plt.title('Hubungan antara Suhu dan Jumlah Penyewaan')
plt.xlabel('Temperatur')
plt.ylabel('Jumlah Penyewaan')
st.pyplot(plt)

# Analisa Korelasi
correlation_temp_rentals = day_df['temperatur'].corr(day_df['user_total'])
st.write(f"Korelasi antara Temperatur dan Jumlah Penyewaan: {correlation_temp_rentals}")

# Regresi Linear
X = day_df['temperatur']
y = day_df['user_total']
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()

st.subheader("Hasil Regresi Linear")
st.write("""
- Koefisien Intersep: 1214.64
- Koefisien Temperatur: 6640.71
- R-squared: 0.394
- F-statistic: 473.5
- Prob (F-statistic): 2.81e-81
""")

# Visualisasi Jumlah Penyewaan per Musim
st.header("Jumlah Penyewaan Sepeda per Musim")
seasonal_rentals = day_df.groupby('musim')['user_total'].sum().reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(data=seasonal_rentals, x='musim', y='user_total')
plt.title('Jumlah Penyewaan Sepeda per Musim')
plt.xlabel('Musim')
plt.ylabel('Jumlah Penyewaan Sepeda')
st.pyplot(plt)

# Analisis Varians (ANOVA)
groups = [group['user_total'].values for name, group in day_df.groupby('musim')]
f_statistic, p_value = stats.f_oneway(*groups)
st.write(f'F-statistic: {f_statistic}, p-value: {p_value}')

# Kesimpulan
st.header("Kesimpulan")
st.write("""
- Terdapat hubungan positif yang kuat antara temperatur dan jumlah penyewaan sepeda (korelasi 0.63). 
- Setiap kenaikan satu unit suhu, jumlah penyewaan meningkat rata-rata 6640 unit, dengan R-squared 0.39, 
  menunjukkan suhu berpengaruh signifikan terhadap penyewaan sepeda.
  
- Variasi musiman mempengaruhi jumlah penyewaan sepeda, dengan F-statistic 128.77 dan p-value < 0.001, 
  menunjukkan perbedaan signifikan antara musim.
""")

# Saran
st.header("Saran")
st.write("""
1. Sesuaikan strategi pemasaran untuk hari dengan temperatur tinggi.
2. Kembangkan produk musiman sesuai dengan pola penyewaan.
3. Pantau data cuaca untuk prediksi tren penyewaan.
""")

st.caption(f"Copyright © 2024 All Rights Reserved [Putu Agus Putrawan](https://www.linkedin.com/in/putu-agus-putrawan/)")
