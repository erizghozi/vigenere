#MULAI
#Algoritma kriptanalisis Vigenere
#oleh Mochammad Zulfikar Aditya NIM 10115104
#Program ini menggabungkan enkripsi dengan kunci, namun proses dekripsi akan
#menggunakan kriptoanalisis (tidak mengetahui kunci awalan)

from statistics import mean
from operator import itemgetter

minang_frequences = [
    0.227926795, 0.038317655, 0.00574338, 0.039846636, 0.031371271, 0.000838223,
    0.03605911, 0.02743628, 0.083876626, 0.013613362, 0.062082829, 0.031037534,
    0.037735556, 0.097164012, 0.045799572, 0.026939555, 0.00003104, 0.035919406,
    0.04074695, 0.040009624, 0.06126789, 0.001203005, 0.004664556, 0.0000155226,
    0.010244947, 0.000108659] #frekuensi bahasa Minang

sorted_targets = sorted(minang_frequences)

#fungsi untuk mengkonversi text berhuruf menjadi angka indeks
def konversi_angka(apapun):
    hasil = []
    for x in apapun:
        hasil.append(int(ABJAD.find(x)))
    return hasil

#fungsi untuk menggeser teks sejauh berapa angka
def shifting(initeksnya,iniangkanya):
    save = konversi_angka(initeksnya)
    result = []
    for k in save:
        n = k + iniangkanya
        n %= 26
        result.append(ABJAD[n])
    return result

#fungsi untuk mengenkripsi pesan dengan suatu kunci
def enkripsi_pesan(pesan,kunci):
    (angkapesan , angkakunci) = (konversi_angka(pesan),konversi_angka(kunci))
    hasil_enkripsi = []
    for y in range(len(angkapesan)):
        result = (angkapesan[y] + angkakunci[y%len(angkakunci)])%26
        hasil_enkripsi.append(ABJAD[result])
    return hasil_enkripsi

#fungsi untuk menghitung jumlah huruf pada list
def frequency_analysis(words):
    result = [[c, 0.0] for c in ABJAD]
    for c in words:
        result[ABJAD.find(c)][1] += 1
    return result

#fungsi untuk menghitung nilai korelasi
def correlation(input):
    result = 0.0
    freq = frequency_analysis(input)
    freq.sort(key=itemgetter(1))

    for i,f in enumerate(freq):
        result += f[1] * sorted_targets[i]
    return result

#fungsi untuk menghitung weighted mean frekuensi kata dari kalimat
def weighted_mean(text):
    N = frequency_analysis(text)
    jumlahan = 0
    for i in range(26):
        x = minang_frequences[i] * N[i][1]
        jumlahan =+ x
    return jumlahan

#asumsi awal 
best_len = 0
best_corr = -100.0

#acuan abjad terhadap indeks
ABJAD = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

#membaca input dari suatu teks berbahasa minang
file = open("input_asli.txt", "r")
text_pesan = file.read()
file.close()

#manipulasi teks sehingga tersisa Abjad saja tanpa simbol, spasi, dan line break
text_pesan = text_pesan.replace('\n','').replace('\r','')
save_pesan = [c.upper() for c in text_pesan if c.isalpha()]

text_kunci = input ('Masukkan kata kunci : ')
save_kunci = [c.upper() for c in text_kunci if c.isalpha()]

hasil_enkrip = enkripsi_pesan(save_pesan,save_kunci)
print ('Hasil enkripsi adalah : ', ''.join(hasil_enkrip))

print ('Sekarang akan dilakukan proses dekripsi dengan menebak kunci!')

#akan digunakan IC test
for i in range(2, len(hasil_enkrip) // 10):
    pieces = [[] for _ in range(i)]
    for j, c in enumerate(hasil_enkrip):
        pieces[j % i].append(c)

    corr = -0.5 * i + sum(correlation(p) for p in pieces)
#Jika korelasi yang baru lebih besar dari korelasi sebelumnya, kunci yang digu
#nakan ialah kunci terakhir
    if corr > best_corr:
        best_len = i
        best_corr = corr

#menentukan panjang kunci
print ('Kunci memiliki panjang : ', best_len)

#partisi ciphertext menjadi beberapa sublist sejumlah panjang kunci
ygram = [[] for i in range(best_len)]

for j,k in enumerate(hasil_enkrip):
    ygram[j%best_len].append(k)

#akan dilakukan weighted mean untuk menentukan pergeseran kunci yang cocok
save_wmean = [[] for i in range(best_len)]

#menyimpan semua hasil dari weighted mean
for i in range(best_len):
    for j in range(26):
        save_wmean[i].append(weighted_mean(shifting(ygram[i],j)))

#menyimpan kode angka dari kunci pergeseran yang sesuai
angka_kunci = []

for i in range(best_len):
    angka_kunci.append(25 - save_wmean[i].index(max(save_wmean[i])))

#konversi angka kunci menjadi abjad kembali
text_kunci = []

for j in range(len(angka_kunci)):
    text_kunci.append(ABJAD[angka_kunci[j]])

print ('Kunci yang dipakai ialah : ' , ''.join(text_kunci))

#dan akhirnya dekripsi ciphertext
dekripsi_pesan = []
iter = 0
for k in konversi_angka(hasil_enkrip):
    save_lagi = k - angka_kunci[iter]
    iter = (iter + 1)%best_len
    dekripsi_pesan.append(ABJAD[save_lagi])

print ('Dan hasil dekripsinya ialah : ' , ''.join(dekripsi_pesan))
#SELESAI
