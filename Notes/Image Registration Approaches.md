# Images Registration Approaches
---
Image alignment and registration is the process of:
1. Accepting two input images that contain the same object by at slightly different viewing angles
2. Automatically computing the [[homography matrix]] use to align the images
3. Taking the homography matrix and applying a perspective warp to align the image together.

For our purposes, we will also be applying this homography matrix to our attenuation images to allow for accurate registration.

There are a number of image alignment and registration algorithms. The most popular image alignment algorithms are **[[feature-based]]** and include [[keypoint detectors, local invariant descriptors, and keypoint matching]]. 

Medical applications typically use [[similarity measures]] for image registration.

Deep learning can used for image alignment by automatically learning the homography transform.