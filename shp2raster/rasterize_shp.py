# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 23:36:26 2018

@author: huijian
"""

import sys

from osgeo import gdal
from osgeo import ogr
from osgeo import gdalconst

import numpy as np

from generate_shp import GetImgMetaData


if __name__=="__main__":
    
    # refer image
    ref_img = "./lds-canterbury-03m-rural-aerial-photos-2015-16-JPEG/RGB_BX23_5K_0306.jpg"
    raster_xy, geo_transform, geo_projection = GetImgMetaData(img=ref_img)
    width = geo_transform[1]
    height = geo_transform[5]
    
    # Filename of input OGR file
    shp_fn = 'union.shp'
    
    # Filename of the raster Tiff that will be created
    raster_fn = 'union.tif'
    
    # Open the data source and read in the extent
    source_ds = ogr.Open(shp_fn)
    source_layer = source_ds.GetLayer()
    
    # the extent of the refer image should be taken into consideration.
    raster_x_min = min(raster_xy[0]*width+geo_transform[0],geo_transform[0])
    raster_x_max = max(raster_xy[0]*width+geo_transform[0],geo_transform[0])
    raster_y_min = min(raster_xy[1]*height+geo_transform[3],geo_transform[3])
    raster_y_max = max(raster_xy[1]*height+geo_transform[3],geo_transform[3])
    
    x_min = raster_x_min
    x_max = raster_x_max
    y_min = raster_y_min
    y_max = raster_y_max
    

    # the x_res and y_res should be the same as the refer_image
    target_ds = gdal.GetDriverByName('GTiff').Create(raster_fn, raster_xy[0] ,raster_xy[1], 1, gdal.GDT_Float32)
    # the label raster has the same geo_transform as the original raster
    target_ds.SetGeoTransform(geo_transform)
    target_ds.SetProjection(geo_projection)
    
    # Rasterize
    gdal.RasterizeLayer(target_ds, [1], source_layer, burn_values=[1])
    
    target_ds.FlushCache()
    in_band = target_ds.GetRasterBand(1)
    in_band.SetNoDataValue(0)
    
    # you can check the value with tmp.
    tmp = in_band.ReadAsArray()
    
    source_ds.Destroy()
    target_ds = None