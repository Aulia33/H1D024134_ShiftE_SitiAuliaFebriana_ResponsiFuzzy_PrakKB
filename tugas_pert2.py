import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

suhu = ctrl.Antecedent(np.arange(0, 41, 1), 'suhu')
kelembapan = ctrl.Antecedent(np.arange(0, 101, 1), 'kelembapan')
kipas = ctrl.Consequent(np.arange(0, 101, 1), 'kipas')

suhu['dingin'] = fuzz.trimf(suhu.universe, [0, 0, 20])
suhu['sedang'] = fuzz.trimf(suhu.universe, [15, 25, 35])
suhu['panas'] = fuzz.trimf(suhu.universe, [30, 40, 40])

kelembapan['kering'] = fuzz.trimf(kelembapan.universe, [0, 0, 50])
kelembapan['normal'] = fuzz.trimf(kelembapan.universe, [30, 50, 70])
kelembapan['lembap'] = fuzz.trimf(kelembapan.universe, [60, 100, 100])

kipas['lambat'] = fuzz.trimf(kipas.universe, [0, 0, 50])
kipas['sedang'] = fuzz.trimf(kipas.universe, [30, 50, 70])
kipas['cepat'] = fuzz.trimf(kipas.universe, [60, 100, 100])

rule1 = ctrl.Rule(suhu['dingin'] & kelembapan['kering'], kipas['lambat'])
rule2 = ctrl.Rule(suhu['sedang'] & kelembapan['normal'], kipas['sedang'])
rule3 = ctrl.Rule(suhu['panas'] & kelembapan['lembap'], kipas['cepat'])

sistem = ctrl.ControlSystem([rule1, rule2, rule3])
simulasi = ctrl.ControlSystemSimulation(sistem)

s = float(input("Masukkan suhu: "))
k = float(input("Masukkan kelembapan: "))

simulasi.input['suhu'] = s 
simulasi.input['kelembapan'] = k
simulasi.compute()

print("Kecepatan kipas:", simulasi.output['kipas'])

suhu.view()
kelembapan.view()
kipas.view(sim=simulasi)
input("Tekan ENTER untuk keluar...")