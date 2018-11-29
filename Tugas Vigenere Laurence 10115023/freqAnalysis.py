# Frequency Finder
indonesiaLetterFreq = {'A': 18.994, 'N': 9.577, 'E': 8.377, 'I': 7.796, 'U': 5.410, 'M': 5.270, 'T': 5.251, 'K': 4.693, 'D': 4.456, 'S': 4.392, 'R': 4.223, 'L': 4.068, 'G': 3.814, 'P': 3.790, 'H': 2.293, 'B': 2.125, 'Y': 1.559, 'O': 1.512, 'J': 0.795, 'W': 0.748, 'C': 0.417, 'F': 0.360, 'V': 0.035, 'Z': 0.025, 'Q': 0.010, 'X': 0.010}
ETAOIN = 'ANEIUMTKDSRLGPHBYOJWCFVZQX'
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def getLetterCount(message):
    # Hitung banyak huruf muncul
    letterCount = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}

    for letter in message.upper():
        if letter in LETTERS:
            letterCount[letter] += 1

    return letterCount


def getItemAtIndexZero(x):
    return x[0]


def getFrequencyOrder(message):
    letterToFreq = getLetterCount(message)


    freqToLetter = {}
    for letter in LETTERS:
        if letterToFreq[letter] not in freqToLetter:
            freqToLetter[letterToFreq[letter]] = [letter]
        else:
            freqToLetter[letterToFreq[letter]].append(letter)

    for freq in freqToLetter:
        freqToLetter[freq].sort(key=ETAOIN.find, reverse=True)
        freqToLetter[freq] = ''.join(freqToLetter[freq])

    freqPairs = list(freqToLetter.items())
    freqPairs.sort(key=getItemAtIndexZero, reverse=True)


    freqOrder = []
    for freqPair in freqPairs:
        freqOrder.append(freqPair[1])

    return ''.join(freqOrder)


def indonesiaFreqMatchScore(message):
    # Kembali ke banyak huruf yang cocok
    freqOrder = getFrequencyOrder(message)

    matchScore = 0
    # Cari berapa banyak 6 huruf paling cocok
    for commonLetter in ETAOIN[:6]:
        if commonLetter in freqOrder[:6]:
            matchScore += 1
    # Cari berapa banyak 6 huruf paling tidak cocok
    for uncommonLetter in ETAOIN[-6:]:
        if uncommonLetter in freqOrder[-6:]:
            matchScore += 1

    return matchScore