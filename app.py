from flask import Flask, render_template, request

app = Flask(__name__)

# =========================
# DATA FAKTA
# =========================
fakta = {
    "F001": "Suka wisata alam",
    "F002": "Menyukai tempat sejuk atau pemandangan",
    "F003": "Anggaran kurang dari 25.000",
    "F004": "Jarak kurang dari 20 km",
    "F005": "Suka berfoto di tempat indah",
    "F006": "Menyukai sejarah dan bangunan tua",
    "F007": "Menyukai tempat religi",
    "F008": "Menyukai wisata kuliner",
    "F009": "Membawa keluarga atau anak kecil",
    "F010": "Menyukai suasana pantai",
    "F011": "Akses jalan mudah",
    "F012": "Tersedia fasilitas parkir",
    "F013": "Cocok untuk liburan singkat",
    "F014": "Tiket masuk terjangkau",
    "F015": "Ramah untuk semua usia",
    "F016": "Memiliki nilai edukasi",
    "F017": "Tersedia fasilitas umum",
    "F018": "Cocok untuk wisata keluarga",
    "F019": "Lingkungan aman",
    "F020": "Tidak memerlukan persiapan khusus",
    "F021": "Cocok untuk kunjungan rombongan",
    "F022": "Memiliki spot foto populer",
    "F023": "Tidak terlalu ramai",
    "F024": "Mudah dijangkau transportasi umum",
    "F025": "Waktu kunjungan fleksibel"
}

# =========================
# KESIMPULAN
# =========================
kesimpulan = {
    "K001": "Pantai Menganti",
    "K002": "Benteng Van Der Wijck",
    "K003": "Goa Jatijajar",
    "K004": "Bukit Pentulu Indah",
    "K005": "Kapal Mendoan Alun Alun Kebumen"
}

# =========================
# RULES
# =========================
rules = [
    {
        "if": ["F001", "F003", "F004", "F010", "F011", "F012", "F021"],
        "then": "K001"
    },
    {
        "if": ["F005", "F006", "F009", "F015", "F016", "F017", "F018", "F020"],
        "then": "K002"
    },
    {
        "if": ["F003", "F004", "F007", "F016", "F017", "F018", "F019"],
        "then": "K003"
    },
    {
        "if": ["F001", "F002", "F005", "F013", "F021", "F022", "F025"],
        "then": "K004"
    },
    {
        "if": ["F003", "F008", "F009", "F015", "F023", "F024", "F025"],
        "then": "K005"
    }
]

foto_wisata = {
    "Pantai Menganti": "/static/images/pantai_menganti.jpg",
    "Benteng Van Der Wijck": "/static/images/benteng_vdw.jpg",
    "Goa Jatijajar": "/static/images/goa_jatijajar.jpg",
    "Bukit Pentulu Indah": "/static/images/bukit_pentulu.jpg",
    "Kapal Mendoan Alun Alun Kebumen": "/static/images/kapal_mendoan.jpg"
}

deskripsi_wisata = {
    "Pantai Menganti": "Pantai dengan panorama tebing dan laut lepas yang indah, cocok untuk wisata alam dan menikmati suasana pantai yang menenangkan.",
    "Benteng Van Der Wijck": "Bangunan bersejarah peninggalan Belanda yang memiliki nilai edukasi tinggi dan cocok untuk wisata keluarga.",
    "Goa Jatijajar": "Wisata goa alami yang memiliki nilai religi dan edukasi, dilengkapi fasilitas umum yang memadai.",
    "Bukit Pentulu Indah": "Destinasi wisata alam dengan pemandangan perbukitan dan spot foto populer, cocok untuk liburan singkat.",
    "Kapal Mendoan Alun Alun Kebumen": "Wisata kuliner ikonik di pusat kota Kebumen yang ramah keluarga dan mudah dijangkau."
}


maps_wisata = {
    "Pantai Menganti": "https://www.google.com/maps?q=Pantai+Menganti+Kebumen",
    "Benteng Van Der Wijck": "https://www.google.com/maps?q=Benteng+Van+Der+Wijck+Kebumen",
    "Goa Jatijajar": "https://www.google.com/maps?q=Goa+Jatijajar+Kebumen",
    "Bukit Pentulu Indah": "https://www.google.com/maps?q=Bukit+Pentulu+Indah+Kebumen",
    "Kapal Mendoan Alun Alun Kebumen": "https://www.google.com/maps?q=Alun+Alun+Kebumen"
}


# =========================
# ROUTES
# =========================
@app.route("/")
def index():
    return render_template("index.html", fakta=fakta)

@app.route("/hasil", methods=["POST"])
def hasil():
    nama = request.form.get("nama")
    fakta_dipilih = set(request.form.getlist("fakta"))

    semua_hasil = []

    for rule in rules:
        rule_fakta = set(rule["if"])
        cocok = rule_fakta.intersection(fakta_dipilih)

        skor = (len(cocok) / len(rule_fakta)) * 100
        nama_wisata = kesimpulan[rule["then"]]

        semua_hasil.append({
        "wisata": nama_wisata,
        "skor": round(skor, 2),
        "foto": foto_wisata.get(nama_wisata),
        "deskripsi": deskripsi_wisata.get(nama_wisata),
        "maps": maps_wisata.get(nama_wisata)   # ✅ TAMBAHAN
    })

    # Urutkan dari skor tertinggi
    semua_hasil.sort(key=lambda x: x["skor"], reverse=True)

    # Ambil yang relevan
    hasil_rekomendasi = [h for h in semua_hasil if h["skor"] >= 30]

    # Jika tidak ada yang lolos → ambil 1 terdekat
    if not hasil_rekomendasi and semua_hasil:
        hasil_rekomendasi = [semua_hasil[0]]

    return render_template(
        "result.html",
        nama=nama,
        hasil=hasil_rekomendasi
    )


if __name__ == "__main__":
    app.run(debug=True)
