from survey import Survey
import numpy as np
import matplotlib.pyplot as plt

def get_colorlist(length):
  master_list = ['red','green','blue','purple','orange',
		 'fuchsia','gold','navy','lightgreen','plum',
		 'olive','salmon','teal','pink','darkred']
  return master_list[0:length]

def get_glgb():
  n_elem = 360*180
  gl, gb = np.mgrid[-179.5:180.5:360j,-89.5:90.5:180j]
  gl_1d = np.reshape(gl,n_elem)
  gb_1d = np.reshape(gb,n_elem)
  return gl_1d, gb_1d

if __name__ == "__main__":

  deg2rad = np.pi/180.

  survlist  = ['GBNCC','GBT350','AODRIFT','SMPS','PMPS','PALFA-Wi','PALFA-Mi']
  colorlist = get_colorlist(len(survlist))

  f = plt.figure()
  ax = f.add_subplot(111,aspect=1.0)
  gl,gb = get_glgb()

  for s,c in zip(survlist,colorlist):
    cov = np.loadtxt(s+'.cov')
    inds = np.where(cov > 0.0)
    plt.scatter(gl[inds],gb[inds],c=c,edgecolor='')


  plt.xlim([180,-180])
  plt.ylim([-90,90])
  plt.grid()
  #plt.show()
  plt.savefig('total_coverage.pdf',format='pdf')
