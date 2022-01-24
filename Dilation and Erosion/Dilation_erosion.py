import cv2
import numpy as np 

#Convert all images to binary format so that they're all white & black instead of red/ green & black
def binarying (image, index):
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(grayImage, 0, 255, cv2.THRESH_BINARY)
    image_copy = thresh.copy()
    path = (f'automation\\thresh\contour\img{index}.png')
    #print('what is path', path)
    cv2.imwrite(path, image_copy)


for i in range(2000): # image_1,2,3,4
    i += 1
    path = (f'automation\\thresh\label\img{i}.png')
    #print('what is path ',path)
    image = cv2.imread(path)
    binarying(image, i)

##_____________________________________________________________Detecting no. of white & black coordinates & getting threshold values__________________________________
# Define the blue colour we want to find, the colour codes follow the BGR format as opencv reads image in bgr format
percentage_array = []
array_split = 0
average_array = []

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

    if white_len != 0 :
        percentage_array.append(percentage)

#applying the detecting_colours function to the all images 
for i in range(2000): # image_1,2,3,4
    i += 1
    path = (f'automation\\thresh\contour\img{i}.png')
    #print('what is path ',path)
    image = cv2.imread(path)
    detecting_colours(image)

#sort percentage array in ascencing order and dividing them into 10 sections 
sorted_percentage_array = sorted(percentage_array)
# for higher accuracy, we can split this more
array_split = np.array_split(sorted_percentage_array, 100)
print('what is array_split ',array_split)
#print('what is length', len(four_split))

#find the average of each 10 sections and append values into an array 
for array in array_split:
    sum_array = sum(array)
    length_array = len(array)
    average = sum_array/length_array
    average_array.append(average)

# print('array is ',average_array)

#printing out section and its array 
# for index, array in enumerate(array_split):
    #print(f"\n here is section {index} \n")
    # print(f"\n length of section {index} is {len(array)} \n")
# print('what is ten split array ', array_split)

#print('what is the percentage array ', percentage_array)
#print(f'what is sum {sum(percentage_array)} and length {len(percentage_array)}')
# print('what is length', len(four_split))
#print('what is length', len(percentage_array)) #368 percentages 
#print('what is percentage_area average', sum(percentage_array)/len(percentage_array))

##_______________________________________________________________Applying threshold to images and function__________________________________
#see if picture reaches the nearest section's average value, if not, continue to perform function until it does.

#Function that changes all images to binary images
def binarying (image, index):
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(grayImage, 0, 255, cv2.THRESH_BINARY)
    image_copy = thresh.copy()
    path = (f'automation\\test_coords\\binary\img{index}.png')
    #print('what is path', path)
    cv2.imwrite(path, image_copy)

#For loop that calls the binarying function 
for i in range(38): # image_1,2,3,4
    i += 1
    path = (f'automation\\test_coords\original\img{i}.png')
    #print('what is path ',path)
    image = cv2.imread(path)
    binarying(image, i)

#Defining function that uses the blur function
def blur (image, index):
    median_blur = cv2.medianBlur(image, 5)
    #gaussian_blur = cv2.GaussianBlur(image2,(5,5),0)
    #normal_blur= cv2.blur(image2,(5,5))
    cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
    path = (f'automation\\test_coords\\blur\img{index}.png')
    cv2.imwrite(path, median_blur)

# For loop that calls the blur function
for i in range(38): # image_1,2,3,4
    i += 1
    path = (f'automation\\test_coords\\binary\img{i}.png')
    #print('what is path ',path)
    image = cv2.imread(path)
    blur(image,i)

#Defining function that uses the erode function 
def eroding (image, index): 
    kernel = np.ones((5, 5), 'uint8')
    erode = cv2.erode(image, kernel, iterations= 1) 
    path = (f'automation\\test_coords\erode\img{index}.png')
    cv2.imwrite(path, erode)

#For loop that calls the erode function
for i in range(38): # image_1,2,3,4
    i += 1
    path = (f'automation\\test_coords\\blur\img{i}.png')
    #print('what is path ',path)
    image = cv2.imread(path)
    eroding(image,i)

percentage_array_test = []

# returns the %  of white / every pixel in the image
def detecting_colours_test (image):
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
    # if white_len != 0 :
    #     percentage_array_test.append(percentage)

#Defining a function that compares the percentage of image to the relevant quadrant
def compare_quadrant(percentage):
    for index, array in enumerate(array_split):
        if (index == 0 and percentage < array[0]):
            return average_array[index]
        if (index == len(array_split)-1 and percentage > array[len(array)-1]):
            return average_array[index]
        if (percentage < array[0]):
            return average_array[index-1]
        elif percentage >= array[0] and percentage <= array[len(array)-1]:
            # print('what is percentage array', average_array)
            return average_array[index]

#Defining the function that uses the dilate function
def dilating (image, index, x):
    kernel = np.ones((5,5), np.uint8)
    dilation = cv2.dilate(image, kernel, iterations = x)
    path = (f'automation\\test_coords\dilate\img{index}.png')
    cv2.imwrite(path, dilation)
    return dilation

#Defining another function that uses the erode function
def eroding2 (image, index, x):
    kernel = np.ones((5, 5), 'uint8')
    erode2 = cv2.erode(image, kernel, iterations = x) 
    cv2.imwrite((f'automation\\test_coords\erode2\img{index}.png'), erode2)
    return erode2

# For loop that calls both the dilate, erode2, detecting_colours_test and compare quadrant function
for i in range(38): # image_1,2,3,4
    i += 1
    path = (f'automation\\test_coords\erode\img{i}.png')
    # print('what is path ',path)
    image = cv2.imread(path)
    percentage = detecting_colours_test(image) #check percentage of current image in loop
    print('what is percentage now', percentage)

    if percentage != 0: #if percentage not equal to 0
        average_percentage = compare_quadrant(percentage) #compare quadrant to see which quadrant it falls into and return the corresponding average percentage value of that quadrant
        x = 0
        print('what is average percentage now', average_percentage)
        while(percentage < average_percentage): #while percentage is smaller than said average percentage
            x += 1
            # print('what is x ',x)
            dilatedImage = dilating(image, i, x) #perform both function
            erodedImage = eroding2(dilatedImage, i, x)
            # cv2.imshow('image', image)
            # cv2.waitKey(0)
            percentage = detecting_colours_test(erodedImage) #measure thse new percentage after performing functions to check again
            print('what is new percentage outside ', percentage)

    cv2.imwrite((f'automation\\test_coords\\final\img{i}.png'), image) #loop will immediately fall here if percentage = 0 or if percentage finally becomes > average percentage

# print('what is the percentage array ', percentage_array)
# print(f'what is sum {sum(percentage_array)} and length {len(percentage_array)}')
# print('what is length', len(four_split))
# print('what is length', len(percentage_array)) #368 percentages 
# print('what is percentage_area average', sum(percentage_array)/len(percentage_array))


