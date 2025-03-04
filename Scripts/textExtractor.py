import pymupdf

charSet = []
separator = "\n________________________________________________\n"

digits = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

def filterWords(word):
    for character in word:
        if character in digits:
            return False
    return True

class WordExtractor:

    suffixes = ["lar", 
                "ler", 
                "sız", 
                "suz", 
                "siz", 
                "süz", 
                "sa", 
                "se", 
                "mış", 
                "muş", 
                "miş", 
                "müş", 
                "ke", 
                "din", 
                "de", 
                "ni", 
                "lig", 
                "ig", 
                "li", ]
    reversedSuffixes = []

    def __init__(self, ):
        self.uniqueWordsDict = {}
        for suffix in self.suffixes:
            self.reversedSuffixes.append(suffix[::-1])
    
    def etymonize(self, word):
        minRootLen = 4
        if len(word) <= minRootLen:
            return word
        else:
            word = word[::-1]
            while len(word) >= minRootLen:
                for i in range(len(word) - minRootLen):
                    if word[:i] in self.reversedSuffixes:
                        word = word[i:]
                        break
                if i == len(word) - minRootLen - 1:
                    break
            word = word[::-1]
            return word

    @property
    def etumonsSet(self):
        etumons = set()
        for word in self.uniqueWordsList:
            etumons.add(self.etymonize(word[0]))
        return etumons

    @property
    def uniqueWordsList(self):
        wordsList = [[word, self.uniqueWordsDict[word]] 
                     for word in self.uniqueWordsDict.keys()]
        wordsList = sorted(wordsList, key=lambda word:word[1], reverse=True)
        return wordsList

    def analyzePage(self, pageLines):
        for line in pageLines:
            for word in line.split():
                if filterWords(word):
                    if word in self.uniqueWordsDict.keys():
                        self.uniqueWordsDict[word] += 1
                    else:
                        self.uniqueWordsDict[word]  = 1

    def saveToFile(self, filename):
        wordsFile = open(f"../Text/{filename}", "w")
        for word in self.uniqueWordsList:
            wordsFile.write(f"{word[0]}:{word[1]}\n")
        wordsFile.close()
    
    def saveEtumonsToFile(self, filename):
        etumonsFile = open(f"../Text/{filename}", "w")
        for etumon in self.etumonsSet:
            etumonsFile.write(f"{etumon}\n")
        etumonsFile.close()

def normalizeText(text : str):
    normalized = []
    for line in text.split("\n"):
        line = line[:-1].strip()
        if line:
            normalized.append(line)
    return normalized

if __name__ == "__main__":
    doc = pymupdf.open("../Pdf/kutadgu_bilig_raw.pdf")
    outFile = open("../Text/kutadgu_bilig.txt", "w")

    wordExtractor = WordExtractor()

    for page in doc:
        pageText = page.get_text().lower()
        pageLines = normalizeText(pageText)
        outFile.write("\n".join(pageLines) + separator)

        wordExtractor.analyzePage(pageLines)

        for character in pageText:
            if not character in charSet:
                charSet.append(character)

    outFile.close()
    wordExtractor.saveToFile("Words.txt")
    wordExtractor.saveEtumonsToFile("Etumons.txt")
