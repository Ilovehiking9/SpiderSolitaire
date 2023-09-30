import numpy as np
from PIL import ImageGrab
import cv2
import pytesseract
import os

#Grab images necessary



def TemplateMatch(templateImage, mainImage):
    # Define a threshold to consider a match
    
    copiedImage = mainImage.copy()
    
    threshold = 0.8

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

CardsFolder = r'C:\Users\Nathan\Documents\ProgrammingProjects\Python\SpiderSolitaire\Cards'

PILimg = ImageGrab.grab()
PILimg.save("bufferImg.png")
mainImage = cv2.imread('bufferImg.png')

for filename in os.listdir(CardsFolder):
    templateImage = cv2.imread(f"Cards\\{filename}")
    print(TemplateMatch(templateImage, mainImage))

#issues to work on later
"""many coordinates in a concentrated area should be merged
i.e (222,222), (222,223) should be merged becasue they are similar"""