import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("random_forest_best_model.pkl")

st.title("🩺 Prediksi Kategori Berat Badan Berdasarkan Gaya Hidup")

# Input Data 
age = st.number_input("Usia (tahun)", value=20)

gender = st.radio("Jenis Kelamin", [0, 1], format_func=lambda x: "Perempuan" if x == 0 else "Laki-laki")

height = st.number_input("Tinggi badan (meter)", value=1.70, step=0.01)

weight = st.number_input("Berat badan (kg)", value=65.0, step=0.5)

calc = st.selectbox("Seberapa Sering Konsumsi Alkohol", [0, 1, 2], format_func=lambda x: ["Tidak Pernah", "Kadang", "Sering"][x])

favc = st.selectbox("Sering Konsumsi Makanan Tinggi Kalori?", [0, 1], format_func=lambda x: "Tidak" if x == 0 else "Ya")

fcvc = st.number_input("Frekuensi Konsumsi Sayur (1 - 3)", min_value=1.0, max_value=3.0, step=0.1)

ncp = st.number_input("Jumlah Makan Utama per Hari (1 - 4)", min_value=1.0, max_value=4.0, step=1.0)

scc = st.selectbox("Konsultasi Gizi", [0, 1], format_func=lambda x: "Tidak" if x == 0 else "Ya")

smoke = st.selectbox("Apakah Anda Merokok?", [0, 1], format_func=lambda x: "Tidak" if x == 0 else "Ya")

ch2o = st.number_input("Konsumsi Air Harian (1 - 3 liter)", min_value=1.0, max_value=4.0, step=0.1)
if ch2o < 1.0 or ch2o > 3.0:
    st.info("Model dilatih dengan konsumsi air antara 1 hingga 3 liter. Nilai di luar rentang ini dapat memengaruhi akurasi prediksi.")

history = st.selectbox("Riwayat Keluarga Obesitas", [0, 1], format_func=lambda x: "Tidak" if x == 0 else "Ya")

faf = st.number_input("Aktivitas Fisik Mingguan (jam)", min_value=0.0, max_value=6.0, step=0.1)
if faf < 0.0 or faf > 3.0:
    st.info("Aktivitas fisik dalam data pelatihan berkisar 0 hingga 3 jam. Di atas itu, akurasi model bisa berkurang.")

tue = st.number_input("Waktu di Depan Layar per Hari (jam)", min_value=0.0, max_value=10.0, step=0.1)
if tue < 0.0 or tue > 2.0:
    st.info("Model dilatih dengan waktu layar harian antara 0 hingga 2 jam. Nilai lebih dari itu dapat menghasilkan prediksi yang kurang akurat.")

caec = st.selectbox("Frekuensi Makan Berlebihan", [0, 1, 2, 3], format_func=lambda x: ["Tidak Pernah", "Kadang", "Sering", "Selalu"][x])

mtrans = st.selectbox("Transportasi Harian", [0, 1, 2, 3, 4], format_func=lambda x: ["Transportasi Umum", "Jalan Kaki", "Mobil", "Motor", "Sepeda"][x])

# Prediksi 
if st.button("🔍 Prediksi"):
    # Susun urutan input sesuai model
    data = pd.DataFrame([[
        age, gender, height, weight, calc, favc, fcvc, ncp, scc, smoke,
        ch2o, history, faf, tue, caec, mtrans
    ]], columns=[
        "Age", "Gender", "Height", "Weight", "CALC", "FAVC", "FCVC", "NCP",
        "SCC", "SMOKE", "CH2O", "family_history_with_overweight", "FAF",
        "TUE", "CAEC", "MTRANS"
    ])

    prediction = model.predict(data)[0]

    # Mapping label ke bentuk lebih rapi
    label_desc = {
        0: "Insufficient_Weight",
        1: "Normal_Weight",
        2: "Overweight_Level_I",
        3: "Overweight_Level_II",
        4: "Obesity_Type_I",
        5: "Obesity_Type_II",
        6: "Obesity_Type_III"
    }

    hasil = label_desc.get(prediction, prediction)

    st.subheader("📊 Hasil Prediksi:")
    st.success(f"Kategori Berat Badan Anda: **{hasil}**")
