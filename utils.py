import itertools

aToI = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12,
        'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24,
        'Z': 25}

iToA = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M',
        13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y',
        25: 'Z'}

naturalFreq = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'R', 'H', 'D', 'L', 'U', 'C', 'M', 'F', 'Y', 'W', 'G', 'P', 'B', 'V',
               'K', 'X', 'Q', 'J', 'Z']


def getCipherTextInput():
    while True:
        inType = input("How would you like to enter cipher text? (file/string): ")
        if inType.lower() == "file":
            fileName = input("Enter file name: ")
            try:
                with open(fileName, "r") as file:
                    cipherText = file.read().upper()
                    break
            except FileNotFoundError:
                print("File not found!\n")
        elif inType.lower() == "string":
            cipherText = input("Enter cipher text: ").upper()
            break
        else:
            print("Invalid input!\n")
    return cipherText


def removeUnsupportedChars(text):
    positions = []
    unsupportedChars = []
    for pos, char in enumerate(text):
        if char not in aToI:
            positions.append(pos)
            unsupportedChars.append(char)

    if positions:
        rawText = text[:positions[0]]
        for i in range(0, len(positions) - 1):
            rawText += text[positions[i] + 1:positions[i + 1]]
        rawText += text[positions[-1] + 1:]
    else:
        rawText = text

    return positions, unsupportedChars, rawText


def addUnsupportedChars(text, positions, unsupportedChars):
    for pos, char in zip(positions, unsupportedChars):
        text = text[:pos] + char + text[pos:]
    return text


def textToInt(text):
    return list(map(aToI.get, text))


def intToText(text):
    return list(map(iToA.get, text))


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def freqAnalysis(text):
    freqMap = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0,
               'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
    for char in text:
        try:
            freqMap[char] += 1
        except KeyError:
            pass
    return freqMap


def ICAnalysis(text):
    freqMap = freqAnalysis(text)
    IC = 0
    for key in freqMap:
        IC += freqMap[key] * (freqMap[key] - 1)
    return IC / (len(text) * (len(text) - 1))


def kasiskiAnalysis(text):
    trigrams = {}
    allIndices = {}
    indices = {}
    GCDs = {}
    GCD = 1
    for i in range(0, (len(text) - 2)):
        searchText = text
        currTrigram = text[i] + text[i + 1] + text[i + 2]
        if currTrigram not in trigrams:
            trigrams[currTrigram] = 1
            itr = 0
            while True:
                index = searchText.find(currTrigram) + 1
                allIndices.setdefault(currTrigram, [])
                if index == 0:
                    break
                else:
                    if itr == 0:
                        allIndices[currTrigram].append(index)
                    else:
                        allIndices[currTrigram].append(index + allIndices[currTrigram][itr - 1])
                    trigrams[currTrigram] += 1
                    searchText = searchText[index:]
                    itr += 1
    trigrams = sorted(trigrams, key=trigrams.get, reverse=True)[0:5]
    for key in trigrams:
        indices[key] = allIndices[key]
        for i in range(1, len(indices[key]) - 1):
            if i == 1:
                GCD = gcd(indices[key][i - 1], indices[key][i])
            else:
                GCD = gcd(GCD, indices[key][i])
        GCDs[key] = GCD
    return trigrams, indices, GCDs


def permutations(iterable, n, unique=True):
    """itertools override"""
    perms = []
    swaps = list(itertools.permutations(iterable, r=2))
    i = 0
    while i < n:
        perm = dict(zip(iterable, iterable))
        perm[swaps[i][0]] = swaps[i][1]
        perm[swaps[i][1]] = swaps[i][0]
        perms.append(list(perm.values()))
        i += 1
    if unique:
        return list(set(map(tuple, perms)))
    else:
        return perms
