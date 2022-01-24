#Code for IoU
import numpy as np
import cv2

# Getting all white pixels (pixel coordinates) of an image
# img_gt = cv2.imread(f'automation\\thresh\contour\img7.png',0)
# test = cv2.imread(f'automation\\pred\img7.png') #when reading from images after 2nd method, all images grayscale, no need binarying 
# grayImage = cv2.cvtColor(test, cv2.COLOR_BGR2GRAY)
# ret, thresh = cv2.threshold(grayImage, 0, 255, cv2.THRESH_BINARY)
# img_test = thresh
# white_gt = np.argwhere(img_gt == 255)
# white_test = np.argwhere(img_test == 255)
# #print ('What is white gt', white_gt)
# #print ('What is white test', white_test)

##______________________________________________________________________________________________________________________________________________________________________

#iou_arr = [] #this array contains all values of iou in index format
#img 1= 0.0134; img 2= 0.0135; img3 = 0.00899 ;0.0296

img_test = cv2.imread(f'automation\\post\\test\\img4.png',0) 
GT = cv2.imread(f'automation\\post\\GT\\img4.png')
grayImage = cv2.cvtColor(GT, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(grayImage, 0, 255, cv2.THRESH_BINARY)
img_gt = thresh

#for i in range(len(img_gt)):
#Get all white pixels in the images first 
white_gt = np.argwhere(img_gt == 255)
white_test = np.argwhere(img_test == 255)
    #print ('What is white gt', white_gt)
    #print ('What is white test', white_test)

    # Getting the true positives first (where test meets true)
    # Need to get the intersection/ overlap between the 2 double arrays 
gt_set = set([tuple(x) for x in white_gt])
test_set = set([tuple(x) for x in white_test])
TP = np.array([x for x in gt_set & test_set]) #in this case, TP = overlap/ intersection between both images
print('What is overlap', TP)

    # Now get FP & FN
    # FN = Where the test should've met true but did not meet  
    # FP = where test meets somewhere that's not true and should not have 

    # First get FN
dims_FN = np.maximum(white_gt.max(0),TP.max(0))+1
FN = white_gt[~np.in1d(np.ravel_multi_index(white_gt.T,dims_FN),np.ravel_multi_index(TP.T,dims_FN))]
print('What is FN', FN)

    # Get FP
dims_FP = np.maximum(white_test.max(0),TP.max(0))+1
FP = white_test[~np.in1d(np.ravel_multi_index(white_test.T,dims_FP),np.ravel_multi_index(TP.T,dims_FP))]
    #print('What is FP',FP)

    # Now, with all the variables (TP, FP and FN), you can now get the IoU
    # IoU = TP/(TP + FP + FN) but in this case, you don't want to actually plus and divide them numerically.....but just conceptually 

    #Want to get the ratio of TP: TP + FP +FN(aka: union)
union = np.concatenate((TP,FP),axis=0)
    #print('What is union',union)

union2 = np.concatenate((union,FN),axis=0)
    #print('What is union',union2)

    # Get intersection/overlap between TP and union2
    # Get number of elements in union2 and said intersection/overlap and from there, get a ratio/ percentage/score 
union2_set = set([tuple(x) for x in union2])
TP_set = set([tuple(x) for x in TP])
final_overlap = np.array([x for x in union2_set & TP_set]) 
    #print('What is final overlap', final_overlap)

union2_num = len(union2)
final_overlap_num = len(final_overlap)

    #print('What is length of union2', union2_num)
    #print('What is length of final_overlap', final_overlap_num)

iou_value = final_overlap_num/ union2_num
    #print('What is iou', iou_value)
    #iou_arr.append(iou_value)
print('What is iou', iou_value)


# for i in range(4): # image_1,2,3,4
#     i += 1
#     path = (f'automation\\post\\GT\\img{i}.png')
#     path2 = (f'automation\\post\\test\\img{i}.png') #file name to be changed in the future to post processed (after 2nd method)
#     img_gt = cv2.imread(path,0)
#     img_test = cv2.imread(path2,0)
#     iou(img_gt,img_test)

# print('What is iou', iou_arr)
    


    