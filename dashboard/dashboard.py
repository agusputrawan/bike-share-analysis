import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm

# Memasukkan file CSV
file_path = "dashboard/main_data.csv"
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
X = filtered_data['temperatur']
y = filtered_data['user_total']
X = sm.add_constant(X)  # Tambah konstanta untuk intersep
model = sm.OLS(y, X).fit()  # Fit model regresi
intercept = model.params[0]
coef_temperature = model.params[1]
r_squared = model.rsquared

# Menampilkan hasil regresi
st.subheader("Hasil Regresi Linear")
st.write(f"""
- Koefisien Intersep: {intercept:.2f}
- Koefisien Temperatur: {coef_temperature:.2f}
- R-squared: {r_squared:.2f}
""")

# Kesimpulan
st.header("Kesimpulan")
st.write(f"""
- Terdapat hubungan positif yang kuat antara temperatur dan jumlah penyewaan sepeda (korelasi {correlation_temp_rentals:.2f}). 
- Setiap kenaikan satu unit suhu, jumlah penyewaan meningkat rata-rata {coef_temperature:.2f} unit, dengan R-squared {r_squared:.2f}, 
  menunjukkan suhu berpengaruh signifikan terhadap penyewaan sepeda.
""")

# Saran
st.header("Saran")
st.write(""" 
1. Sesuaikan strategi pemasaran untuk hari dengan temperatur tinggi.
2. Kembangkan produk musiman sesuai dengan pola penyewaan.
3. Pantau data cuaca untuk prediksi tren penyewaan.
""")

st.caption(f"Copyright © 2024 All Rights Reserved [Putu Agus Putrawan](https://www.linkedin.com/in/putu-agus-putrawan/)")
