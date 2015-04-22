import math
import numpy as np
import random
from math import sqrt

_iterations = 200000 # N maximum number of iterations allowed in algorithm
_samplesCount = 10 # S samples count
_minDistance = 0.05 # X minimum distance between model and data point
_ratio = 8 # C number of data vals required to assert that a model fits well to data
_minDegrees = 40 # D degrees beetween random point

def findLineModel(firstPoint, secondPoint):
    checkForZero = secondPoint.x - firstPoint.x
    if checkForZero == 0.0:
        checkForZero = checkForZero + 0.001
    b = (secondPoint.y - firstPoint.y) / checkForZero
    c = secondPoint.y - b * secondPoint.x
 
    return b, c

def findInterceptPoint(b, c, point):
    x = (point.x + b * point.y - b * c) / (1 + math.pow(b, 2))
    y = (b * point.x + math.pow(b, 2) * point.y - math.pow(b, 2) * c) / (1 + math.pow(b, 2)) + c
 
    return x, y

def anyPointsLeft(data):
    return len(data) > 0

def degToRad(degrees):
    return degrees * math.pi / 180

def getRandomSamples(data, middle, angle, count):
    sublist = data[int(middle.num - angle) : int(middle.num + angle)]
    if count > len(sublist):
        count = len(sublist)
    randlist = random.sample(sublist, count)
    return randlist

def calculateDistance(point, k, m):
    A = abs(1 / k)
    B = 0
    if k > 0:
        B = -1
    else:
        B = 1
        
    C = -A * m * B;
    distance = abs(A * point.x + B * point.y + C) / sqrt(pow(A, 2) + pow(B, 2))
    return distance

def ransac(data):
    iterations = 0
    indices = {}
    for dataPoint in data:
        indices[dataPoint.num] = dataPoint
    lines = []
    
    while (len(indices) and _iterations > iterations):
        iterations = iterations + 1
        
        randomSample = random.sample(list(indices), 1)
        dictlist = []
        for key in indices.keys():
            dictlist.append(indices[key])
    
        samples = getRandomSamples(dictlist, indices[randomSample[0]], _minDegrees, _samplesCount)
        
        if len(samples) > 2:
            xData = []
            yData = []
            for point in samples:
                xData.append(point.x)
                yData.append(point.y)
                
            p = np.polyfit(xData, yData, 1)
            correctPoints = []
            correctSamplesCounter = 0
            for point in samples:
                if calculateDistance(point, p[0], p[1]) < _minDistance:
                    correctSamplesCounter = correctSamplesCounter + 1
                    correctPoints.append(point)
                    
            if correctSamplesCounter > _ratio:
                xData = []
                yData = []
                for point in correctPoints:
                    xData.append(point.x)
                    yData.append(point.y)
                    del indices[point.num]
                
                p = np.polyfit(xData, yData, 1)
                polynomial = np.poly1d(p)
                ys = polynomial(xData)
                
                lines.append([xData, ys])
    return lines
            