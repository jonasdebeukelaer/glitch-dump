
import math
import numpy as np
from scipy import signal
from PIL import Image
import time
import random

import filter1


Im = Image.open("source/brain_sick.jpg")

imageArray = np.array(Im)

#------------------------------------------------------------------------------------

#imageArray = filter1.highPass(imageArray, 100)

#imageArray = filter1.outlines(imageArray, 20, 8, False)

for i in [2]:
	print "loop for %i" % i
	imageArray = filter1.affectOnLineContrast(imageArray, contrast=100, span=(20/i), vertical=False, randomise=True, ifContrastLessThan=False)
	#imageArray = filter1.affectOnLineContrast(imageArray, contrast=50, span=(20/i), vertical=False, randomise=True, ifContrastLessThan=False)



#imageArray = filter1.outlines(imageArray, 10, 20, True)
#imageArray = filter1.affectOnLineContrast(imageArray, contrast=20, span=4, vertical=True, randomise=True, ifContrastLessThan=False)
#imageArray = filter1.mixup(imageArray)
#imageArray = filter1.mixup(imageArray)
#imageArray = filter1.mixup(imageArray)

#imageArray = filter1.offset(imageArray, 10)

#------------------------------------------------------------------------------------

print 'renormalise...'

#print imageArray

imageArray = 255. * imageArray / imageArray.max()

#print imageArray

smooshFaceImage = Image.fromarray(imageArray.astype('uint8'))
smooshFaceImage.save("pic_archive/Smoosh_%s.bmp" % (time.strftime("%y-%m-%d, %H:%M")))



