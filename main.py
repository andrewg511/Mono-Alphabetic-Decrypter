import os
import numpy as np


def heatmap(message, length):
    letterpercentages = [0] * 26
    # calculate a heat map for the letters
    while True:
        symbol = message.read(1)
        if not symbol:
            break
        symbol = symbol.lower()
        if symbol == 'a':
            letterpercentages[0] += 1
        elif symbol == 'b':
            letterpercentages[1] += 1
        elif symbol == 'c':
            letterpercentages[2] += 1
        elif symbol == 'd':
            letterpercentages[3] += 1
        elif symbol == 'e':
            letterpercentages[4] += 1
        elif symbol == 'f':
            letterpercentages[5] += 1
        elif symbol == 'g':
            letterpercentages[6] += 1
        elif symbol == 'h':
            letterpercentages[7] += 1
        elif symbol == 'i':
            letterpercentages[8] += 1
        elif symbol == 'j':
            letterpercentages[9] += 1
        elif symbol == 'k':
            letterpercentages[10] += 1
        elif symbol == 'l':
            letterpercentages[11] += 1
        elif symbol == 'm':
            letterpercentages[12] += 1
        elif symbol == 'n':
            letterpercentages[13] += 1
        elif symbol == 'o':
            letterpercentages[14] += 1
        elif symbol == 'p':
            letterpercentages[15] += 1
        elif symbol == 'q':
            letterpercentages[16] += 1
        elif symbol == 'r':
            letterpercentages[17] += 1
        elif symbol == 's':
            letterpercentages[18] += 1
        elif symbol == 't':
            letterpercentages[19] += 1
        elif symbol == 'u':
            letterpercentages[20] += 1
        elif symbol == 'v':
            letterpercentages[21] += 1
        elif symbol == 'w':
            letterpercentages[22] += 1
        elif symbol == 'x':
            letterpercentages[23] += 1
        elif symbol == 'y':
            letterpercentages[24] += 1
        elif symbol == 'z':
            letterpercentages[25] += 1
        else:
            continue

    count = 0
    for x in letterpercentages:
        x = x / length * 100
        letterpercentages[count] = x
        count += 1

    return letterpercentages


def trainDecrypt(directoryPath, amount_of_files):
    trained_percentages = [0] * 26
    originalPercentages = [[0] * 26] * amount_of_files
    count = 0
    for textfile in os.listdir(directoryPath):
        if textfile.endswith(".txt"):
            f = open(os.path.join(directoryPath, textfile), 'r', encoding='utf-8')
            messlen = len(f.read())
            f = open(os.path.join(directoryPath, textfile), 'r', encoding='utf-8')
            perc = heatmap(f, messlen)
            originalPercentages[count] = perc
            count += 1
        else:
            continue

    # now we need to take the averages
    for row in originalPercentages:
     #   print(row)
        trained_percentages = np.add(trained_percentages, row)

    count = 0
    for element in trained_percentages:
        trained_percentages[count] = element / amount_of_files
        count += 1

    return trained_percentages


def numWordFilter(message, number_of_characters):
    thletterarray = ["", ""]
    theletterindex = [0, 0]
    thlettercount = 0
    word = ""

    while True:
        symbol = message.read(1)
        if not symbol:
            break
        if symbol.isalpha():
            word += symbol
        elif symbol == ' ' or symbol == '\t':
            if len(word) != number_of_characters:
                word = ""
            else:
                word = word.lower()
                if word in thletterarray:
                    newcount = 0
                    for theword in thletterarray:
                        if theword == word:
                            theletterindex[newcount] += 1
                            break
                        newcount += 1
                else:
                    if thlettercount == 2:
                        thletterarray.append(word)
                        theletterindex.append(1)
                    else:
                        thletterarray[thlettercount] = word
                        theletterindex[thlettercount] = 1
                        thlettercount += 1

            word = ""

    for i in range(1, len(theletterindex)):
        key_item = theletterindex[i]
        let_item = thletterarray[i]
        j = i - 1
        while j >= 0 and theletterindex[j] > key_item:
            theletterindex[j + 1] = theletterindex[j]
            thletterarray[j + 1] = thletterarray[j]
            j -= 1

        theletterindex[j + 1] = key_item
        thletterarray[j + 1] = let_item

    theletterindex = np.flip(theletterindex, axis = 0)
    thletterarray = np.flip(thletterarray, axis = 0)
    the = thletterarray[0]
    tand = thletterarray[1]

    return the, tand, thletterarray


def wordFilter(message, cipherL, plainL, the, tand):
    key = list(the + tand)
    plainkey = list("theand")
    plainL = plainL.tolist()
    cipherL = cipherL.tolist()
    wordlist = ["each", "as", "use", "even", "to", "in", "this", "it", "is", "not", "also", "again", "go", "some", "same", "can", "come",
                "if", "their", "her", "there", "for", "more", "from", "think", "like", "make", "with", "know", "us", "much", "number", "over", "only", "they", "be", "but",
                "year", "my", "you", "could", "up", "have", "zip", "utilize", "utilizing", "realize", "realized",
                "size", "zero", "luxury", "next", "part", "help", "open", "person", "example", "explain", "explained", "exact", "exactly"
                "jump", "object", "objects", "subject",
                "subjects", "just", "project", "quest", "quit", "quick", "question", "queen"]
 #   print("Before Change:")
 #   print(cipherL)
#    print(plainL)
 #   print("After change")
    # -1. find i, its special
    a, i, _ = numWordFilter(message, 1)
 #   print(a, i)
    message.seek(0)

    if a in key:
        if a != key[3]:
            plainkey = list("andthe")

    # 0. you must delete letters from the cipher list (CL) and plain list (PL) for the and and
    for char in plainkey:
        plainL.remove(char)
    for char in key:
        cipherL.remove(char)
    # 1. query up the word (loop)
    for word in wordlist:
        # 2. find out the length of the word
        wordlength = len(word)
        word = list(word)
        # 3. get all the words in the txt with that length
        _, _, txtarray = numWordFilter(message, wordlength)
        message.seek(0)
        # 4. get the index of the character that is missing in the word (when you find it you can stop since all
        # words only have one new character)
        # 5. covert the word to ciphertext
        indexFound = False
        index = 0
        current = 0
        for char in word:
            if char not in plainkey:
                indexFound = True
            elif not indexFound:
                for x, y in zip(key, plainkey):
                    if y == char:
                        word[current] = x
                        break
                index += 1
            elif indexFound:
                for x, y in zip(key, plainkey):
                    if y == char:
                        word[current] = x
                        break

            current += 1

        if indexFound:
            # 6. loop through the cipher word list,
            for cipherword in txtarray:
                # loop through the individual words and compare the letters array with the word
                cipherWL = list(cipherword)
                current = 0
                letterSave = ""
                correctWord = True
                for x, y in zip(cipherWL, word):
                    # if index of the word is the unknown letter, continue
                    if current == index and x not in key:
                        letterSave = x
                    # elif a letter you know does not match up skip word (make boolean false and break)
                    elif x != y or current == index:
                        correctWord = False
                        break

                    current += 1

                # check boolean. if true, append unknown letter, delete letters from CL and PL and break,
                if correctWord:
                    key.append(letterSave)
                    plainkey.append(word[index])
                    cipherL.remove(letterSave)
                    plainL.remove(word[index])
                    break

    # 7. once all done, attach the CL to key and attach PL to plainkey
    key = key + cipherL
    plainkey = plainkey + plainL
    # 8. Sort plainkey while sorting key in the process

    return key, plainkey


def decrypt(message, lperc, trained):
    oriLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z']
    letters = oriLetters
    key = ""
    # 1. we need to sort the heat map and the letters
    for i in range(1, len(lperc)):
        key_item = lperc[i]
        let_item = letters[i]
        j = i - 1
        while j >= 0 and lperc[j] > key_item:
            lperc[j + 1] = lperc[j]
            letters[j + 1] = letters[j]
            j -= 1

        lperc[j + 1] = key_item
        letters[j + 1] = let_item

    lperc = np.flip(lperc, axis = 0)
    letters = np.flip(letters, axis = 0)

    # 2. we need to utilize the trained algorthm that knows the english heatmap
    letters2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
  #  print(letters2)
    for i in range(1, len(trained)):
        key_item = trained[i]
        let_item = letters2[i]
        j = i - 1
        while j >= 0 and trained[j] > key_item:
            trained[j + 1] = trained[j]
            letters2[j + 1] = letters2[j]
            j -= 1

        trained[j + 1] = key_item
        letters2[j + 1] = let_item

    trained = np.flip(trained, axis = 0)
    letters2 = np.flip(letters2, axis = 0)
    message.seek(0)
    the, tand, _ = numWordFilter(message, 3)
    message.seek(0)
    key, plainkey = wordFilter(message, cipherL=np.array(letters), plainL=np.array(letters2), the=the, tand=tand)

   # print(key)
   # print(plainkey)
    for i in range(1, len(plainkey)):
        key_item = plainkey[i]
        let_item = key[i]
        j = i - 1
        while j >= 0 and plainkey[j] > key_item:
            plainkey[j + 1] = plainkey[j]
            key[j + 1] = key[j]
            j -= 1

        plainkey[j + 1] = key_item
        key[j + 1] = let_item

    newkey = ""
    newplainkey = ""
    for x, y in zip(key, plainkey):
        newkey += x
        newplainkey += y

    return newkey.upper(), newplainkey.upper()


def main():
    # train
    trainedPerc = trainDecrypt(directoryPath="TrainingFiles", amount_of_files=8)
    # print(trainedPerc)
    # test file & decrypt
    print("Hello! Can you please give me the name of the encrypted file:")
    inputfile = input()
    print("----------- Loading Key -----------")
    f = open(inputfile, "r", encoding='utf-8')
    messlen = len(f.read())
    f.seek(0)
    lperc = heatmap(f, messlen)
    key, plainkey = decrypt(f, lperc, trainedPerc)
    output = open("key.txt", "w")
    output.write(key)
    print("Key printed to key.txt!")



if __name__ == "__main__":
    main()
