from __future__ import print_function
from survey import Survey
import numpy as np
import healpy as hp
import matplotlib.pyplot as plt
from convert import galactic2RaDec

#
# COMMENT NEEDED
#
def avg_offset(fwhm):

    return fwhm/(2.0*np.sqrt(2))

def minmax(arr):

    print(min(arr),max(arr))


#
# COMMENT NEEDED
#
def make_cov(surv_str,write_cov=1.0,plot_cov=1.0):

    s = Survey(surv_str)

    # Partition regions of sky with healpy.
    NSIDE = 32 
    NPIX = hp.nside2npix(NSIDE)
    IPIX = np.arange(NPIX)
    theta, phi = hp.pix2ang(nside=NSIDE,ipix=IPIX,lonlat=True)
    X1d,Y1d = theta,phi

    cov = np.zeros(NPIX)
    pixel_resolution = hp.nside2resol(NSIDE, arcmin=True)/60.0
    pixel_area = pixel_resolution ** 2

    # Determine whether to use RA/DEC/gl/gb limits or pointingslist.
    try:
        
        s.pointingslist.any()
        print('Using pointing list...')

    # If no 'pointingslist'...
    except AttributeError:

        print('No pointing list. Using survey limits...')
        pointing_list_exists = 0

        # This is where a 1d sky grid is generated; do this
        # with healpy instead for more "robustness"
        # hp natively assigns 0 < theta (gl) < 360, which 
        # is potentially a problem here...
        # Need to deal with this.

        ra,dec = galactic2RaDec(X1d,Y1d)

        # print(minmax(X1d))
        # print(minmax(ra))

        # NOTE: similar to step below, I may need to
        # take care to make sure GLmin/max and RAmin/max
        # cooperate with native hp theta range (0:360)

        for ii,rr,dd,ll,bb in zip(IPIX,ra,dec,X1d,X1d):

            if ll < s.GLmax and ll > s.GLmin:
                if bb < s.GBmax and bb > s.GBmin:
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

        # This step prevents offsets introduced by
        # different conventions -180:180 vs 0:360 deg.
        gl[gl < 0.] += 360.

        print('	Parsing '+str(len(gl))+' pointings.')
        #minmax(gl)
        #minmax(X1d)

        # Magic: pointing positions -> parent pixel index
        pixel_assignments = hp.pixelfunc.ang2pix(NSIDE,gl,gb,lonlat=True)
        for pa in pixel_assignments: cov[pa] += 1.0

        fwhm_deg = s.fwhm/60.
        beams_per_sq_deg = 1.0/fwhm_deg**2  
        cov /= beams_per_sq_deg 

    inds = [cov > 0.0]

    # Write .cov file
    if write_cov == 1.0:

        print('...writing...')
        print('')
        file = open(surv_str+'.cov','w')
        for pt in cov:
            file.write(str(pt)+'\n')
        file.close()

    # Plot coverage
    if plot_cov == 1.0:
        print('...plotting...')
        deg2rad = np.pi/180.

        cm = plt.cm.get_cmap('Greys')    # 'RdYlBu'
        f = plt.figure()
        ax = f.add_subplot(111,projection='mollweide')
    
        # Plot grid positions (color corresponds to fractional coverage)
        plt.scatter(X1d[inds]*deg2rad,Y1d[inds]*deg2rad,
                    edgecolor='',s=1,c=cov[inds],cmap=cm)
        cbar = plt.colorbar()

        if pointing_list_exists:

            # Plot pointing positions
            plt.scatter(gl*deg2rad,gb*deg2rad,c='red',edgecolor='',
                      s=fwhm_deg/2.0,alpha=0.25)
    
        plt.grid()
        plt.xlabel('Galactic Longitude (deg)')
        plt.ylabel('Galactic Latitude (deg)')
        plt.title(surv_str)
        plt.savefig(surv_str+'_cov.pdf',format='pdf')

    if plot_cov == 2.0:
       
        deg2rad = np.pi/180.
 
        # Re-cast grid...
        PIXINDS = hp.pixelfunc.ang2pix(NSIDE,-1*X1d,Y1d,
                                       lonlat=True)
        cov = cov[PIXINDS]
        hp.mollview(cov)

        # Doesn't *quite* work, but so close.
        # Really need to figure out position convention...

        if pointing_list_exists:

            # Once again:
            gl = -1 * gl
            gl[gl < 0.] += 360.

            # Plot pointing positions
            hp.visufunc.projscatter(gl,gb,
                        alpha=0.2, s=0.2,
                        c='white', lonlat=True)

            hp.visufunc.graticule(c='white',alpha=0.3)

        # plt.grid(True)
        plt.show()

if __name__ == "__main__":

    surv_list = ['AODRIFT']
    for s in surv_list:
        print(s)
        x = make_cov(s,plot_cov=2.0)
