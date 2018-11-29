from __future__ import division
# -*- coding: utf-8 -*-
"""
Author: Anggia
Created 19 Oct 2018
"""

import re
import vigenere_decrypt_nokey as nokey
import unidecode
import io

alphabets = "abcdefghijklmnopqrstuvwxyz" # huruf, asumsi dua jenis e pada bahasa sunda adalah sama
def encrypt(p, k):
    c = "" #calon tempat menyimpan ciphertext
    k_index = [] # calon tempat menyimpan indeks dari setiap huruf
    for char in k:
       # k_index.append(alphabets.find(x))
       k_index.append(ord(char)-97) #konversi huruf ke indeksnya bilangan [0,25]
    #enkripsi
    i = 0
    for char in p:
      if i == len(k_index): #pengulangan kunci
          i = 0
      p_index = ord(char)-97 + k_index[i] #proses pergeseran
      #print(p_index)
      if p_index > 25:
          p_index = p_index-26      # index tidak boleh lebih dari 25
      c += alphabets[p_index].lower()  #ciphertext dijadikan lowercase
      i +=1
    return c

def decrypt(c, k):
    p = "" #calon tempat menyimpan plaintext
    k_index = [] # calon tempat menyimpan indeks dari setiap huruf
    for char in k:
       # k_index.append(alphabets.find(x))
       k_index.append(ord(char)-97) #konversi huruf ke indeksnya bilangan [0,25]
    #dekripsi
    i = 0
    for char in c:
      if i == len(k_index): #pengulangan kunci
          i = 0
      p_index = ord(char) -97 - k_index[i] #proses pergeseran
      #print(p_index)
      if p_index < 0:
          p_index = p_index+26      # index tidak boleh kurang dari 0
      p += alphabets[p_index].lower()  #plaintext dijadikan lowercase
      i +=1
    return p

def text_strip(p):
    p=unidecode.unidecode(p) #menghilangkan huruf dengan aksen
    p = p.replace('\n', ' ').replace('\r', '') #menghapus linebreak
    p = p.replace(" ", "")  # menghapus spasi dari plaintext
    p= p.strip()
    p = re.sub('[^a-zA-Z\n\.]', '', p) #menghapus simbol dan angka dari plaintext
    p=p.replace('.','') #menghapus titik
    p=p.lower() #mengubah plaintext menjadi lowercase
    return p

try:
    print("Program Vigenere Cipher. \n\n"
          "Input plaintext terdiri dari huruf saja, jika terdapat simbol/angka/spasi akan dihapus \n"
          "Input kunci terdiri dari huruf tanpa spasi, jika terdapat simbol/angka/spasi akan dihapus \n"
          "Pastikan semua file .txt memiliki encoding UTF-8. \n"
          "Pilih 1 untuk enkripsi pesan, 2 untuk dekripsi pesan dengan kunci, 3 untuk dekripsi tanpa kunci dengan index of coincidence, 4 untuk dekripsi tanpa kunci dengan kasiski.")
    choice = raw_input("Pilihan : ")
    if choice == '1':
       p = io.open('plaintext.txt', 'r', encoding='utf-8').read() #input plaintext dari .txt
       p=text_strip(p)
       
       k = raw_input("Masukkan kunci: ")
       k=text_strip(k)
       
       c = encrypt(p, k) #enkripsi
       print "Cipher text: ", c
       #hasil dimasukkan ke txt
       file = open('ciphertext.txt', 'w')
       file.write(c) 
       file.close()
       

    elif choice == '2':
       c = io.open('ciphertext.txt', 'r', encoding='utf-8').read() #input ciphertext dari .txt
       c=text_strip(c)
       
       k = raw_input("Masukkan kunci: ")
       k=text_strip(k)
       
       p = decrypt(c, k) #dekripsi
       print "Plain text: ", p
       #hasil dimasukkan ke txt
       file = open('decrypted.txt', 'w')
       file.write(p) 
       file.close()
       
    elif choice =='3':
       c = io.open('ciphertext.txt', 'r', encoding='utf-8').read() #input ciphertext dari .txt
       c=text_strip(c)
       
       c_index=nokey.indexing(c)
       m=nokey.index_of_coincidence(c_index) #panjang kunci
       p=nokey.decrypt_nokey(c_index,m)
       print "Plain text: ", p
       #hasil dimasukkan ke txt
       file = open('decrypted_nokey_ioc.txt', 'w')
       file.write(p) 
       file.close()

    elif choice=='4':
       c = io.open('ciphertext.txt', 'r', encoding='utf-8').read() #input ciphertext dari .txt
       c=text_strip(c)
       
       c_index=nokey.indexing(c)
       m=nokey.kasiski(c_index) #panjang kunci
       if m==0:
           exit(0) #jika fungsi menghasilkan panjang kunci nol proses dekripsi dihentikan
       else:
           p=nokey.decrypt_nokey(c_index,m)
           print "Plain text: ", p
           #hasil dimasukkan ke txt
           file = open('decrypted_nokey_kasiski.txt', 'w')
           file.write(p) 
           file.close()
        
    else:
        print("Pilihan tidak tersedia.")
except Exception as e:
    print(e)
    exit("Teks tidak valid.")