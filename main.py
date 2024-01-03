import numpy as np
from PIL import ImageGrab
import cv2
import os
import math
import time
import re
from pprint import pprint
import copy

# Finds Distance from (x1, y1) to (x2, y2)
def calculateDistance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# placeholder for an explanation for this shitty code

def filterDuplicates(inputList):
    coordinateList = inputList
    FilteredCoordinateList = []
    closeCoordinates = []

    while len(coordinateList) != 0:
        for i in range(1, len(coordinateList)):
            distance = calculateDistance(coordinateList[0], coordinateList[i])

            if distance <= 3:
                closeCoordinates.append(coordinateList[i])

        for i in closeCoordinates:
            coordinateList.remove(i)

        FilteredCoordinateList.append(coordinateList.pop(0))
        closeCoordinates.clear()

    return FilteredCoordinateList


def TemplateMatch(templateImage, mainImage, threshold=.93):
    # Define a threshold to consider a match

    copiedImage = mainImage.copy()

    # Perform template matching
    result = cv2.matchTemplate(copiedImage, templateImage, cv2.TM_CCOEFF_NORMED)

    # Find the location(s) where the template match exceeds the threshold
    locations = np.where(result >= threshold)

    # Draw rectangles around the matched regions on the main image

    Positions = []

    for pt in zip(*locations[::-1]):  # Reverse the coordinates

        bottom_right = (pt[0] + templateImage.shape[1], pt[1] + templateImage.shape[0])
        cv2.rectangle(copiedImage, pt, bottom_right, (0, 255, 0), 2)
        cv2.imwrite('result.png', copiedImage)

        Positions.append(pt)

    return Positions


def groupCoordinatesIntoStacks(inputList, rangeLimit=5):
    outputList = []
    try:
        currentGroup = [inputList[0]]
    except IndexError:
        print("try opening your spider solitaire game you goof.")
        print("https://www.spider-solitaire-game.com/")
        return outputList

    for i in range(1, len(inputList)):
        if abs(inputList[i]["position"][0] - currentGroup[0]["position"][0]) <= rangeLimit:
            currentGroup.append(inputList[i])
        else:
            outputList.append(currentGroup)
            currentGroup = [inputList[i]]

    outputList.append(currentGroup)  # Add the last group
    return outputList


def splitString(input_string):
    # Define a regular expression pattern to match the number and letter
    pattern = re.compile(r'(?P<number>\d+)(?P<letter>[a-zA-Z])')

    # Use the pattern to search for matches in the input string
    match = pattern.match(input_string)

    # Check if a match is found
    if match:
        # Extract the matched groups and convert the number to an integer
        result = {
            "number": int(match.group('number')),
            "color": match.group('letter')
        }
        return result
    else:
        # If no match is found, return None or handle as needed
        return None


if __name__ == "__main__":

    time.sleep(1)

    primaryCardList = []

    xCoordinateList = []

    CardsFolder = r'C:\Users\Nathan\Documents\ProgrammingProjects\Python\SpiderSolitaire\Cards'

    PILimg = ImageGrab.grab()
    PILimg.save("bufferImg.png")
    mainImage = cv2.imread('bufferImg.png')

    print("Captured...")

    for filename in os.listdir(CardsFolder):
        print(f"Processing {filename}")
        templateImage = cv2.imread(f"Cards\\{filename}")
        thresholds = {"1b.png": 0.92,
                      "2b.png": 0.93,
                      "3b.png": 0.93,
                      "4b.png": 0.93,
                      "5b.png": 0.93,
                      "6b.png": 0.94,
                      "7b.png": 0.93,
                      "8b.png": 0.945,
                      "9b.png": 0.93,
                      "10b.png": 0.92,
                      "11b.png": 0.93,
                      "12b.png": 0.93,
                      "13b.png": 0.93,
                      "1r.png": 0.92,
                      "2r.png": 0.93,
                      "3r.png": 0.93,
                      "4r.png": 0.93,
                      "5r.png": 0.94,
                      "6r.png": 0.945,
                      "7r.png": 0.93,
                      "8r.png": 0.945,
                      "9r.png": 0.96,
                      "10r.png": 0.92,
                      "11r.png": 0.91,
                      "12r.png": 0.92,
                      "13r.png": 0.93,
                      "empty.png": 0.93}
        coordinateList = filterDuplicates(TemplateMatch(templateImage, mainImage, threshold=thresholds[filename]))

        for coordinate in coordinateList:
            primaryCardList.append(dict(cardID=filename.replace(".png", ""), position=coordinate))

    print("Processing...")

    # sort cards by x-coordinate

    sortedCards = sorted(primaryCardList, key=lambda x: x['position'][0])

    print("Sorting...")

    GameList = groupCoordinatesIntoStacks(sortedCards)

    # sort cards by y-coordinate per stack

    tempList = []

    for stack in GameList:
        sortedStack = sorted(stack, key=lambda y: y["position"][1])
        tempList.append(sortedStack)

    GameList = tempList

    for stack in GameList:
        for card in stack:
            splitCardName = splitString(card["cardID"])
            if card["cardID"] != "empty":
                del (card["cardID"])
                try:
                    card["number"] = splitCardName["number"]
                    card["color"] = splitCardName["color"]
                except TypeError:
                    continue
            else:
                del (card["cardID"])
                card["number"] = "empty"
                card["color"] = "empty"

# adds stack label to cards

for index, stack in enumerate(GameList):
    for card in stack:
        card["stack"] = index


class gameProcessing:
    def __init__(self, game):
        self.game = game

    def getAllMoveableCards(self):
        # I don't remember how I did this
        allMoveableCards = []
        nextCard = None
        for stack in self.game:
            for index, card in enumerate(stack):

                try:
                    nextCard = stack[index + 1]
                except IndexError:
                    allMoveableCards.append(card)
                    continue
                if card["color"] == nextCard["color"]:
                    try:
                        if card["number"] == nextCard["number"] + 1:
                            allMoveableCards.append(card)
                    except TypeError:
                        continue

        return (allMoveableCards)

    def getAllCardMovements(self):

        moveableCards = gameProcessing(self.game).getAllMoveableCards()

        # make a list of last cards in each stack
        lastCards = []

        for stack in self.game:
            lastCards.append(stack[len(stack) - 1])

        allCardMovements = []

        for card in moveableCards:
            for destination in lastCards:
                if card["number"] == destination["number"] - 1:
                    allCardMovements.append([card, destination])

        return allCardMovements

    def getDraggedStack(self, cardMovement):

        movingCard = cardMovement[0]
        cardStack = movingCard["stack"]
        gameStack = self.game[cardStack]

        draggedStack = gameStack[gameStack.index(movingCard):]

        return draggedStack

    def simulateGame(self, cardMovement):
        simulatedGame = copy.deepcopy(self.game)


        draggedStack = gameProcessing(simulatedGame).getDraggedStack(cardMovement)
        destination = simulatedGame[cardMovement[1]["stack"]]
        origin = simulatedGame[cardMovement[0]["stack"]]
        for card in draggedStack:
            destination.append(card)

        for card in draggedStack:
            origin.remove(card)
        return simulatedGame


if __name__ == "__main__":

    allCardMovements = gameProcessing(GameList).getAllCardMovements()

    for i in allCardMovements:
        pprint(gameProcessing(GameList).simulateGame(i))
        pprint(f"\nmovement: {i}")

'''
shit to do:
3. simulate the game
4. Figure out what the best move is (Our green earth is now red)
5. Move the card (we're nearing the end, yay!)
6. repeat. (in a loop ofc, so very easy)
'''
