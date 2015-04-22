import math
import numpy as np
import matplotlib.pyplot as plt
import ransac

class DataPoint(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.num = 0
        
_isDataMockuped = True
_displayOriginal = True
 
def findVertices(data):
    lastDistance = -100000 
    isRising = -1 
    isDecreasing = -1 
    vertices = []
    indices = []
    for index in range(len(data)):
        if round(data[index], 1) > lastDistance: 
            lastDistance = round(data[index], 1) 
            isRising = 1 
        elif round(data[index], 2) < lastDistance: 
            lastDistance = round(data[index], 1) 
            isDecreasing = 1 
         
        if isRising == 1 and isDecreasing == 1: 
            vertices.append(data[index])
            indices.append(index)
            isRising = -1 
            isDecreasing = -1 
    return [vertices, indices]

def getPosition(num, distance):
    degrees = degToRad(0.36) * num
    point = DataPoint()
    point.x = math.cos(degrees) * distance
    point.y = math.sin(degrees) * distance
    point.num = num
    
    return point
    

def degToRad(degrees):
    return degrees * math.pi / 180

def radToDeg(radians):
    return radians * 180 / math.pi

def convertArrayToFloats(array):
    for index in range(len(array)):
        array[index] = float(array[index])
    return

def loadData():
    if (_isDataMockuped):
        dataFile = open("../data/data.txt", "r")
        skan = dataFile.read().split(", ")
        convertArrayToFloats(skan)
    else:
        skan = 5;
        # skan = RosAriaDriver('/PIONIER4');
    
    return skan

def plotPolarCoordinates(distanceData):
    fig1 = plt.figure()

    if (_displayOriginal):
        x = np.arange(0, 512)
        theta = degToRad(0.36) * x
        
        ax1 = fig1.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
        ax1.plot(theta, distanceData, lw = 2.5)
        
    theta = [] #degToRad(0.36) * resultArray[1]  # kat w radianach
    for num in resultArray[1]:
        theta.append(degToRad(0.36) * num)
    
    ax1 = fig1.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
    ax1.set_ylim(0, 2)
    return

def plotCartesianCoordinates(distanceData):
    fig2 = plt.figure()
    counter = 0
    xData = []
    yData = []
    for distance in distanceData:
        dataPoint = getPosition(counter, distance)
        if not math.isnan(dataPoint.x) and not math.isnan(dataPoint.y) and not math.isinf(dataPoint.x) and not math.isinf(dataPoint.y):
            xData.append(dataPoint.x)
            yData.append(dataPoint.y)
            
        counter = counter + 1
    
    plt.plot(xData, yData, 'ro')
    return

def plotFoundLines(lines):
    for line in lines:
        plt.plot(line[0], line[1])
    return

# Tu podaj numer robota 
# robot=RosAriaDriver('/PIONIER4') 
 
# Wczytanie danych ze skanera 
# skan=robot.ReadLaser() 
_skan = loadData();
 
resultArray = findVertices(_skan)

plotPolarCoordinates(_skan)

plotCartesianCoordinates(_skan)

formattedData = []
counter = 0
for num in _skan:
    dataPoint = getPosition(counter, num)
    if not math.isnan(dataPoint.x) and not math.isnan(dataPoint.y) and not math.isinf(dataPoint.x) and not math.isinf(dataPoint.y):
        formattedData.append(getPosition(counter, num))
    
    counter = counter + 1

lines = ransac.ransac(formattedData)

plotFoundLines(lines)

plt.show()

