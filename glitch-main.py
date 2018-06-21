
import numpy as np
import random
from PIL import Image
import sys

import tools
import filter1
import filterFourier
import filterLines
import filterBlur
import filterCutoff
import filterWave
import filterPostProcessing


fileName = 'ink'

Im = Image.open("source/%s.jpg" % (fileName))
imageArray = np.array(Im)

def gifGlitch(infile):
    try:
        im = Image.open(infile)
    except IOError:
        print "Can't load gif", infile
        sys.exit(1)
    i = 0
    mypalette = im.getpalette()
    gifImgs = []
    try:
        while i+1:
            im.putpalette(mypalette)
            new_im = Image.new("RGBA", im.size)
            new_im.paste(im)
            imArray = np.array(new_im)
            imArray = imArray[:, :, :-1]
            #imArray = filter1.increaseContrast(imArray, factor=1.8)
            imArray = filterLines.linify(imArray, separateColours=False, lineFactor=4, lean=1, allowLineMerging=True)
            imArray = filter1.affectOnLineContrast(imArray, contrast=150, span=8, vertical=True, randomise=True, ifContrastLessThan=False)
            gifImgs.append(imArray)
            i += 1
            im.seek(im.tell() + 1)

    except EOFError:
        pass # end of sequence
    tools.saveNewGif(gifImgs, fileName)

def imgToGifGlitch(img, rangeMax):
	imgList = []
	for i in range(0, rangeMax):
		print""
		print "creating img %i" % i

		vCutoff = int(255 - abs(255 - ((1.0*i/rangeMax)*510)))
		vSigma = max(0.01, 10 - abs(10 - (1.0*20*i/rangeMax)))
		
		print "params: vCutoff %i, vSigma %i" % (vCutoff, vSigma)

		newImageArray = filterBlur.selectiveBlur(imageArray, splits=2, cutoff=vCutoff, sigma=vSigma)
		imgList.append(int(newImageArray+0.5))

	tools.saveNewGif(imgList, fileName)

#gifGlitch("source/%s.gif" % (fileName))
#imgToGifGlitch(imageArray, 60)


def imgToimg(imageArray):
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

imgToimg(imageArray)


#TODO MAKE PARAMS CHANGE AS USER GIVES POSITIVE/NEGATIVE FEEDBACK ~~MACHINE LEARNING~~


