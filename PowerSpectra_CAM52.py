# PowerSpectra_CAM52.py
# Marcello DiStasio
# August 2019

import os, re
import numpy as np
import matplotlib
#matplotlib.use('Qt5Agg')
import pylab as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import imageio
from skimage.color import rgb2hed

# Package importa
from pitck import impsd

basedir = '/home/md267/Workspace/Pituitary_CAM52/raw_images/'

ChannelOfInterest = 2

filelist_dot = [os.path.join(basedir,f) for f in os.listdir('/home/md267/Workspace/Pituitary_CAM52/raw_images/') if re.match(r'.*58513.*20x.*\.jpg',f)]
filelist_ring = [os.path.join(basedir,f) for f in os.listdir('/home/md267/Workspace/Pituitary_CAM52/raw_images/') if re.match(r'.*20x.*\.jpg',f) and not re.match(r'.*58513', f)]

y_train = np.concatenate((np.ones(len(filelist_dot)), np.zeros(len(filelist_ring))))

x_train = []
print('Loading Files...')
for fn in np.append(filelist_dot, filelist_ring):
    x_train.append(np.array(imageio.imread(fn)))
print('Loaded.')


print('Color deconvolution...')
ihc_hed = np.array([rgb2hed(x) for x in x_train])
print('Scaling...')
#ihc_hed_scaled = np.array([scaleChannels(x) for x in ihc_hed])
ihc_hed_scaled = np.array([impsd.scaleChannels(x) for x in np.expand_dims(ihc_hed[:,:,:,ChannelOfInterest],3)])
print('Bandpass filtering...')
ihc_hed_scaled_bandpassed = np.array([impsd.bandpassChannels(x) for x in ihc_hed_scaled])

# Subtract the bandpass filtered image from the original image
ihc_hed_scaled_bpdiff = np.squeeze(ihc_hed_scaled - ihc_hed_scaled_bandpassed)

bpdiffmeans = []
for i in np.arange(0,np.shape(ihc_hed_scaled_bpdiff)[0]):
    diffmean = np.sum(np.abs(ihc_hed_scaled_bpdiff[i]))/np.size(ihc_hed_scaled_bpdiff[i])
    bpdiffmeans.append(diffmean)
bpdiffmeans = np.array(bpdiffmeans)








# --------------------------------------------------
# Plotting the results
















# # Fig 1
# fig, ax = plt.subplots()
# ax.plot(r,p_smooth)
# ax.title.set_text('(Densely Granular) - (Sparsely Granular)')


# # Fig 2 - PSDs with colorbars

# fig, ax = plt.subplots(3,2)

# divider = make_axes_locatable(ax[0])
# cax = divider.append_axes('right', size='5%', pad=0.05)
# im = ax[0].imshow(ftmean_dotlike)
# fig.colorbar(im, cax=cax, orientation='vertical')
# ax[0].title.set_text('Densely Granular')

# divider = make_axes_locatable(ax[1])
# cax = divider.append_axes('right', size='5%', pad=0.05)
# im = ax[1].imshow(ftmean_ringlike)
# fig.colorbar(im, cax=cax, orientation='vertical')
# ax[1].title.set_text('Sparsely Granular')

# divider = make_axes_locatable(ax[2])
# cax = divider.append_axes('right', size='5%', pad=0.05)
# im = ax[2].imshow(ftmean_dotlike - ftmean_ringlike)
# fig.colorbar(im, cax=cax, orientation='vertical')
# ax[2].title.set_text('(Densely Granular) - (Sparsely Granular)')

# plt.show()

# plt.savefig('PowerSpectra_Sparsely_vs_Densely_Granular_CAM52.pdf')






# # Fig 3 - PSDs and PSDs integrated around the circle (project onto single (polar) axis)

# fig, ax = plt.subplots(3,6)

# # Col 1
# divider = make_axes_locatable(ax[0,0])
# cax = divider.append_axes('right', size='5%', pad=0.05)
# im = ax[0,0].imshow(ftmean_dotlike)
# fig.colorbar(im, cax=cax, orientation='vertical')
# ax[0,0].title.set_text('Densely Granular')

# divider = make_axes_locatable(ax[1,0])
# cax = divider.append_axes('right', size='5%', pad=0.05)
# im = ax[1,0].imshow(ftmean_ringlike)
# fig.colorbar(im, cax=cax, orientation='vertical')
# ax[1,0].title.set_text('Sparsely Granular')

# divider = make_axes_locatable(ax[2,0])
# cax = divider.append_axes('right', size='5%', pad=0.05)
# im = ax[2,0].imshow(ftmean_dotlike - ftmean_ringlike)
# fig.colorbar(im, cax=cax, orientation='vertical')
# ax[2,0].title.set_text('(Densely Granular) - (Sparsely Granular)')

# # Col 2
# r,p = getPolarMean(ftmean_dotlike)                                                                       
# p_smooth = Smooth(p)
# ax[0,1].plot(r,np.log(p_smooth))
# ax[0,1].title.set_text('mean(Densely Granular)')

# r,p = getPolarMean(ftmean_ringlike)                                                                       
# p_smooth = Smooth(p)
# ax[1,1].plot(r,np.log(p_smooth))
# ax[1,1].title.set_text('mean(Sparsely Granular)')

# r,p = getPolarMean(ftmean_dotlike-ftmean_ringlike)                                                                       
# p_smooth = Smooth(p)
# ax[2,1].plot(r,p_smooth)
# ax[2,1].title.set_text('mean(Densely Granular) - mean(Sparsely Granular)')



# # Col 3
# ax[0,2].plot(Pss_dot.T)
# ax[0,2].title.set_text('Densely Granular')

# ax[1,2].plot(Pss_ring.T)
# ax[1,2].title.set_text('Sparsely Granular')


# # Col 4
# ax[0,3].plot(np.diff(Pss_dot.T,n=1,axis=1))
# ax[0,3].title.set_text('Densely Granular')

# ax[1,3].plot(np.diff(Pss_ring.T,n=1,axis=1))
# ax[1,3].title.set_text('Sparsely Granular')

# # Col 5
# ax[0,4].plot(np.diff(np.diff(Pss_dot.T,n=1,axis=1),n=1,axis=1))
# ax[0,4].title.set_text('Densely Granular')

# ax[1,4].plot(np.diff(np.diff(Pss_ring.T,n=1,axis=1),n=1,axis=1))
# ax[1,4].title.set_text('Sparsely Granular')


# # Col 6
# ax[0,5].plot(Pss_dot.T)
# ax[0,5].title.set_text('Densely Granular')

# ax[1,5].plot(Pss_ring_diffring.T)
# #ax[1,5].set_ylim(-0.000005,0.000005)
# ax[1,5].title.set_text('Sparsely Granular - mean(Sparsely Granular)')

# ax[2,5].plot(Pss_dot_diffring.T)
# #ax[2,5].set_ylim(-0.000005,0.000005)
# ax[2,5].title.set_text('Densely Granular - mean(Sparsely Granular)')


# plt.show()
# plt.savefig('PowerSpectra_Sparsely_vs_Densely_Granular_CAM52.pdf')




# Fig 4

fig, ax = plt.subplots(int(np.ceil(np.sqrt(np.shape(ihc_hed_scaled_bpdiff)[0]))),int(np.ceil(np.sqrt(np.shape(ihc_hed_scaled_bpdiff)[0]))), sharex='col', sharey='row')
for i in np.arange(0,np.shape(ihc_hed_scaled_bpdiff)[0]):
    np.ravel(ax)[i].imshow(ihc_hed_scaled_bpdiff[i,:,:]) 
plt.show()


# Fig 5

# fig, ax = plt.subplots(1,1)
# ax.plot(bpdiffmeans)
# plt.show()








x_p = 1-bpdiffmeans
y_p = y_train

fig, ax = plt.subplots(1,1)
bp0 = ax.boxplot(x_p[np.where(y_p==1)], positions = [1])
dots0 = ax.scatter(1*np.ones(sum(y_p==1)),x_p[np.where(y_p==1)])
bp1 = ax.boxplot(x_p[np.where(y_p==0)], positions = [2])
dots1 = ax.scatter(2*np.ones(sum(y_p==0)),x_p[np.where(y_p==0)])

ax.set_xticklabels(['Densely Granular', 'Sparsely Granular'])
ax.set_ylabel('Density Index')

# Color s
elements = ['boxes','caps','whiskers','medians']
for elem in elements:
    [plt.setp(bp0[elem][idx], color='red') for idx in range(len(bp0[elem]))]
    [plt.setp(bp1[elem][idx], color='blue') for idx in range(len(bp1[elem]))]
plt.show()
