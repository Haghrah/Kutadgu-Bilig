from collections import Counter




if __name__ == "__main__":
    wordsList = []
    mergedFile = open("../Text/merged.txt", "r")
    for line in mergedFile:
        if line[:4] != "beyt" and line[:3] != "بیت":
            wordsList.extend(line.strip().split())
    mergedFile.close()
    wordsList.sort(key=len)
    uniqueWords = list(set(wordsList))
    uniqueWords.sort(key=len)
    
    
    morphologicallyUniqueWordsList = uniqueWords[:]
    for uniqueWord in uniqueWords:
        offset = 0
        for i in range(len(morphologicallyUniqueWordsList)):
            if len(uniqueWord) > 3:
                if (morphologicallyUniqueWordsList[i - offset][:len(uniqueWord)] == uniqueWord and 
                    morphologicallyUniqueWordsList[i - offset] != uniqueWord):
                    del morphologicallyUniqueWordsList[i - offset]
                    offset += 1
                else:
                    pass
            else:
                pass

    for uniqueWord in uniqueWords:
        for morphologicallyUniqueWord in morphologicallyUniqueWordsList:
            if len(morphologicallyUniqueWord) > 3 and uniqueWord[:len(morphologicallyUniqueWord)] == morphologicallyUniqueWord:
                print(f"{uniqueWord}:{morphologicallyUniqueWord}")
                break

    wordsCount = Counter(wordsList)







