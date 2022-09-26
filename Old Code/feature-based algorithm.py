import cv2 as cv
import numpy as np

# Code based on https://www.geeksforgeeks.org/image-registration-using-opencv-python/

# Open the image files
img1 = cv.imread(
    r"C:\Users\Vraj\Documents\Thesis\Image-Algorithm\Sample Images\Test_Images\im1.jpg"
)  # Image to be aligned.
img2 = cv.imread(
    r"C:\Users\Vraj\Documents\Thesis\Image-Algorithm\Sample Images\Test_Images\im2.jpg"
)  # Reference image.
# img3 = cv.imread(
#     "./Sample Images/Image_Set_1/Attenuation_p1.png"
# )  # Matching attenuation image

# Convert images to grayscale
img1_g = cv.cvtColor(img1, cv.COLOR_RGB2GRAY)
img2_g = cv.cvtColor(img2, cv.COLOR_RGB2GRAY)
height, width = img2_g.shape

# Create an ORB detector with 5000 features
orb_detector = cv.ORB_create(5000)

# Find the keypoints and descriptors. First arg is image, second arg is the mask (not required)
kp1, d1 = orb_detector.detectAndCompute(img1_g, None)
kp2, d2 = orb_detector.detectAndCompute(img2_g, None)

# Match features between two images using a Brute Force matcher
matcher = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)

# Match the two sets of descriptors
matches = matcher.match(d1, d2)
matchesList = list(matches)  # converting to list so that we can sort the results

# Sort matches on the basis of their Hamming distance
matchesList.sort(key=lambda x: x.distance)
matches = tuple(matchesList)  # converting back to tuple

# Take the top 90% of matches forward
matches = matches[: int(len(matches) * 0.9)]
no_of_matches = len(matches)

# Define empty matrices of shape no_of_matches * 2
p1 = np.zeros((no_of_matches, 2))
p2 = np.zeros((no_of_matches, 2))

for i in range(len(matches)):
    p1[i, :] = kp1[matches[i].queryIdx].pt
    p2[i, :] = kp2[matches[i].trainIdx].pt

# Find the homography matrix.
homography, mask = cv.findHomography(p1, p2, cv.RANSAC)

# Use this matrix to transform the colored image wrt the reference image.
transformed_img = cv.warpPerspective(img1, homography, (width, height))

# # Use this matrix to transform the attenuation data wrt the reference img
# transformed_attenuation = cv.warpPerspective(img3,
#                     homography, {width,height})

# Save the output.
cv.imwrite("output.jpg", transformed_img)
# cv.imwrite('output.jpg', transformed_attenuation)

crossCorellation = cv.matchTemplate(img2, transformed_img, cv.TM_CCORR_NORMED)
score = "{0:.2%}".format(crossCorellation[0][0])
print(score)
