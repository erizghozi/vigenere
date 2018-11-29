# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 22:15:01 2018

@author: Steven-10115033
"""

#Mendefinisikan objek himpunan alfabet yang dikaji (dalam kasus ini berupa 
#karakter alfabet dalam huruf kecil).
lowercase=[chr(i) for i in range(ord("a"),ord("a")+26)]

#Pendefinisian sub-program "vigenere_encrypt" untuk melakukan enkripsi terhadap
#teks asal menggunakan sandi Vigenere.
def vigenere_encrypt(ekey, sentence):
     #Banyaknya himpuanan karakter (huruf kecil).
    nchars=len(lowercase)
    
    #Menghilangkan spasi dan tandabaca serta mengonversi huruf pada teks input  
    #menjadi indeks angka.
    cleaned=[ord(c) for c in sentence.lower() if c.islower()]
    #Menghilangkan spasi dan tandabaca serta mengonversi huruf pada kunci input 
    #menjadi indeks angka.
    ekeynum=[ord(c) for c in ekey.lower() if c.islower()]
    
    #Meyusun Ciphertext secara iteratif.
    cipher=""
    for i,c in enumerate(cleaned):
        cipher+=chr(((c+ekeynum[i%len(ekeynum)]-2*ord("a"))%nchars)+ord("A"))
    return cipher

#Pendefinisian program utama
def main():
    
    #Input teks berbahasa Jawa.
    plain_text = """
       mbiyasaknakagemnyikatwajakitakapingkalihsadintenutawisawisingdhaharkersa
       nipuntirahtirahdhaharanmbotenngendaptengselaselawajadadosipunwajakitabad
       helangkungwaluyaugiresiksabendintenipun"""
    
    #Input kata kunci.
    key = """TRIAL"""
    
    #Menjalankan sub-program "vigenere_encrypt" untuk mengenkripsi plaintext men-
    #-jadi ciphertext dan menampilkan hasil enkripsi nya.
    cipher_text = vigenere_encrypt(key, plain_text)
    print ("Ciphertext:", cipher_text)
 
main()
