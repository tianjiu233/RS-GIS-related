## A bigger shapefile and a small raster

#### background:
When I want to prepare some samples for segmentation, I find some data on [LINZ Data Service](https://data.linz.govt.nz/).<br>
It provides a big vector file and many raster files. And I want to convert ```.shp``` to a ```.tif``` or ```.jpg```, which has the same extent as the certain raster file.

The situation is as follow:
![](https://github.com/huijianpzh/RS-GIS-related/blob/master/shp2raster/pic1.png) 


### steps:
(1) generate shapefile:
For the raster file we have is a georeferenced one, It can provide the geo_extent. <br>
So we could construct a new rectangle vector that shares the same extent as the raster file. <br>
You can get the result.
![](https://github.com/huijianpzh/RS-GIS-related/blob/master/shp2raster/pic5.png) 
Then 
The functin in gdal ```.SetSpatialFilter()``` is used to extract the features(geometries) within rectangle vector from the big vector file. <br>
(a) vector file <br>
![](https://github.com/huijianpzh/RS-GIS-related/blob/master/shp2raster/pic3.png) 
(b) raster file and vector file <br>
![](https://github.com/huijianpzh/RS-GIS-related/blob/master/shp2raster/pic2.png) 

(2) raster shapefile:
