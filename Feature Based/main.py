# Imports
import cv2 as cv
import numpy as np
from functions import *
import os
from tkinter import Tk
from tkinter.filedialog import askdirectory
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar


# Load data
# OCT_Folder_Root = askdirectory(title="Select folder containing OCT images")
OCT_Folder_Root = r"C:\Users\Vraj\Documents\Thesis\Image-Algorithm\Sample Images\Image_Set_1\OCT Images"
OCT_File_List = []

# ATT_Folder_Root = askdirectory(title="Select folder containing attenuation images")
ATT_Folder_Root = r"C:\Users\Vraj\Documents\Thesis\Image-Algorithm\Sample Images\Image_Set_1\Attenuation Images"
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

# Set up list to store homography data
homography_matrix = []

# Main Loop

# For all but the last OCT image:
for i in range(0, len(OCT_File_List) - 1):
    print(i)
    # Read in images
    img0 = cv.imread(OCT_File_List[i])
    # img0 = Prime_Images[i]
    img1 = cv.imread(OCT_File_List[i + 1])
    att1 = cv.imread(ATT_File_List[i + 1])

    # Convert OCT images to greyscale
    img0_gray = cv.cvtColor(img0, cv.COLOR_RGB2GRAY)
    img1_gray = cv.cvtColor(img1, cv.COLOR_RGB2GRAY)

    # Pass images into feature extraction function
    features0 = featureExtraction(img0_gray)
    features1 = featureExtraction(img1_gray)

    # Display detected keypoints in image

    keypoints_without_size = np.copy(img0)
    keypoints_with_size = np.copy(img0)

    cv.drawKeypoints(img0, features0.kps, keypoints_without_size, color=(0, 255, 0))
    cv.drawKeypoints(
        img0,
        features0.kps,
        keypoints_with_size,
        flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
    )

    # Display image with and without keypoints size
    # fx, plots = plt.subplots(1, 2, figsize=(20, 10))

    # plots[0].set_title("Original Image")
    # plots[0].imshow(img0, cmap="gray")

    # plots[1].set_title("Detected Keypoints")
    # plots[1].imshow(keypoints_without_size, cmap="gray")

    # plots[0].set_xlabel("Pixels")
    # plots[0].set_ylabel("Pixels")
    # plots[1].set_xlabel("Pixels")
    # plots[1].set_ylabel("Pixels")

    # scalebar = ScaleBar(1, "px", dimension="pixel-length", length_fraction=0.2)
    # plt.gca().add_artist(scalebar)

    # plt.show()

    # Match features using feature matching function
    matches = featureMatching(features0, features1)

    # Perform homography calculation using RANSAC to find the transformation matrix
    homography, _ = cv.findHomography(
        features0.matched_pts, features1.matched_pts, cv.RANSAC, 5.0
    )

    # Save calculated homography matrix to homography_matrix list
    homography_matrix.append(homography)

    # Calculate dimensions of image to be warped
    height, width, _ = img1.shape

    # Warp target image to source image using homography matrix
    warped = cv.warpPerspective(
        img0,
        homography,
        (width, height),
        borderMode=cv.BORDER_CONSTANT,  # need to see if applying a border around the image would be a good idea to avoid errors
        borderValue=(0, 0, 0, 0),
    )

    # Warp attenuation image using calculated OCT homography matrix
    warped_att = cv.warpPerspective(
        att1,
        homography,
        (width, height),
        borderMode=cv.BORDER_CONSTANT,
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

    # Save registered images to Prime_Images and Registered_ATT list
    Prime_Images.append(output)
    Registered_ATT.append(output_att)

    # Test attenuation performance between the orignal and the registered image
    image1 = Prime_Images[i]
    image2 = Prime_Images[i - 1]
    test = crossCorellation(image1, image2)
    print(test)

# for i in range(len(Prime_Images)):
#     filename = str(i) + ".png"
#     filename_att = "att " + str(i) + ".png"
#     cv.imwrite(filename, Prime_Images[i], [cv.IMWRITE_PNG_COMPRESSION, 0])
#     cv.imwrite(filename_att, Registered_ATT[i], [cv.IMWRITE_PNG_COMPRESSION, 0])

warped_image = []

#%%
for i in range(len(homography_matrix)):
    height, width, _ = img1.shape

    homogrpahy_new = homography_matrix[i]
    img0 = cv.imread(OCT_File_List[i])
    img1 = cv.imread(OCT_File_List[i + 1])
    att1 = cv.imread(ATT_File_List[i + 1])

    warped = cv.warpPerspective(
        img0,
        homography,
        (width, height),
    )

    output = np.zeros((height, width, 3), np.uint8)
    alpha = warped[:, :, 2] / 255.0
    output[:, :, 0] = (1.0 - alpha) * img1[:, :, 0] + alpha * warped[:, :, 0]
    output[:, :, 1] = (1.0 - alpha) * img1[:, :, 1] + alpha * warped[:, :, 1]
    output[:, :, 2] = (1.0 - alpha) * img1[:, :, 2] + alpha * warped[:, :, 2]


# Write image to disk
# cv.imwrite("img01.jpg", output)
# cv.imwrite("att01.jpg", output_att)
# cv.imshow("Image 1", img0)
# cv.imshow("Image 2", img1)
# cv.imshow("Registered Image", output)
# cv.imshow("Registered Attenuation Image", output_att)
# cv.waitKey(0)
