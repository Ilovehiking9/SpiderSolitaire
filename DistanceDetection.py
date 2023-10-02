import math

def calculateDistance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)







#placeholder for an explanation for this shitty code
def filterDuplicates(inputList):
    threshold = 3
    coordinateList = inputList
    FilteredCoordinateList = []
    closeCoordinates = []

    while len(coordinateList) != 0:
        for i in range(1, len(coordinateList)):
            Distance = calculateDistance(coordinateList[0], coordinateList[i])
            
            if Distance <= threshold:
                closeCoordinates.append(coordinateList[i])

        for i in closeCoordinates:
            coordinateList.remove(i)

        FilteredCoordinateList.append(coordinateList.pop(0))
        closeCoordinates.clear()
    return FilteredCoordinateList



print(filterDuplicates([(52, 314), (137, 314), (52, 315), (136, 315), 
    (137, 315), (52, 316), (137, 316), (475, 377), 
    (475, 378)]))







