import cv2 as cv
from utilities import *
from image_area import threshold_area

# font = cv.FONT_HERSHEY_COMPLEX
# image = cv.imread('im1.png',0)
# image = cv.imread('savedImage25v2.png')
# # image = cv.imread('img5.png')
# imgray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
# ret, thresh = cv.threshold(imgray, 127, 255, 0)
# # contours3, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
img = cv.imread(f'input\\img39.png',0)
# erode = cv.imread('img2.png',0)
height = img.shape[0]
width = img.shape[1]
# # percentage of white/ black
# total_contour_area_percentage = detecting_colours(image)
# total_contour_area = height*width*total_contour_area_percentage / 100
# print('what is total_contour_area for white', total_contour_area)

total_contour_area = 0
no_of_contour = 0
print('what is threshold_area ', threshold_area)
# while(no_of_contour != 1 or total_contour_area < threshold_area):
while( total_contour_area < threshold_area ):
    #resets it to 0 so that it can add up the areas again below later
    total_contour_area = 0
    #_______________________________________________________________________________________________________________________________________
    #Find contour
    #CHAIN_APPROX_SIMPLE = compresses horizontal, vertical, and diagonal segments and leaves only their end points. In this case, since rectangular, would encode with 4 points. 
    # contours, hierarchy = cv.findContours(img, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv.findContours(img, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    # contours2, hierarchy2 = cv.findContours(img, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    contours2, hierarchy2 = cv.findContours(img, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

    no_of_contour = len(contours)
    # cv.drawContours(img, contours3, -1, (0,225,0), 3)
    # cv.imshow('talalal',img)
    # cv.waitKey(0)
    # print('what is my contour ',contours3)
    #print('what is contour len ', no_of_contour)
    # print('what is contour ', contours)
    # cv.imshow("Image", img)

    # cv.waitKey(0)
    contourDict = []
    biggestArea = 0
    # image = cv.cvtColor(img, cv.COLOR_GRAY2BGR)  #add this line to change out of greyscale if you run approximation

    # remove noise where area is too small and fill in contourDict with contour information
    # contourDict, eg. [{'gradient': [0, 1], 'ytop': 330, 'ybottom': 709, 'xtop': 494, 'xbottom': 494, 'thickness': 10, 'area': 3411.0, 'action': 'no', 'all': [array([490, 330], dtype=int32), array([490, 709], dtype=int32), array([499, 709], dtype=int32), array([499, 330], dtype=int32)]}, {'gradient': [0, 1], 'ytop': 160, 'ybottom': 259, 'xtop': 584, 'xbottom': 584, 'thickness': 10, 'area': 891.0, 'action': 'no', 'all': [array([580, 160], dtype=int32), array([580, 259], dtype=int32), array([589, 259], dtype=int32), array([589, 160], dtype=int32)]}]
    for index, contour in enumerate(contours):
        area = cv.contourArea(contour)
        # the lower the accuracy the more detailed it'll get in the approximation as in more points, abit ironic
        # accuracy = 0.009 # 0.001 -> 0.1 choose any in between or just try whatever
        # epsilon = accuracy * cv.arcLength(contour, True)
        # approximations = cv.approxPolyDP(contour, epsilon, True)
        # if(index == 1):
            # print('what are approximations ',approximations)
        #  third argument is index of contours (useful when drawing individual contour. To draw all contours, pass -1) 
        # cv.drawContours(img, [approximations], -1, (0,0,255), 2)

        # ignore contours that are smaller or equal to 0.03% of the picture
        if(area >= (((width * height) / 100000) * 5)):

            allcod = []
            # for coordinate in approximations:
            for coordinate in contour:
                # print('what is coordinate ',coordinate)
                allcod.append(coordinate[0])
            # if(index == 1):
            #     grad = (219 - 218.5) / (386 - 373.5)
            #     g = [grad,grad]
            # returns all the information of the contour
            g,x1,x2,y1,y2,tks = find_gradient(allcod)
            # g,y1,y2,x1,x2,tks = extract_information(contour)
                # find_gradient(allcod)

            item = {
                "gradient":g, # [[0,1],[1,0],..]
                "ytop":y1, # [40,60,50....]
                "ybottom":y2, # [40,60,50....]
                "xtop":x1, # [49,50,69,60...]
                "xbottom":x2,  # [49,50,69,60...]
                "thickness":tks,
                "area": area,
                "allcod": allcod,
                "action":'no', #initialise with no first
                "originalIndex": index
            }
            # find the biggest area
            if area > biggestArea:
                biggestArea = area
            contourDict.append(item)
        else:
            # takes the contour and fill them up if they're too small
            # print('what is contours2[index]', contours2[index])
            #print('how many that are too small')
            # print('what is the contour ',contour)
            # print('what is ')
            cv.fillPoly(img, pts =[contours2[index]], color=(0,0,0))
            # cv.imshow(" ", img)
            # cv.waitKey()

    # Determine which contour should move by their area and update their actions
    for contour in contourDict:
        # adding up all the area should give the total total_contour_area
        total_contour_area += contour['area']
        # if the contour is smaller or equal to 90% of the biggest contour, then you should be joining up with others
        if(contour['area'] <= biggestArea * 0.9):
            contour['action'] = 'yes'

    #print('what is the total area ',total_contour_area)

    # go through the contourDict and determine the distances of the contour's points to the other contours 
    # and save the coordinate in contourDict again
    for index, contour in enumerate(contourDict):
        # run through the isolated contour check, to see if we need to remove anymore contours
        if(contour['action'] == 'yes'):
            contour['distances'] = find_distances(index, contour, contourDict)
            # print('what is their distances', contour['distance'])
            # {62.51399843235114: [[318, 352, 310, 290]], 62.80127387243033: [[320, 352, 310, 290]], 63.0317380372777: [[318, 352, 316, 289]], 
            
            # first value of the dict in contour['distances'] means the shortest distance it has with the others
            shortest_distance = list(contour['distances'].keys())[0]
            # if shortest value is larger than 25% of the images's length, remove it as it is quite far away from the others
            if(shortest_distance > (width * 0.25) and contour['area'] < 3.05):
                print('pop?')
                contourDict.pop(index)
                # fill in the space as it is now removed from the image
                cv.fillPoly(img, pts =[contours2[contour['originalIndex']]], color=(0,0,0))


    # go through the contourDict again and now find the line which needs to be drawn from the coordinates
    for index, contour in enumerate(contourDict):
        if(contour['action'] == 'yes'):
            origx, origy, otherx, othery = return_coordinates(contour['gradient'],contour)
            cv.line(img, (origx,origy), (otherx, othery), (255,255,255), 2)
            contour['action'] = 'no'
            #append a new item inside the contour called 'line' with the 4 coordinates
            # contour['line'] = [[origx,origy],[otherx,othery]]

    # now that you have updated line, you can add pixel to them
    # for index, contour in enumerate(contourDict):
    #     gradient = []
    #     if(contour['action'] == 'yes'):
    #         origx = contour['line'][0][0]
    #         origy = contour['line'][0][1]
    #         otherx = contour['line'][1][0]
    #         othery = contour['line'][1][1]
            

    kernel = np.ones((5,5),np.uint8)
    dilate = cv.dilate(img,kernel,iterations = 1)
    erode = cv.erode(dilate,kernel,iterations = 1)
    img = erode
    # if no of contour is reduced to 1, break out of the for loop
    if(no_of_contour == 1):
        break

# just displaying the image to be shown
# new_contours, hierarchy = cv.findContours(img, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
# print('what is len here ', len(new_contours))
# Using cv2.imwrite() method
cv.imwrite(f'output\\img39.png', img)


# from PIL import Image
      
# creating a image object
# imagetest = Image.open("im1.png")
# imagetest.putpixel((200, 200), (255, 0, 0))

# now that you have updated line, you can add pixel to them
# for index, contour in enumerate(contourDict):
#     gradient = []
#     if(contour['action'] == 'yes'):
#         origx = contour['line'][0][0]
#         origy = contour['line'][0][1]
#         otherx = contour['line'][1][0]
#         othery = contour['line'][1][1]
#         print('line?')
#         # drawing the line
#         # imagePIL.putpixel((origx, origy), (255, 0, 0))
#         # cv.line(img, (origx,origy), (otherx, othery), (255,255,255), 10)
#         contour['action'] = 'no'
# imagetest.show()
# cv.imshow("Image", img)

# cv.waitKey(0)
# cv.destroyAllWindows()