[source](https://stackoverflow.com/posts/56901836/timeline)

There is no such thing as "best" feature detector, absolutely speaking, the quality of the matching strongly depends on the specific image and moreover on the parameters you use to configure your detector, although there are feature detectors that objectively have a wider range of conditions in which they work well

- **SURF** and **SIFT** are often considered to be the best feature detectors out there, for good reasons, they are very robust and very fast in most situations, the only scenario I found so far in which they show their weaknesses is with highly detailed targets (electrical boards for instance), but keep in mind that SURF and SIFT are both patent protected so you will have to pay lots of money if your goal involves commercial use

- **FAST** is, as its name suggests, very fast, and very "greedy", it extracts a lot of keypoints compared to other detectors, but it is **not** rotation invariant (meaning that it won't work if the target is rotated respect the reference image). Also it is a just a detector, so you will have to describe the keypoints you extract with some other descriptor, and the matching robustness will depend on this, my advice is to try FREAK or ORB as descriptor both of which gave me good results with FAST

- **BRIEF** has good performance and does extract a lower number of keypoints than FAST, just like FAST it is **not** rotation invariant and does not have a corresponding descriptor

- **ORB** is basically an evolution of the previous 2 detectors (ORB stands for Oriented fast and Rotated Brief) that **is** rotation invariant and also implements its own descriptor, **this is probably the best choice** for general purposes, it is free to use and its robustness is comparable to SIFT/SURF/AKAZE while the performances slightly overcomes them (using default parameters), although the robustness is actually a little inferior in most of the situations, there are specific scenarios in which it overcomes SURF/SIFT/AKAZE (once again electrical boards for instance)

- **BRISK** has a behaviour very similar to ORB with a little more CPU load, since ORB in most cases works better in both terms of robustness and performances people usually end up using ORB instead

- **HOG** (which you mentioned) is actually not meant to be used with features matching, it is more likely suitable for deep learning classification

those are the most popular detectors (and descriptors), there are lots of other detectors (AGAST, GFTT, MSER, STAR, etc.) and descriptors (LATCH, LUCID, DAISY, etc.) which are, in most conditions, inferior to the ones I listed but that can probably fit specific situations better

If you are interested in testing those detectors/descriptors robustness and performances in a quick way I suggest you to download and install Find-Object ([http://introlab.github.io/find-object/](http://introlab.github.io/find-object/)) which lets you benchmark those algorithms through target image matching providing a comfortable interface to do that with ease, also the source code is available on GitHub if you are interested in it ([https://github.com/introlab/find-object](https://github.com/introlab/find-object))