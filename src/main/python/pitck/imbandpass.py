# imbandpass.py
# Aug 2019
# Marcello DiStasio

import os, re
import numpy  as np

import matplotlib
matplotlib.use('Qt5Agg')
import pylab as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import imageio

from skimage.color import rgb2hed
from skimage.filters import thresholding

class ImageOperations():

    def __init__(self):
        self.ChannelOfInterest = 2

    def processImage(self,fname):

        self.iminput = np.array(imageio.imread(fname))
        ihc_hed = rgb2hed(self.iminput)
        ihc_hed_scaled = self.scaleChannel(ihc_hed[:,:,self.ChannelOfInterest])
        ihc_hed_scaled_bandpassed = self.bandPass(ihc_hed_scaled)
        ihc_hed_scaled_bpdiff = ihc_hed_scaled - ihc_hed_scaled_bandpassed
        diffmean = np.sum(np.abs(ihc_hed_scaled_bpdiff))/np.size(ihc_hed_scaled_bpdiff)
        density_index = 1 - diffmean

        return {'density_index': density_index, 'bpdiffim': ihc_hed_scaled_bpdiff}

    def scaleChannel(self, img):
        #out = np.empty_like(img)
        #        for chan in np.arange(0,np.shape(img)[len(np.shape(img))-1]):
        # x = img[:,:,self.ChannelOfInterest]
        # out[:,:,self.ChannelOfInterest] = (x-np.min(x))/np.ptp(x)
        x = img
        return (x-np.min(x))/np.ptp(x)

    def normChannels(self, img):
        out = np.empty_like(img)
        for chan in np.arange(0,np.shape(img)[len(np.shape(img))-1]):
            x = img[:,:,chan]
            out[:,:,chan] = (x-np.mean(x))/np.std(x)
            return out

    def bandpassChannels(self, img):
        out = np.empty_like(img)
        for chan in np.arange(0,np.shape(img)[len(np.shape(img))-1]):
            x = img[:,:,chan]
            out[:,:,chan] = bandPass(x)
            return out

    def thresholdChannels(self, img):
        out = np.empty_like(img)
        for chan in np.arange(0,np.shape(img)[len(np.shape(img))-1]):
            x = img[:,:,chan]
            thr = thresholding.threshold_otsu(x)
            out[:,:,chan] = x > thr
            return out

    def PowerSpectrumImage(self, img):

        ftimage = np.fft.fft2(img)
        ftimage = np.fft.fftshift(ftimage)
        m = int(np.floor(np.shape(ftimage)[0]/2))
        n = int(np.floor(np.shape(ftimage)[1]/2))
        ftimage = np.fliplr(ftimage[0:m,0:n]) #FFT is symmetric about the origin, so just take a quadrant

        PSD2d = np.power(np.abs(ftimage),2)

        side_of_square = min(np.shape(img))
        PSD2d_crop = PSD2d[np.shape(PSD2d)[0]-side_of_square:np.shape(PSD2d)[0],0:side_of_square] # crop to a square (from bottom left)
        PSD2d_crop_norm = (PSD2d_crop-np.mean(PSD2d_crop))/np.std(PSD2d_crop)

        return PSD2d_crop_norm


    def getPolarMean(self, x2d):
        # Project onto polar distance along frequency axis (i.e. 2D -> 1D), with origin at lower left
        a = np.indices(np.shape(x2d))
        rmap = np.flipud(np.floor(np.sqrt(np.power(a[0,:,:],2) + np.power(a[1,:,:],2))))

        r = []
        p = []
        for k in np.unique(rmap):
            r.append(k)
            p.append(np.sum(x2d[rmap==k])/np.sum(rmap==k)) # Mean around the circle

        return r,p

    def getPSDPolarMean(self, image):
        return getPolarMean(PowerSpectrumImage(image))

    def bandPass(self, img, lims = [6,60]):

        # bandPass method
        # 2D bandpass filter (with hard cutoffs; may produce ringing)
        # [6,60] works @ 40x
        # default lims is for images taken from a microscope with a 40x objective

        im_fft = np.fft.fft2(img)

        # Call ff a copy of the original transform. Numpy arrays have a copy
        # method for this purpose.
        im_fft2 = im_fft.copy()

        # Set r and c to be the number of rows and columns of the array.
        r, c = im_fft2.shape

        im_fft2[0:lims[0]] = 0
        im_fft2[lims[1]:r-lims[1]] = 0
        im_fft2[r-lims[0]:r] = 0

        im_fft2[:, 0:lims[0]] = 0
        im_fft2[:, lims[1]:c-lims[1]] = 0
        im_fft2[:, c-lims[0]:c] = 0

        im_new = np.fft.ifft2(im_fft2).real

        return im_new
