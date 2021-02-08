# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 14:52:54 2021

@author: huijianpzh
"""


"""
Reference:
    https://zhuanlan.zhihu.com/p/110228230
    http://murphylab.web.cmu.edu/publications/boland/boland_node26.html
    https://prism.ucalgary.ca/handle/1880/51900
    https://github.com/LinghuiXia/GLCM
    https://scikit-image.org/docs/0.14.x/api/skimage.feature.html?highlight=grey#skimage.feature.greycoprops
"""
import numpy as np
import matplotlib.pyplot as plt
import cv2
from skimage import data,io
from math import floor,ceil
from skimage.feature import greycomatrix,greycoprops
from skimage.color import rgb2gray

from matplotlib import pyplot as plt

def image_patch(image,slide_window,h,w):
    
    patch = np.zeros((slide_window,slide_window,h,w),dtype=np.uint8)
    for i in range(patch.shape[2]):
        for j in range(patch.shape[3]):
            patch[:,:,i,j] = image[i:i+slide_window,j:j+slide_window]
    return patch

def compute_glcm(image,
               gray_min=0,gray_max=255,nbit=64,
               slide_window=5,step=[2],angle=[0]):
    """
    The image is supposed to be [h,w], a gray image.
    """
    h,w = image.shape[0:2]
    
    # compressed gray range { gray_min:0-->0; gray_max:(256-1)-->(nbit-1)}
    bins = np.linspace(gray_min,gray_max+1,nbit+1)
    image = np.digitize(image,bins) - 1
    
    # (h,w) -> (h+slide_window,w+slide_window) 
    image = cv2.copyMakeBorder(image,
                               floor(slide_window/2),floor(slide_window/2),
                               floor(slide_window/2),floor(slide_window/2),
                               cv2.BORDER_REPLICATE)
    
    patch = image_patch(image,slide_window,h,w)
    
    # calculate GLCM (5,5,512,512) --> (64,64,512,512)
    glcm = np.zeros((nbit,nbit,len(step),len(angle),h,w),dtype=np.uint8)
    for i in range(patch.shape[2]):
        for j in range(patch.shape[3]):
            glcm[:,:,:,:,i,j] = greycomatrix(patch[:,:,i,j],
                                             step,angle,
                                             levels=nbit)
            
    # glcm: [nbit,nbit,len(step),len(angle),h,w], usually the len(step) and len(angle) is 1.
    return glcm

def compute_glcm_feature(glcm):
    """
    glcm:[nbit,nbit,len(step),len(angle),h,w], usually the len(step) and len(angle) is 1.
    """
    nbit,_,len_step,len_angle,h,w = glcm.shape
    # create zeros-array
    contrast = np.zeros(shape=(h,w,len_step,len_angle),dtype=np.float32)
    dissimilarity = np.zeros(shape=(h,w,len_step,len_angle),dtype=np.float32)
    homogeneity = np.zeros(shape=(h,w,len_step,len_angle),dtype=np.float32)
    energy = np.zeros(shape=(h,w,len_step,len_angle),dtype=np.float32)
    correlation = np.zeros(shape=(h,w,len_step,len_angle),dtype=np.float32)
    ASM = np.zeros(shape=(h,w,len_step,len_angle),dtype=np.float32)
    
    for i in range(h):
        for j in range(w):
            contrast[i,j] = greycoprops(glcm[:,:,:,:,i,j],"contrast")
            dissimilarity = greycoprops(glcm[:,:,:,:,i,j],"dissimilarity")
            homogeneity = greycoprops(glcm[:,:,:,:,i,j],"homogeneity")
            energy = greycoprops(glcm[:,:,:,:,i,j],"energy")
            correlation = greycoprops(glcm[:,:,:,:,i,j],"correlation")
            ASM = greycoprops(glcm[:,:,:,:,i,j],"ASM")
    
    """
    contrast = greycoprops(glcm,"constrast")
    dissimilarity = greycoprops(glcm,"dissimilarity")
    homogeneity = greycoprops(glcm,"homogeneity")
    energy = greycoprops(glcm,"energy")
    correlation = greycoprops(glcm,"corellation")
    ASM = greycoprops(glcm,"ASm")
    """
    
    texture = {"contrast":contrast,
               "dissimilarity":dissimilarity,
               "homogeneity":homogeneity,
               "energy":energy,
               "correlation":correlation,
               "ASM":ASM
        }
    
    return texture

if __name__=="__main__":
    print("Testing get_glcm.py")
    
    image_path="part.tif"
    image = io.imread(image_path)
    image = rgb2gray(image) # 0-1
    
    # ------ normalization ------
    image = np.uint8(255.0*(image-np.min(image))/(np.max(image)-np.min(image)))
    h,w = image.shape[0:2]
    # ------ set the hyperparameters ------
    nbit = 64 # gray level
    # the minimum and the maximum gray level
    min_ = 0
    max_ = 255
    slide_window = 7 # slide window
    # step = [2,4,8,16]
    step = [2]
    # angle = [0,np.pi/4,np.pi/2,np.pi*3/4] (also known as direction)
    angle = [0]
    
    # ------ calculate the GLCM ------
    # glcm: [nbit,nbit,len(step),len(angle),h,w], usually the len(step) and len(angle) is 1.
    glcm = compute_glcm(image,min_,max_,nbit,slide_window,step,angle)
    

    texture = compute_glcm_feature(glcm)