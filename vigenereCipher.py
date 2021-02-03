import utils as utils


def decrypt(cipherText, key):
    if len(key) != 0:
        for i in range(0, int(len(cipherText)/len(key))):
            for j in range(0, len(key)):
                cipherText[(i * len(key)) + j] = (cipherText[(i * len(key)) + j] - key[j]) % 26
    return cipherText


def genKey(cipherText, GCDs, itr):
    try:
        keyLen = GCDs[itr]
    except IndexError:
        print("Maximum keys attempted! Try a different cipher.")
        return []

    subStrs = {}
    for i in range(0, len(cipherText)):
        subStrs.setdefault(i % keyLen, [])
        subStrs[i % keyLen].append(cipherText[i])

    subFreqs = []
    for subStr in subStrs.values():
        subFreqs.append(utils.textToInt(sorted(utils.freqAnalysis(subStr),
                                               key=utils.freqAnalysis(subStr).get,
                                               reverse=True)))

    key = []
    for subFreq in subFreqs:
        key.append((subFreq[0] - 4) % 26)

    if itr != 0:
        print("Key updated! Try vigenere cipher again.")

    return key
