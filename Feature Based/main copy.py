import os
import cv2 as cv
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askdirectory
from functions import featureExtraction, featureMatching

# OCT_Folder_Root = askdirectory(title="Select folder containing OCT images")
# OCT_File_List = os.listdir(OCT_Folder_Root)
# ATT_Folder_Root = askdirectory(title="Select folder containing attenuation images")
# ATT_File_List = os.listdir(ATT_Folder_Root)

# Hardcode folders for testing
OCT_Folder_Root = "/home/vraj/Documents/Onedrive/Thesis/Image-Algorithm/Sample Images/Image_Set_1/OCT Images/"
ATT_Folder_Root = "/home/vraj/Documents/Onedrive/Thesis/Image-Algorithm/Sample Images/Image_Set_1/Attenuation Images/"
OCT_File_List = os.listdir(OCT_Folder_Root)
ATT_File_List = os.listdir(ATT_Folder_Root)

# For all files in the folder
for i in range(1, len(OCT_File_List)):

    img0 = cv.imread(os.path.join(OCT_Folder_Root, OCT_File_List[i - 1]))
    img1 = cv.imread(os.path.join(OCT_Folder_Root, OCT_File_List[i]))
    att = cv.imread(os.path.join(ATT_Folder_Root, ATT_File_List[i]))

    # Check if what is selected is a file - can extend this so that it also checks if the appropriate file is slected (e.g. filetype, name, etc.)
    # if os.path.isfile(img0) and os.path.isfile(img1) and os.path.isfile(att):

    # Convert OCT images to greyscale
    img0_gray = cv.cvtColor(img0, cv.COLOR_RGB2GRAY)
    img1_gray = cv.cvtColor(img1, cv.COLOR_RGB2GRAY)

    # Show images
    # cv.imshow('Image 1', img0)
    # cv.imshow('Image 2', img1)
    # cv.waitKey(0)

    # Pass images into feature extraction function
    features0 = featureExtraction(img0_gray)
    features1 = featureExtraction(img1_gray)

    # Match features using feature matching function
    matches = featureMatching(features0, features1)

    # Homography calculation using RANSAC to find the transformation matrix
    homography, _ = cv.findHomography(
        features0.matched_pts, features1.matched_pts, cv.RANSAC, 5.0
    )
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

    # # Warp attenuation image to source image
    # warped_att = cv.warpPerspective(
    #     att0,
    #     homography,
    #     (width, height),
    #     borderMode=cv.BORDER_CONSTANT,
    #     borderValue=(0,0,0,0)

    # )

    # Some stuff is happening here
    output = np.zeros((height, width, 3), np.uint8)
    alpha = warped[:, :, 2] / 255.0
    output[:, :, 0] = (1.0 - alpha) * img1[:, :, 0] + alpha * warped[:, :, 0]
    output[:, :, 1] = (1.0 - alpha) * img1[:, :, 1] + alpha * warped[:, :, 1]
    output[:, :, 2] = (1.0 - alpha) * img1[:, :, 2] + alpha * warped[:, :, 2]

    # Doing the same to the attenuation data
    output_att = np.zeros((height, width, 3), np.uint8)
    alpha_att = warped[:, :, 2] / 255.0
    output_att[:, :, 0] = (1.0 - alpha) * att[:, :, 0] + alpha * warped[:, :, 0]
    output_att[:, :, 1] = (1.0 - alpha) * att[:, :, 1] + alpha * warped[:, :, 1]
    output_att[:, :, 2] = (1.0 - alpha) * att[:, :, 2] + alpha * warped[:, :, 2]

    # Write image to disk
    # cv.imwrite('img01.jpg', output)
    # cv.imwrite('att01.jpg', output)
    # cv.imshow('Registered Image', output)
    # cv.imshow('Registered Attenuation Image', output_att)
    # cv.waitKey(0)
