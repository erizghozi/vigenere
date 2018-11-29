""" Made by Eriz Ghozi Al Hakim.
Start: 21 September 2018. End: 21 October 2018.

Ini adalah program utama untuk melakukan deciphering pada cipher
Vigenere dalam bahasa Betawi. Terdapat tiga pilihan mode pada
program ini: enkripsi, dekripsi dengan kunci, dan dekripsi
tanpa kunci, yang menjadi fitur utama program ini.

Pada mode ketiga, program menerima masukan dari file ciphertext.txt,
lalu melakukan Kasiski test pada file untuk mencari panjang kunci,
dan kemudian mencari posisi siklus kunci dan menemukan kunci aslinya.
"""
import kasiskitest as kas  # File pendukung untuk mencari trigram
import frequencyanalysis as frq  # File pendukung untuk mencari panjang kunci

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def main():
    """Program utama dari rangkaian program ini.
    Berfungsi untuk menentukan pilihan mode penyandian.
    """
    print("---Program enkripsi dan dekripsi sandi Vigenere---"
          "\nMode:"
          "\n1. Enkripsi dari plaintext.txt ke ciphertext.txt"
          "\n2. Dekripsi dari ciphertext.txt ke decrypted.txt"
          " dengan kunci diketahui"
          "\n3. Dekripsi dari ciphertext.txt ke decryptionresult.txt"
          " tanpa mengetahui apapun tentang kunci"
          "\n4. Dekripsi dari ciphertext.txt ke decryptionresult.txt"
          " dengan panjang kunci diketahui")
    while True:
        cho = int(input("Pilih mode: "))
        if cho == 1:
            encrypt_message()
            break
        elif cho == 2:
            decrypt_message()
            break
        elif cho == 3:
            attack_message('blind')
            break
        elif cho == 4:
            attack_message('length-known')
            break
        else:
            print("\nInput tidak dimengerti.")


def read_file(filename):
    """
    :param filename: File yang akan dibaca
    :return: hasil pembacaan file (str)
    """
    with open(str(filename), 'r') as f:
        text = f.read()
    print("Berkas {} berhasil dibaca.".format(filename))
    return text


def write_file(filename, text=""):
    """
    :param filename: File yang akan ditulis
    :param text: teks yang akan dituliskan ke file (str)
    """
    with open(str(filename), 'w') as f:
        f.write(text)
    print("Teks dengan panjang {} berhasil dituliskan ke {}."
          .format(len(text), filename))


def encrypt_message():
    plain_text = read_file('plaintext.txt')
    key = input("Masukkan kunci: ")
    cipher_text = translate_message(plain_text, key, 'encrypt')
    write_file('ciphertext.txt', cipher_text)


def decrypt_message():
    cipher_text = read_file('ciphertext.txt')
    key = input("Masukkan kunci: ")
    decrypted_text = translate_message(cipher_text, key, 'decrypt')
    write_file('decrypted.txt', decrypted_text)


def attack_message(mode='blind'):
    cipher_text = read_file('ciphertext.txt').upper()
    cipher_text = remove_symbol(cipher_text, LETTERS)

    if mode == 'length-known':
        key_length = int(input("Masukkan panjang kunci: "))
    else:  # mode == 'blind'
        key_length = search_key_length(cipher_text)

    deducted_key = find_key(cipher_text, key_length)
    cho = str(input("Mau memilih kunci sendiri? (Y/N) "))
    if cho.upper() == 'Y':
        deducted_key = str(input("Masukkan dugaan kunci : "))

    decrypted_text = translate_message(cipher_text, deducted_key, 'decrypt')
    write_file('decryptionresult.txt', decrypted_text)


def translate_message(message, key, mode='encrypt'):
    """Mentranslasikan pesan menggunakan sandi Vigenere,
    enkripsi ataupun dekripsi.

    :param message: Pesan yang akan ditranslasikan (str).
    :param key: Kunci yang akan digunakan dalam penyandian (str).
    :param mode: Mode penyandian: enkripsi('encrypt') atau
    dekripsi (decrypt).

    :return: pesan yang telah disandikan (str).
    """
    translated = []
    key_index = 0
    key = key.upper()
    message = remove_symbol(message, LETTERS)

    for symbol in message:
        num = LETTERS.find(symbol.upper())
        if mode == 'encrypt':
            num += LETTERS.find(key[key_index])
            num %= len(LETTERS)
        elif mode == 'decrypt':
            num -= LETTERS.find(key[key_index])
            num %= len(LETTERS)

        if num != -1:
            if mode == 'decrypt':
                translated.append(LETTERS[num].lower())
            else:
                translated.append(LETTERS[num])

        key_index += 1
        if key_index == len(key):
            key_index = 0
    return ''.join(translated)


def remove_symbol(text, allowed):
    """Menghilangkan seluruh simbol nonalfabet pada teks.

    :param text: Teks yang akan dihilangkan simbolnya.
    :param allowed: String berisi simbol yang masih diizinkan.
    :return: Teks ALLCAPS yang sudah dihilangkan seluruh simbolnya (str).
    """
    text = text.upper()
    texts = text[:]
    res = texts[:]
    for symbol in text:
        num = allowed.find(symbol)
        if num == -1:
            res = texts.replace(symbol, "")
            texts = res[:]
    return res


def search_key_length(cipher_text):
    """Menentukan panjang kunci melalui perhitungan FPC

    :param cipher_text: kata-sandi yang akan dicari panjang kuncinya
    :return: prediksi panjang kunci (int)
    """
    trigram_list = kas.find_trigrams(cipher_text)
    trigram_occur = kas.count_occurence_list(trigram_list, cipher_text)
    key_length_list = kas.find_key_length(trigram_occur)

    print("Kemungkinan panjang kunci: ")
    for i in key_length_list.keys():
        print("Panjang: {}, Frekuensi: {}".format(i, key_length_list[i]))

    cho = input("Mau memilih panjang kunci secara manual? (Y/N): ")
    if cho.upper() == 'Y':
        key_length = int(input("Masukkan prediksi panjang kunci: "))
    else:
        key_length = kas.choose_max_value(key_length_list)

    return key_length


def find_key(cipher_text, key_length):
    """Menemukan kunci dari kata-sandi dengan panjang kunci diberikan.

    :param cipher_text: Katai-sandi yang akan dicari kuncinya (str).
    :param key_length: Panjang kunci yang telah diketahui (int).
    :return: Dugaan kunci dari panjang yang diberikan (str).
    """
    cipher_block = frq.column_break(cipher_text, key_length)
    freq_count = frq.count_frequency(cipher_block)
    shift_counter = frq.cycle_search(freq_count)
    key = frq.num_to_key(shift_counter)
    print("Dugaan kunci: ", key)
    return key


if __name__ == '__main__':
    main()
