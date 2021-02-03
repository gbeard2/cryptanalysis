def decrypt(cipherText, key):
    for i in range(0, len(cipherText)):
        cipherText[i] = (cipherText[i] + key) % 26
    return cipherText
