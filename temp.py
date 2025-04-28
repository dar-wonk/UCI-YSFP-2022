import lfdfiles as lfd
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import filedialog
import time
import ntpath as nt
import statistics as stat
    
#store intensity as list
def getIntensity():
    for y in range(intensityArray.shape[0]):
        for x in range(intensityArray.shape[1]):
            intensity.append(intensityArray[x,y])
#statistics of intensity
##mean
def mean(intensity):
    global avg
    avg = sum(intensity)/len(intensity)
    avg = round(avg, 2)
    
##median
def middle(intensity):
    global median
    intensity.sort()
    if (len(intensity) % 2 != 0):
        middleIndex = int((len(intensity) - 1) /2)
    else:
        middleIndex = int(len(intensity) / 2)
    median = intensity[middleIndex]
#1st quartile of set of intensities
def quartile(intensity):
    global quart
    #turns intensity list into a set
    intensitySet = [*set(intensity)]
    #finds 1st quartile by finding median and subtracting by half
    if (len(intensitySet) % 2 != 0):
        setMedianIndex = int((len(intensitySet) + 1)/2)
    else:
        setMedianIndex = int(len(intensitySet)/2)
    quartIndex = setMedianIndex - int((setMedianIndex)/2)
    quart = intensitySet[quartIndex]
    
                
                
def toList():
    #iterates through array, doenst matter which as long as its the image shape    
    for i in range(len(sortedIntensityPos)):
        x,y = sortedIntensityPos[i].split(',')
        x = int(x)
        y = int(y)
        if intensityArray[x,y] > quart:
            #basically gets rid of the lowest 25% intensity pixels using quartile
            #and adds the phase and modulation values of each to a list
            modList.append(newModArray[x,y])
            radians = newPhaseArray[x,y]*np.pi/180
            phaseList.append(radians)
            phaseList2.append(radians)
            intensityList.append(newIntensityArray[x,y])
    
            
#histogram of tweaked (and default) images
def getHistogram(img1,intensityArray):
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(1,3,1)
    ax1.set_title('Default Image')
    ax1.set_xlabel('Intensity')
    ax1.set_ylabel('Pixel Count')
    ax1.hist(img1.flat, bins = 100, range = (0,255))
    
    ax2 = fig1.add_subplot(1,3,3)
    ax2.set_title('Processed Image')
    ax2.set_xlabel('Intensity')
    ax2.set_ylabel('Pixel Count')
    ax2.hist(intensityArray.flat, bins = 100, range = (0,255))
    plt.show()



def ebutton():
    #use cv2 library to mimic ebutton from SimFCS with a kernal size of 3x3
    global newIntensityArray
    global newPhaseArray
    global newModArray
    newIntensityArray = cv.blur(intensityArray,(3,3))
    newPhaseArray = cv.blur(phaseArray,(3,3))
    newModArray = cv.blur(modArray,(3,3))


def getAngle():
    global avgAngle
    #adds to avgAngle dictionary  using the tail (filename) as a key 
    #and average angle per image as a value
    avgAngle[tail] = (sum(phaseList2)/len(phaseList2))
    

def toDict():
    global sortedIntensityList
    global sortedIntensityPos
    #initialize dict of intensities
    intensityDict = {}
    for y in range(intensityArray.shape[0]):
        for x in range(intensityArray.shape[1]):
            #iterate through intensity, and then store the position as a string
            #with the value as its intensity
            position = str(x) + ',' + str(y)
            intensityDict[position] = intensityArray[x,y]
    #sorts the values in ascending order
    sortedIntensityList = sorted(intensityDict.items(), key = lambda x: x[1])      
    for i in sortedIntensityList:
        #stores the keys in a string list
        sortedIntensityPos.append(i[0])
        
        
def getPhasor(modList,phaseList):
    #labeling names on each image 
#    head, tail = nt.split(fileName)
#    annotation = tail[:2] + ',' + tail[-20:-16]
#    labelIndex = (len(intensityList) - 2)
#    labelPosTheta = phaseList[labelIndex]
#    labelPosR = modList[labelIndex]
#    ax.annotate(annotation,
#                (labelPosTheta, labelPosR),
#                size=1,)
#                arrowprops=dict(facecolor='black', width = .01))    
    
    modList.append(0)
    phaseList.append(0)
    #this line is because of the colorspace i use, as it is based on the max value
    #since it will make the highest intensity dark red if i dont have this
    intensityList.append((max(intensityList) + 4))
    r = modList
    theta = phaseList

    colors = intensityList
    ax.scatter(theta,
                       r,
                       c = colors,
                       s = .15,
                       linewidths = 0,
                       cmap = 'jet',
                       marker = ','
                        ) 

    plt.savefig("cool.png",bbox_inches='tight',dpi=1000)

def barPlot():
#***names and such only work if starts with something like “W1” 
    fig2, ax = plt.subplots()
    xPos = wellNameList
    ax.bar(xPos, wellMean, align='center', ecolor='black', capsize=10)
    ax.set_ylabel('Angle (radians)')
    ax.set_xticks(xPos)
    ax.set_xticklabels(wellNameList)
    ax.set_title('Average Phase Angle per Well')
    ax.yaxis.grid(True)
    yMax = max(wellMean) + .1
    yMin = min(wellMean) - .1
    plt.ylim(yMin,yMax)

    plt.tight_layout()
    plt.savefig('newcool', dpi = 1000)
    
    
def stats():
    #initialzing a list for each well
    W1 = []
    W2 = []
    W3 = []
    W4 = []
    W5 = []
    W6 = []
    W7 = []
    W8 = []
    wellList2 = []

    for key in avgAngle:
        roundedAngle = round(avgAngle[key], 2)
        #the stuff you see with the key just means that it grabs certain letters
        #so it only works with the ones taken on 7/13 
        print((key[:2] + ',' + key[-20:-16]),' Average Angle: ', roundedAngle)
        argument = key[:2]
        #pretend its a switch statement
        if argument == 'W1':
            W1.append(avgAngle[key])
        elif argument == 'W2':
            W2.append(avgAngle[key])
        elif argument == 'W3':
            W3.append(avgAngle[key])
        elif argument == 'W4':
            W4.append(avgAngle[key])
        elif argument == 'W5':
            W5.append(avgAngle[key])
        elif argument == 'W6':
            W6.append(avgAngle[key])
        elif argument == 'W7':
            W7.append(avgAngle[key])
        elif argument == 'W8':
            W8.append(avgAngle[key])
        
        
#store data per well to get avg and stdev per well        
    wellList2.extend((W1,W2,W3,W4,W5,W6,W7,W8))
    for i in range(len(wellList2)):
        #only adds each well if it is detected in wellList2
        if len(wellList2[i]) > 1:
            wellList.append(wellList2[i])
    for i in range(len(wellList)):
        #adds to mean, stdev, and name lists as long as there is more than one list
        #and that list has something in it
        if sum(wellList[i]) != 0 and len(wellList[i]) > 1:
            name = wellNameList[i]
            avg = sum(wellList[i])/len(wellList[i])
            avg = round(avg, 4)
            stdev = stat.stdev(wellList[i])
            stdev = round(stdev,4)
            print(name + " average is: " + str(avg) + "; Standard deviation is: " + str(stdev))
            wellMean.append(avg)
            wellStdev.append(stdev)
            wellName.append(name)
        
#timer to see how long it runs (irrelevant)
start_time = time.time()

#file open prompt
root = tk.Tk()
root.withdraw()
filePaths = filedialog.askopenfilenames()

#phasor plot initialization
fig1 = plt.figure()
ax = fig1.add_subplot(projection ='polar')
#next 7 lines changes the shape of the plot and sets the xticks as radians
ax.set_yticklabels([])
ax.set_xticks(np.arange(1.9,2.5,.1))
ax.set_thetamin(1.8 * 180 / np.pi)
ax.set_thetamax(2.6 * 180 / np.pi)
anglePos = ax.get_xticks()
anglePos = [round(label,3) for label in anglePos]
ax.set_xticklabels(anglePos)

#initialize global lists and such
wellMean = []
wellStdev = []
wellName = []    
wellList = []       
wellNameList = []
avgAngle = {}
for fileName in filePaths:
    
    #open image
    img = lfd.SimfcsR64(fileName)
    img1 = lfd.SimfcsR64.asarray(img)
    imgArray1 = lfd.SimfcsR64.asarray(img)   
     
    #gets the name of the image in tail, not the whole directory 
    head, tail = nt.split(fileName)
    wellName.append(tail[:2])
    
    #initialize variables to each image
    avg = 0
    median = 0
    quart = 0
    intensity = []
    phaseList2 = []

    phaseArray = img1[1,:,:]
    modArray = img1[2,:,:]
    intensityArray = img1[0,:,:]
    newIntensityArray = []
    newPhaseArray = []
    newModArray = []
    
    modList = []
    phaseList = []  
    intensityList = []
    sortedIntensityList = []
    sortedIntensityPos = []
    
    avgList = []
        
    getIntensity()  
    mean(intensity)
    middle(intensity)
    quartile(intensity)
    ebutton()
    toDict()
    toList()
    getAngle()
    getPhasor(modList,phaseList)
    
