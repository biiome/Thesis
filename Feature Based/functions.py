import cv2 as cv
import numpy as np
import copy

# Setup for functions

## Create an ORB detector with 10000 features
orb_detector = cv.ORB_create(
    nfeatures=10000, scaleFactor=1.2, scoreType=cv.ORB_HARRIS_SCORE
)

## Feature Matching setup
LOWES_RATIO = 0.7
MIN_MATCHES = 75
index_params = dict(
    algorithm=6, table_number=6, key_size=10, multi_probe_level=2  # FLANN_INDEX_LSH
)
search_params = dict(checks=50)
flann = cv.FlannBasedMatcher(
    index_params,
    search_params,
)


# Feature detection algorithm
class featureExtraction:
    def __init__(self, img):

        # Create a copy of the input image so that we can have a version that we can modify
        self.img = copy.copy(img)

        # Detect keypoints and descriptors
        self.kps, self.des = orb_detector.detectAndCompute(self.img, None)
        # Draw detected kepoints in source image in new output image
        self.img_kps = cv.drawKeypoints(
            self.img,  # source image
            self.kps,  # keypoints in source image
            0,  # Not quite sure what this is doing here?
            flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,  #
        )
        self.matched_pts = []


def featureMatching(features0, features1):
    matches = []
    # Use FLANN to compute the pairs of matching features
    if features0.des is not None and len(features0.des) > 2:
        all_matches = flann.knnMatch(features0.des, features1.des, k=2)
        # Lowe's test to remove false positives
        try:
            for x, y in all_matches:
                if x.distance < LOWES_RATIO * y.distance:
                    matches.append(x)
        except ValueError:
            pass

        # If number of matches is above specified threshold
        if len(matches) > MIN_MATCHES:
            # Write matches_pts attribute to features object
            features0.matched_pts = np.float32(
                [features0.kps[x.queryIdx].pt for x in matches]
            ).reshape(-1, 1, 2)
            features1.matched_pts = np.float32(
                [features1.kps[x.trainIdx].pt for x in matches]
            ).reshape(-1, 1, 2)

    return matches


def absDifference(image1, image2):
    # Convert images to grayscale
    image1_gray = cv.cvtColor(image1, cv.COLOR_RGB2GRAY)
    image2_gray = cv.cvtColor(image2, cv.COLOR_RGB2GRAY)

    # Take absolute difference of 2 images
    abs_difference = cv.absdiff(image1_gray, image2_gray)

    # Display absolute difference image
    cv.imshow("Absolute Difference Image", abs_difference)
    cv.waitKey(0)
