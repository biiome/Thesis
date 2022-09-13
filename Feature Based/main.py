import cv2 as cv
import numpy as np
from functions import *
import os
from tkinter import Tk
from tkinter.filedialog import askdirectory

# OCT_Folder_Root = askdirectory(title="Select folder containing OCT images")
OCT_Folder_Root = "Sample Images/Image_Set_1/OCT Images/"
OCT_File_List = []

# ATT_Folder_Root = askdirectory(title="Select folder containing attenuation images")
ATT_Folder_Root = "Sample Images/Image_Set_1/Attenuation Images/"
ATT_File_List = []

# Populate OCT_File_List
for root, dirs, files in os.walk(os.path.abspath(OCT_Folder_Root)):
    for file in files:
        # print(os.path.join(root, file))
        OCT_File_List.append(os.path.join(root, file))

# Populate ATT_File_List
for root, dirs, files in os.walk(os.path.abspath(ATT_Folder_Root)):
    for file in files:
        # print(os.path.join(root, file))
        ATT_File_List.append(os.path.join(root, file))

# Reverse list order so that operations can be performed in the correct order
OCT_File_List.reverse()
ATT_File_List.reverse()


# Load images
# img0 = cv.imread(OCT_Folder_Root + "OCT_p1.png")
# img1 = cv.imread(OCT_Folder_Root + "OCT_p2.png")
# att0 = cv.imread(ATT_Folder_Root + "Attenuation_p1.png")
# att1 = cv.imread(ATT_Folder_Root + "Attenuation_p6.png")


# Set up list of prime images
Prime_Images = [
    cv.imread(OCT_File_List[0]),
]

# Set up list of registered attenuation images
Registered_ATT = [
    cv.imread(ATT_File_List[0]),
]

homography_matrix = []

for i in range(0, len(OCT_File_List) - 1):
    print(i)
    # Read in images
    # img0 = Prime_Images[i]
    img0 = cv.imread(OCT_File_List[i])
    img1 = cv.imread(OCT_File_List[i + 1])
    att1 = cv.imread(ATT_File_List[i + 1])

    # Convert OCT images to greyscale
    img0_gray = cv.cvtColor(img0, cv.COLOR_RGB2GRAY)
    img1_gray = cv.cvtColor(img1, cv.COLOR_RGB2GRAY)

    # Pass images into feature extraction function
    features0 = featureExtraction(img0_gray)
    features1 = featureExtraction(img1_gray)

    # Display detected keypoints in image
    # img0_kps = cv.drawKeypoints(img0, features0.kps, None, flags=None)
    # img1_kps = cv.drawKeypoints(img1, features0.kps, None, flags=None)

    # cv.imshow("Image 0 keypoints", img0_kps)
    # cv.imshow("Image 1 keypoints", img1_kps)
    # cv.waitKey(0)

    # Match features using feature matching function
    matches = featureMatching(features0, features1)

    # Homography calculation using RANSAC to find the transformation matrix
    homography, _ = cv.findHomography(
        features0.matched_pts, features1.matched_pts, cv.RANSAC, 5.0
    )

    homography_matrix.append(homography)

    # Save dimensions of image to be warped
    height, width, _ = img1.shape

    # Warp target image to source image
    warped = cv.warpPerspective(
        img0,
        homography,
        (width, height),
        borderMode=cv.BORDER_CONSTANT,  # need to see if applying a border around the image would be a good idea to avoid errors
        borderValue=(0, 0, 0, 0),
    )

    warped_att = cv.warpPerspective(
        att1,
        homography,
        (width, height),
        borderMode=cv.BORDER_CONSTANT,  # need to see if applying a border around the image would be a good idea to avoid errors
        borderValue=(0, 0, 0, 0),
    )

    # Some stuff is happening here
    output = np.zeros((height, width, 3), np.uint8)
    alpha = warped[:, :, 2] / 255.0
    output[:, :, 0] = (1.0 - alpha) * img1[:, :, 0] + alpha * warped[:, :, 0]
    output[:, :, 1] = (1.0 - alpha) * img1[:, :, 1] + alpha * warped[:, :, 1]
    output[:, :, 2] = (1.0 - alpha) * img1[:, :, 2] + alpha * warped[:, :, 2]

    # Doing the same to the attenuation data
    output_att = np.zeros((height, width, 3), np.uint8)
    alpha_att = warped[:, :, 2] / 255.0
    output_att[:, :, 1] = (1.0 - alpha) * att1[:, :, 1] + alpha * warped_att[:, :, 1]
    output_att[:, :, 0] = (1.0 - alpha) * att1[:, :, 0] + alpha * warped_att[:, :, 0]
    output_att[:, :, 2] = (1.0 - alpha) * att1[:, :, 2] + alpha * warped_att[:, :, 2]

    # Write registered image to Prime_Images and Registered_ATT list
    Prime_Images.append(output)
    Registered_ATT.append(output_att)
    # cv.imwrite(filename, output, [cv.IMWRITE_PNG_COMPRESSION, 0])
    # print(output)
    image1 = Prime_Images[i]
    image2 = Prime_Images[i - 1]
    test = crossCorellation(image1, image2)
    print(test)

for i in range(len(Prime_Images)):
    filename = str(i) + ".png"
    filename_att = "att " + str(i) + ".png"
    cv.imwrite(filename, Prime_Images[i], [cv.IMWRITE_PNG_COMPRESSION, 0])
    cv.imwrite(filename_att, Registered_ATT[i], [cv.IMWRITE_PNG_COMPRESSION, 0])
    print(homography_matrix[1])


# Write image to disk
# cv.imwrite("img01.jpg", output)
# cv.imwrite("att01.jpg", output_att)
# cv.imshow("Image 1", img0)
# cv.imshow("Image 2", img1)
# cv.imshow("Registered Image", output)
# cv.imshow("Registered Attenuation Image", output_att)
# cv.waitKey(0)
