

if __name__ == "__main__":
    linesList = []
    mergedFile = open("../Text/merged.txt", "r")
    uvFile = open("../Text/uv.txt", "w")
    for line in mergedFile:
        linesList.append(line)

    count = 0
    uSet = set()
    for i in range(len(linesList) // 2):
        uvFile.write(linesList[2 * i])
        if "v" not in linesList[2 * i] and "u" in linesList[2 * i]:
            uvFile.write(linesList[2 * i + 1].replace("و", "ۇ"))
        else:
            if "v" in linesList[2 * i] and "u" in linesList[2 * i]:
                for word in linesList[2 * i].split(" "):
                    if "u" in word:
                        uSet.add(word)
                count += 1
            uvFile.write(linesList[2 * i + 1])


    mergedFile.close()
    uvFile.close()

    for word in uSet: print(word)
    print(count)