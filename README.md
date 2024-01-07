Python script quality control XYZ files 
Functionality:
1 dialog box with input,coordinate system selection, report output
2 possibility to input multiple XYZ files
3 check if the coordinates are within the range (bounding box) of the indicated coordinate system EPSG:32633,EPSG:32632,EPSG:2180,EPSG:2178 Bounding box of the systems to find on epsg.io
4 search for minimum,maximum,average height of points for a given XYZ file
5 calculating the average density of points per square meter for a given XYZ file
6 detection of outliers by statistical method
7 report in txt format containing:
File name
Whether it meets the conditions from point 3
listing minimum/maximum/average height
listing the number of lines with outliers from point 6
8 message about completed operation
