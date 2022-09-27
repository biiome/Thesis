# Notes on article
---
[Link to article](https://magamig.github.io/posts/accurate-image-alignment-and-registration-using-opencv/)
[main.py](file://)

## 1. Introduction
- The first step is computing the projection that established the mathematical relationships which maps pixel coordinates from one image to another.
- The most general planar 2D transformation is the right-parameter perspective transform or homography denoted by a general 3 x 3 matrix $\mathbf{H}$ 

- It operates on 2D homogeneous coordinate vectors, $\mathbf{x’} = (x’,y’,1)$ and $\mathbf{x} = (x,y,1)$, as follows:
$$\mathbf{x’} \sim \mathbf{Hx}$$
- Afterwards, we take the homographic matrix and use it to warp the perspective of one of the images over the other, aligning the images together.
---

## 2. Achieving this using OpenCV
### 2.1 Feature Detection
- To compute the perspective transform matrix $\mathbf{H}$, we need the link both input images and assess which regions are the same.
- We could manually select the corners of each scene/object but this is not ideal as it would require manual work per scene, which is not feasible if we want to process numerous scenes in an automatic manner.
- Therefore,  a feature detection and matching process is used to link common regions in both images.
- The limitation of this technique is that the scene must include *enough* features evenly distributed.
- The method used here was ORB (but other feature extraction methods are also available)

***Code***
```python
img0 = cv.imread("pressue0.jpg, CV.COLOR_BGR2RGBA")
img0 = cv.imread("pressure1, CV.COLOR_BGR2RGBA")
features0 = FeatureExtraction(img0)
features1 = FeatureExtraction(img1)
```

***Inputs***
- Images to register (*e.g. pressure0.jpg, pressure1.jpg*)

***Output***
- [[Keypoints]] - Position of the detected features
- [[Descriptors]] - descriptions of of said feature


### 2.2 Feature Matching
- As stated, the outputs of the `FeatureExtraction` class are the [[Keypoints]] and [[Descriptors]] for both images.
- We now have to pair them up and remove the outliers.
- Firstly, FLANN (Fast Library for Approximate Nearest Neighbours) computes the pairs of matching features whilst taking into account the nearest neighbours of each feature
- Secondly, the best features are selected using the Lowe's ratio of distance test, which aims to eliminate false matches from the previous phase

***Code***
```python
matches = feature_matching(features0, features1)
matched_images = cv.drawMatches (img0, features0.kps, img1, features1.kps, matches None, flags=2)
```

***Inputs***
- [[Keypoints]] and [[Descriptors]]

***Output***
- Pairs of matching features of the input images


### 2.3 Homography Computation
- After computing the pairs of matching features of the input images, it is possible to compute the homography matrix.
- It takes as input the matching points on each image and using RANSAC (random sample consensus) we are able to efficiently compute the [[Projective Matrix]].
- The feature pairs are filtered again at this stage so that only the inliers are used to compute the homography
	- The removes the outliers from the calculation, which leads to a minimisation of the error associated with the homography computation

***Code***
```python
H, _ = cv.findHomography( features0.matched_pts, \
    features1.matched_pts, cv.RANSAC, 5.0)
```

***Inputs***
- Pairs of matching features of the input images

***Outputs***
- [[Transformation matrix]] that establishes the mathematical relationships which maps pixel coordinates from one image to another
- This function outputs the following $3 \times 3$ matrix (for our input):
![[Pasted image 20220822211510.png]]


### 2.4 Perspective Warping & Overlay
- Now that we have calculated the transformation matrix, we can do the image registration process
- The process will do a perspective warp of one of the input images so that it overlaps on the other one
- To verify correct alignment, the outside of the warped image is filled with transparency to allow us to overlay that image over the other image

***Code***
```python
h, w, c = img1.shape
warped = cv.warpPerspective(img0, H, (w, h), \
    borderMode=cv.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
output = np.zeros((h, w, 3), np.uint8)
alpha = warped[:, :, 3] / 255.0
output[:, :, 0] = (1. - alpha) * img1[:, :, 0] + alpha * warped[:, :, 0]
output[:, :, 1] = (1. - alpha) * img1[:, :, 1] + alpha * warped[:, :, 1]
output[:, :, 2] = (1. - alpha) * img1[:, :, 2] + alpha * warped[:, :, 2]
```

***Inputs***
- Original images
- Transformation matrix

***Outputs***
- Final registered image