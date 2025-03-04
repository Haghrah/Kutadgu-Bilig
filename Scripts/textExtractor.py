import pymupdf

charSet = []
separator = "\n________________________________________________\n"

digits = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

la2arDict = {" ":"", "\n":"", "y":"", "û":"", "s":"", "u":"", "f":"", 
             "h":"", "â":"", "c":"", "i":"", "̇":"", "b":"", "k":"", 
             "t":"", "a":"", "d":"", "ğ":"", "l":"", "g":"", "m":"", 
             "e":"", "n":"", "z":"", "ı":"", "r":"", "ç":"", "1":"", 
             "©":"", ".":"", "ü":"", "v":"", "p":"", "3":"", "7":"", 
             "4":"", "2":"", "0":"", "9":"", "8":"", "-":"", "5":"", 
             "w":"", "o":"", ":":"", "@":"", "’":"", "ö":"", "ş":"", 
             "(":"", "6":"", ")":"", "‘":"", "î":"", "[":"", "]":"", 
             "?":"", "~":"", ",":"", "ñ":"", "é":"", ";":"", "ˆ":"", 
             "<":"", ">":"", "j":"", "ô":"", "x":"", "/":"", "!":"", }

def rawLa2Ar(token):
    o = ""
    
    return o

def filterWords(word):
    for character in word:
        if character in digits:
            return False
    return True

class WordExtractor:

    suffixes = ["lar", "ler", 
                "sız", "suz", "siz", "süz", 
                "sa", "se", 
                "mış", "muş", "miş", "müş", 
                "lığ", "lık", "luğ", "luk", "lig", "lik", "lüg", "lük", 
                "lı", "lu", "li", "lü", 
                "ıp", "up", "ip", "üp", 
                "ma", "me", 
                "ke", "ka", 
                "dın", "din", "tın", "tin", 
                "da", "de", "ta", "te", 
                "nı", "nu", "ni", "nü", 
                "maz", "mez", 
                "mağ", "mak", "meg", "mek", 
                "ığ", "uğ", "ig", "üg", 
                "ğı", "ğu", "gi", "gü", 
                "la", "le", 
                "lan", "len", 
                "çı", "çu", "çi", "çü", 
                "ğınça", "ğunça", "ginçe", "günçe", 
                "ğısı", "ğusı", "gisi", "güsi", 
                "dım", "dum", "dim", "düm", 
                "dıñ", "duñ", "diñ", "düñ", 
                "dı", "du", "di", "dü", 
                "dık", "duk", "dik", "dük", 
                "dıñız", "duñuz", "diñiz", "düñüz", 
                "dılar", "dular", "diler", "düler", 
                "tı", "tu", "ti", "tü", 
                "ça", "çe", 
                "yın", "yin", 
                "dır", "dur", "dir", "dür", 
                "tır", "tur", "tir", "tür", 
                "ğıl", "gil", ]
    reversedSuffixes = []

    def __init__(self, ):
        self.uniqueWordsDict = {}
        for suffix in self.suffixes:
            self.reversedSuffixes.append(suffix[::-1])
    
    def etymonize(self, word):
        minEtumonLen = 3
        if len(word) <= minEtumonLen:
            return word
        else:
            word = word[::-1]
            index = 0
            for i in range(len(word) - minEtumonLen + 1):
                if word[:i] in self.reversedSuffixes:
                    index = i
            
            if index > 0:
                word = word[index:]
                return self.etymonize(word[::-1])
            else:
                return word[::-1]

    @property
    def etumonsSet(self):
        etumons = set()
        for word in self.uniqueWordsList:
            etumon = self.etymonize(word[0])
            etumons.add(etumon)
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
    
    tmp = "la2arDict = {"
    for character in charSet:
        tmp += f"\"{character}\":\"\", "
    tmp += "}"
    print(tmp)





















