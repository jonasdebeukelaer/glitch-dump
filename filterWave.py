import numpy as np
from tools import wrap, monocrome

def wavify(img, lineCount, overlap=0):
	sparseness = img.shape[0] / lineCount
	
	img = monocrome(img)

	if len(img.shape) == 3:
		img = np.sum(img, axis=2).astype(np.float)
	else:
		img = img.astype(np.float)

	hLineShape = img.shape[1]
	blankHLine = np.zeros((hLineShape))

	lineImg = np.array([ sparsify(x, sparseness, i, blankHLine) for i, x in enumerate(img) ])

	wavyImg = np.zeros((lineImg.shape))
	lineImg = lineImg * 1. / np.max(lineImg)

	maxIndex = [wavyImg.shape[0]-1, wavyImg.shape[1]-1]

	for i, row in enumerate(lineImg):
		if i % sparseness != 0: continue

		for j, element in enumerate(row):
			newYIndex = wrap( maxIndex[0], (i + verticalise(sparseness, element, overlap)))
			wavyImg[newYIndex, j] = 255



	return wavyImg

def sparsify(x, sparseness, index, blankHLine):
	if index % sparseness == 0:
		return x
	else:
		return blankHLine

def verticalise(sparseness, brightness, overlap):
	return -int((brightness-0.5) * sparseness * (1+overlap))