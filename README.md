# BarcodeScan
Barcode detection and scanning



This code helps in locating a barcode present anywhere in an image (Ex: Barcodes printed on product packages.) and decodes the 
value. (Works with Indian Barcodes, i.e. Barcodes starting from digit 8)

---- REQUIREMENTS -----
1. Numpy
2. OpenCv

----- How to Use -----

Inside main.py file provide the path of the image to <b>path</b> variable. And execute the program.

------ FUTURE WORK -------
1. Even though the barcode is detected in a scene, sometimes the edges at extreme ends are not not correct, which leads to incorrect results.
The barcode region needs to be cropped more efficiently.

2. Will modify the decode logic to include barcodes from other other countries apart from India


