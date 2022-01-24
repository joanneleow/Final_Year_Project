import math
import numpy as np 
import cv2

def find_gradient(contour):
    gradient = []
    length = len(contour)
    x1,x2,y1,y2,thickness = 0,0,0,0,0

    # ascending means that x is smaller first, meaning its left
    # sort first column ascending, second column ascending too
    contour.sort(key=lambda x: (x[0],x[1]))   
    left_top = contour[0] #first coord in the array
    left_point = contour[0][0]

    right_bot = contour[length-1] #last num in the array
    right_point = contour[length-1][0]

    # sort first column ascending, second column descending
    contour.sort(key=lambda x: (x[0],-x[1]))   
    left_bot = contour[0]
    right_top = contour[length-1]

    # sort based of second column only, so its y axis
    contour.sort(key=lambda x: (x[1]))
    top_point = contour[0][1]
    bottom_point = contour[length-1][1]

    # now we need to decide if the line is horizontal or vertical
    if( (right_point - left_point) >= (bottom_point - top_point) ):
        # line type is horizontal
        x2 = (left_bot[0] + left_top[0]) / 2
        y2 = (left_bot[1] + left_top[1]) / 2 
        x1 = (right_bot[0] + right_top[0]) / 2
        y1 = (right_bot[1] + right_top[1]) / 2
        thickness = bottom_point - top_point
    else:
        # line type is vertical
        x2 = (left_bot[0] + right_bot[0]) / 2
        y2 = (left_bot[1] + right_bot[1]) / 2
        x1 = (left_top[0] + right_top[0]) / 2
        y1 = (left_top[1] + right_top[1]) / 2
        thickness = right_point - left_point

    if x2 - x1 == 0:
        if y2 > y1: #meaning ybottom > ytop, go up 
            gradient = [0,1] 
        else:
            gradient = [0,-1] #meaning ytop > ybottom, so negative value, go down 
    # if y = 0, means its horizontal (going left or right along the x axis)
    elif y2 - y1 == 0:
        if x2 > x1:
            gradient = [1,0] #meaning xbottom > xtop, go right
        else:
            gradient = [-1,0] #meaning xtop >xbottom, so negative value, go left
    else:
        g = (y2 - y1) / (x2 - x1)

        # print(f'what is y2 {y2} - y1 {y1} / x2 {x2} - x1 {x1} = g {g}')
        gradient = [g,g]

    return gradient, x1, x2, y1, y2, thickness

def extract_information(contours):
    #First step is to store end points into arrays
    #initialise all y(s) to 0 at first
    ytop, ybottom = 0,0,
    xtop, xbottom = [],[]

    finalXtop, finalXbottom = 0,0
    gradient = []
    topCount, bottomCount = 0,0
    for contour in contours:
        # contour = [[49,20]]: array inside an array 'double array', contour[0] = [49,20]: single array 
        #contour[0][0] = the x value; contour [0][1] = y value
        #This for loop would then run through all end points coord. one by one in particular sequence 
        x,y = contour[0][0], contour[0][1]
        # initialise ytop
        if ytop == 0 and topCount == 0:
            ytop = y
            xtop.append(x) #meaning appending the corresponding x value 
            topCount += 1
        # meaning if the current y coordinate is smaller than yTop, in this case means a higher y coordinate
        elif y < ytop: 
            ytop = y
            xtop.clear()
            xtop.append(x)
        # if you have a y coordinate the same height as yTop, you append the x coordinate, meaning there's 2 point at the same height
        elif y == ytop: 
            xtop.append(x)
        # now onto ybottom
        else:
            # initialise ybottom
            if ybottom == 0 and bottomCount == 0:
                ybottom = y
                xbottom.append(x)
                bottomCount += 1
            # meaning a new y is lower than the ybottom coordinate, u clear the xbottom array and then add the new one in
            elif y > ybottom:
                ybottom = y
                xbottom.clear()
                xbottom.append(x)
            # if y coordinate same height as ybottom, append x coordinate to the array too
            elif y == ybottom:
                xbottom.append(x)
    # finalising what the xtop and xbottom should be
    # if xtop has multiple values, eg. [49,50], get the average by adding them up -> sum(xtop) and dividing the number in the array -> len(xtop)
    # and then round it down by math.floor. Same goes for finalXbottom
    finalXtop = math.floor(sum(xtop)/len(xtop))
    finalXbottom = math.floor(sum(xbottom)/len(xbottom))
    thickness = max(xtop) - min(xtop) + 1 #eg. 50-49 = 1, but thickness is 2 pixel, hence + 1 at the back

    # have gradient for each contour and at each direction (x and y)
    # if x = 0, means its vertical (going up or down the y axis)
    if finalXbottom - finalXtop == 0:
        if ybottom > ytop: #meaning ybottom > ytop, go up 
            gradient = [0,1] 
        else:
            gradient = [0,-1] #meaning ytop > ybottom, so negative value, go down 
    # if y = 0, means its horizontal (going left or right along the x axis)
    elif ybottom - ytop == 0:
        if finalXbottom > finalXtop:
            gradient = [1,0] #meaning xbottom > xtop, go right
        else:
            gradient = [-1,0] #meaning xtop >xbottom, so negative value, go left
    else:
        g = (ybottom - ytop) / (finalXbottom - finalXtop) #theory of (y2-y1)/(x2-x1)
        gradient = [g,g]

    # print(f'what is ytop, xtop {ytop,finalXtop}')
    # print(f'what is ybottom, xbottom {ybottom,finalXbottom}')
    # print('what is gradient ',gradient)   '''

    return gradient, ytop, ybottom, finalXtop, finalXbottom, thickness

def check_gradient(item, gradient):
    origx = item[0]
    origy = item[1]
    otherx = item[2]
    othery = item[3]
    direction_gradient = []
    # [[318, 352, 311, 289], [317, 353, 310, 290]]
    if otherx - origx == 0:
        if(origy > othery): # so origy is lower than the othery, means we're going up
            direction_gradient = [0,1] 
        else: # going down as our point is located higher than the others, 
            direction_gradient = [0,-1] 
            
    # if y = 0, means its horizontal (going left or right along the x axis)
    elif othery - origy == 0:
        if(origx > otherx): # if origx bigger than the other one, 
            direction_gradient = [-1,0] # go left
        else:
            direction_gradient = [1,0] #go right
    else:
        g = (origy - othery) / (origx - otherx) #theory of (y2-y1)/(x2-x1)
        direction_gradient = [g,g]

    # print('what is direction gradient ', direction_gradient)

    # most of the time gradient[0] and [1] will be the same, however, I split it into 2 just in case of rare cases
    # like horizontal [1,0] and vertical [0,1]
    if (abs(gradient[0] - direction_gradient[0]) <= 0.25):
        # print('what is gradient[0] - direction gradient[0] ',abs(gradient[0] - direction_gradient[0]))
        if(abs(gradient[1] - direction_gradient[1]) <= 0.25):
            # print(f'what is gradient here - {gradient[1]} and what is direction gradient {direction_gradient[1]}')
            # print('what is gradient[1] - direction gradient[1] ',abs(gradient[1] - direction_gradient[1]))
            return True

# finds distance of all the coordinates to the actioned contour's coordinates and save them in a dict
def find_distances(index, actioned_contour, contourDict):
    distance_dict = {} # distance_dict = {distance_1:[x,y], distance_2:[x2,y2], distance_3:...}
    # use a temporary contour, initialise it to contour
    temp_contours = m = [x for x in contourDict]
    # pops out the contour that is being actioned
    temp_contours.pop(index)
    # this is now a array that doesn't contained the dict that is being actioned on 

    # loop through all the coordinates in the actioned dict
    for coordinates in actioned_contour['allcod']:
        # loop through how many other contours they are in the temp_contours
        for other_contours in temp_contours:
            # now you get the coordinates in each looped 'other contour'
            for other_cod in other_contours['allcod']:
                #calculate the distance of your origx and origy to the otherx othery
                distance = math.sqrt( ((coordinates[0]-other_cod[0])**2)+((coordinates[1]-other_cod[1])**2) )
                dist_cod = [coordinates[0],coordinates[1],other_cod[0],other_cod[1]]
                # just saving the coordinates into array with distance as the key
                if distance not in distance_dict:
                    distance_dict[distance] = [dist_cod]
                # if distance as key already exists, just append it into the array
                else: 
                    distance_dict[distance].append(dist_cod)

    # sorted dict by ascending so the item on top will be the one with the closest distance
    sorted_distance_dict = dict(sorted(distance_dict.items()))

    return sorted_distance_dict


def return_coordinates(gradient, actioned_contour):
    origx, origy, otherx, othery = 0,0,0,0
    found_cod = False

    # sort out which points to return by using direction gradient and the line's original gradient as a reference 
    first_value = list(actioned_contour['distances'].values())[0]

    # assigning the first value which is the coordinates of the points that are of the closest distance incase
    # there is no points where the gradient will stick to
    origx = first_value[0][0]
    origy = first_value[0][1]
    otherx = first_value[0][2]
    othery = first_value[0][3]
    for index, item in enumerate(actioned_contour['distances'].values()):   
        if(index == 100):
            break

        for i in range(len(item)):
            found_cod = check_gradient(item[i], gradient)
            if(found_cod):
                origx = item[i][0]
                origy = item[i][1]
                otherx = item[i][2]
                othery = item[i][3]
                print(f'what is origx - {origx}, origy - {origy}, otherx - {otherx}, othery - {othery}')
                return origx, origy, otherx, othery

    # if nothing is returned come here
    print('nothing is returned from gradient so the shortest line is chosen')
    return origx, origy, otherx, othery
    
def detecting_colours (image):

    white = [255,255,255]
    black = [0,0,0]
    # Get X and Y coordinates of all white and black pixels
    X,Y = np.where(np.all(image==white,axis=2))
    X2,Y2 = np.where(np.all(image==black,axis=2))

    #Zipping all each colour's coordinates in an array for easier read 
    zipped = np.column_stack((X,Y))
    zipped2 = np.column_stack((X2,Y2))
    #print(zipped2)

    #Calculate percentage of white/ black: no. of coordinates
    #Find length of each colour's zipped array = total no. of elements in the array/object.
    white_len = len(zipped)
    black_len = len(zipped2)
    percentage = (white_len/ (white_len + black_len)) * 100 
    return percentage