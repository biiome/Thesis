import cv2 as cv

registered_image_path = "C:\\Users\Vraj\OneDrive - The University of Western Australia\\Thesis\\Image-Algorithm\\att01.jpg"
original_image_path = "C:\\Users\Vraj\OneDrive - The University of Western Australia\\Thesis\\Image-Algorithm\\Sample Images\\Image_Set_1\OCT Images\\OCT_p2.png"

# Load Images
registered_image = cv.imread(registered_image_path)
original_image = cv.imread(original_image_path)

# Convert both images to grayscale
registered_image_gray = cv.cvtColor(registered_image, cv.COLOR_RGB2GRAY)
original_image_gray = cv.cvtColor(original_image, cv.COLOR_RGB2GRAY)

# Find absolute difference between the two images
abs_difference = cv.absdiff(registered_image_gray, original_image_gray)
cv.imshow("Absolute Difference Between 2 Images", abs_difference)
cv.waitKey(0)
