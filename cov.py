from survey import Survey
import numpy as np
import matplotlib.pyplot as plt
from convert import galactic2RaDec
import quickNdirty as qd

def avg_offset(fwhm):
  return fwhm/(2.0*np.sqrt(2))

def get_glgb():
  n_elem = 360*180
  gl, gb = np.mgrid[-179.5:180.5:360j,-89.5:90.5:180j]
  gl_1d = np.reshape(gl,n_elem)
  gb_1d = np.reshape(gb,n_elem)
  return gl_1d, gb_1d

def make_cov(surv_str,write_cov=1.0,plot_cov=1.0):
  s = Survey(surv_str)

  # Determine whether to use RA/DEC/gl/gb limits or pointingslist.
  try:
    s.pointingslist.any()
    print 'Using pointing list...'
  # If no 'pointingslist'...
  except AttributeError:
    print 'No pointing list. Using survey limits...'
    pointing_list_exists = 0

    gl,gb = get_glgb()
    X1d,Y1d = gl,gb
    ra,dec = galactic2RaDec(gl,gb)
    cov = np.zeros(len(gl))
    inds = np.arange(len(gl))
    for ii,rr,dd,ll,bb in zip(inds,ra,dec,gl,gb):
      if ll < s.GLmax and ll > s.GLmin:
        if np.absolute(bb) < s.GBmax and np.absolute(bb) > s.GBmin:
          if rr < s.RAmax and rr > s.RAmin:
            if dd < s.DECmax and dd > s.DECmin:
              cov[ii] = 1.0
      else:
        cov[ii] = 0.0

  # Otherwise...
  else:
    pointing_list_exists = 1
    x = s.pointingslist

    gl = x[:,0]
    gb = x[:,1]
    print '	Parsing '+str(len(gl))+' pointings.'

    X1d,Y1d = get_glgb()
    I1d = np.arange(len(X1d))

    fwhm_deg = s.fwhm/60.
    beams_per_sq_deg = 1.0/fwhm_deg**2  
 
    cov = np.zeros(len(X1d))
    for ii,xx,yy in zip(I1d,X1d,Y1d):
      # Is there a pointing nearby?
      test_arr  = qd.ang_offset(gl,gb,xx,yy)		# Find angular offsets between grid point and ALL pointings
      test_inds = [test_arr < 1.0]                      # pointings within 1 deg of test position
      n_nearby  = np.sum(test_inds)
      if n_nearby >= 1:
        if n_nearby > beams_per_sq_deg:
          cov[ii] = 1.0
        else:
          cov[ii] = n_nearby/beams_per_sq_deg

  inds = [cov > 0.0]

  # Write .cov file
  if write_cov == 1.0:
    print '	...writing...'
    print ''
    file = open(surv_str+'.cov','w')
    for pt in cov:
      file.write(str(pt)+'\n')
    file.close()

  # Plot coverage
  if plot_cov == 1.0:
    print '	...plotting...'
    deg2rad = np.pi/180.

    cm = plt.cm.get_cmap('Greys')    # 'RdYlBu'
    f = plt.figure()
    ax = f.add_subplot(111,projection='mollweide')
    
    # Plot grid positions (color corresponds to fractional coverage)
    plt.scatter(X1d[inds]*deg2rad,Y1d[inds]*deg2rad,edgecolor='',s=1,c=cov[inds],cmap=cm)
    cbar = plt.colorbar()

    if pointing_list_exists:
      # Plot pointing positions
      plt.scatter(gl*deg2rad,gb*deg2rad,c='red',edgecolor='',s=fwhm_deg/2.0,alpha=0.25)
    plt.grid()
    plt.xlabel('Galactic Longitude (deg)')
    plt.ylabel('Galactic Latitude (deg)')
    plt.title(surv_str)
    plt.savefig(surv_str+'_cov.pdf',format='pdf')


if __name__ == "__main__":
  surv_list = ['AODRIFT','GBNCC','GBT350','HTRU-Nh','HTRU-Nl','HTRU-Nm',
               'HTRU-Sh','HTRU-Sl','HTRU-Sm','PALFA-Mi','PALFA-Wi','PMPS','SMPS']
  #surv_list = ['AODRIFT','GBNCC','PMSURV']
  for s in surv_list:
    print s
    x = make_cov(s)
