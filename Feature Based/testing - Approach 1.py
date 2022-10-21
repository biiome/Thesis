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

img1_path = r"C:\Users\Vraj\Documents\Thesis\Image-Algorithm\Registered Image.png"

img0 = cv.imread(img0_path)
img1 = cv.imread(img1_path)


# Canculate Absolute Difference
# absDiff = absDifference(img0, output)

# Overlay Images
overlay = overlayImages(img0, img1)

# Calculate Cross Correlation
cross = crossCorellation(img0, img1)
print(cross)
