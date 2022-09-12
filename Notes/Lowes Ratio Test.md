# Lowes Ratio Test
[link](https://stackoverflow.com/questions/51197091/how-does-the-lowes-ratio-test-work)

***Short Explanation***
Each keypoint in the first image is matched to a number of keypoints from the second image. We keep the 2 best matches for each keypoint (best matches = the ones with the smallest distance measurement). Lowe's test checks that the two distances are sufficiently different. If they are not, the the keypoint is eliminated and will not be used for further calculations.

***Long Explanation***
David Lowe proposed a simple method for filtering keypoint matches by eliminating matches when the second-best match is almost as good.

Let's suppose that L1 is the set of keypoints of image 1, each keypoint having a description that lists information about the keypoint. L2 is the set of keypoints for image 2. A typical matching algorithm will work by finding, for each keypoint in L1, the closest match in L2. If using Euclidian distance, this means that the keypoint from set L2 that has the smallest Euclidian distance from the keypoint in L1.

One would think that we can use a threshold in this situation to eliminate all the pairings where the distance is above that threshold. It is not that simple however as not all variables inside the descriptors are as "discriminant": two keypoints could have a small distance measurement because most of the variables inside their descriptors have similar values, but then those variables could be irrelevant to the actual matching.

Lowe's Method:
First, we match the keypoints in L1 with **two** keypoints in L2. Working from the assumption that a keypoint in image 1 can't have more than one equivalent in image 2, we deduce that those two matches can't both be right - at least one of them is wrong. Following Lowe's reasoning, the match with the smallest distance is the "good" match, and the match with the second-smallest distance is the equivalent of random noise, a base rate of sorts. If the "good" match can't be distinguished from noise, then the "good" match should be rejected because it does not bring anything interesting, information-wise. So the general principle is that there needs to be enough difference between the best and second-best matches.

How the concept of *enough distance* is operationalised is important: Lowe uses a ratio of the two distances:
```python
if distance1 < distance2 * a_constant then ...
```
Where distance1 is the distance between the keypoint and its best match, and distance2 is the distance between the keypoint and its second-best match.

In OpenCV world, the knnMatch function will return the matches from best to worst, so the 1st match will have a smaller distance.