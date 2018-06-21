import numpy as np

def highPass(img, cutoff):
  print "running highpass..."
  img = midPass(img, cutoff, 256)

  return img

def lowPass(img, cutoff):
  print "running lowPass..."
  img = midPass(img, 0, cutoff)

  return img

def midPass(img, cutoffLower, cutoffHigher):
  print "running midPass..."

  magImg = np.zeros((img.shape[0], img.shape[1]))
  magImg = (np.amax(img, axis=2)).astype(int)

  cut = np.ones(magImg.shape)
  cut[magImg < cutoffLower] = 0
  cut[magImg > cutoffHigher] = 0

  return cut.astype(bool)