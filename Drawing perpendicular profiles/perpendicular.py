import cv2 as cv2
import matplotlib.pyplot as plt
from numpy.lib.type_check import real
from skimage.measure import profile_line
from skimage import io
# from scipy.interpolate import make_interp_spline
import numpy as np
import copy
import math
# from scipy import ndimage
# from scipy import stats
# from scipy import misc
# from skimage.morphology import skeletonize
from scipy.interpolate import interp1d

#Font for plt later 
# plt.rcParams['font.size']=16
# plt.rcParams['font.family'] = 'sans-serif'

#Read image and convert to grayscale/ binary 
img = cv2.imread(f'output\\img1.png')
height = img.shape[0]
#img = cv2.imread(r'C:\\Users\\Joanne Leow\\Desktop\\test.jpg')
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY)
cv2.imshow('binary',thresh)
cv2.waitKey(0)

#skeletonize
skeletonized = cv2.ximgproc.thinning(thresh,0)
cv2.imshow('skeletonized',skeletonized)
cv2.waitKey(0)
cv2.imwrite('img1_skel.png', skeletonized)

skeleton = cv2.imread(f'img1_skel.png')
gray_img_skel = cv2.cvtColor(skeleton, cv2.COLOR_BGR2GRAY)
ret2, skel_thresh = cv2.threshold(gray_img_skel, 0, 255, cv2.THRESH_BINARY)

skelCoord = np.nonzero(skel_thresh)
lineCoord = np.nonzero(skel_thresh)

skelCoord = np.array(skelCoord).tolist()
lineCoord = np.array(lineCoord).tolist()

count = 0

#popping out ranges that are 0 or height-1, basically lines on the wall
for i in range(len(skelCoord[1])):
    if(skelCoord[1][i] == 0 or skelCoord[0][i] == 0 or skelCoord[1][i] == height-1 or skelCoord[0][i] == height-1):
        lineCoord[0].pop(i-count)
        lineCoord[1].pop(i-count)
        count += 1

# make a combinedCoord of x,y to find out the coordinates
combinedCoord = []
intersectionCoord = []
for i in range(len(lineCoord[1])):
    # 1 is x, 0 is y
    combinedCoord.append([lineCoord[1][i],lineCoord[0][i]])

# going through the combinedCoord to find the coordinate that has intersection of more or equal than 3 
for i in range(len(combinedCoord)):
    intersectCount = 0
    for j in range(len(combinedCoord)):
        # compared the coordinates with ALL the others except its own coord
        if(i != j):
            # if x and y axis difference is 1 then it passes and increase the intersect count by 1
            if(abs(combinedCoord[j][0] - combinedCoord[i][0]) <= 1 and abs(combinedCoord[j][1] - combinedCoord[i][1]) <= 1):
                intersectCount += 1
                # if it intersects more than 3 times
                if(intersectCount >= 3):
                    intersectionCoord.append([combinedCoord[i][0],combinedCoord[i][1]])
                    break

print('what is intersectionCoord ',intersectionCoord)


# print('line coord is x is', lineCoord[1])
# print('line coord is y is', lineCoord[0])

x = np.array(lineCoord[1])
y = -np.array(lineCoord[0])
# prime_numbers.sort()

plt.plot(x,y,'.')
plt.title("")
plt.show()

# from scipy.signal import savgol_filter
# # Savitzky-Golay filter
# y_filtered = savgol_filter(y, len(x)-1, 3)
# # Plotting
# fig = plt.figure()
# ax = fig.subplots()
# plt.title("wow")
# p = ax.plot(x, y, '-*')
# p, = ax.plot(x, y_filtered, 'g')
# plt.subplots_adjust(bottom=0.25)
# plt.show()

# finding out the vessels based on distance of each coordinates

#make a copy of lineCoord
# tempCoord = [[],[]]
# for i in range(len(lineCoord[1])):
#     tempCoord[0][i] = lineCoord[0][i]
#     tempCoord[1][i] = lineCoord[1][i]

# vessels = [[]]
# vesselCount = 0
# vesselPopCount = 0
# previousNumber = {'index':0,'value':0}

# # we will break the loop when tempcoord[1] = 0, meaning everything has been popped
# while(len(tempCoord[1]) == 0):
#     for i in range(len(lineCoord[1])):
#         if(i == 0):
#             vessels[0].append((tempCoord[1][i],tempCoord[0][i]))
#             tempCoord[1].pop(i) #pop the coordinates that have been used out of the tempCoord
#             tempCoord[0].pop(i)
#             vesselPopCount += 1
#         elif():

# # first, we combine lineCoord 1 and 0 into XY array format
# print('what is linecoord ',lineCoord)



# this will initiate the array 
list = lineCoord[1] # X axis
list2 = lineCoord[0] # Y axis
contourX = []
contourY = []

# index is used to keep track which contour you were at, value is basically the value in the list
previousNumber = {'index':0,'value':0}

for i in range(len(list)):
    # if it is just initialised and i is 0, just save the token into the first array, meaning the first contour
    if(i == 0):
        contourX.append([list[i]]) # adding [list[i]], meaning you're adding a new item which is [1], an array with the value 1
        contourY.append([list2[i]]) # so you're saving an array -> [1] into the array contourX -> [[1]]
        previousNumber['index'] = 0
        previousNumber['value'] = list[i]

    # # checks if the differenc of the previous number and current is smaller than 1, if so, that means its part of the same contour
    elif(abs(list[i]-previousNumber['value']) <= 1):
        # you will then append the value into the array of the same contour
        contourX[previousNumber['index']].append(list[i])
        contourY[previousNumber['index']].append(list2[i])
        # now assign the value to previousNumber so you can use it to compare in the next for loop
        previousNumber['value'] = list[i]

    # you will come in here if the current number is not part of the same contour as the previous one
    else:
        found = False
        # loop through the contour array to find where to insert the new value, either in an existing one 
        # but a different one than your current one, or just put it into an entirely new one, meaning a new contour
        for index, contour in enumerate(contourX):
            for j in range(len(contour)):
                # loop through the entire contour to find in each contour if it has a coordinate that is next to the current one
                if(abs(list[i] - contourX[index][j]) <= 1):
                    if(abs(list2[i] - contourY[index][j]) <= 1):
                        previousNumber['index'] = index
                        previousNumber['value'] = list[i]
                        contourX[index].append(list[i])
                        contourY[index].append(list2[i])
                        found = True

                        # just checking if the last number in the contour has the diff distance of 1, if not, that means it could potentially have branched out 
                        # if(abs(list[i] - contourX[index][len(contourX[index])-1]) <= 1):
 
                # if both if loop conditions are true on the above, break out of this for loop and go back to the big one    
                if(found):
                    break    
        # if you can't find a place for your value where the previous points in the contour - current <= 1, you're a new contour
        # so just create a new one  
        if(not found):
            # cjust initiate the values in them and count it as a new contour
            previousNumber['index'] = len(contourX) # index is the len as you're appending a new array to the contour
            previousNumber['value'] = list[i]
            contourX.append([list[i]])
            contourY.append([list2[i]])
            found = True

# print('contour x is ',contourX)
# print('contour y is ',contourY)

##_________________________________________________________Drawing the coordinates on the raw graph__________________________________________________
# combining the contourX and contourY so that it'll appears the contour format
finalContour = []

# combining final contour from contour x and y
for index, contour in enumerate(contourX): 
    finalContour.append([])
    for i in range (len(contour)):
        finalContour[index].append([contourX[index][i],contourY[index][i]])
# print('what is the finalContour ',finalContour)

chosenIntersectionCoord = []
# take the coordinates inside intersection coord and compare with the start or ending points of each contour to find the point of seperation
for i in range(len(intersectionCoord)):
    for j in range(len(finalContour)):
        currentContour = finalContour[j]
        if(intersectionCoord[i] in [currentContour[0]] or intersectionCoord[i] in [currentContour[len(currentContour)-1]]):
            chosenIntersectionCoord.append(intersectionCoord[i])
            # break

print('what is chosen intersec coord ',chosenIntersectionCoord)

candidateIntersectionCoord = [[]]
addCounter = False
newCounter = 0
# now find the coordinates close to the point of seperation 
for i in range(len(chosenIntersectionCoord)):
    if(addCounter):
        candidateIntersectionCoord.append([])
        addCounter = False
        newCounter += 1
    for j in range(len(intersectionCoord)):
        if(chosenIntersectionCoord[i] != intersectionCoord[j]):
            if(abs(chosenIntersectionCoord[i][0] - intersectionCoord[j][0]) <= 1 and abs(chosenIntersectionCoord[i][1] - intersectionCoord[j][1]) <= 1):
                candidateIntersectionCoord[newCounter].append(intersectionCoord[j])
                addCounter = True

print('what is candidateIntersectionCoord ',candidateIntersectionCoord)

realIntersectionCoord = []
# after finding out the coordinates that are close to the point of seperation, get the mean of it, and that coordinate will be used to split 
# a contour up to be more accurate
for index, candidate in enumerate(candidateIntersectionCoord):
    x,y = 0,0
    for i in range(len(candidate)):
        x += candidate[i][0]
        y += candidate[i][1]
    x = math.ceil(x/len(candidate))
    y = math.ceil(y/len(candidate))
    realIntersectionCoord.append([x,y])

print('what is realIntersectionCoord ',realIntersectionCoord)

# print('what is final contour again ', len(finalContour))
# take the coordinates in realIntersectionCoord
for coord in realIntersectionCoord:
    # to go over the entire finalContour and find which contour its in
    for index, contour in enumerate(finalContour):
        found = False
        # print('what is len of finalContour ',len(finalContour))
        # and then split the contour in half where the coord is located
        for i in range(len(contour)):
            # found the position oc the coordinate
            if(coord == contour[i]):
                print('found?')
                # split the contour into 2 halfs
                firstHalf = contour[:i]
                secondHalf = contour[i:]
                # pop the entire contour out of final contour
                finalContour.pop(index)
                # insert the first half and then the second half into final contour in sequence
                finalContour.insert(index,firstHalf)
                finalContour.insert(index+1,secondHalf)
                found = True
                break
        if(found):
            break

# print('what is final contour again now', finalContour)

############################################################# after seperating all the contours, now seperate into vessels

# vessels = []

# for contour in finalContour:
    
############################################################# now read the vessels and print them onto the image

from PIL import Image
raw_img = cv2.imread(f'GT\\img1.png')
raw_height = raw_img.shape[0]
raw_width = raw_img.shape[1]
# creating a image object
raw_pil_image = Image.open(r'GT\\img1.png') 
  
# for contour in finalContour:
#     for i in range(len(contour)):=
#         image.putpixel( (contour[i][0], contour[i][1]), (0, 0, 0, 255) )

# image.show()

from shapely.geometry import LineString

def check_limit(point, limit):
    if(point < 0):
        point = 0
    elif(point > limit):
        point = limit - 1
    return point

perpend_line_array = []

for contour in finalContour:
    # split the contour array into 8 parts
    array_split = np.array_split(contour, 15)

    for i in range(len(array_split)):
        # coordinate at the start of the contour
        a = (array_split[i][0][0],array_split[i][0][1])
        # take the middle point for b so that it doesn't get drawn at the edge
        # coordinate in the middle of the contour
        b = (array_split[i][math.ceil(len(array_split)/2)][0],array_split[i][math.ceil(len(array_split)/2)][1])
        cd_length = 90

        ab = LineString([a, b])
        left = ab.parallel_offset(cd_length / 2, 'left')
        right = ab.parallel_offset(cd_length / 2, 'right')
        c = left.boundary[1]
        d = right.boundary[0]  # note the different orientation for right offset
        cd = LineString([c, d])
        firstX, firstY = math.ceil(c.x), math.ceil(c.y)
        secondX, secondY = math.ceil(d.x), math.ceil(d.y)
        firstX = check_limit(firstX,raw_width)
        firstY = check_limit(firstY,raw_height)
        secondX = check_limit(secondX,raw_width)
        secondY = check_limit(secondY,raw_height)
        # print('what is c de x ', c.x , 'and y ', c.y)
        # print('what is d de x ', d.x , 'and y ', d.y)
        # draws the line with colour and thickness
        cv2.line(raw_img, (firstX,firstY), (secondX, secondY), (255,0,0), 3)

        pt_a = [firstX,firstY]
        pt_b = [secondX,secondY]

        # this linspace will retrieve the coordinates between pt a and pt b that has length of cd_length
        points_on_line = np.linspace(pt_a, pt_b, cd_length)
        # perpend_line_array.append(points_on_line)
        # i should append it into an array, but for now i'm just taking ONE to test
        perpend_line_array = np.round(points_on_line)
        # print('what are points on line ', np.round(points_on_line))

cv2.imshow('drawn ',raw_img)
cv2.imwrite(f'drawn\\img1.png',raw_img)
cv2.waitKey(0)

red_array = []
green_array = []
the_x = []
the_y = []
# determine the intensity of the array by getting the r and g
# just a test for loop
for cod in perpend_line_array:
    rgb = raw_pil_image.getpixel((cod[0],cod[1]))
    r,g,b = rgb  #now you can use the RGB value
    # print('what is r ',r)
    # print('what is g ',g)
    red_array.append(r)
    green_array.append(g)
    the_x.append(cod[0])
    the_y.append(cod[1])

# plt.xlabel('X - AXIS')
# plt.ylabel('Y - AXIS')
# plt.title('Histogram of RED Intensity')
# plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
# plt.xlim(40, 160)
# plt.ylim(0, 0.03)
# plt.grid(True)
# plt.show()

# plt.plot(red_array,the_x)
# plt.plot(the_x, red_array)
# plt.title("intensity chart for red x")
# plt.show()
