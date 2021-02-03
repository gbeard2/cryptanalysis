import shiftCipher as shiftCipher
import subCipher as subCipher
import vigenereCipher as vigenereCipher
import utils as utils

shiftKey = None
subKey = None
vigenereKey = None
vigenereItr = 0

while True:
    choice = input("What would you like to do?\n"
                   "1: Cipher Text Analysis\n"
                   "2: Crack Cipher Text\n"
                   "3: Exit\n"
                   "Choice: ")
    if choice == '1':
        while True:
            analysisType = input("What form of analysis would you like to perform?\n"
                                 "1: Frequency Analysis\n"
                                 "2: Index of Coincidence\n"
                                 "3: Kasiki Analysis\n"
                                 "4: Cancel\n"
                                 "Choice: ")

            if analysisType == '4':
                break

            cipherText = utils.getCipherTextInput()
            _, _, cipherText = utils.removeUnsupportedChars(cipherText)

            if analysisType == '1':
                freqMap = utils.freqAnalysis(cipherText)
                freqMap = dict(sorted(freqMap.items(), key=lambda value: value[1], reverse=True))
                print(freqMap)
            elif analysisType == '2':
                IC = utils.ICAnalysis(cipherText)
                print(IC)
            elif analysisType == '3':
                _, _, GCDs = utils.kasiskiAnalysis(cipherText)
                GCDs = list(dict.fromkeys(GCDs.values()))
                output = "Potential key lengths: "
                for gcd in GCDs:
                    output += str(gcd) + ", "
                print(output[:-2] + "\n")
            else:
                print("Invalid input!\n")

    elif choice == '2':
        cipherText = utils.getCipherTextInput()
        positions, unsupportedChars, cipherText = utils.removeUnsupportedChars(cipherText)

        freqList = sorted(utils.freqAnalysis(cipherText), key=utils.freqAnalysis(cipherText).get, reverse=True)
        IC = utils.ICAnalysis(cipherText)
        trigrams, indices, GCDs = utils.kasiskiAnalysis(cipherText)
        GCDs = list(dict.fromkeys(GCDs.values()))

        print("IC: ", IC)
        if abs(IC - 0.0686) < 0.02:
            print("Recommended cipher: Shift or Substitution\n")
        elif abs(IC - 0.038466) < 0.003:
            print("Cipher text is likely random\n")
        else:
            print("Recommended cipher: Vigenere\n")

        while True:
            cancel = False
            plainText = ''

            while True:
                cipherType = input("What cipher would you like to try?\n"
                                   "1: Shift\n"
                                   "2: Substitution\n"
                                   "3: Vigenere\n"
                                   "4: Cancel\n"
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
                elif cipherType == '4':
                    cancel = True
                    break
                else:
                    print("Invalid input!\n")

            if cancel:
                break

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
                    print('Key updated! Try shift cipher again.\n')
                elif cipherType == '2':
                    subKey = subCipher.genKey(subKey)
                elif cipherType == '3':
                    vigenereKey = vigenereCipher.genKey(cipherText, GCDs, vigenereItr)
                    vigenereItr += 1
    elif choice == '3':
        break
