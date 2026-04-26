# 🏃‍♂️ Sistem Fuzzy Rekomendasi Pola Olahraga & Kebutuhan Kalori Mahasiswa Sibuk

## 📌 Deskripsi

Sistem ini merupakan aplikasi berbasis web yang menggunakan **Logika Fuzzy (Fuzzy Logic)** untuk memberikan rekomendasi:

* Intensitas olahraga
* Kebutuhan kalori harian

Sistem dirancang khusus untuk **mahasiswa sibuk** yang memiliki keterbatasan waktu dan kondisi fisik yang bervariasi.

---

## 🎯 Tujuan

* Membantu mahasiswa menentukan pola olahraga yang realistis
* Memberikan estimasi kebutuhan kalori berdasarkan kondisi tubuh
* Menggunakan pendekatan adaptif (fuzzy), bukan perhitungan kaku

---

## ⚙️ Teknologi yang Digunakan

* Python
* Flask (Web Framework)
* NumPy
* Scikit-Fuzzy
* HTML + CSS

---

## 🧠 Konsep Sistem

### 1. Sistem Fuzzy Intensitas Olahraga

#### Input:

* Aktivitas Harian (0–10)
* Waktu Luang (0–120 menit)
* Tingkat Kelelahan (0–10)

#### Output:

* Intensitas Olahraga (0–100)

  * Ringan
  * Sedang
  * Berat

---

### 2. Sistem Fuzzy Kebutuhan Kalori

#### Input:

* BMI (10–40)
* Aktivitas Harian (0–10)

#### Output:

* Kebutuhan Kalori (1200–3500 kkal)

  * Rendah
  * Normal
  * Tinggi

---

## 🔄 Alur Sistem

1. User memasukkan data (aktivitas, waktu, kelelahan, BMI)
2. Sistem melakukan **fuzzifikasi**
3. Sistem menerapkan **rule base (inferensi)**
4. Dilakukan **defuzzifikasi**
5. Sistem menghasilkan:

   * Nilai intensitas olahraga
   * Nilai kebutuhan kalori
   * Kategori hasil
   * Rekomendasi olahraga

---

## 📊 Contoh Input & Output

### Input:

* Aktivitas: 5
* Waktu: 60 menit
* Kelelahan: 4
* BMI: 22

### Output:

* Intensitas: 55 → Sedang
* Kalori: 2300 → Normal
* Rekomendasi:

  > Jogging ringan, bersepeda, atau latihan 30–45 menit

---

## 🧩 Rule Fuzzy (Contoh)

### Intensitas:

* IF kelelahan tinggi THEN intensitas ringan
* IF aktivitas rendah AND waktu sedikit THEN intensitas ringan
* IF aktivitas sedang AND waktu cukup THEN intensitas sedang
* IF aktivitas tinggi AND waktu banyak THEN intensitas berat

### Kalori:

* IF BMI berlebih AND aktivitas rendah THEN kalori rendah
* IF BMI normal AND aktivitas sedang THEN kalori normal
* IF BMI kurus AND aktivitas tinggi THEN kalori tinggi

---

## 🌐 Struktur Project

```
project/
├── app.py
├── static/
│   └── foto1.png
└── templates/
    └── index.html
```

---

## 🚀 Cara Menjalankan

1. Install dependency:

```bash
pip install flask scikit-fuzzy numpy
```

2. Jalankan aplikasi:

```bash
python app.py
```

3. Buka di browser:

```
http://127.0.0.1:5001
```

---

## ⚠️ Catatan Penting

* Input harus sesuai rentang:

  * Aktivitas: 0–10
  * Waktu: 0–120
  * Kelelahan: 0–10
  * BMI: 10–40
* Jika input tidak valid, sistem akan menampilkan error

---

## 💡 Kelebihan Sistem

* Adaptif terhadap kondisi pengguna
* Lebih realistis dibanding metode konvensional
* Menggunakan pendekatan berbasis rule (expert-like)

---


## 👨‍💻 Pengembang

Nama: Siti Aulia Febriana

---

## 📌 Kesimpulan

Sistem ini menunjukkan bagaimana logika fuzzy dapat digunakan untuk membantu pengambilan keputusan dalam kondisi yang tidak pasti, khususnya dalam menentukan pola olahraga dan kebutuhan kalori bagi mahasiswa sibuk.
