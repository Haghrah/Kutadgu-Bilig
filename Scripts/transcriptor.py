import csv
import re

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

def roman2Arabic(roman: str) -> int:
    roman_values = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100,
        'D': 500, 'M': 1000
    }
    total = 0
    prev_value = 0
    for char in reversed(roman):  # Process from right to left
        value = roman_values[char]
        if value < prev_value:
            total -= value  # Subtractive notation (e.g., IV = 4)
        else:
            total += value
        prev_value = value
    return str(total)

def removeHindiNumbers(text):
    pattern = r"(?<!بیت )[۱۲۳۴۵۶۷۸۹۰]{4}\."
    return re.sub(pattern, "", text)

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
beytIndex = 0.
for i, line in enumerate(kutadguLa):
    if line == "_" * 48:
        continue
    # A line with only digits
    if re.search(r"^\d+$", line):
        continue
    # A line with only Roman numbers
    if re.fullmatch(r"\bM{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,4})(IX|IV|V?I{0,3})\b", line.upper()):
        arNumber = roman2Arabic(line.upper())
        lineAr = ""
        for character in arNumber:
            lineAr += digits[character]
        kutadguAr.append(lineAr)
        continue
    lineAr = ""
    for token in line.split():
        if token in la2ArDict:
            lineAr += la2ArDict[token] + " "
        elif isNumeric(token):
            for character in token:
                if character == ".":
                    lineAr += "."
                else:
                    lineAr+= digits[character]
        else:
            lineAr += token + " "
            print(token)
    if lineAr != "":
        kutadguAr.append(removeHindiNumbers(lineAr))

kutadguArTmp = []
for i, line in enumerate(kutadguAr):
    if line[:3] == "بیت":
        kutadguArTmp.append("")
    elif re.fullmatch(r"باب [۱۲۳۴۵۶۷۸۹۰]{4}\.", line):
        kutadguArTmp.append("")
    kutadguArTmp.append(line)

offset = 0
for i in range(len(kutadguArTmp)-3):
    index = i + offset
    line = kutadguArTmp[index]
    if line[:3] == "بیت" and kutadguArTmp[index + 3] != "":
        kutadguArTmp.insert(index + 3, "")
        offset += 1


kutadguAr = kutadguArTmp[:]

kutadguArFile = open("../Text/rawFinal.txt", "w")
kutadguArFile.write("\n".join(kutadguAr))
kutadguArFile.close()
