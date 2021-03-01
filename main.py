import shiftCipher
import subCipher
import vigenereCipher
import utils

CIPHER_TEXT = None
POSITIONS = None
UNSUPPORTED_CHARS = None


def updateCipherText():
    global CIPHER_TEXT, POSITIONS, UNSUPPORTED_CHARS, CIPHER_TEXT
    CIPHER_TEXT = utils.getCipherTextInput()
    POSITIONS, UNSUPPORTED_CHARS, CIPHER_TEXT = utils.removeUnsupportedChars(CIPHER_TEXT)


while True:
    shiftKey = None
    subKey = None
    vigenereKey = None
    vigenereItr = 0
    subItr = 0

    choice = input('\nWhat would you like to do?\n'
                   '1: Cipher Text Analysis\n'
                   '2: Crack Cipher Text\n'
                   '3: Change Cipher Text\n'
                   '4: Utils\n'
                   '4: Exit\n'
                   'Choice: ')

    if choice == '1':
        while True:
            analysisType = input('\nWhat form of analysis would you like to perform?\n'
                                 '1: Frequency Analysis\n'
                                 '2: Index of Coincidence\n'
                                 '3: Kasiki Analysis\n'
                                 '4: Cancel\n'
                                 'Choice: ')

            if analysisType == '4':
                break

            if CIPHER_TEXT is None:
                updateCipherText()

            if analysisType == '1':
                freqMap = utils.freqAnalysis(CIPHER_TEXT)
                freqMap = dict(sorted(freqMap.items(), key=lambda value: value[1], reverse=True))
                print(freqMap)
            elif analysisType == '2':
                IC = utils.ICAnalysis(CIPHER_TEXT)
                print(IC)
            elif analysisType == '3':
                _, _, GCDs = utils.kasiskiAnalysis(CIPHER_TEXT)
                GCDs = list(dict.fromkeys(GCDs.values()))
                output = 'Potential key lengths: '
                for gcd in GCDs:
                    output += str(gcd) + ', '
                print(output[:-2])
            else:
                print('Invalid input!')

    elif choice == '2':
        if CIPHER_TEXT is None:
            updateCipherText()

        freqList = sorted(utils.freqAnalysis(CIPHER_TEXT), key=utils.freqAnalysis(CIPHER_TEXT).get, reverse=True)
        IC = utils.ICAnalysis(CIPHER_TEXT)
        trigrams, indices, GCDs = utils.kasiskiAnalysis(CIPHER_TEXT)
        GCDs = list(dict.fromkeys(GCDs.values()))

        if abs(IC - 0.0686) < 0.02:
            print('Recommended cipher: Shift or Substitution')
        elif abs(IC - 0.038466) < 0.003:
            print('Cipher text is likely random')
        else:
            print('Recommended cipher: Vigenere')

        while True:
            cancel = False
            plainText = ''

            while True:
                cipherType = input('\nWhat cipher would you like to try?\n'
                                   '1: Shift\n'
                                   '2: Substitution\n'
                                   '3: Vigenere\n'
                                   '4: Cancel\n'
                                   'Choice: ')

                if cipherType == '1':
                    if shiftKey is None:
                        shiftKey = (utils.aToI[utils.naturalFreq[0]] - utils.aToI[freqList[0]]) % 26
                    plainText = ''.join(utils.intToText(shiftCipher.decrypt(utils.textToInt(CIPHER_TEXT), shiftKey)))
                    break
                elif cipherType == '2':
                    if subKey is None:
                        subKey = dict(zip(freqList, utils.naturalFreq))
                    plainText = subCipher.decrypt(CIPHER_TEXT, subKey)
                    break
                elif cipherType == '3':
                    if vigenereKey is None:
                        vigenereKey = vigenereCipher.genKey(CIPHER_TEXT, GCDs, vigenereItr)
                        vigenereItr += 1
                    plainText = ''.join(utils.intToText(vigenereCipher.decrypt(utils.textToInt(CIPHER_TEXT), vigenereKey)))
                    break
                elif cipherType == '4':
                    cancel = True
                    break
                else:
                    print('Invalid input!')

            if cancel:
                break

            formattedText = utils.addUnsupportedChars(plainText, POSITIONS, UNSUPPORTED_CHARS)
            print('Cipher text: ', CIPHER_TEXT)
            print(' Plain text: ', formattedText)

            correct = input('Does this look correct? (y/n): ')
            if correct.lower() == 'y':
                if cipherType == '1':
                    print('Key: ', shiftKey)
                elif cipherType == '2':
                    print('Key: ', subKey)
                elif cipherType == '3':
                    print('Key: ', utils.intToText(vigenereKey))
                break
            else:
                if cipherType == '1':
                    shiftKey = (shiftKey + 1) % 26
                    if shiftKey == 0:
                        shiftKey = 1
                    print('Key updated! Try shift cipher again.')
                elif cipherType == '2':
                    keyGenType = input('Automatically generate next key? (y/n): ')
                    keyGenTypes = {'y': 'auto', 'n': 'manual'}
                    subKey = subCipher.genKey(subKey, keyGenTypes[keyGenType], subItr)
                    subItr += 1 if keyGenType == 'y' else 0
                elif cipherType == '3':
                    vigenereKey = vigenereCipher.genKey(CIPHER_TEXT, GCDs, vigenereItr)
                    vigenereItr += 1
    elif choice == '3':
        updateCipherText()
    elif choice == '4':
        while True:
            util_select = input('Utilities\n'
                                '1: Text to Int\n'
                                '2: Int to Text\n'
                                '3: Cancel\n'
                                'Choice: \n')
            if util_select == '1':
                print(utils.textToInt(CIPHER_TEXT))
            elif util_select == '2':
                print(utils.intToText(list(map(int, input('Enter int array (comma separated): ').split(',')))))
            elif util_select == '3':
                break
            else:
                print('Invalid input!')
    elif choice == '5':
        break
    else:
        print('Invalid input!')
