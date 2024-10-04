import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

# Memasukkan file CSV
file_path = "main_data.csv"
day_df = pd.read_csv(file_path)

# Konversi kolom 'tanggal' menjadi datetime
day_df['tanggal'] = pd.to_datetime(day_df['tanggal'])
datetime_columns = ["tanggal"]
day_df.sort_values(by="tanggal", inplace=True)
day_df.reset_index(inplace=True)

# Filter Sidebar untuk memfilter tanggal
st.sidebar.header("Filter Data")
min_date = day_df['tanggal'].min()
max_date = day_df['tanggal'].max()

# Membuat komponen filter
start_date, end_date = st.sidebar.date_input(
    label='Range of Time', 
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Filter data berdasarkan tanggal yang dipilih
filtered_data = day_df[(day_df['tanggal'] >= pd.to_datetime(start_date)) & (day_df['tanggal'] <= pd.to_datetime(end_date))]

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

# User perhari
st.subheader('Jumlah Pengguna Harian')
col1, col2, col3 = st.columns(3)

with col1:
    total_casual = filtered_data['user_kasual'].sum()
    st.metric("Total Casual User", value=f'{total_casual:,}')

with col2:
    total_registered = filtered_data['user_terdaftar'].sum()
    st.metric("Total Registered User", value=f'{total_registered:,}')

with col3:
    total_users = filtered_data['user_total'].sum()
    st.metric("Total Users", value=f'{total_users:,}')

# Visualisasi Jumlah Pengguna Kasual dan Terdaftar per Hari
st.header("Jumlah Pengguna Kasual dan Terdaftar per Hari")
plt.figure(figsize=(10, 6))
sns.lineplot(data=filtered_data, x='tanggal', y='user_kasual', label='Pengguna Kasual')
sns.lineplot(data=filtered_data, x='tanggal', y='user_terdaftar', label='Pengguna Terdaftar')
plt.title('Jumlah Pengguna Kasual dan Terdaftar per Hari')
plt.xlabel('Tanggal')
plt.ylabel('Jumlah Pengguna')
plt.xticks(rotation=45)
plt.legend()
st.pyplot(plt)

# Visualisasi Suhu dan Jumlah Penyewaan
st.header("Visualisasi Suhu dan Jumlah Penyewaan")
plt.figure(figsize=(10, 6))
sns.scatterplot(data=filtered_data, x='temperatur', y='user_total')
plt.title('Hubungan antara Suhu dan Jumlah Penyewaan')
plt.xlabel('Temperatur')
plt.ylabel('Jumlah Penyewaan')
st.pyplot(plt)

# Analisa Korelasi
correlation_temp_rentals = filtered_data['temperatur'].corr(filtered_data['user_total'])
st.write(f"Korelasi antara Temperatur dan Jumlah Penyewaan: {correlation_temp_rentals}")

# Hasil Regresi Linear
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
seasonal_rentals = filtered_data.groupby('musim')['user_total'].sum().reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(data=seasonal_rentals, x='musim', y='user_total')
plt.title('Jumlah Penyewaan Sepeda per Musim')
plt.xlabel('Musim')
plt.ylabel('Jumlah Penyewaan Sepeda')
st.pyplot(plt)

# Analisis Varians (ANOVA)
groups = [group['user_total'].values for name, group in filtered_data.groupby('musim')]
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
