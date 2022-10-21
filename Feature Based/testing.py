import os
import cv2 as cv
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askdirectory
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
from functions import (
    featureExtraction,
    featureMatching,
    absDifference,
    crossCorellation,
    overlayImages,
)

img0_path = r"C:\Users\Vraj\Documents\Thesis\Image-Algorithm\Sample Images\Image_Set_1\OCT Images\OCT_p7.png"
img1_path = r"C:\Users\Vraj\Documents\Thesis\Image-Algorithm\Sample Images\Image_Set_1\OCT Images\OCT_p5.png"
# img0_path = r"C:\Users\Vraj\Documents\Thesis\Image-Algorithm\7.png"
# img1_path = r"C:\Users\Vraj\Documents\Thesis\Image-Algorithm\Registered Image.png"

img0 = cv.imread(img0_path)
img1 = cv.imread(img1_path)


img0_gray = cv.cvtColor(img0, cv.COLOR_RGB2GRAY)
img1_gray = cv.cvtColor(img1, cv.COLOR_RGB2GRAY)


# for method in methods:
#     print(method)
#     score = cv.matchTemplate(img, template, method)
#     result.append(score)

# print(result)

features0 = featureExtraction(img0_gray)
features1 = featureExtraction(img1_gray)


matches = featureMatching(features0, features1)

# print(matches)

# print(features0.matched_pts)
# print(features1.matched_pts)

# Draw first 30 matches.
# img3 = cv.drawMatches(img0, features0.kps, img1, features1.kps, matches, None, flags=2)

# plt.imshow(img3)
# plt.axis("off")
# plt.show()

homography, _ = cv.findHomography(
    features0.matched_pts, features1.matched_pts, cv.RANSAC, 5.0
)

height, width, _ = img1.shape

warped = cv.warpPerspective(
    img0,
    homography,
    (width, height),
    borderMode=cv.BORDER_CONSTANT,  # need to see if applying a border around the image would be a good idea to avoid errors
    borderValue=(0, 0, 0, 0),
)

output = np.zeros((height, width, 3), np.uint8)
alpha = warped[:, :, 2] / 255.0
output[:, :, 0] = (1.0 - alpha) * img1[:, :, 0] + alpha * warped[:, :, 0]
output[:, :, 1] = (1.0 - alpha) * img1[:, :, 1] + alpha * warped[:, :, 1]
output[:, :, 2] = (1.0 - alpha) * img1[:, :, 2] + alpha * warped[:, :, 2]

# Output registered image
cv.imwrite("test.png", output, [cv.IMWRITE_PNG_COMPRESSION, 0])

# # Canculate Absolute Difference
# absDiff = absDifference(img0, output)

# Overlay Images
overlay = overlayImages(img1, output)

# Calculate Cross Correlation
cross = crossCorellation(img1, output)
print(cross)
