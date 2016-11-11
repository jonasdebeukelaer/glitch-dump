
import numpy as np
import random
from PIL import Image

import tools
import filter1
import filterFourier
import filterLines


fileName = 'circular'
Im = Image.open("source/%s.jpg" % (fileName))
imageArray = np.array(Im)

#------------------------------------------------------------------------------------

#imageArray = filter1.highPass(imageArray, 100)
#imageArray = filter1.mixup(imageArray)
# for i in range(0, 100):
# 	imageArray = filterFourier.fourierEffect(imageArray, [int(200/(i+1)*2), int(300/(i+1)*2), int(400/(i+1)*2)])
# 	imageArray = filterFourier.fourierEffect(np.transpose(imageArray, (1,0,2)), [int(200/(i+1)*2), int(300/(i+1)*2), int(400/(i+1)*2)])
# 	imageArray = np.transpose(imageArray, (1,0,2))

# 	tools.saveNewFile(imageArray, "frame_%03d" % (i//2), True)
# 	tools.saveNewFile(imageArray, "frame_%03d" % ((199-i)//2), True)
#imageArray = filter1.affectOnLineContrast(imageArray, contrast=100, span=3, vertical=False, randomise=True, ifContrastLessThan=False)
#imageArray = filter1.affectOnLineContrast(imageArray, contrast=100, span=2, vertical=True, randomise=True, ifContrastLessThan=False)
#imageArray = np.transpose(imageArray[::-1], (1, 0, 2))
#imageArray = filter1.affectOnLineContrast(imageArray, contrast=100, span=3, vertical=False, randomise=True, ifContrastLessThan=False)
#imageArray = filter1.affectOnLineContrast(imageArray, contrast=100, span=2, vertical=True, randomise=True, ifContrastLessThan=False)
#imageArray = np.transpose(imageArray, (1, 0, 2))[::-1]

#imageArray = filter1.increaseContrast(imageArray)
#imageArray = filter1.increaseContrast(imageArray)


for i in range(0, 20):
	print "creating img %i" % i

	rContrastFactor = 1 + random.random() + 1

	rLineFactor = int(random.random() * 16 + 0.5)
	rLean = int(random.random()**2 * 4) * (-1)**(int(random.random()*2))
	rSeparateColours = random.random() > 0.7
	rAllowLineMerging = random.random() > 0.8
	print "params: lineFactor %i, lean %i, separateColours %r" % (rLineFactor, rLean, rSeparateColours)

	rContrast = int(random.random() * 200)
	rSpan = int(random.random() * 5)
	rVertical = random.random() > 0.3
	rRandomise = random.random() > 0.8
	rIfContrastLessThan = random.random() > 0.7

	newImageArray = filter1.increaseContrast(imageArray, factor=rContrastFactor)
	newImageArray = filterLines.linify(newImageArray, separateColours=rSeparateColours, lineFactor=rLineFactor, lean=rLean, allowLineMerging=rAllowLineMerging)
	newImageArray = filter1.affectOnLineContrast(newImageArray, contrast=rContrast, span=rSpan, vertical=rVertical, randomise=rRandomise, ifContrastLessThan=rIfContrastLessThan)

	tools.saveNewFile(newImageArray, fileName)


	#TODO MAKE PARAMS CHANGE AS USER GIVES POSITIVE/NEGATIVE FEEDBACK ~~MACHINE LEARNING~~