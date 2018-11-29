LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def main():
    myMessage = """Prestasi membanggakan kembali ditorehkan mahasiswa Institut Teknologi Bandung (ITB) di kancah internasional. 
    Kali ini pencapaian itu berhasil diraih Bimo Adityarahman Wiraputra, mahasiswa Prodi Teknik Informatika, 
    STEI-ITB dalam ajang International Mathematic Competition (IMC) 2018 di Bulgaria.Dalam kompetisi yang berlangsung sejak 22-28 Juli 2018 di Kota Blagoevrad itu, Bimo berhasil mendapatkan medali emas atau first prize setelah ia bersaing dengan 351 peserta lain dari berbagai negara di dunia. Termasuk bersaing dengan 9 delegasi lain dari Indonesia. 
    Atas prestasi yang membanggakan tersebut tentunya telah membawa harum nama Indonesia dan membanggakan civitas akademika ITB khususnya. """
    myKey = 'HOPEINC'
    myMode = 'encrypt' # pilih 'encrypt' atau 'decrypt'
    if myMode == 'encrypt':
        translated = encryptMessage(myKey, myMessage)
    elif myMode == 'decrypt':
        translated = decryptMessage(myKey, myMessage)
    print('%sed message:' % (myMode.title()))
    print(translated)
    print()
    print('The message has been copied to the clipboard.')
def encryptMessage(key, message):
    return translateMessage(key, message, 'encrypt')
def decryptMessage(key, message):
    return translateMessage(key, message, 'decrypt')
def translateMessage(key, message, mode):
    translated = [] # simpan hasil di string
    keyIndex = 0
    key = key.upper()
    for symbol in message: # lulangi tiap karakter di pesan
        num = LETTERS.find(symbol.upper())
        if num != -1: # -1 artinya simbol.upper tidak ditemukan
            if mode == 'encrypt':
                num += LETTERS.find(key[keyIndex]) 
            elif mode == 'decrypt':
                num -= LETTERS.find(key[keyIndex]) 
            num %= len(LETTERS) 
            if symbol.isupper():
                translated.append(LETTERS[num])
            elif symbol.islower():
                translated.append(LETTERS[num].lower())
            keyIndex += 1 # pindah ke huruf selanjutnya di kunci
            if keyIndex == len(key):
                keyIndex = 0
        else:
            # Jika bukan huruf, abaikan
            translated.append(symbol)
    return ''.join(translated)
if __name__ == '__main__':
    main()