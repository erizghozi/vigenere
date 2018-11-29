# Vigenere Cipher Hacker

import itertools, re 
import vig, freqAnalysis 
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' 
SILENT_MODE = False # jika bernilai benar, tidak akan dilakukan apa-apa 
NUM_MOST_FREQ_LETTERS = 4 # melihat banyak huruf per subkunci
MAX_KEY_LENGTH = 16 # maksimal panjang kunci
NONLETTERS_PATTERN = re.compile('[^A-Z]')

def main():
    ciphertext = """Wftwbnup atqjnpnupoia mlaqetv fphdvmumhb bepnupgle Qauawiyb Ggrbdpwtk Iochcai (PHQ) hq xcuqpl qavlfceavquoa.
    Oiyk pbx tmaehdpmia kai qizuczwa hqecpv Qmub Ckwiciecoapr Evthdjxzn, ohvpwqfyh Dgslv Vlycms Vpmcgqigkro,
    HXMV-KAP setno hxpro Vpasgrigkvbpp Unvosbebve Jcbtmgkawdr (QZE) 2018 kw Qyttcywp.Hiyct ydqxrvpgx ciai isgpiaizick arlhy 22-28 Yytv 2018 fp Ydxi Onhudideck wiy, Jvov ptvpnupz bivqcwoioia olrppq rohg pxih hpfhx xekgs hibrnhv xe jrtzoxro qguupr 351 xrulfie tnku rpvq ogyppkiv plupvi qk kicmi. Ggyapwcx dlfheqai ksckia 9 flztkifk soxr lntp Wchwagzwp.
    Ebnu wftwbnup mpro zgtpprotcroc xmeulpjx brpaicci ggsow qmzdhkp liewt bpqi Vpkcciavc koc qmzdhbvkixcu qxzqgcz ozelropyp MBO moihyaaah.


    """
    hackedMessage = hackVigenere(ciphertext)

    if hackedMessage != None:
        print('Copying hacked message to clipboard:')
        print(hackedMessage)
    else:
        print('Failed to hack encryption.')


def findRepeatSequencesSpacings(message):
    # Mencari trigram
    message = NONLETTERS_PATTERN.sub('', message.upper())

    seqSpacings = {} # melihat kunci sebagai barisan
    for seqLen in range(3, 6):
        for seqStart in range(len(message) - seqLen):
            # Menentukan barisan dan menginput ke variabel seq
            seq = message[seqStart:seqStart + seqLen]

            # Mencari barisan ini di sisa input
            for i in range(seqStart + seqLen, len(message) - seqLen):
                if message[i:i + seqLen] == seq:
                    # Menemukan barisan berulang
                    if seq not in seqSpacings:
                        seqSpacings[seq] = [] # inisialisasi

                    # Hitung jarak barisan berulang
                    seqSpacings[seq].append(i - seqStart)
    return seqSpacings


def getUsefulFactors(num):
    if num < 2:
        return [] # tidak ada faktor penting

    factors = [] # list faktor berulang yang ditemukan

    # Setelah ditemukan faktor, akan diperiksa apakah lebih dari
    # MAX_KEY_LENGTH.
    for i in range(2, MAX_KEY_LENGTH + 1):
        if num % i == 0:
            factors.append(i)
            factors.append(int(num / i))
    if 1 in factors:
        factors.remove(1)
    return list(set(factors))


def getItemAtIndexOne(x):
    return x[1]


def getMostCommonFactors(seqFactors):
    # Hitung berapak kali faktor muncul dalam seqFactors
    factorCounts = {} # kunci adalah faktor, dihitung banyaknya

    for seq in seqFactors:
        factorList = seqFactors[seq]
        for factor in factorList:
            if factor not in factorCounts:
                factorCounts[factor] = 0
            factorCounts[factor] += 1

    # Tempatkan faktor dan hitungannya ke tuple
    # kita bisa urutkan tuple
    factorsByCount = []
    for factor in factorCounts:
        if factor <= MAX_KEY_LENGTH:
            factorsByCount.append( (factor, factorCounts[factor]) )

    # Urutkan list dengan hitung faktor
    factorsByCount.sort(key=getItemAtIndexOne, reverse=True)

    return factorsByCount


def kasiskiExamination(ciphertext):
    # Cari barisan 3 hingga 5 huruf yang muncul berulang kali di barisan
    repeatedSeqSpacings = findRepeatSequencesSpacings(ciphertext)

    seqFactors = {}
    for seq in repeatedSeqSpacings:
        seqFactors[seq] = []
        for spacing in repeatedSeqSpacings[seq]:
            seqFactors[seq].extend(getUsefulFactors(spacing))

    # Periksa getMostCommonFactors
    factorsByCount = getMostCommonFactors(seqFactors)

    allLikelyKeyLengths = []
    for twoIntTuple in factorsByCount:
        allLikelyKeyLengths.append(twoIntTuple[0])

    return allLikelyKeyLengths


def getNthSubkeysLetters(n, keyLength, message):
    message = NONLETTERS_PATTERN.sub('', message)

    i = n - 1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += keyLength
    return ''.join(letters)


def attemptHackWithKeyLength(ciphertext, mostLikelyKeyLength):
    # Determine the most likely letters for each letter in the key.
    ciphertextUp = ciphertext.upper()
    # allFreqScores is a list of mostLikelyKeyLength number of lists.
    # These inner lists are the freqScores lists.
    allFreqScores = []
    for nth in range(1, mostLikelyKeyLength + 1):
        nthLetters = getNthSubkeysLetters(nth, mostLikelyKeyLength, ciphertextUp)

        # freqScores adalah list tuple:
        freqScores = []
        for possibleKey in LETTERS:
            decryptedText = vig.decryptMessage(possibleKey, nthLetters)
            keyAndFreqMatchTuple = (possibleKey, freqAnalysis.indonesiaFreqMatchScore(decryptedText))
            freqScores.append(keyAndFreqMatchTuple)
        # Urutkan berdasarkan skor kecocokan
        freqScores.sort(key=getItemAtIndexOne, reverse=True)

        allFreqScores.append(freqScores[:NUM_MOST_FREQ_LETTERS])

    if not SILENT_MODE:
        for i in range(len(allFreqScores)):
            print('Possible letters for letter %s of the key: ' % (i + 1), end='')
            for freqScore in allFreqScores[i]:
                print('%s ' % freqScore[0], end='')
            print()

    # Coba semua kombinasi di berbagai tempat
    for indexes in itertools.product(range(NUM_MOST_FREQ_LETTERS), repeat=mostLikelyKeyLength):
        # Bentuk kunci yang mungkin dari allFreqScores
        possibleKey = ''
        for i in range(mostLikelyKeyLength):
            possibleKey += allFreqScores[i][indexes[i]][0]

        if not SILENT_MODE:
            print('Attempting with key: %s' % (possibleKey))

        decryptedText = vig.decryptMessage(possibleKey, ciphertextUp)

        # Set the hacked ciphertext to the original casing.
        origCase = []
        for i in range(len(ciphertext)):
            if ciphertext[i].isupper():
                origCase.append(decryptedText[i].upper())
            else:
                origCase.append(decryptedText[i].lower())
        decryptedText = ''.join(origCase)

        print('Possible encryption hack with key %s:' % (possibleKey))
        print(decryptedText[:200]) 
        print()
        print('Enter D for done, or just press Enter to continue hacking:')
        response = input('> ')

        if response.strip().upper().startswith('D'):
            return decryptedText

    return None


def hackVigenere(ciphertext):
    # Akan digunakan Kasiski
    allLikelyKeyLengths = kasiskiExamination(ciphertext)
    if not SILENT_MODE:
        keyLengthStr = ''
        for keyLength in allLikelyKeyLengths:
            keyLengthStr += '%s ' % (keyLength)
        print('Kasiski Examination results say the most likely key lengths are: ' + keyLengthStr + '\n')

    for keyLength in allLikelyKeyLengths:
        if not SILENT_MODE:
            print('Attempting hack with key length %s (%s possible keys)...' % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
        hackedMessage = attemptHackWithKeyLength(ciphertext, keyLength)
        if hackedMessage != None:
            break

    # Jika tidak ada kunci ditemukan, gunakan Kasiski
    # Jika bekerja, periksa satu-satu
    if hackedMessage == None:
        if not SILENT_MODE:
            print('Unable to hack message with likely key length(s). Brute-forcing key length...')
        for keyLength in range(1, MAX_KEY_LENGTH + 1):
            # tidak periksa panjang kunci yang sudah dicek di Kasiski
            if keyLength not in allLikelyKeyLengths:
                if not SILENT_MODE:
                    print('Attempting hack with key length %s (%s possible keys)...' % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
                hackedMessage = attemptHackWithKeyLength(ciphertext, keyLength)
                if hackedMessage != None:
                    break
    return hackedMessage


if __name__ == '__main__':
    main()