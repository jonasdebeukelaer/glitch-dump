import numpy as np
from math import sin, pi
from tools import wrap, monocrome, displayPercentage

def wavifyConstantWave(img, lineCount, overlap=0, constantWaveCount=10):
	return wavify(img, lineCount, overlap=0, constantWave=True, constantWaveCount=constantWaveCount)

def wavify(img, lineCount, overlap=0, constantWave=False, constantWaveCount=0):
	print ""
	sparseness = img.shape[0] / lineCount
	
	if len(img.shape) == 2:	
		return wavifyMonocrome(img, lineCount, sparseness, overlap)
	else:
		img0 = wavifyMonocrome(img[:, :, 0], lineCount, sparseness, overlap, 0, constantWave, constantWaveCount)
		img1 = wavifyMonocrome(img[:, :, 1], lineCount, sparseness, overlap, 0, constantWave, constantWaveCount)
		img2 = wavifyMonocrome(img[:, :, 2], lineCount, sparseness, overlap, 0, constantWave, constantWaveCount)
		img = np.dstack([img0, img1, img2])
		return img

def wavifyMonocrome(img, lineCount, sparseness, overlap, offset, constantWave, constantWaveCount):
	print ""
	img = img.astype(np.float)

	hLineShape = img.shape[1]
	blankHLine = np.zeros((hLineShape))

	lineImg = np.array([ sparsify(x, sparseness, i, blankHLine, offset) for i, x in enumerate(img) ])

	wavyImg = np.zeros((lineImg.shape))
	lineImg = lineImg * 1. / np.max(lineImg)

	maxIndex = [wavyImg.shape[0]-1, wavyImg.shape[1]-1]

	for i, row in enumerate(lineImg):
		displayPercentage("running wavify... ", i, img.shape[0])
		if (i - offset) % sparseness != 0: continue

		for j, element in enumerate(row):
			newYIndex = None
			if not constantWave:
				newYIndex = wrap( maxIndex[0], (i + verticalise(sparseness, element, overlap)))	
			else:
				wavelength = int(1. * maxIndex[1] / constantWaveCount)
				newYIndex = wrap( maxIndex[0], (i + sinVerticalise(sparseness, element, overlap, j, wavelength)))
			
			wavyImg[newYIndex, j] = 255

	return wavyImg

def sparsify(x, sparseness, index, blankHLine, offset):
	if (index - offset) % sparseness == 0:
		return x
	else:
		return blankHLine

def verticalise(sparseness, brightness, overlap):
	return -int((brightness-0.5) * sparseness * (1+overlap))

def sinVerticalise(sparseness, brightness, overlap, j, wavelength):
	vanillaSineWave = sin(2. * pi * j / wavelength)
	return -int((brightness-0.5) * sparseness * (1+overlap)) * vanillaSineWave