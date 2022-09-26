# Keypoints
Related: [[Accurate Image Alignment and Registration using OpenCV|Accurate Image Alignment and Registration]], [[Descriptors]]

---
[Source](https://www.educba.com/opencv-keypoint/)
- The distinct features in a given image that makes the image stand out are called keypoints in a given image
- Keypoints of a given image assists us in object detection of comparison of images. There are several algorithms to detect keypoints in a given image
- In order to be able to draw the detected keypoints on a given image, we make use of a function called `drawKeypoints()` function in OpenCV. The `drawKeypoints() `function takes the input image, keypoints, colour and flag as the input.
- The keypoints are scale invariant and are circular
- The `drawKeypoints()` function returns an image with keypoints drawn on the image.

![[Pasted image 20220824004351.png]]

---
[Source](https://answers.opencv.org/question/37985/meaning-of-keypoints-and-descriptors/)
- One important thing to understand is that after extracting the keypoints, you only obtain information about their positions, and sometimes their coverage area
- Depending on the algorithm used to extract  keypoints (SIFT, Harris corners, MSER), you will know some general characteristics of the extracted keypoints but not how different or similar one keypoint is to the other

See [[Descriptors]] to see how different keypoints can be compared