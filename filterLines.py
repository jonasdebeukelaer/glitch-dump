import numpy as np
# import random
from tools import displayPercentage
from tools import wrap
import math

def linify(img, separateColours=False, lineFactor=4, lean=0, allowLineMerging=False, leftOnly=False, straightOnly=False):
	if lineFactor == 0: lineFactor = 1

	print ""

	newImg = np.zeros((img.shape))

	colourMap = {0:"red",1:"blue",2:"green",3:"???"}

	numberOfLines = int(1.0 * img.shape[1] / lineFactor) - 1

	gradientArray = np.zeros((img.shape[0], img.shape[1] - 1, img.shape[2]))
	imgTemp = img[:, 1:, :]
	gradientArray = img[:, :-1, :] - imgTemp

	imgWidth = img.shape[1]-2

	for colour in range(0, 2):
		offset = colour if separateColours else (lineFactor / 2)

		previousPositions = np.zeros((img.shape[0]))
		previousPositions = [x*lineFactor + 1 for x in range(0, numberOfLines)]
		newImg[0, 2::lineFactor, :] = img[0, 2::lineFactor, :]
		for i in range(1, img.shape[0]):
			displayPercentage("running linify for colour %s... " % colourMap[colour], i, img.shape[0])
			for j in range(0, numberOfLines):
				direction = 0
				if leftOnly:
					if gradientArray[i, wrap(imgWidth-1, previousPositions[j]), colour] - gradientArray[i, wrap(imgWidth-1, previousPositions[j]-1), colour] > lean:
						direction = 1
				else:
					if straightOnly:
						gradientDirection = gradientArray[i, wrap(imgWidth-1, previousPositions[j]), colour] - int(gradientArray[i, wrap(imgWidth-1, previousPositions[j]-1), colour])
						if gradientDirection > lean:
							direction = 1
						elif gradientDirection < lean:
							direction = -1
					else:

						direction = int(gradientArray[i, wrap(imgWidth-1, previousPositions[j]), colour] - int(gradientArray[i, wrap(imgWidth-1, previousPositions[j]-1), colour])/500)

				if separateColours:
					newImg[i, wrap(imgWidth, previousPositions[j]+direction), colour] = img[i, wrap(imgWidth, previousPositions[j]+direction), colour]
				else: 
					if straightOnly:
						newImg[i, wrap(imgWidth, previousPositions[j]+direction), 0] = img[i, wrap(imgWidth, previousPositions[j]+direction), 0]
						newImg[i, wrap(imgWidth, previousPositions[j]+direction), 1] = img[i, wrap(imgWidth, previousPositions[j]+direction), 1]
						newImg[i, wrap(imgWidth, previousPositions[j]+direction), 2] = img[i, wrap(imgWidth, previousPositions[j]+direction), 2]
					else:
						newImg[i, previousPositions[j]:wrap(imgWidth, previousPositions[j]+direction), 0] = img[i, wrap(imgWidth, previousPositions[j]+direction), 0]
						newImg[i, previousPositions[j]:wrap(imgWidth, previousPositions[j]+direction), 1] = img[i, wrap(imgWidth, previousPositions[j]+direction), 1]
						newImg[i, previousPositions[j]:wrap(imgWidth, previousPositions[j]+direction), 2] = img[i, wrap(imgWidth, previousPositions[j]+direction), 2]

				if allowLineMerging or previousPositions[wrap(numberOfLines-1, j+1)] > previousPositions[j]:
					previousPositions[j] += direction
					previousPositions[j] = wrap(imgWidth, previousPositions[j])


	return newImg