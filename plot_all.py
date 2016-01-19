import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from cov import get_glgb
from plot_cov import get_colorlist

surv_list = ['AODRIFT','GBNCC','GBT350','HTRU-Nh','HTRU-Nl','HTRU-Nm','HTRU-Sh',
               'HTRU-Sl','HTRU-Sm','PALFA-Mi','PALFA-Wi','PMPS','SMPS']

col  = np.loadtxt('color_all.dat',dtype='str')
smin = np.loadtxt('smin_all.dat',dtype='float')
num  = np.loadtxt('num_all.dat',dtype='float')

colorlist = get_colorlist(len(surv_list))			# assign color to each survey

# If generating color plot to show most sensitive survey f(sky position)
patch_list = []
for ss,cc in zip(surv_list,colorlist):
  patch_list.append(mpatches.Patch(color=cc,label=ss))

gl,gb = get_glgb()
deg2rad = np.pi/180.

cm = plt.cm.get_cmap('RdYlBu')
f = plt.figure()
ax = f.add_subplot(111,projection='mollweide')

# To avoid major outliers, find 10th and 90th percentiles of sensitivity distribution
#smin_10 = np.percentile(smin,10.0)
#smin_90 = np.percentile(smin,90.0) 

# Plot covered grid positions (color corresponds to Smin)
#plt.scatter(gl*deg2rad,gb*deg2rad,edgecolor='',s=1.5,c=smin,cmap=cm)  #,vmin=smin_10,vmax=smin_90)
plt.scatter(gl*deg2rad,gb*deg2rad,edgecolor='',s=2.5,c=col)
#cbar = plt.colorbar()
#cbar.set_label(r"S$_{\rm 1400}$ (mJy)")
plt.legend(handles=patch_list,loc=8, ncol=4,fontsize='small',frameon=False,bbox_to_anchor=(0.5,-0.38))  # 8: lower center
plt.grid()
plt.xlabel('Galactic Longitude (deg)')
plt.ylabel('Galactic Latitude (deg)')
plt.title('Sensitivity Map (1400 MHz)')
plt.savefig('all.pdf',format='pdf')
