from __future__ import division
# -*- coding: utf-8 -*-
"""
Author: Anggia
Created 19 Oct 2018
"""

import numpy as np
from collections import Counter,OrderedDict
from fractions import gcd



alphabets = "abcdefghijklmnopqrstuvwxyz" # huruf, asumsi dua jenis e pada bahasa sunda adalah sama
#peluang kemunculan huruf di bahasa sunda
prob=[0.200533885,
0.02294436,
0.007590615,
0.031442943,
0.072800901,
0.000444904,
0.053261422,
0.030716569,
0.060316336,
0.012212174,
0.051527203,
0.030780126,
0.030371541,
0.115874918,
0.023552698,
0.023352945,
0,
0.040758698,
0.03383998,
0.047541222,
0.08341505,
0.000326869,
0.011730951,
2.7239E-05,
0.014581971,
5.44781E-05]

#menghitung indeks coincidence
i_c=0
for i in range(0,len(prob)):
    i_c=i_c+prob[i]**2

#fungsi yang mengubah huruf menjadi index dari 0 sampai 25    
def indexing(c):
    c_index = [] # calon tempat menyimpan indeks dari setiap huruf
    for char in c:
       c_index.append(ord(char)-97)
    return c_index

#fungsi untuk menghitung index of coincidence
def index_of_coincidence(c_index): 
    print "Index of Coincidence Bahasa Sunda : ", i_c
    ioc=[]
    #threshold=0.01
    i=1
    ioc.append(0)
    while 1:
        #proses pemisahan string menjadi i buah list
        temp_list=[]
        for a in range(0,i):
            temp=[]
            for j in range(0,len(c_index)):
                if j%i==a:
                    temp.append(c_index[j])
            temp_list.append(temp)
        
        count=Counter(temp_list[0]) #menghitung frekuensi huruf dari list pertama saja (perwakilan)
        n=len(temp_list[0])
        #perhitungan index of coincidence
        for k in range(0,26):
            ioc[i-1]= ioc[i-1]+ count[k]*(count[k]-1)
        ioc[i-1]=ioc[i-1]/(n*(n-1))
        print "m=",i,": ", ioc[i-1]
        #jika nilai index of coincidence lebih dari index of coincidence bahasa sunda dikurang threshold
        if ioc[i-1]>i_c:
            print "Panjang kunci adalah ", i
            break
        else:
            i+=1
            ioc.append(0)
    return i
            
def kasiski(c_index):
    n=10
    #n=input("Masukkan jumlah trigram dengan kemunculan tersering yang ingin diambil: ") #diambil n buah trigram dengan kemunculan tersering
    c_index=tuple(c_index) #c_index diubah jadi tuple untuk menghindari list of list
    trigram=[c_index[i:i+3] for i in range(len(c_index)-2)] #mencari semua trigram dari ciphertext
    #mencari n trigram yang muncul paling sering
    temp=Counter(trigram).most_common(n)
    #jika tidak ada trigram yang muncul 2 kali tes kasiski tidak bisa digunakan.
    if temp==[]:
        print "Tes Kasiski tidak bisa digunakan."
        return 0
    else:
        #mencari indeks kemunculan trigram
        indeks=[]
        indeks_n=[]
        for x in range(n):
            indeks=[i for i, j in enumerate(trigram) if j == temp[x][0]]
            indeks_n.append(indeks)
    
        #menyelisihkan indeks kemunculan trigram kemudian mencari gcd
        diff=[]     
        gcdlist=[]
        for x in range(n):
            temps= map(lambda y: y-indeks_n[x][0], indeks_n[x])
            diff.append(temps[1:])
        for x in range(n):
            temps=reduce(gcd,diff[x])
            gcdlist.append(temps)
            gcdlist=list(OrderedDict.fromkeys(gcdlist)) #menghapus nilai berganda pada list
            gcdlist=filter(lambda a: a != 1, gcdlist) #menghapus nilai 1 dari list gcd
        print "Selisih index kemunculan", diff
        print "List gcd index kemunculan", gcdlist
        #mencari nilai KPK
        lcm=gcdlist[0]
        for h in gcdlist[1:]:
            lcm=lcm*h/(reduce(gcd,[lcm,h]))
        #print lcm
        i=int(lcm) #mengambil nilai KPK dari list sebagai jumlah kunci
        if i==1:
            print "Tes Kasiski Gagal."
            return 0
        else:
            print "Panjang kunci adalah ", i
            return i
            
    
def decrypt_nokey(c_index,i):
    # memisahkan string menjadi i buah list
    char_list=[]
    for a in range(i):
        temp=[]
        for j in range(len(c_index)):
            if j%i==a:
                temp.append(c_index[j])
        char_list.append(temp)
    
    #menghitung frekuensi huruf setiap list    
    count=[]
    count_temp=[]    
    for k in range(i):
        count_temp=Counter(char_list[k])
        count.append(count_temp)
    
    #menghitung nilai M_g dan mencari index dimana M_g bernilai maksimum, index tersebut disimpan sebagai kunci
    k_index=[]
    M = [[0 for g in range(26)] for a in range(len(count))] 
    for a in range(len(count)):
        for g in range(26):
            for l in range(26):
                M[a][g]=M[a][g]+prob[l]*count[a][(l+g)%26]
            M[a][g]=M[a][g]/len(char_list[a])
        k_index.append(np.argmax(M[a])) #mencari index dari nilai maksimum M_g
    
    #menampilkan karakter alfabet kunci
    k=''
    for x in k_index:
        k+=chr(ord('a')+x)
    print "Kunci yang digunakan adalah:" , k
    #dekripsi dengan kunci yang didapat
    n = 0
    p=""
    for char in c_index:
      if n == len(k_index): #pengulangan kunci
          n = 0
      p_index = char - k_index[n] #proses pergeseran
      #print(p_index)
      if p_index < 0:
          p_index = p_index+26      # index tidak boleh kurang dari 0
      p += alphabets[p_index].lower()  #plaintext dijadikan lowercase
      n +=1
    return p