"""Made by Eriz Ghozi Al Hakim.
Start: 10 October 2018. End: 21 October 2018

Fungsi-fungsi pendukung yang digunakan pada proses penyerangan sandi
Vigenere. Digunakan pada tahap 2: Menentukan siklus kunci.
"""

from collections import Counter

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
PROBABILITY_BETAWI = [0.1789, 0.0248, 0.0042, 0.0301,
                      0.1007, 0.0004, 0.0649, 0.0057,
                      0.0626, 0.0145, 0.0626, 0.0324,
                      0.0488, 0.1225, 0.0233, 0.0317,
                      0.0004, 0.0202, 0.0404, 0.0473,
                      0.0568, 0.0004, 0.0092, 0.0004,
                      0.0164, 0.0004]  # IoC = 0.08382002
PROBABILITY_INDONESIA = [0.19807, 0.02973, 0.00670, 0.03719,
                         0.08175, 0.00253, 0.03964, 0.01967,
                         0.08076, 0.00851, 0.05349, 0.03499,
                         0.04853, 0.09559, 0.01596, 0.02769,
                         0.00004, 0.05005, 0.04108, 0.05118,
                         0.05568, 0.00079, 0.00412, 0.00004,
                         0.01604, 0.00015]  # IoC = 0.0835725599


def column_break(text, column):
    """Memisahkan kata-sandi ke dalam kolom-kolom untuk dihitung
    frekuensinya per kolom

    :param text: Teks yang akan dipisakan per kolom (str).
    :param column: Banyak kolom (int).
    :return: Hasil pemisahan (List[list]).
    """
    text_block = []
    for i in range(column):
        text_block.append([])

    for i in range(len(text)):
        text_block[i % column].append(text[i])

    return text_block


def count_frequency(array):
    """Menghitung frekuensi kemunculan elemen dari array 2D.

    :param array: Array yang akan dihitung frekuensinya (List[list]).
    :return: Hasil pencacahan elemen (List[Counter]).
    """
    freq_count = []
    for i in array:
        freq_count.append(Counter(i))
    return freq_count


def cycle_search(list_count):
    """Menentukan kemngkinan kunci secara statistik menggunakan
    Index of Coincidence.
    Perhatikan bahwa program memerlukan tambahan berupa referensi
    probabilitas tiap huruf pada suatu bahasa menggunakan variabel
    freq_ref (List[float]). Variabel ini dapat diganti dengan tabel
    probabilitas dalam bahasa-bahasa lain.
    Untuk ke depannya, gunakan percabangan untuk memilih bahasa
    yang akan dipakai tabelnya dalam perhitngan IoC.

    :param list_count: List berisi seluruh hasil pencacahan
    elemen-elemen dari blok teks (List[Counter]).

    :return: List berisi daftar dugaan pergeseran dari sandi
    (List[int]).
    """
    freq_ref = PROBABILITY_BETAWI
    ioc = 0
    for i in freq_ref:  # Meghitung Index of Coincidence
        ioc += i ** 2

    shift = []

    for counter_element in list_count:
        length = sum(list(counter_element.values()))
        # Length: total dari seluruh pencacahan
        ioc_diff = []
        for shift_num in range(len(LETTERS)):
            coincidence = 0
            for sym_index in range(len(LETTERS)):
                c_key = LETTERS[(sym_index + shift_num) % 26]
                x = freq_ref[sym_index] * counter_element[c_key] / length
                coincidence += x
            ioc_diff.append(abs(coincidence - ioc))
        shift_value = ioc_diff.index(min(ioc_diff))
        print(counter_element)
        print(ioc_diff)
        shift.append(shift_value)
    print("\nIoC = ", ioc)

    return shift


def num_to_key(num_list):
    """Mengubah list bilangan menjadi teks dalam urutan yang sesuai.

    :param num_list: List pergeseran kunci (List[int]).
    :return: Dugaan kunci (str).
    """
    key = []
    for i in num_list:
        key.append(LETTERS[i])
    return ''.join(key)
