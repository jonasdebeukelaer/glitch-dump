import math
import tools
import numpy as np

from filterCutoff import midPass
import filterLines
import filter1

def gaussianBlur(img, sigma=5):
    print ""
    print "Running Gaussian blur..."
    fImgRed = np.fft.rfft2(img[:,:,0], axes=(0,1))
    fImgBlue = np.fft.rfft2(img[:,:,1], axes=(0,1))
    fImgGreen = np.fft.rfft2(img[:,:,2], axes=(0,1))
    
    gShape = img.shape
    muX = int((gShape[0]) / 2)
    muY = int((gShape[1]) / 2)

    gaussian = [[(1.0/(2*math.pi*sigma**2))*math.exp((-1.0)*((i-muY)**2+(j-muX)**2)/(2*sigma**2)) for i in range(gShape[1])] for j in range(gShape[0])]
    gaussian = np.array(gaussian)
    fGaussian = np.fft.rfft2(gaussian, axes=(0,1))

    blurredImg = np.zeros(img.shape)
    blurredImg[:, :, 0] = np.fft.irfft2(fImgRed * fGaussian)
    blurredImg[:, :, 1] = np.fft.irfft2(fImgBlue * fGaussian)
    blurredImg[:, :, 2] = np.fft.irfft2(fImgGreen * fGaussian)
    blurredImg = np.fft.fftshift(blurredImg, axes=(0,1))

    gaussian3 = np.zeros(img.shape)
    gaussian3[:, :, 0] = gaussian
    gaussian3[:, :, 1] = gaussian
    gaussian3[:, :, 2] = gaussian

    blurredImg = 255.0 * blurredImg / blurredImg.max()
    return blurredImg



def selectiveBlur(img, splits=2, cutoff=127, sigma=5):
    print ""
    print "Running Selective blur..."
    interval = int(1.0 * 255 / splits)
    rangesCeiling = [interval * x for x in range(1,splits)]
    imgLayers = []
    originalLayers = []
    # for i, upperBound in enumerate(rangesCeiling):
    #     newImg = midPass(img, upperBound-interval, upperBound)
    #     originalLayers.append(newImg)

    #     newImg = gaussianBlur(newImg, sigma=(5-i))
    #     imgLayers.append(newImg)

    # finalImg = np.zeros(img.shape)
    # for image in imgLayers:
    #     finalImg

    truth1 = midPass(img, 0, cutoff-1)
    truth2 = midPass(img, cutoff, 256)
    img1 = np.array(img)
    img2 = np.array(img)
    img1[truth1 == False] = 0

    img1 = filterLines.linify(img1, separateColours=False, lineFactor=2, lean=1, allowLineMerging=False)
    img1 = filter1.affectOnLineContrast(img1, contrast=50, span=5, vertical=True, randomise=False, ifContrastLessThan=True)
    img1 = gaussianBlur(img1, sigma=sigma)

    

    finalImg = np.array(img1)
    finalImg[truth1 == False] = img2[truth1 == False]



    return finalImg
