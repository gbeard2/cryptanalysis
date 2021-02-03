def decrypt(cipherText, key):
    return ''.join(list(map(key.get, cipherText)))


def genKey(key):
    cipherWord = input("Enter an incorrect word from the plain text: ").upper()
    plainWord = input("Enter the correct word: ").upper()
    if len(cipherWord) != len(plainWord):
        print("Length of words must match! Key failed to update.")
        return key
    elif not (cipherWord.isalpha() and plainWord.isalpha()):
        print("Numbers can not be entered! Key failed to update.")
    else:
        cipherWordArray = []
        cipherWordArray[:0] = cipherWord
        plainWordArray = []
        plainWordArray[:0] = plainWord
        inverseKey = dict(zip(key.values(), key.keys()))
        for i in range(0, len(cipherWordArray)):
            if cipherWordArray[i] != plainWordArray[i]:
                key[inverseKey[cipherWordArray[i]]] = plainWordArray[i]
                key[inverseKey[plainWordArray[i]]] = cipherWordArray[i]
        print("Key updated! Try substitution cipher again.")
    return key
