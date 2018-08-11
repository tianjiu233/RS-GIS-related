# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 11:51:47 2018

@author: huijian
"""

import sys

from osgeo import gdal
from osgeo import ogr
from osgeo import gdalconst

def GetImgMetaData(img):
    """
    img: the file_path of Image
    """
    img = gdal.Open(img,gdalconst.GA_ReadOnly)
    geo_transform = img.GetGeoTransform()
    # geo_transform[0]: top left x
    # geo_transform[1]:pixel width
    # geo_transform[2]: 0
    # geo_transform[3]: top left y
    # geo_transform[4]: 0
    # geo_transform[5]:pixel height (negative value)
    # the upper left corner of the upper left pixel is at position (padTranform[0],padTransform[3])
    raster_xy = [img.RasterXSize, img.RasterYSize]
    geo_projection = img.GetProjectionRef()
    return raster_xy,geo_transform,geo_projection

def GetShpMetaData(shp):
    """
    shp: the file_path of shapefile
    """
    driver = ogr.GetDriverByName("ESRI Shapefile")
    ds = driver.Open(shp,0) # 0:read-only, it can be closed with fcn. ds.Destroy()
    if ds is None:
        print("Could not open file")
        sys.exit(1)
        
    layer = ds.GetLayer()
    
    # metadata
    # geom_type
    geom_type = layer.GetGeomType()
    
    # extent
    extent = layer.GetExtent()
    
    # num_of_features
    if False:
    # loop through the features and count them
        num_feats = 0
        feature = layer.GetNextFeature()
        while feature:
            num_feats = num_feats + 1
            feature.Destroy()
            feature = layer.GetNextFeature()
    else:
        num_feats = layer.GetFeatureCount()
        
    # spatialref
    spatial_ref = layer.GetSpatialRef()
    
    ds.Destroy()
    
    return spatial_ref, extent, geom_type, num_feats

def CreateShp(geoms,name,spatial_ref,geom_type):
    """
    geoms: list.
    name: str # like "myshp", but usually there will be a path prefix
    """
    driver = ogr.GetDriverByName("ESRI Shapefile")
    ds = driver.CreateDataSource(name+".shp")
    
    layer = ds.CreateLayer(name, spatial_ref, geom_type)
    
    fieldDefn = ogr.FieldDefn('id', ogr.OFTString)
    fieldDefn.SetWidth(4)
    layer.CreateField(fieldDefn)
    featureDefn = layer.GetLayerDefn()

    feature = ogr.Feature(featureDefn)
    feature.SetGeometry(geoms)
    feature.SetField('id', 0)
    
    layer.CreateFeature(feature)
    # close ds
    ds.Destroy()

if __name__=="__main__":
    
    jpg_file = "./lds-canterbury-03m-rural-aerial-photos-2015-16-JPEG/RGB_BX23_5K_0306.jpg"
    shp_file = "./lds-nz-building-outlines-pilot-SHP/nz-building-outlines-pilot.shp"
    
    # get the information about the raster file
    raster_xy, geo_transform, geo_projection = GetImgMetaData(img=jpg_file)
    raster_x_size = raster_xy[0]
    raster_y_size = raster_xy[1]
    
    # get the information about the shapefile
    spatial_ref, extent, geom_type, num_feats = GetShpMetaData(shp=shp_file)
    
    # build or choose the features/geometry
    driver = ogr.GetDriverByName("ESRI Shapefile")
    ds = driver.Open(shp_file,0) # 0:read-only, it can be closed with fcn. ds.Destroy()
    layer = ds.GetLayer()
    
    # (1) rectangle
    ring = ogr.Geometry(ogr.wkbLinearRing)
    x = geo_transform[0]
    y = geo_transform[3]
    width = geo_transform[1]
    height = geo_transform[5]

    ring.AddPoint(x,y)
    ring.AddPoint(x+raster_x_size*width,y)
    ring.AddPoint(x+raster_x_size*width,y+raster_y_size*height)
    ring.AddPoint(x,y+raster_y_size*height)

    rectangle = ogr.Geometry(ogr.wkbPolygon)
    rectangle.AddGeometry(ring)
    # poly.ExportToWkt()
    
    # (2) union
    extent_polygon = rectangle.Clone()
    print(layer.GetFeatureCount())
    layer.SetSpatialFilter(extent_polygon)
    print(layer.GetFeatureCount())
    union = ogr.Geometry(3) # polygon
    # do a loop to get a union
    tmp_feat = layer.GetNextFeature()
    while tmp_feat:
        tmp_geom = tmp_feat.GetGeometryRef()
        union = union.Union(tmp_geom)
        tmp_feat.Destroy()
        tmp_feat = layer.GetNextFeature()
    
    # create two shp
    # one is a rectangle, and the other is the union
    reg_shp = "rectangle"
    union_shp = "union"
    
    CreateShp(geoms=rectangle,name="rectangle",spatial_ref=spatial_ref,geom_type=3)
    CreateShp(geoms=union,name="union",spatial_ref=spatial_ref,geom_type=3)
    
