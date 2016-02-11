import numpy as np
import random
import tools

def highPass(img, cutoff):
  print "running highpass..."
  for i in range(0, img.shape[0]):
    for j in range(0, img.shape[1]):
      if img[i, j, 0] < cutoff:
        img[i, j][:] = 0

  return img

def lowPass(img, cutoff):
  print "running lowpass..."
  for i in range(0, img.shape[0]):
    for j in range(0, img.shape[1]):
      if img[i, j, 0] > cutoff:
        img[i, j][:] = 255

  return img

def affectOnLineContrast(img, contrast=10, span=10, vertical=False, randomise=False, ifContrastLessThan=True):
  print "running outlines..."
  if vertical:
    img = np.swapaxes(img, 0, 1)
  newImg = img
  ymax = img.shape[0]
  xmax = img.shape[1]
  for y in range(0, ymax):
    tools.displayPercentage(y, ymax)
    for x in range(span, xmax-span):
      maxVal = 0
      minVal = 255
      avrg = 0
      for i in range(x-span, x+span):
        if img[y, i, 0] > maxVal:
          maxVal = img[y, i, 0]
        elif img[y, i, 0] < minVal:
          minVal = img[y, i, 0]
        avrg += img[y, i, 0]

      avrg /= (span * 2 + 1)

      if ifContrastLessThan == ((maxVal - minVal) < contrast):
        if randomise:
          new_red = int(img[int(y - int(span / 2) + random.random() * span), x, 0] / min(0.003 * x, 20.))
          new_green = int(img[int(y - int(span / 2) + random.random() * span), x, 1] / min(0.003* x, 20.))
          new_blue = int(img[int(y - int(span / 2) + random.random() * span), x, 2] / min(0.003 * x, 20.))
        else:
          new_red = int(1. * (int(img[y, x-1, 0]) + int(img[y, x-2, 0]) + int(img[y, x+1, 0]) + int(img[y, x+2, 0])) / 4)
          new_green = int(1. * (int(img[y, x-1, 1]) + int(img[y, x-2, 1]) + int(img[y, x+1, 1]) + int(img[y, x+2, 1])) / 4)
          new_blue = int(1. * (int(img[y, x-1, 2]) + int(img[y, x-2, 2]) + int(img[y, x+1, 2]) + int(img[y, x+2, 2])) / 4)
          
        newImg[y][x- span:min(x+300, xmax)][:] = [new_red, new_green, new_blue]

  if vertical:
    newImg = np.swapaxes(newImg, 0, 1)

  return newImg

def offset(img, offset):
  print "nah"

def mixup(img):
  print "running mixup..."
  ymax = img.shape[0]
  xmax = img.shape[1]
  newImg = img
  for y in range(0, ymax):
    for x in range(0, xmax):
      if img[y, x, 2] <100 and img[y, x, 1] <100:
        newx = ((x + img[y, x, 2]) * 2) % xmax
        newImg[y, newx][:] = (0.3 * img[y, x][:] + 0.7 * img[y, newx][:])
        newImg[y, x][:] = (0.7 * img[y, x][:] + 0.3 * img[y, newx][:])

  return newImg

