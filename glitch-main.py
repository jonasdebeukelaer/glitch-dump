
import numpy as np
import random
from PIL import Image

import tools
import filter1
import filterFourier
import filterLines
import filterWave
import filterPostProcessing


fileName = 'portait_1.jpg'
Im = Image.open("source/%s" % (fileName))
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


for i in range(0, 1):
	print "creating img %i" % i

	rContrastFactor = 1 + random.random() + 1

	rLineFactor = int(random.random() * 16 + 0.5)
	rLean = int(random.random()**2 * 4) * (-1)**(int(random.random()*2))
	rSeparateColours = random.random() > 0.7
	rAllowLineMerging = random.random() > 0.8
	#print "params: lineFactor %i, lean %i, separateColours %r" % (rLineFactor, rLean, rSeparateColours)

	rContrast = int(random.random() * 200)
	rSpan = int(random.random() * 5)
	rVertical = random.random() > 0.3
	rRandomise = random.random() > 0.8
	rIfContrastLessThan = random.random() > 0.7

	imageArray = filterFourier.blur2D(imageArray, gaussianAccent=180)
	imageArray = filterWave.wavify(imageArray, lineCount=100, overlap=1.8)
	#imageArray = filterPostProcessing.antialiase(imageArray)
	imageArray = filterFourier.blur2D(imageArray, gaussianAccent=400, process="antialiase")

	tools.saveNewFile(imageArray, fileName)


	#TODO MAKE PARAMS CHANGE AS USER GIVES POSITIVE/NEGATIVE FEEDBACK ~~MACHINE LEARNING~~