import random
from PIL import Image
import sys

import tools
import filter1
import filterFourier
import filterLines
import filterBlur
import filterCutoff

def randomising(imageArray, fileName):
	for i in range(0, rangeMax):
		print "creating img %i" % i

		rContrastFactor = 1 + random.random()**2
		print "params1: contrastFactor %i" % rContrastFactor

		rLineFactor = int((random.random() + 0.5) * 4)
		rLean = 0 #int(random.random()**2 * 4) * (-1)**(int(random.random()*2))
		rSeparateColours = random.random() > 0.7
		rAllowLineMerging = random.random() > 0.8
		print "params: lineFactor %i, lean %i, separateColours %r, allowLineMerging %r" % (rLineFactor, rLean, rSeparateColours, rAllowLineMerging)

		rContrast = int(random.random() * 200)
		rSpan = max(1, int(random.random() * 5))
		rVertical = random.random() > 0.3
		rRandomise = random.random() > 0.8
		rIfContrastLessThan = random.random() > 0.7
		print "params: contrast %i, span %i, vertical %r, randomise %r, ifContrastLessThan %r" % (rContrast, rSpan, rVertical, rRandomise, rIfContrastLessThan)

		rCutoff = max(150, int(random.random() * 250))
		rSigma = max(1, int(random.random() * 10))

		print "params: rCutoff %i, rSigma %i" % (rCutoff, rSigma)

		#newImageArray = filter1.increaseContrast(imageArray, factor=rContrastFactor)
		#newImageArray = filterLines.linify(imageArray, separateColours=rSeparateColours, lineFactor=rLineFactor, lean=rLean, allowLineMerging=rAllowLineMerging)
		#newImageArray = filter1.affectOnLineContrast(newImageArray, contrast=rContrast, span=rSpan, vertical=rVertical, randomise=rRandomise, ifContrastLessThan=rIfContrastLessThan)
		vCutoff = int(255 - abs(255 - ((1.0*i/rangeMax)*510)))
		vSigma = max(0.01, 10 - abs(10 - (1.0*20*i/rangeMax)))
		
		print "params: vCutoff %i, vSigma %i" % (vCutoff, vSigma)

		newImageArray = filterBlur.selectiveBlur(imageArray, splits=2, cutoff=vCutoff, sigma=vSigma)
		imgList.append(newImageArray)
		#imageArray = filterBlur.selectiveBlur(imageArray, splits=2)

		tools.saveNewFile(imageArray, fileName)