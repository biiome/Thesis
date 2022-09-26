# Descriptors
Related: [[Keypoints]], [[Accurate Image Alignment and Registration using OpenCV|Accurate Image Alignment and Registration]]

---
[Source](https://answers.opencv.org/question/37985/meaning-of-keypoints-and-descriptors/)
- Keypoint extraction only provides information about the location of keypoints in the image
- Descriptors are the way to compare the keypoints in an image
- Descriptors summarise, in vector format, some characteristics about the keypoints
	- e.g. intensity in the direction of their most pronounced orientation

- Descriptors should be independent of keypoint position
	- If the same keypoint is extracted at different position (e.g. because of translation) the descriptor should be the same
- Descriptors should be robust against image transformations
	- Examples: contrast, changes in perspective
	- Of course no descriptor is completely robust against all transformation. Different descriptors are designed to be robust against different transformations which is sometimes opposed to the speed they are computed at
- Scale independent

- As the descriptors are vectors of numbers, you can compare them with something as simple as Euclidean distance
- There are some more complex distances that can be used as a similarity measure, of course. But, in the end, you would say that the **keypoints whose descriptors have the smallest distance between them are matches**