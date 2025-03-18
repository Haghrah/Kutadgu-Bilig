import csv

digits = {"1":"۱", 
          "2":"۲", 
          "3":"۳", 
          "4":"۴", 
          "5":"۵", 
          "6":"۶", 
          "7":"۷", 
          "8":"۸", 
          "9":"۹", 
          "0":"۰", }

def isNumeric(token):
    for character in token:
        if (not character in digits) and (character != "."):
            return False
    return True

kutadguLa = []
kutadguLaFile = open("../Text/rawLa.txt", "r")
for line in kutadguLaFile:
    kutadguLa.append(line.strip())
kutadguLaFile.close()

la2ArDict = {}

with open("../Text/supervisedWords.csv", newline='', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        la2ArDict[row[0]] = row[2]

kutadguAr = []
for line in kutadguLa:
    lineAr = ""
    for token in line.split():
        if token in la2ArDict:
            lineAr += la2ArDict[token] + " "
        elif isNumeric(token):
            lineAr += "\n"
            for character in token:
                if character == ".":
                    lineAr += "."
                else:
                    lineAr+= digits[character]
        elif token == "_" * 48:
            lineAr += token
        else:
            lineAr += token + " "
            print(token)
    kutadguAr.append(lineAr)

kutadguArFile = open("../Text/rawFinal.txt", "w")
kutadguArFile.write("\n".join(kutadguAr))
kutadguArFile.close()
