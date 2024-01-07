# Python script quality control XYZ files 
Functionality:
* dialog box with input,coordinate system selection, report output
* possibility to input multiple XYZ files
* check if the coordinates are within the range (bounding box) of the indicated coordinate system EPSG:32633,EPSG:32632,EPSG:2180,EPSG:2178 Bounding box of the systems to find on epsg.io
* search for minimum,maximum,average height of points for a given XYZ file
* calculating the average density of points per square meter for a given XYZ file
* detection of outliers by statistical method
* report in txt format containing:
- File name
- Whether it meets the conditions from point 3
- listing minimum/maximum/average height
- listing the number of lines with outliers from point 6
- 8 message about completed operation
