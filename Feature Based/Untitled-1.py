import os
import cv2 as cv
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askdirectory
from functions import (
    featureExtraction,
    featureMatching,
    absDifference,
    crossCorellation,
)


OCT_Folder_Root = askdirectory(title="Select folder containing OCT images")
OCT_File_List = []
ATT_Folder_Root = "Sample Images\Image_Set_1\Attenuation Images"

for root, dirs, files in os.walk(os.path.abspath(OCT_Folder_Root)):
    for file in files:
        # print(os.path.join(root, file))
        OCT_File_List.append(os.path.join(root, file))

OCT_File_List.reverse()

img0_path = r"C:\Users\Vraj\Documents\Thesis\Image-Algorithm\output.png"
img1_path = r"C:\Users\Vraj\Documents\Thesis\Image-Algorithm\Sample Images\Image_Set_1\OCT Images\OCT_p5.png"
img2_path = r"C:\Users\Vraj\Documents\Thesis\Image-Algorithm\Sample Images\Image_Set_1\OCT Images\OCT_p6.png"

img0 = cv.imread(img0_path)  # 6 prime
img1 = cv.imread(img1_path)  # Image 5
img2 = cv.imread(img2_path)  # Image 6


img0_gray = cv.cvtColor(img0, cv.COLOR_RGB2GRAY)
img1_gray = cv.cvtColor(img1, cv.COLOR_RGB2GRAY)
img2_gray = cv.cvtColor(img2, cv.COLOR_RGB2GRAY)

# Calculate Normalised Crosscorrelation of 2 images
score = crossCorellation(img0, img2)
print(score)


# test = absDifference(img0, img1)
# cv.imshow("test", test)
# cv.waitKey(0)


# for method in methods:
#     print(method)
#     score = cv.matchTemplate(img, template, method)
#     result.append(score)

# print(result)

# features0 = featureExtraction(img0_gray)
# features1 = featureExtraction(img1_gray)
# features2 = featureExtraction(img2_gray)


# matches = featureMatching(features0, features1)
# matches2 = featureMatching(features2, features1)


# print(matches)
# print(matches2)

# homography, _ = cv.findHomography(
#     features0.matched_pts, features1.matched_pts, cv.RANSAC, 5.0
# )


# Prime_Images = [
#     cv.imread("../" + OCT_Folder_Root + list[0]),
# ]

# for i in len(list) - 1:

#     # Convert images to grayscale
#     img0_gray = cv.cvtColor(i, cv.COLOR_RGB2GRAY)
#     img1_gray = cv.cvtColor(i + 1, cv.COLOR_RGB2GRAY)

#     # Extract features
#     features0 = featureExtraction(img0_gray)
#     features1 = featureExtraction(img1_gray)

#     Prime_Images[i + 1] = some_func(prime[i], list[i + 1])


# print(list)
