from math import sqrt
import tools
import numpy as np

def fourierEffect(img, steps):
    fImg = np.fft.rfft2(img, axes=(0,1))
    newFimg = fImg
    
    ymax = fImg.shape[0]
    xmax = fImg.shape[1]
    print ""
    for y in range(0, ymax):
        tools.displayPercentage("running Fourier stuff... ", y, ymax)
        for x in range(0, xmax):
            newFimg[y, x, 0] = fImg[y, x][0].real * sqrt(abs(x - (xmax/2))) + fImg[y, x][0].imag
            newFimg[y, x, 1] = fImg[y, x][1].real * sqrt(abs(x - (xmax/2))) + fImg[y, x][1].imag
            newFimg[y, x, 2] = fImg[y, x][2].real * sqrt(abs(x - (xmax/2))) + fImg[y, x][2].imag
            for index, step in enumerate(steps):
                if (x % step == 0):
                   newFimg[y][x][index] = 0

    newImg = np.real(np.fft.irfft2(newFimg, axes=(0,1)))
    return newImg