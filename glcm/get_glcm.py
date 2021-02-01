# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 10:33:23 2021

@author: huijian
"""
import numpy as np
import matplotlib.pyplot as plt
import cv2
from skimage import data,io
from math import floor,ceil
from skimage.feature import greycomatrix,greycoprops
from skimage.color import rgb2gray

def image_patch(image,slide_window,h,w):
    
    patch = np.zeros((slide_window,slide_window,h,w),dtype=np.uint8)
    for i in range(patch.shape[2]):
        for j in range(patch.shape[3]):
            patch[:,:,i,j] = image[i:i+slide_window,j:j+slide_window]
    return patch

def calcu_glcm(image,
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
    return glcm

def calcu_glcm_mean(glcm,nbit=64):
    
    mean = np.zeros((glcm.shape[2],glcm.shape[3]),dtype=np.float32)
    for i in range(nbit):
        for j in range(nbit):
            mean += glcm[i,j]*i/(nbit)**2

    return mean

def calcu_glcm_variance(glcm,nbit=64):
    
    mean = np.zeros(glcm.shape[2],glcm.shape[3],dtype=np.float32)
    for i in range(nbit):
        for j in range(nbit):
            mean += glcm[i,j]*i/(nbit)**2
    variance = np.zeros((glcm.shape[2],glcm.shape[3]),dtype=np.float32)
    for i in range(nbit):
        for j in range(nbit):
            variance += glcm[i,j] * (i-mean)**2
            
    return

def calcu_glcm_homogeneity(glcm,nbit=64):
    
    homogeneity = np.zeros((glcm.shape[2],glcm.shape[3]),dtype=np.float32)
    for i in range(nbit):
        for j in range(nbit):
            homogeneity += glcm[i,j]/(1.+(i-j)**2)
            
    return homogeneity

def calcu_glcm_contrast(glcm,nbit=64):
    
    contrast = np.zeros((glcm.shape[2],glcm.shape[3]),dtype=np.float32)
    for i in range(nbit):
        for j in range(nbit):
            contrast += glcm[i,j]*(i-j)**2
    
    return contrast

def calcu_glcm_dissimilarity(glcm,nbit=64):
    
    dissimilarty = np.zeors((glcm.shape[2],glcm.shape[3]),dtype=np.float32)
    for i in range(nbit):
        for j in range(nbit):
            dissimilarty += glcm[i,j] * np.abs(i-j)
            
    return dissimilarty

def calcu_glcm_energy(glcm, nbit=64):

    energy = np.zeros((glcm.shape[2], glcm.shape[3]), dtype=np.float32)
    for i in range(nbit):
        for j in range(nbit):
            energy += glcm[i, j]**2

    return energy

def calcu_glcm_correlation(glcm, nbit=64):
    
    mean = np.zeros((glcm.shape[2], glcm.shape[3]), dtype=np.float32)
    for i in range(nbit):
        for j in range(nbit):
            mean += glcm[i, j] * i / (nbit)**2

    variance = np.zeros((glcm.shape[2], glcm.shape[3]), dtype=np.float32)
    for i in range(nbit):
        for j in range(nbit):
            variance += glcm[i, j] * (i - mean)**2
    
    correlation = np.zeros((glcm.shape[2], glcm.shape[3]), dtype=np.float32)
    for i in range(nbit):
        for j in range(nbit):
            correlation += ((i - mean) * (j - mean) * (glcm[i, j]**2))/variance

    return correlation

def calcu_glcm_auto_correlation(glcm, nbit=64):

    auto_correlation = np.zeros((glcm.shape[2], glcm.shape[3]), dtype=np.float32)
    for i in range(nbit):
        for j in range(nbit):
            auto_correlation += glcm[i, j] * i * j
    
    return auto_correlation
    
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
    glcm = calcu_glcm(image,min_,max_,nbit,slide_window,step,angle)
    
    # ------ calculate the feature ------
    
    
    # ------ visulization ------
    #plt.subplot(2,5,1)
    
    
    
    
    
    
    
    
    
    
    
    
    
    