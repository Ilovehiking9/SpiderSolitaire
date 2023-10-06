import numpy as np
from PIL import ImageGrab
import cv2
import pytesseract
import os
import math

#Finds Distance from (x1, y1) to (x2, y2)
def calculateDistance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)



#placeholder for an explanation for this shitty code

def filterDuplicates(inputList):
    coordinateList = inputList
    FilteredCoordinateList = []
    closeCoordinates = []

    while len(coordinateList) != 0:
        for i in range(1, len(coordinateList)):
            Distance = calculateDistance(coordinateList[0], coordinateList[i])
            
            if Distance <= 3:
                closeCoordinates.append(coordinateList[i])

        for i in closeCoordinates:
            coordinateList.remove(i)

        FilteredCoordinateList.append(coordinateList.pop(0))
        closeCoordinates.clear()

    return FilteredCoordinateList

#sorry for the poor name, but this function literally filters 6's and 9's



def TemplateMatch(templateImage, mainImage):
    # Define a threshold to consider a match
    
    

    copiedImage = mainImage.copy()
    
    threshold = 0.85

    # Perform template matching
    result = cv2.matchTemplate(copiedImage, templateImage, cv2.TM_CCOEFF_NORMED)

    # Find the location(s) where the template match exceeds the threshold
    locations = np.where(result >= threshold)

    # Draw rectangles around the matched regions on the main image
    
    Positions = []
    
    for pt in zip(*locations[::-1]):  # Reverse the coordinates

        bottom_right = (pt[0] + templateImage.shape[1], pt[1] + templateImage.shape[0])
        cv2.rectangle(copiedImage, pt, bottom_right, (0, 255, 0), 2)
        #cv2.imwrite('result.png', copiedImage)


        Positions.append(pt)

        

    return Positions

CardsFolder = r'C:\Users\Nathan\Documents\ProgrammingProjects\Python\SpiderSolitaire\Cards'

PILimg = ImageGrab.grab()
PILimg.save("bufferImg.png")
mainImage = cv2.imread('bufferImg.png')

for filename in os.listdir(CardsFolder):
    templateImage = cv2.imread(f"Cards\\{filename}")

    coordinateList = filterDuplicates(TemplateMatch(templateImage, mainImage))
    
    print(f"{filename} : {coordinateList}")

