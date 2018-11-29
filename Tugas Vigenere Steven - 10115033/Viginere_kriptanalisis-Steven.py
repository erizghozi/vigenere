# -*- coding: utf-8 -*-

"""
Created on Sat Oct 20 19:12:03 2018

@author: Steven-10115033
"""
#Mengimpor "itemgetter" untuk melakukan 'sorting' dengan aturan tertentu.
from operator import itemgetter

#Mendefinisikan objek himpunan alfabet yang dikaji (dalam kasus ini berupa 
#karakter alfabet dalam huruf kapital).
uppercase=[chr(i) for i in range(ord("A"),ord("A")+26)]

#Pendefinisian sub-program "vigenere_decrypt" untuk melakukan kriptanalisis
#terhadap teks hasil enkripsi menggunakan sandi Vigenere.
def vigenere_decrypt(target_freqs, input):
    #Banyaknya himpuanan karakter (alfabet kapital).
    nchars = len(uppercase) 
    #Urutan karakter pada python untuk obyek karakter "A". 
    ordA = ord('A') 
    #Deklarasi variabel yang berisikan nilai peluang kemunculan huruf dalam teks
    #berbahasa Jawa yang diurutkan dari paling kecil.
    sorted_targets = sorted(target_freqs) 
    
    #Pendefinisian sub-sub-program "frequency" untuk menghitung frekuensi 
    #kemunculan setiap huruf pada teks input.  
    def frequency(sentence):
        result = [[c, 0.0] for c in uppercase]
        for c in sentence:
            result[c - ordA][1] += 1
        return result
    
    #Pendefinisian sub-sub-program "correlation" untuk menghitung indeks korelasi
    #pada suatu teks dengan membandingkan nya terhadap tabel peluang kemunculan
    #huruf dalam bahasa Jawa.
    def correlation(input):
        result = 0.0
        freq = frequency(input)
        freq.sort(key=itemgetter(1))
 
        for i, f in enumerate(freq):
            result += f[1] * sorted_targets[i]
        return result
    
    #Menghilangkan spasi dan tandabaca serta mengonversi huruf pada teks input  
    #menjadi indeks angka.
    cleaned = [ord(c) for c in input.upper() if c.isupper()]
    
    #Inisiasi variabel pembanding.
    best_len = 0
    best_corr = -999.0
 
    # Asumsi:   -kunci memiliki panjang 2 sampai 20 karakter 
    #           -teks input memiliki lebih dari 60 huruf  
    
    #Dilakukan pencarian panjang kunci dengan membandingkan nilai indeks korelasi
    for i in range(2, len(cleaned) // 20):
        parts = [[] for _ in range(i)]
        for j, c in enumerate(cleaned):
            parts[j % i].append(c)

        corr = sum(correlation(p) for p in parts)
 
        if corr > best_corr:
            best_len = i
            best_corr = corr
 
    if best_len == 0:
        return ("Text is too short to analyze", "")
 
    #Setelah didapatkan panjang kunci ("best_len"). Misalkan kuncinya: K=k1k2..kn 
    # akan dicari ki dengan cara mencari nilai korelasi terbesar anatara seluruh
    #huruf ke-i(mod n) dengan distribusi peluang kemunculan huruf pada teks ber-
    #-bahasa Jawa untuk suatu tebakan ki dari "A" sampai "Z".
    parts = [[] for _ in range(best_len)]
    for i, c in enumerate(cleaned):
        parts[i % best_len].append(c)
 
    freqs = [frequency(p) for p in parts]
 
    key = ""
    for fr in freqs:
        fr.sort(key=itemgetter(1), reverse=True)
 
        m = 0
        max_corr = 0.0
        for j in range(nchars):
            corr = 0.0
            c = ordA + j
            for frc in fr:
                d = (ord(frc[0]) - c + nchars) % nchars
                corr += frc[1] * target_freqs[d]
 
            if corr > max_corr:
                m = j
                max_corr = corr
                
        #Menyusun kunci dengan menggabungkan hasil tebakan setiap iterasi.        
        key += chr(m + ordA)
    
    #Menyusun tebakan plain text berdasarkan tebakan kunci.
    text=""
    for i, c in enumerate(cleaned):
        text += chr(((c-ord(key[i % best_len]) + nchars-2*ord("A")) % nchars)+ord("a"))
    
    #Output berupa tupel/pasangan kunci dan plain text hasil tebakan.
    return (key,text)
 
#Pendefinisian program utama 
def main():
    #input ciphertext dari hasil enkripsi teks berbahasa jawa dengan diketahui
    #menggunakan sandi Vegenere.
    cipher_text = """FSQYLLRSNLDROEXGPQKLMNIJLDZBAVTGQNRDRTISLRLIYMVVUETNQSLPZAIYZU
    PASTISECLRVIANEBICTYBICTYLHLARZAYFSWTPGEOEYWRXTPGXAEWTJMLLPRRAOTUWSTILVWLCR
    SIETSIDSXCINRDLVGHTCCYLNXQRPLZSSLUVVDTGKMNTILV"""
 
    #Nilai peluang kemunculan huruf/abjad dalam teks berbahasa jawa. Berdasarkan
    #15319 huruf dari berbagai sumber.
    java_frequences = [
        0.16528, 0.02304, 0.00855, 0.03009, 0.08323, 0.00287, 0.06136,
        0.02095, 0.07918, 0.00770, 0.06097, 0.02793, 0.02970, 0.12618,
        0.03055, 0.02454, 0.00007, 0.04047, 0.05006, 0.04223, 0.05274,
        0.00065, 0.02108, 0.00013, 0.01024, 0.00013]
    
    #Menjalankan sub-program "vigenere_decrypt" yang telah didefinisikan pada
    #baris ke-15 sampai baris ke-105 pada program ini. Output berupa Kunci yang
    #'diprediksi' dan plain_text yang 'diprediksi'.
    (key, plain_text) = vigenere_decrypt(java_frequences, cipher_text)
    print ("Key:", key)
    print ("\nText:", plain_text)
 
main()
