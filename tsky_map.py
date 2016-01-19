import numpy as np
import survey_sensitivity as ss

# Takes position arrays (alter to take arrays or individual points?) and returns corresponding Tsky
def tsky_glgb(gl,gb,freq):
  tsky_freq = ss.tsky_test(freq)	# Use i, j to get correct Tsky for a given position
  tsky_glgb = []
  for ll, bb in zip(gl,gb):
    i, j = ss.get_ij(ll,bb)
    tsky_glgb.append(tsky_freq[180*int(i)+int(j)])
  return np.array(tsky_glgb)

