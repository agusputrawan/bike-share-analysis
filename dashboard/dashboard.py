import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from babel.numbers import format_currency

def create_rfm_df(df):
    rfm_df = df.groupby(by="hari", as_index=False).agg({
        "tanggal": "max",   
        "instant": "nunique", 
        "user_total": "sum"  
    })
    rfm_df.columns = ["hari", "max_order_timestamp", "frequency", "monetary"]
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = df["tanggal"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    
    return rfm_df


# Memasukkan file CSV
file_path = "dashboard/main_data.csv"
day_df = pd.read_csv(file_path)
day_df['tanggal'] = pd.to_datetime(day_df['tanggal'])
day_df.sort_values(by="tanggal", inplace=True)

day_df["user_total"] = day_df["user_kasual"] + day_df["user_terdaftar"]
day_df_resampled = day_df.resample('W', on='tanggal').sum()

# Konversi kolom 'tanggal' menjadi datetime
day_df['tanggal'] = pd.to_datetime(day_df['tanggal'])
datetime_columns = ["tanggal"]
day_df.sort_values(by="tanggal", inplace=True)
day_df.reset_index(inplace=True)

# Filter Sidebar untuk memfilter tanggal
st.sidebar.header("Filter Data")
min_date = day_df['tanggal'].min()
max_date = day_df['tanggal'].max()

start_date, end_date = st.sidebar.date_input(
    label='Range of Time', 
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Filter data berdasarkan tanggal yang dipilih
filtered_data = day_df[(day_df['tanggal'] >= pd.to_datetime(start_date)) & (day_df['tanggal'] <= pd.to_datetime(end_date))]

with st.sidebar:
    # Menambah logo
    st.image("dashboard/Bike_rental.jpg")

# Judul
st.title("Dashboard Penyewaan Sepeda:sparkles:")

# User perhari
st.subheader('Jumlah Pengguna Harian')

col1, col2, col3 = st.columns(3)

with col1:
    total_casual = filtered_data['user_kasual'].sum()
    st.metric("Total Pengguna Kasual", value=f'{total_casual:,}')

with col2:
    total_registered = filtered_data['user_terdaftar'].sum()
    st.metric("Total Pengguna Terdaftar", value=f'{total_registered:,}')

with col3:
    total_users = filtered_data['user_total'].sum()
    st.metric("Total Pengguna", value=f'{total_users:,}')


day_df_resampled["user_kasual_avg"] = day_df_resampled["user_kasual"].rolling(window=4, min_periods=1).mean()

# Plot grafik dengan perbaikan
# st.header("Jumlah Pengguna Kasual per Minggu")
st.markdown(
    "<h3 style='text-align: center;'>Jumlah Pengguna Kasual per Minggu</h3>", 
    unsafe_allow_html=True
)

plt.figure(figsize=(12, 6))

sns.lineplot(data=day_df_resampled, x=day_df_resampled.index, y='user_kasual_avg', 
             color='royalblue', linewidth=2, label="Moving Average (4 Minggu)")
sns.scatterplot(data=day_df_resampled, x=day_df_resampled.index, y='user_kasual', 
                color='red', alpha=0.5, label="Data Asli")

plt.title("Trend Jumlah Pengguna Kasual per Minggu", fontsize=14)
plt.xlabel("Tanggal", fontsize=12)
plt.ylabel("Jumlah Pengguna Kasual", fontsize=12)
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
st.pyplot(plt)

# Visualisasi Suhu dan Jumlah Penyewaan
# st.header("Visualisasi Suhu dan Jumlah Penyewaan")
st.markdown(
    "<h3 style='text-align: center;'>Visualisasi Suhu dan Jumlah Penyewaan</h3>", 
    unsafe_allow_html=True
)

plt.figure(figsize=(10, 6))
sns.regplot(data=day_df, x="temperatur", y="user_total", scatter_kws={'alpha': 0.5, 's': 30}, line_kws={'color': 'red'})
plt.title('Hubungan antara Suhu dan Jumlah Penyewaan', fontsize=14)
plt.xlabel('Temperatur', fontsize=12)
plt.ylabel('Jumlah Penyewaan', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)

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
# st.header("Jumlah Penyewaan Sepeda per Musim")
st.markdown(
    "<h3 style='text-align: center;'>Jumlah Penyewaan Sepeda per Musim</h3>", 
    unsafe_allow_html=True
)
seasonal_rentals = filtered_data.groupby('musim')['user_total'].sum().reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(data=seasonal_rentals, x='musim', y='user_total')
plt.title('Jumlah Penyewaan Sepeda per Musim')
plt.xlabel('Musim')
plt.ylabel('Jumlah Penyewaan Sepeda')
st.pyplot(plt)

#RFM
df_rfm = create_rfm_df(day_df)
if not df_rfm.empty:
    # st.subheader("Best Customer Based on RFM Parameters (Hari)")
    st.markdown(
    "<h3 style='text-align: center;'>Best Customer Based on RFM Parameters (Hari)</h3>", 
    unsafe_allow_html=True
)
    col1, col2, col3 = st.columns(3)

    with col1:
        avg_recency = round(df_rfm.recency.mean(), 1)
        st.metric("Rata-rata Recency (hari)", value=avg_recency)

    with col2:
        avg_frequency = round(df_rfm.frequency.mean(), 2)
        st.metric("Rata-rata Frequency", value=avg_frequency)

    with col3:
        avg_monetary = format_currency(df_rfm.monetary.mean(), "IDR", locale='id_ID') 
        st.metric("Rata-rata Monetary", value=avg_monetary)
    
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(18, 6), constrained_layout=True)
    colors = ["#64b5f6"] * 5  # Warna lebih soft
    
    # Recency
    sns.barplot(y="recency", x="hari", data=df_rfm.nsmallest(5, "recency"), palette=colors, ax=ax[0])
    ax[0].set_title("By Recency (days)", fontsize=12, fontweight='bold')
    ax[0].set_xlabel("Hari", fontsize=10)
    ax[0].set_ylabel("Recency (days)", fontsize=10)
    ax[0].tick_params(axis='x', rotation=30)
    ax[0].grid(axis='y', linestyle="--", alpha=0.6)

    # Frequency
    sns.barplot(y="frequency", x="hari", data=df_rfm.nlargest(5, "frequency"), palette=colors, ax=ax[1])
    ax[1].set_title("By Frequency", fontsize=12, fontweight='bold')
    ax[1].set_xlabel("Hari", fontsize=10)
    ax[1].set_ylabel("Frequency", fontsize=10)
    ax[1].tick_params(axis='x', rotation=30)
    ax[1].grid(axis='y', linestyle="--", alpha=0.6)

    # Monetary
    sns.barplot(y="monetary", x="hari", data=df_rfm.nlargest(5, "monetary"), palette=colors, ax=ax[2])
    ax[2].set_title("By Monetary", fontsize=12, fontweight='bold')
    ax[2].set_xlabel("Hari", fontsize=10)
    ax[2].set_ylabel("Monetary (IDR)", fontsize=10)
    ax[2].tick_params(axis='x', rotation=30)
    ax[2].grid(axis='y', linestyle="--", alpha=0.6)
    
    st.pyplot(fig)



# Kesimpulan
st.header("Kesimpulan")
st.write("""
- Terdapat hubungan positif yang kuat antara temperatur dan jumlah penyewaan sepeda dalam rentang waktu 2011/01/01 – 2012/12/31 dengan hasil (korelasi 0.63). 
- Di dalam rentang waktu 2011/01/01 – 2012/12/31 untuk setiap kenaikan satu unit suhu, jumlah penyewaan meningkat rata-rata 6640 unit, dengan R-squared 0.39, 
  menunjukkan suhu berpengaruh signifikan terhadap penyewaan sepeda.
- Rata-rata recency adalah 3 hari, artinya pelanggan terbaik (best customers) melakukan pembelian terakhir mereka rata-rata 3 hari yang lalu.
  Pelanggan yang paling sering kembali bertransaksi cenderung melakukan pembelian terbaru pada hari Senin, sedangkan pelanggan yang jarang kembali melakukan pembelian terakhir mereka pada hari Jumat.
- Rata-rata frekuensi transaksi pelanggan terbaik adalah 104 kali, menunjukkan bahwa pelanggan ini sangat loyal dan melakukan pembelian berulang kali.
  Hari-hari dengan frekuensi transaksi tertinggi relatif merata di beberapa hari seperti Minggu, Selasa, Senin, Jumat, dan Kamis. Tidak ada hari tertentu yang mendominasi secara signifikan.
  Monetary (Total Pengeluaran) 
- Rata-rata pengeluaran pelanggan terbaik adalah sekitar Rp470.382,71.
- Hari dengan jumlah pengeluaran tertinggi adalah Sabtu dan Jumat, sementara pengeluaran lebih rendah terjadi pada Rabu.
- Pelanggan terbaik cenderung melakukan transaksi terbaru dalam 3 hari terakhir, sangat sering bertransaksi (~104 kali), dan memiliki rata-rata pengeluaran yang cukup tinggi (~Rp470 ribu).
- Frekuensi transaksi cukup merata sepanjang minggu, tetapi pengeluaran terbesar terjadi pada akhir pekan (Sabtu & Jumat), yang bisa menjadi insight penting untuk strategi promosi dan diskon.
""")

# Saran
st.header("Saran")
st.write("""
1. Sesuaikan strategi pemasaran untuk hari dengan temperatur tinggi.
2. Kembangkan produk musiman sesuai dengan pola penyewaan.
3. Pantau data cuaca untuk prediksi tren penyewaan.
4. Menargetkan promosi akhir pekan (Jumat-Sabtu) untuk meningkatkan total pengeluaran.
5. Menggunakan program loyalitas untuk mendorong pelanggan agar lebih sering kembali.
6. Memanfaatkan hari Senin untuk retargeting pelanggan karena pelanggan aktif kembali setelah akhir pekan.
""")

st.caption(f"Copyright © 2024 All Rights Reserved [Putu Agus Putrawan](https://www.linkedin.com/in/putu-agus-putrawan/)")
