import shiftCipher as shiftCipher
import subCipher as subCipher
import vigenereCipher as vigenereCipher
import utils as utils

shiftKey = None
subKey = None
vigenereKey = None
vigenereItr = 0

cipherText = utils.getCipherTextInput()
positions, unsupportedChars, cipherText = utils.removeUnsupportedChars(cipherText)

freqList = sorted(utils.freqAnalysis(cipherText), key=utils.freqAnalysis(cipherText).get, reverse=True)
IC = utils.ICAnalysis(cipherText)
trigrams, indices, GCDs = utils.kasiskiAnalysis(cipherText)
GCDs = list(dict.fromkeys(GCDs.values()))


print("IC: ", IC)
if abs(IC - 0.0686) < 0.02:
    print("Recommended cipher: Shift or Substitution")
elif abs(IC - 0.038466) < 0.003:
    print("Cipher text is likely random")
else:
    print("Recommended cipher: Vigenere")

while True:
    while True:
        cipherType = input("What cipher would you like to try?\n"
                           "1: Shift\n"
                           "2: Substitution\n"
                           "3: Vigenere\n"
                           "Choice: ")

        if cipherType == '1':
            if shiftKey is None:
                shiftKey = (utils.aToI[utils.naturalFreq[0]] - utils.aToI[freqList[0]]) % 26
            plainText = ''.join(utils.intToText(shiftCipher.decrypt(utils.textToInt(cipherText), shiftKey)))
            break
        elif cipherType == '2':
            if subKey is None:
                subKey = dict(zip(freqList, utils.naturalFreq))
            plainText = subCipher.decrypt(cipherText, subKey)
            break
        elif cipherType == '3':
            if vigenereKey is None:
                vigenereKey = vigenereCipher.genKey(cipherText, GCDs, vigenereItr)
                vigenereItr += 1
            plainText = ''.join(utils.intToText(vigenereCipher.decrypt(utils.textToInt(cipherText), vigenereKey)))
            break
        else:
            print("Invalid input!\n")

    formattedText = utils.addUnsupportedChars(plainText, positions, unsupportedChars)
    print("Cipher text: ", cipherText)
    print(" Plain text: ", formattedText)

    correct = input("Does this look correct? (y/n): ")
    if correct.lower() == 'y':
        if cipherType == '1':
            print("Key: ", shiftKey)
        elif cipherType == '2':
            print(freqList)
            print("Key: ", subKey)
        elif cipherType == '3':
            print("Key: ", utils.intToText(vigenereKey))
        break
    else:
        if cipherType == '1':
            shiftKey = (shiftKey + 1) % 26
            if shiftKey == 0:
                shiftKey = 1
            print('Key updated! Try shift cipher again.')
        elif cipherType == '2':
            subKey = subCipher.genKey(subKey)
        elif cipherType == '3':
            vigenereKey = vigenereCipher.genKey(cipherText, GCDs, vigenereItr)
            vigenereItr += 1
