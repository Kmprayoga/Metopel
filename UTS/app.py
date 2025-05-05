from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Data fitur utama dan sub-fitur
fitur_subfitur = {
    "Demam": ["Demam tinggi", "Menggigil"],
    "Batuk": ["Batuk", "Batuk berdahak", "Batuk berdarah", "Batuk tidak berhenti", "Batuk menahun", "Batuk persisten"],
    "Sesak Napas": ["Sesak napas", "Napas pendek", "Sesak napas disertai wheezing (mengi)"],
    "Dahak": ["Dahak kental berwarna kuning", "Dahak berdarah", "Beringus (rhinorrhea)", "Pilek / hidung meler"],
    "Penurunan Kondisi Umum": ["Kehilangan nafsu makan", "Berat badan menurun", "Kelelahan / lelah"],
    "Kesadaran": ["Disorientasi", "Kehilangan kesadaran"],
    "Pencernaan": ["Muntah-muntah"],
    "Suara dan Tenggorokan": ["Suara serak/parau", "Tenggorokan sakit", "Pembengkakan"],
    "Nyeri dan Tubuh": ["Sakit kepala", "Nyeri dada", "Sakit otot"],
    "Mata dan Hidung": ["Mata merah / berair", "Bersin", "Gelisah / susah tidur"],
    "Sirkulasi / Kronis": ["Kulit kebiruan / pucat", "Clubbing finger (jari tabuh)"],
    "ISPA Ringan": ["Flu atau pilek"]
}

# Bobot sub-fitur
bobot_subfitur = {
    "Demam tinggi": 1, "Menggigil": 1,
    "Batuk": 1, "Batuk berdahak": 10, "Batuk berdarah": 10, "Batuk tidak berhenti": 10, "Batuk menahun": 10, "Batuk persisten": 10,
    "Sesak napas": 1, "Napas pendek": 10, "Sesak napas disertai wheezing (mengi)": 10,
    "Dahak kental berwarna kuning": 10, "Dahak berdarah": 10, "Beringus (rhinorrhea)": 1, "Pilek / hidung meler": 1,
    "Kehilangan nafsu makan": 1, "Berat badan menurun": 1, "Kelelahan / lelah": 1,
    "Disorientasi": 10, "Kehilangan kesadaran": 10,
    "Muntah-muntah": 1,
    "Suara serak/parau": 1, "Tenggorokan sakit": 1, "Pembengkakan": 1,
    "Sakit kepala": 1, "Nyeri dada": 10, "Sakit otot": 1,
    "Mata merah / berair": 1, "Bersin": 1, "Gelisah / susah tidur": 1,
    "Kulit kebiruan / pucat": 10, "Clubbing finger (jari tabuh)": 10,
    "Flu atau pilek": 1
}

df_kasus = pd.read_excel("Tabel_18_Kasus_Biner.xlsx")
basis_kasus = {
    row["Nama Kasus"]: row.drop("Nama Kasus").tolist() for _, row in df_kasus.iterrows()
}
subfitur_list = list(bobot_subfitur.keys())

# Hitung similarity berbobot dan lokal
def jaccard_similarity(kasus1, kasus2):
    skor_lokal = []
    total_bobot_aktif = 0
    total_bobot_cocok = 0
    for i, fitur in enumerate(subfitur_list):
        if kasus1[i] == 1 or kasus2[i] == 1:
            total_bobot_aktif += bobot_subfitur[fitur]
            if kasus1[i] == kasus2[i] == 1:
                skor_lokal.append((fitur, bobot_subfitur[fitur]))
                total_bobot_cocok += bobot_subfitur[fitur]
            else:
                skor_lokal.append((fitur, 0))
    similarity_global = total_bobot_cocok / total_bobot_aktif if total_bobot_aktif else 0
    return similarity_global, skor_lokal, total_bobot_cocok

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        selected_subfitur = request.form.getlist("subfitur")
        kasus_baru = [1 if fitur in selected_subfitur else 0 for fitur in subfitur_list]
        hasil = []
        for nama_kasus, vektor in basis_kasus.items():
            skor_global, skor_lokal, skor_lokal_total = hitung_similarity(kasus_baru, vektor)
            hasil.append((nama_kasus, skor_global, skor_lokal, skor_lokal_total))
        hasil = sorted(hasil, key=lambda x: x[1], reverse=True)[:5]
        return render_template("hasil.html", hasil=hasil)
    return render_template("index.html", fitur_subfitur=fitur_subfitur)

if __name__ == '__main__':
    app.run(debug=True)
