# How To Get Started

The code was written and executed on Python 3.10.6. While is should work on all newer versions of Python, if you encounter errors you may want to install this specific version if you encounter errors.

## 1. Install required packages
* Once Python3 is installed we can install the necessary packages required to run the code.
* This is done by opening a terminal windows in the project directory and running the following code:
* 
`pip install -r requirements.txt`

## 2. Running the program
* To run the program you need to execute the main.py file
* To execute the file, open a terminal window in the project directory and run the following code:

`python ./main.py`
* You can also open the file in your code editor of choise and run it through there

## 3. Things to look out for
The program expects to be pointed to a seperate directory containing the image sequence that you want to register. Ensure that ONLY the images you want to register are in that folder and that the images are named is a structed way (e.g. (1.png, 2.png, 3.png) or (a.png, b.png, 3.png)). The program pulls in files alphabetically and so the naming should reflect the sequence in which the images were taken.

If you want to register only a portion of the images in the sequence, simply remove all other images from the folder.
