import re

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


if __name__ == "__main__":
    rawAr = []
    rawArFile = open("../Text/rawAr.txt", "r")
    for line in rawArFile:
        line = line.strip()
        if len(line) != 0:
            rawAr.append(line.strip())
    rawArFile.close()

    rawLa = []
    rawLaFile = open("../Text/rawLa.txt")
    for line in rawLaFile:
        rawLa.append(line.strip())
    rawLaFile.close()

    offset = 0
    for i in range(len(rawLa)):
        if rawLa[i - offset] == "_" * 48:
            del rawLa[i + 1 - offset]
            del rawLa[i - offset]
            offset += 2
        elif len(rawLa[i - offset]) == 0:
            del rawLa[i - offset]
            offset += 1
        elif re.fullmatch(r"^[\d]+$", rawLa[i - offset]):
            del rawLa[i - offset]
            offset += 1
        elif re.fullmatch(r"\bM{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,4})(IX|IV|V?I{0,3})\b", rawLa[i - offset].upper()):
            arNumber = roman2Arabic(rawLa[i - offset].upper())
            rawLa[i - offset] = str(arNumber)
    

    mergedFile = open("../Text/merged.txt", "w")
    for arLine, laLine in zip(rawAr, rawLa):
        mergedFile.write(laLine + "\n")
        mergedFile.write(arLine + "\n")
    mergedFile.close()












