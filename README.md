# Fruit_Ripenes_Recognition
Determines if a fruit is ripe or not

reference article(s):
http://thesai.org/Downloads/Volume7No5/Paper_69-Detection_and_Counting_of_On_Tree_Citrus_Fruit.pdf


Image references:
https://wikifarmer.com/growing-orange-trees-for-profit/


right number of fruit (how many did it find vs how many are there)
location of the fruit (how close are they to image compared to how far they actually are)
ripeness (if needed)


Installation

This project is compatible with python 2.7 or later.
To run make sure you have the following python modules installed:

- multiprocess
- joblib
- scipy
- numpy
- opencv-python



to run the project

make sure that there is a directory called `images` in the working directory that contains all the .jpg
color images that you wish to check.


This will save all of the intermediaries to a directory called intermediaries  as
"<filename>\_<stepname>.jpg"


The final image that includes all of the circled oranges will be in the directory called final.
