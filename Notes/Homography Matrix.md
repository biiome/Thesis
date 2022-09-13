# Homography Matrix
---
[link](https://math.stackexchange.com/questions/2388259/differences-between-homography-and-transformation-matrix)

We have two images of the same place, taken from different angles. We will compute homography **H**. If we now select one pixel with coordinates (x1, y1) from the first image and another pixel (x2,y2) that represents the same point in the original image, we can transform the latter pixel to have the same viewing perspective as the first one by applying **H**:
![[Pasted image 20220913190631.png]]

This is identical to applying transformation matrix, hence homography is just a special case of transformation. While transformation is a very general concept and includes all kinds of conversions, include conversion between coordinate frames, homography is a subset of it, mostly only applied when rotation is needed. 