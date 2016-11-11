import numpy as np
import random
import tools
from tools import wrap
import math

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
  if vertical:
    img = np.swapaxes(img, 0, 1)
  newImg = np.asarray(img[:])
  ymax = img.shape[0]-1
  xmax = img.shape[1]-1
  print ""
  for y in range(0, ymax):
    tools.displayPercentage("running outlines... ", y, ymax)
    for x in range(span, xmax-span):
      maxVal = 0
      minVal = 255
      avrg = 0
      for i in range(x-span, x+span):
        if max(img[y, i, 0:2]) > maxVal:
          maxVal = max(img[y, i, 0:2])
        elif min(img[y, i, 0:2]) < minVal:
          minVal = min(img[y, i, 0:2])
        avrg += img[y, i, 0]

      avrg /= (span * 2 + 1)

      if ifContrastLessThan == ((maxVal - minVal) < contrast):
        if randomise:
          randY = int(y - (span / 2) + random.random() * span)
          new_red = getRandomColourFromYSpan(img, randY, x, span, ymax, 0)
          new_green = getRandomColourFromYSpan(img, randY, x, span, ymax, 1)
          new_blue = getRandomColourFromYSpan(img, randY, x, span, ymax, 2)
        else:
          new_red = int(1. * (int(img[wrap(ymax, y), wrap(xmax, x-1), 0]) + int(img[wrap(ymax, y), wrap(xmax-1, x-2), 0]) + int(img[wrap(ymax, y), wrap(xmax, x+1), 0]) + int(img[wrap(ymax, y), wrap(xmax, x+2), 0])) / 4)
          new_green = int(1. * (int(img[wrap(ymax, y), wrap(xmax, x-1), 1]) + int(img[wrap(ymax, y), wrap(xmax-1, x-2), 1]) + int(img[wrap(ymax, y), wrap(xmax, x+1), 1]) + int(img[wrap(ymax, y), wrap(xmax, x+2), 1])) / 4)
          new_blue = int(1. * (int(img[wrap(ymax, y), wrap(xmax, x-1), 2]) + int(img[wrap(ymax, y), wrap(xmax-1, x-2), 2]) + int(img[wrap(ymax, y), wrap(xmax, x+1), 2]) + int(img[wrap(ymax, y), wrap(xmax, x+2), 2])) / 4)
          
        if new_red > 10 or new_green > 10 or new_blue > 10:
          newImg[y][max(x-span, 0):min(x+span, xmax)][:] = [new_red, new_green, new_blue]

  if vertical:
    newImg = np.swapaxes(newImg, 0, 1)

  return newImg

def getRandomColourFromYSpan(img, randY, x, span, ymax, colourNumber):
  return int(img[min(randY, ymax-1), x, colourNumber])

def offset(img, offset):
  print "nah"

def mixup(img):
  weight = 0.4
  cutoff = 200
  print "running mixup..."
  ymax = img.shape[0]
  xmax = img.shape[1]
  newImg = img
  for y in range(0, ymax):
    tools.displayPercentage("running mix up... ", y, ymax)
    for x in range(0, xmax):
      if img[y, x, 2] < cutoff and img[y, x, 1] < cutoff:
        newx = ((x + img[y, x, 2]) * 2) % xmax
        newImg[y, newx][:] = ((1.0 - weight) * img[y, x][:] + weight * img[y, newx][:])
        newImg[y, x][:] = (weight * img[y, x][:] + (1.0 - weight) * img[y, newx][:])

  return newImg

def increaseContrast(img, factor=2):
  ymax = img.shape[0]
  xmax = img.shape[1]
  newImg = img
  print ""
  for y in range(0, ymax):
    tools.displayPercentage("running increase contrast... ", y, ymax)
    for x in range(0, xmax):
      newImg[y, x, 0] = int(img[y, x, 0]**(factor))
      newImg[y, x, 1] = int(img[y, x, 1]**(factor))
      newImg[y, x, 2] = int(img[y, x, 2]**(factor))

  return newImg


