import matplotlib.pyplot as plt
import numpy as np
import survey_sensitivity as ss
from survey import Survey
from radiometer import calcFlux
from cov import get_glgb
from plot_cov import get_colorlist 

# Takes position arrays (alter to take arrays or individual points?) and returns corresponding Tsky
def tsky_glgb(gl,gb,freq):
  tsky_freq = ss.tsky_test(freq)	# Use i, j to get correct Tsky for a given position
  tsky_glgb = []
  for ll, bb in zip(gl,gb):
    i, j = ss.get_ij(ll,bb)
    tsky_glgb.append(tsky_freq[180*int(i)+int(j)])
  return np.array(tsky_glgb)

# Generates an array of Smin given various things
# Can use duty == 0.0 to trigger pulse width calculator...
def Smin(surv_str,duty=0.06):

  s = Survey(surv_str)
  gl,gb = get_glgb()
  Tsky = tsky_glgb(gl,gb,s.freq)
  cov = np.loadtxt(surv_str+'.cov',dtype='float')
  cov_inds = [cov > 0.0]

  # Return an array based on tsky map.
  Smin = calcFlux(s.SNRlimit,
                s.beta,
                s.tsys,
                Tsky,
                s.gain,
                s.npol,
                s.tobs,
                s.bw,
                duty)

  # Print some pertinent information:
  print ''
  print 'Survey:                  '+s.surveyName
  print 'Center frequency (MHz):  '+str(s.freq)
  print 'Tsky mean, median (K):   '+str(np.mean(Tsky[cov_inds]))+', '+str(np.median(Tsky[cov_inds]))
  print 'Smin mean, median (mJy): '+str(np.mean(Smin[cov_inds]))+', '+str(np.median(Smin[cov_inds]))
  print ''

  # Set positions without coverage == 999999.0
  not_cov_inds = [cov == 0.0]
  Smin[not_cov_inds] = 999999.0

  return Smin


if __name__ == "__main__":

  surv_list = ['AODRIFT','GBNCC','GBT350','HTRU-Nh','HTRU-Nl','HTRU-Nm','HTRU-Sh',
               'HTRU-Sl','HTRU-Sm','PALFA-Mi','PALFA-Wi','PMPS','SMPS']

  #"""
  # Added to compare survey sensitivities
  desired_frequency = 900.0
  colorlist        = get_colorlist(len(surv_list))			# assign color to each survey
  surv_obj_list    = [Survey(s) for s in surv_list]			# list of survey objects
  surv_cfreq_list  = [s.freq for s in surv_obj_list]			# get c_freq from each survey
  seff_factor_list = [(f/desired_frequency)**1.4 for f in surv_cfreq_list]		# convert S_xxx to desired frequency  

  surv_sens_list  = []
  for surv_str in surv_list:
    smin = Smin(surv_str) 
    surv_sens_list.append(smin)

  gl,gb = get_glgb()
  smin_overall = np.zeros(len(gl))+999999.0	# Set index to lowest smin.
  survey_color = ['black']*len(gl)		# Set index to most sensitive survey color.
  num_overall  = np.zeros(len(gl))		# Set index to number of surveys that overlap.

  # Determine most sensitive survey, redundancies, etc.
  for ii in range(len(surv_list)):
    print surv_list[ii],seff_factor_list[ii]
    for jj in range(len(gl)):
      if surv_sens_list[ii][jj] < 999999.0:	# First count coverage/sky position
        num_overall[jj] += 1.0
        fac = seff_factor_list[ii]		# Use to convert to "effective sensitivity" (1400 MHz)
        if surv_sens_list[ii][jj]*fac < smin_overall[jj]:
          smin_overall[jj] = surv_sens_list[ii][jj]*fac
          survey_color[jj] = colorlist[ii]
      
  file = open('all.dat','w')
  file.write('# '+str(desired_frequency)+'\n')    # Record effective frequency at which all sensitivities are quoted.
  for ss,sc,sn in zip(smin_overall,survey_color,num_overall):
    file.write(str(ss)+'  '+str(sc)+'  '+str(sn)+'\n')
  file.close() 

  #"""

  """
  # Will plot survey sensitivities at their nominal center frequencies.
  ....loop over surveys...
    # Kind of janky just to get c_freq... (fix this)
    s = Survey(surv_str)
    freq_str = str(np.int(s.freq))

    gl,gb = get_glgb()
    deg2rad = np.pi/180.

    cm = plt.cm.get_cmap('RdYlBu')
    f = plt.figure()
    ax = f.add_subplot(111,projection='mollweide')

    # To avoid major outliers, find 10th and 90th percentiles of sensitivity distribution
    smin_10 = np.percentile(smin[inds],10.0)
    smin_90 = np.percentile(smin[inds],90.0) 

    # Plot covered grid positions (color corresponds to Smin)
    plt.scatter(gl[inds]*deg2rad,gb[inds]*deg2rad,edgecolor='',s=1.5,c=smin[inds],cmap=cm,vmin=smin_10,vmax=smin_90)

    cbar = plt.colorbar()
    cbar.set_label(r"S$_{\rm "+freq_str+"}$ (mJy)")

    plt.grid()
    plt.xlabel('Galactic Longitude (deg)')
    plt.ylabel('Galactic Latitude (deg)')
    plt.title(surv_str+' ('+freq_str+' MHz)')
    plt.savefig(surv_str+'_sens.pdf',format='pdf')
  """
