import numpy as np

import tools

def antialiase(img):

	antialiaseOverlay = np.zeros((img.shape))

	for xIndex, row in enumerate(img):
		tools.displayPercentage("running antialiasing... ", xIndex, img.shape[0])
		if (xIndex == 0 or xIndex >= img.shape[0]-1): continue

		for yIndex, elem in enumerate(row):
			if (yIndex == 0 or yIndex >= img.shape[1]-1): continue

			neighbours = [img[xIndex, yIndex-1], img[xIndex, yIndex+1], img[xIndex-1, yIndex], img[xIndex+1, yIndex]]
			averageNeighbour = np.sum(neighbours) * 1. / 4

			if elem < averageNeighbour:
				antialiaseOverlay[xIndex, yIndex] = (elem * 1. + averageNeighbour) / 2

	newImg = img
	newImg[img < antialiaseOverlay] = 120
	return newImg
