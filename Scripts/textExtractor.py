import pymupdf

charSet = []
separator = "\n________________________________________________\n"

digits = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

la2arDictInitial = {" ":" ", "\n":"\n", "y":"ی", "û":"او", "s":"س", "u":"او", "f":"ف", 
                    "h":"ه", "â":"آ", "c":"ج", "i":"ای", "̇":"̇", "b":"ب", "k":"ک", "q":"ق", 
                    "t":"ت", "a":"آ", "d":"د", "ğ":"غ", "l":"ل", "g":"گ", "m":"م", 
                    "e":"ائ", "n":"ن", "z":"ز", "ı":"اې", "r":"ر", "ç":"چ", "1":"۱", 
                    "©":"©", ".":".", "ü":"اۆ", "v":"و", "p":"پ", "3":"۳", "7":"۷", 
                    "4":"۴", "2":"۲", "0":"۰", "9":"۹", "8":"۸", "-":"-", "5":"۵", 
                    "w":"و", "o":"اۏ", ":":":", "@":"@", "’":"’", "ö":"اؤ", "ş":"ش", 
                    "(":"(", "6":"۶", ")":")", "‘":"‘", "î":"ای", "[":"[", "]":"]", 
                    "?":"؟", "~":"~", ",":"،", "ñ":"ڭ", "é":"ای", ";":"؛", "ˆ":"ˆ", 
                    "<":">", ">":"<", "j":"ژ", "ô":"اۏ", "x":"خ", "/":"/", "!":"!", }

la2arDictMiddle  = {" ":" ", "\n":"\n", "y":"ی", "û":"و", "s":"س", "u":"و", "f":"ف", 
                    "h":"ه", "â":"ا", "c":"ج", "i":"ی", "̇":"̇", "b":"ب", "k":"ک", "q":"ق", 
                    "t":"ت", "a":"ا", "d":"د", "ğ":"غ", "l":"ل", "g":"گ", "m":"م", 
                    "e":"ئ", "n":"ن", "z":"ز", "ı":"ې", "r":"ر", "ç":"چ", "1":"۱", 
                    "©":"©", ".":".", "ü":"ۆ", "v":"و", "p":"پ", "3":"۳", "7":"۷", 
                    "4":"۴", "2":"۲", "0":"۰", "9":"۹", "8":"۸", "-":"-", "5":"۵", 
                    "w":"و", "o":"ۏ", ":":":", "@":"@", "’":"’", "ö":"ؤ", "ş":"ش", 
                    "(":"(", "6":"۶", ")":")", "‘":"‘", "î":"ی", "[":"[", "]":"]", 
                    "?":"؟", "~":"~", ",":"،", "ñ":"ڭ", "é":"ی", ";":"؛", "ˆ":"ˆ", 
                    "<":">", ">":"<", "j":"ژ", "ô":"ۏ", "x":"خ", "/":"/", "!":"!", }

la2arDictFinal   = {" ":" ", "\n":"\n", "y":"ی", "û":"و", "s":"س", "u":"و", "f":"ف", 
                    "h":"ه", "â":"ا", "c":"ج", "i":"ی", "̇":"̇", "b":"ب", "k":"ک", "q":"ق", 
                    "t":"ت", "a":"ا", "d":"د", "ğ":"غ", "l":"ل", "g":"گ", "m":"م", 
                    "e":"ئ", "n":"ن", "z":"ز", "ı":"ې", "r":"ر", "ç":"چ", "1":"۱", 
                    "©":"©", ".":".", "ü":"ۆ", "v":"و", "p":"پ", "3":"۳", "7":"۷", 
                    "4":"۴", "2":"۲", "0":"۰", "9":"۹", "8":"۸", "-":"-", "5":"۵", 
                    "w":"و", "o":"ۏ", ":":":", "@":"@", "’":"’", "ö":"ؤ", "ş":"ش", 
                    "(":"(", "6":"۶", ")":")", "‘":"‘", "î":"ی", "[":"[", "]":"]", 
                    "?":"؟", "~":"~", ",":"،", "ñ":"ڭ", "é":"ی", ";":"؛", "ˆ":"ˆ", 
                    "<":">", ">":"<", "j":"ژ", "ô":"ۏ", "x":"خ", "/":"/", "!":"!", }

def K2Q(token : str):
    for vowel in ["o", "u", "a", "ı", ]:
        if vowel in token:
            return token.replace("k", "q")
    return token

def G2Q(token : str):
    for vowel in ["o", "u", "a", "ı", ]:
        if vowel in token:
            return token.replace("g", "q")
    return token

def rawLa2Ar(token):
    token = G2Q(K2Q(token))
    o = ""
    L = len(token)
    for i, character in enumerate(token):
        if i == 0:
            o += la2arDictInitial[character]
        elif i == L:
            o += la2arDictFinal[character]
        else:
            o += la2arDictMiddle[character]
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

    def saveWordsToFile(self, filename):
        wordsFile = open(f"../Text/{filename}", "w")
        for word in self.uniqueWordsList:
            wordsFile.write(f"{word[0]}:{word[1]}:{rawLa2Ar(word[0])}\n")
        wordsFile.close()
    
    def saveEtumonsToFile(self, filename):
        etumonsFile = open(f"../Text/{filename}", "w")
        for etumon in self.etumonsSet:
            etumonsFile.write(f"{etumon}:{rawLa2Ar(etumon)}\n")
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
    wordExtractor.saveWordsToFile("Words.txt")
    wordExtractor.saveEtumonsToFile("Etumons.txt")
    
    tmp = "la2arDict = {"
    for character in charSet:
        tmp += f"\"{character}\":\"\", "
    tmp += "}"
    print(tmp)





















