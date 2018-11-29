"""Made by Eriz Ghozi Al Hakim.
Start: 9 October 2018. End: 21 October 2018.

Fungsi-fungsi pendukung yang digunakan untuk proses penyerangan pada
sandi Vigenere. Digunakan pada tahap 1: Menentukan panjang kunci.
"""

from math import gcd
from itertools import combinations


def find_trigrams(text):
    """Menemukan seluruh trigram dari teks dalam bentuk list.

    :param text: masukan yang akan dicari trigram (str).
    :return: daftar seluruh trigram unik (list).
    """
    trigrams = [text[i: i+3] for i in range(len(text) - 2)]
    trigrams = list(set(trigrams))
    return trigrams


def count_occurence_list(substring_list, string):
    """Menemukan seluruh lokasi kemunculan dari seluruh trigram pada
    daftar trigram.

    :param substring_list: Daftar seluruh trigram yang akan dicari
    kemunculannya (list).
    :param string: Teks yang akan dicari lokasi kemunculan trigramnya (str).
    :return: Daftar seluruh trigram beserta lokasi kemunculannya (dict).
    """
    count_result = {x: count_occur(x, string) for x in substring_list}
    return count_result


def count_occur(substring, string):
    """Menemukan seluruh kemunculan dari suatu substring pada sebuah string.

    :param substring: substring yang akan dicari kemunculannya (str).
    :param string: string rujukan (str).
    :return: daftar seluruh lokasi kemunculan substring (list).
    """
    last_found = -1
    occurence = []
    while True:
        last_found = string.find(substring,   last_found + 1)
        if last_found == -1:
            break
        else:
            occurence.append(last_found)
    return occurence


def find_elements_distance(num_list):
    """Menemukan jarak dari elemen-elemen pada suatu list

    :param num_list: List yang akan dicari selisih-selisihnya
    (list of int)

    :return: List berisi jarak kemunculan dari elemen-elemen
    berdekatan (list of int).
    """
    num_list.sort()
    occur_distance = []
    for i in range(len(num_list) - 1):
        occur_distance.append(abs(num_list[i+1] - num_list[i]))
    return occur_distance


def find_gcd_list(num_list):
    """Menemukan FPB secara tunggal dari suatu list angka.

    :param num_list: List yang akan dicari FPB-nya (list of int)
    :return: FPB dari list tersebut (int).
    """
    if len(num_list) == 1:
        return num_list[0]
    else:
        g = gcd(num_list[0], num_list[1])
        for j in range(len(num_list) - 2):
            g = gcd(g, num_list[j])
        return g


def find_key_length(occur_list):
    """Membuat daftar kunci-kunci yang mungkin dari suatu kata sandi
    beserta frekuensi kemungkinannya.

    :param occur_list: masukan berupa daftar trigram yang telah ditemukan
    beserta lokasinya. (Dict [str, list of int]).

    :return: prediksi panjang kunci
    (Dict [panjang kunci, frekuensi kemungkinan])
    """
    multi_occur = {}
    for i in occur_list.keys():
        if len(occur_list[i]) > 1:
            multi_occur[i] = find_elements_distance(occur_list[i])
    print(multi_occur)

    gcd_num = []
    for i in multi_occur.keys():
        gcd_num.append(find_gcd_list(multi_occur[i]))

    key_length = {}
    for i, j in combinations(gcd_num, 2):
        g = gcd(i, j)
        if g not in key_length:
            key_length[g] = 1
        else:
            key_length[g] += 1
    return key_length


def choose_max_value(dictionary):
    """Menentukan panjang kunci secara otomatis dari kamus
    berisi kemungkinan panjang kunci.

    :param dictionary: Kamus berisi seluruh kemungkinan kunci
    beserta frekuensi kemunculannya (Dict [int, int])

    :return: Panjang kunci yang paling mungkin (int)
    """
    max_val = max(dictionary.values())
    max_key = list(dictionary.keys())[list(dictionary.values()).index(max_val)]
    return int(max_key)
