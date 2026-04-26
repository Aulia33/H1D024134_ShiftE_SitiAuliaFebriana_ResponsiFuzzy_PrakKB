from flask import Flask, render_template, request
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

app = Flask(__name__)

# =========================
# FUZZY SYSTEM 1: INTENSITAS OLAHRAGA
# =========================

aktivitas = ctrl.Antecedent(np.arange(0, 11, 1), 'aktivitas')
waktu = ctrl.Antecedent(np.arange(0, 121, 1), 'waktu')
kelelahan = ctrl.Antecedent(np.arange(0, 11, 1), 'kelelahan')
intensitas = ctrl.Consequent(np.arange(0, 101, 1), 'intensitas')

aktivitas['rendah'] = fuzz.trimf(aktivitas.universe, [0, 0, 5])
aktivitas['sedang'] = fuzz.trimf(aktivitas.universe, [3, 5, 7])
aktivitas['tinggi'] = fuzz.trimf(aktivitas.universe, [5, 10, 10])

waktu['sedikit'] = fuzz.trimf(waktu.universe, [0, 0, 40])
waktu['cukup'] = fuzz.trimf(waktu.universe, [30, 60, 90])
waktu['banyak'] = fuzz.trimf(waktu.universe, [80, 120, 120])

# Catatan:
# 0 = tidak lelah, 10 = sangat lelah
kelelahan['rendah'] = fuzz.trimf(kelelahan.universe, [0, 0, 5])
kelelahan['sedang'] = fuzz.trimf(kelelahan.universe, [3, 5, 7])
kelelahan['tinggi'] = fuzz.trimf(kelelahan.universe, [5, 10, 10])

intensitas['ringan'] = fuzz.trimf(intensitas.universe, [0, 0, 50])
intensitas['sedang'] = fuzz.trimf(intensitas.universe, [30, 50, 70])
intensitas['berat'] = fuzz.trimf(intensitas.universe, [60, 100, 100])

# Rules intensitas dibuat lebih lengkap agar tidak terjadi KeyError
rule1 = ctrl.Rule(kelelahan['tinggi'], intensitas['ringan'])
rule2 = ctrl.Rule(waktu['sedikit'] & kelelahan['sedang'], intensitas['ringan'])
rule3 = ctrl.Rule(aktivitas['rendah'] & waktu['sedikit'], intensitas['ringan'])
rule4 = ctrl.Rule(aktivitas['rendah'] & kelelahan['tinggi'], intensitas['ringan'])

rule5 = ctrl.Rule(aktivitas['rendah'] & waktu['cukup'] & kelelahan['rendah'], intensitas['sedang'])
rule6 = ctrl.Rule(aktivitas['sedang'] & waktu['cukup'], intensitas['sedang'])
rule7 = ctrl.Rule(aktivitas['sedang'] & kelelahan['sedang'], intensitas['sedang'])
rule8 = ctrl.Rule(waktu['cukup'] & kelelahan['rendah'], intensitas['sedang'])

rule9 = ctrl.Rule(aktivitas['tinggi'] & kelelahan['rendah'], intensitas['berat'])
rule10 = ctrl.Rule(waktu['banyak'] & kelelahan['rendah'], intensitas['berat'])
rule11 = ctrl.Rule(aktivitas['tinggi'] & waktu['banyak'], intensitas['berat'])
rule12 = ctrl.Rule(aktivitas['sedang'] & waktu['banyak'] & kelelahan['rendah'], intensitas['berat'])

int_ctrl = ctrl.ControlSystem([
    rule1, rule2, rule3, rule4,
    rule5, rule6, rule7, rule8,
    rule9, rule10, rule11, rule12
])


# =========================
# FUZZY SYSTEM 2: KEBUTUHAN KALORI
# =========================

bmi = ctrl.Antecedent(np.arange(10, 41, 1), 'bmi')
aktivitas_kalori = ctrl.Antecedent(np.arange(0, 11, 1), 'aktivitas_kalori')
kalori = ctrl.Consequent(np.arange(1200, 3501, 1), 'kalori')

bmi['kurus'] = fuzz.trimf(bmi.universe, [10, 10, 20])
bmi['normal'] = fuzz.trimf(bmi.universe, [18, 23, 28])
bmi['berlebih'] = fuzz.trimf(bmi.universe, [25, 40, 40])

aktivitas_kalori['rendah'] = fuzz.trimf(aktivitas_kalori.universe, [0, 0, 5])
aktivitas_kalori['sedang'] = fuzz.trimf(aktivitas_kalori.universe, [3, 5, 7])
aktivitas_kalori['tinggi'] = fuzz.trimf(aktivitas_kalori.universe, [5, 10, 10])

kalori['rendah'] = fuzz.trimf(kalori.universe, [1200, 1500, 2000])
kalori['normal'] = fuzz.trimf(kalori.universe, [1800, 2200, 2700])
kalori['tinggi'] = fuzz.trimf(kalori.universe, [2500, 3100, 3500])

# Rules kalori
rulek1 = ctrl.Rule(bmi['berlebih'] & aktivitas_kalori['rendah'], kalori['rendah'])
rulek2 = ctrl.Rule(bmi['berlebih'] & aktivitas_kalori['sedang'], kalori['rendah'])
rulek3 = ctrl.Rule(bmi['berlebih'] & aktivitas_kalori['tinggi'], kalori['normal'])

rulek4 = ctrl.Rule(bmi['normal'] & aktivitas_kalori['rendah'], kalori['normal'])
rulek5 = ctrl.Rule(bmi['normal'] & aktivitas_kalori['sedang'], kalori['normal'])
rulek6 = ctrl.Rule(bmi['normal'] & aktivitas_kalori['tinggi'], kalori['tinggi'])

rulek7 = ctrl.Rule(bmi['kurus'] & aktivitas_kalori['rendah'], kalori['normal'])
rulek8 = ctrl.Rule(bmi['kurus'] & aktivitas_kalori['sedang'], kalori['tinggi'])
rulek9 = ctrl.Rule(bmi['kurus'] & aktivitas_kalori['tinggi'], kalori['tinggi'])

kal_ctrl = ctrl.ControlSystem([
    rulek1, rulek2, rulek3,
    rulek4, rulek5, rulek6,
    rulek7, rulek8, rulek9
])


# =========================
# FUNGSI INTERPRETASI HASIL
# =========================

def kategori_intensitas(nilai):
    if nilai < 40:
        return "Ringan"
    elif nilai < 70:
        return "Sedang"
    return "Berat"


def kategori_kalori(nilai):
    if nilai < 1900:
        return "Rendah"
    elif nilai < 2700:
        return "Normal"
    return "Tinggi"


def rekomendasi_olahraga(kategori):
    if kategori == "Ringan":
        return "Jalan santai, stretching, yoga ringan, atau workout ringan 20–30 menit."
    elif kategori == "Sedang":
        return "Jogging ringan, bersepeda, bodyweight workout, atau olahraga 30–45 menit."
    return "Latihan intensitas tinggi seperti HIIT, strength training, atau olahraga 45–60 menit."


def penjelasan_hasil(aktivitas_input, waktu_input, kelelahan_input, bmi_input, kat_intensitas, kat_kalori):
    return (
        f"Berdasarkan aktivitas harian {aktivitas_input}/10, waktu luang {waktu_input} menit, "
        f"tingkat kelelahan {kelelahan_input}/10, dan BMI {bmi_input}, sistem merekomendasikan "
        f"intensitas olahraga {kat_intensitas.lower()} dengan kebutuhan kalori kategori "
        f"{kat_kalori.lower()}."
    )


# =========================
# ROUTE
# =========================

@app.route('/')
def home():
    return render_template(
        'index.html',
        page='home',
        intensitas=None,
        kalori=None
    )


@app.route('/tentang')
def tentang():
    return render_template(
        'index.html',
        page='tentang',
        intensitas=None,
        kalori=None
    )


@app.route('/hitung', methods=['GET', 'POST'])
def hitung():
    if request.method == 'POST':
        try:
            aktivitas_input = float(request.form['aktivitas'])
            waktu_input = float(request.form['waktu'])
            kelelahan_input = float(request.form['kelelahan'])
            bmi_input = float(request.form['bmi'])

            if not (0 <= aktivitas_input <= 10):
                raise ValueError("Aktivitas harus berada pada rentang 0 sampai 10.")

            if not (0 <= waktu_input <= 120):
                raise ValueError("Waktu luang harus berada pada rentang 0 sampai 120 menit.")

            if not (0 <= kelelahan_input <= 10):
                raise ValueError("Kelelahan harus berada pada rentang 0 sampai 10.")

            if not (10 <= bmi_input <= 40):
                raise ValueError("BMI harus berada pada rentang 10 sampai 40.")

            # Simulasi dibuat baru setiap submit agar hasil tidak bentrok
            int_sim = ctrl.ControlSystemSimulation(int_ctrl)
            int_sim.input['aktivitas'] = aktivitas_input
            int_sim.input['waktu'] = waktu_input
            int_sim.input['kelelahan'] = kelelahan_input
            int_sim.compute()
            hasil_intensitas = int_sim.output['intensitas']

            kal_sim = ctrl.ControlSystemSimulation(kal_ctrl)
            kal_sim.input['bmi'] = bmi_input
            kal_sim.input['aktivitas_kalori'] = aktivitas_input
            kal_sim.compute()
            hasil_kalori = kal_sim.output['kalori']

            kat_intensitas = kategori_intensitas(hasil_intensitas)
            kat_kalori = kategori_kalori(hasil_kalori)

            return render_template(
                'index.html',
                page='hitung',
                intensitas=round(hasil_intensitas, 2),
                kalori=round(hasil_kalori, 2),
                kategori_intensitas=kat_intensitas,
                kategori_kalori=kat_kalori,
                rekomendasi=rekomendasi_olahraga(kat_intensitas),
                penjelasan=penjelasan_hasil(
                    aktivitas_input,
                    waktu_input,
                    kelelahan_input,
                    bmi_input,
                    kat_intensitas,
                    kat_kalori
                ),
                error=None
            )

        except Exception as e:
            return render_template(
                'index.html',
                page='hitung',
                intensitas=None,
                kalori=None,
                error=str(e)
            )

    return render_template(
        'index.html',
        page='hitung',
        intensitas=None,
        kalori=None,
        error=None
    )


if __name__ == '__main__':
    app.run(debug=True, port=5001)