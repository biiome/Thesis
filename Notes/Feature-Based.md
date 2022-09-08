# Feature Based Registration Algorithms

## Detailed Description
Feature based methods have some advantage over [[pixel based]] methods when we are trying to register pictures that have been shot under different lighting conditions or exposition times, or when the images overlap only partially.

The fundamental steps for feature based image registration are as follows:
**1. Feature Detection** 
* Distinctive objects or features like points, closed-boundary regions, edges, contours, line intersections, corners, etc. are detected.
	* Points are most commonly used for registration because they are easy to locate and descript compared with other features.
* Once identified,  features can be represented by their point representative's centre of gravity, line endings, distinctive point which are called control points (CPs)

**2. Feature Matching**
**3. Transformation Model Estimation**
**4. Image Transformation & Resampling**






## Sources
1. https://docs.opencv.org/4.x/db/d61/group__reg.html
2. https://www.ijedr.org/papers/IJEDR1401064.pdf
