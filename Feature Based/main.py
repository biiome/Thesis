# Imports
import cv2 as cv
import numpy as np
from functions import *
import os
from tkinter import Tk
from tkinter.filedialog import askdirectory

# Load data

## You can set the routes statically by replacing the OCT_Folder_Root and ATT_Folder_Root with the below 2 lines of code
# OCT_Folder_Root = r"C:\Users\Vraj\Documents\Thesis\Image-Algorithm\Sample Images\Image_Set_1\OCT Images"
# ATT_Folder_Root = r"C:\Users\Vraj\Documents\Thesis\Image-Algorithm\Sample Images\Image_Set_1\Attenuation Images"
OCT_Folder_Root = askdirectory(title="Select folder containing OCT images")
ATT_Folder_Root = askdirectory(title="Select folder containing OCT images")
OCT_File_List = []
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

# Set up list of prime images
Registered_OCT = [
    cv.imread(OCT_File_List[0]),
]

# Set up list of registered attenuation images
Registered_ATT = [
    cv.imread(ATT_File_List[0]),
]

# Set up empty list to store homography data
homography_matrix = []

# For all OCT images
for i in range(0, len(OCT_File_List) - 1):
    print(i)
    # Read in image
    img0 = cv.imread(OCT_File_List[i])
    img1 = cv.imread(OCT_File_List[i + 1])
    # att1 = cv.imread(ATT_File_List[i + 1])

    # Convert OCT images to greyscale
    img0_gray = cv.cvtColor(img0, cv.COLOR_RGB2GRAY)
    img1_gray = cv.cvtColor(img1, cv.COLOR_RGB2GRAY)

    # Pass images into feature extraction function
    features0 = featureExtraction(img0_gray)
    features1 = featureExtraction(img1_gray)

    # Match features using feature matching function
    matches = featureMatching(features0, features1)
    print(len(features1.matched_pts))

    # Perform homography calculation using RANSAC to find the transformation matrix
    homography, _ = cv.findHomography(
        features0.matched_pts, features1.matched_pts, cv.RANSAC, 5.0
    )

    # Save calculated homography matrix to homography_matrix list
    homography_matrix.append(homography)

# Multiply all the homography matrix together
final_H = homography_matrix[0]
for h in homography_matrix[1:]:
    final_H = np.matmul(final_H, h)

# Apply homography matrix to original image
img_location = OCT_File_List[0]
img = cv.imread(img_location)

height, width, _ = img.shape

warped = cv.warpPerspective(
    img,
    homography,
    (width, height),
    borderMode=cv.BORDER_CONSTANT,  # need to see if applying a border around the image would be a good idea to avoid errors
    # borderValue=(100, 100, 100, 100),
)

# Rescale image to original dimensions
output = np.zeros((height, width, 3), np.uint8)
alpha = warped[:, :, 2] / 255.0
output[:, :, 0] = (1.0 - alpha) * img0[:, :, 0] + alpha * warped[:, :, 0]
output[:, :, 1] = (1.0 - alpha) * img0[:, :, 1] + alpha * warped[:, :, 1]
output[:, :, 2] = (1.0 - alpha) * img0[:, :, 2] + alpha * warped[:, :, 2]

# Output registered image
cv.imwrite("Registered Image.png", output, [cv.IMWRITE_PNG_COMPRESSION, 0])
img_reference = cv.imread(OCT_File_List[0])
corellation = crossCorellation(img_reference, output)
print(corellation)

# Ignore the section below this.
"""
for i in range(len(homography_matrix)):
    print(i)
    homography = homography_matrix[i]
    img0 = Registered_OCT[i]
    img1 = cv.imread(OCT_File_List[i + 1])

    height, width, _ = img1.shape

    warped = cv.warpPerspective(
        img0,
        homography,
        (width, height),
    )

    # Stretch image back into original dimensions
    output = np.zeros((height, width, 3), np.uint8)
    alpha = warped[:, :, 2] / 255.0
    output[:, :, 0] = (1.0 - alpha) * img1[:, :, 0] + alpha * warped[:, :, 0]
    output[:, :, 1] = (1.0 - alpha) * img1[:, :, 1] + alpha * warped[:, :, 1]
    output[:, :, 2] = (1.0 - alpha) * img1[:, :, 2] + alpha * warped[:, :, 2]

    Registered_OCT.append(output)


count = len(Registered_OCT)

for image in Registered_OCT:
    filename = str(count) + ".png"
    cv.imwrite(filename, image, [cv.IMWRITE_PNG_COMPRESSION, 0])
    count = count - 1

original_image_path = str(len(Registered_OCT)) + ".png"
final_image_path = "1.png"
original_image = cv.imread(original_image_path)
final_image = cv.imread(final_image_path)
corellation = crossCorellation(original_image, final_image)
print(corellation)

"""
