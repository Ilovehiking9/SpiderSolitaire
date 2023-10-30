import time

print("yowuch")
inputList = [1, 1, 2, 9, 9, 12, 19, 188]




def groupNumbers(inputList, rangeLimit = 5):
    outputList = []
    currentGroup = [inputList[0]]

    for i in range(1, len(inputList)):
        if abs(inputList[i] - currentGroup[-1]) <= rangeLimit:
            currentGroup.append(inputList[i])
        else:
            outputList.append(currentGroup)
            currentGroup = [inputList[i]]

    outputList.append(currentGroup)  # Add the last group
    return outputList

print(groupNumbers(inputList))


