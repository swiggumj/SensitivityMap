import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from cov import get_glgb
from plot_cov import get_colorlist

surv_list = ['AODRIFT','GBNCC','GBT350','HTRU-Nh','HTRU-Nl','HTRU-Nm','HTRU-Sh',
               'HTRU-Sl','HTRU-Sm','PALFA-Mi','PALFA-Wi','PMPS','SMPS']

col  = np.loadtxt('all.dat', usecols=[1],dtype='str',unpack=True)
smin,ncov = np.loadtxt('all.dat',dtype='float',usecols=[0,2],unpack=True)

# What kind of plot??
# 0: smin, 1: most sensitive survey, 2: redundancy
plot_type = 2

gl,gb = get_glgb()
deg2rad = np.pi/180.

f = plt.figure()
ax = f.add_subplot(111,projection='mollweide')

if plot_type == 0:

  outfile = 'lowest_smin.pdf'
  cm = plt.cm.get_cmap('RdYlBu')

  # To avoid major outliers, find 10th and 90th percentiles of sensitivity distribution
  smin_lo = np.percentile(smin,10.0)
  smin_hi = np.percentile(smin,90.0)
  plt.scatter(gl*deg2rad,gb*deg2rad,edgecolor='',s=1.5,c=smin,cmap=cm,vmin=smin_lo,vmax=smin_hi)
  cbar = plt.colorbar()
  cbar.set_label(r"S$_{\rm 1400}$ (mJy)")
  plt.title('Sensitivity Map (1400 MHz)')

if plot_type == 1:

  outfile = 'most_sensitive_survey.pdf'
  patch_list = []
  colorlist = get_colorlist(len(surv_list))                       # assign color to each survey
  for ss,cc in zip(surv_list,colorlist):
    patch_list.append(mpatches.Patch(color=cc,label=ss))

  plt.scatter(gl*deg2rad,gb*deg2rad,edgecolor='',s=2.5,c=col)
  plt.legend(handles=patch_list,loc=8, ncol=4,fontsize='small',frameon=False,bbox_to_anchor=(0.5,-0.38))  # 8: lower center
  plt.title('Most Sensitive Surveys')

if plot_type == 2:

  outfile = 'redundant_coverage.pdf'
  cm = plt.cm.get_cmap('Greys')
  plt.scatter(gl*deg2rad,gb*deg2rad,edgecolor='',s=2.5,c=ncov/np.float(len(surv_list)),cmap=cm)
  cbar = plt.colorbar()
  cbar.set_label("Fractional Redundancy")
  plt.title('Survey Redundancy')

plt.grid()
plt.xlabel('Galactic Longitude (deg)')
plt.ylabel('Galactic Latitude (deg)')
plt.savefig(outfile,format='pdf')
