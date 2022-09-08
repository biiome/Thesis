import enum
import os
from functions import featureExtraction, featureMatching
import cv2 as cv
from tkinter import Tk
from tkinter.filedialog import askdirectory


OCT_Folder_Root = askdirectory(title="Select folder containing OCT images")
OCT_File_List = []
ATT_Folder_Root = "Sample Images\Image_Set_1\Attenuation Images"

for root, dirs, files in os.walk(os.path.abspath(OCT_Folder_Root)):
    for file in files:
        # print(os.path.join(root, file))
        OCT_File_List.append(os.path.join(root, file))

OCT_File_List.reverse()


for elem in OCT_File_List:
    print(elem)


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
