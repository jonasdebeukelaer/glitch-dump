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

def blur2D(img, gaussianAccent=0.4, process="gaussian"):
    if len(img.shape) == 2: 
        return blur2DMonocrome(img, lineCount, sparseness, overlap)
    else:
        img0 = blur2DMonocrome(img[:, :, 0], gaussianAccent, process)
        img1 = blur2DMonocrome(img[:, :, 1], gaussianAccent, process)
        img2 = blur2DMonocrome(img[:, :, 2], gaussianAccent, process)
        img = np.dstack([img0, img1, img2])
        return img

def blur2DMonocrome(img, gaussianAccent, process):
    print ""
    img = tools.monocrome(img)
    fImg = np.fft.rfft2(img, axes=(0,1))

    kernel = createKernel(img.shape, gaussianAccent, process)
    fKernel = np.fft.rfft2(kernel, axes=(0,1))

    newFImg = (fKernel * fImg)

    newImg = np.real(np.fft.irfft2(newFImg, axes=(0,1)))
    return np.fft.ifftshift(newImg)

def createKernel(imgShape, gaussianAccent, process):
    x_ = int(imgShape[0]/2+1)
    y_ = int(imgShape[1]/2+1)
    kernel = np.zeros((imgShape))

    for xIndex, x in enumerate(kernel):
        tools.displayPercentage("running %s blur... " % (process), xIndex, imgShape[0])
        for yIndex, y in enumerate(x):

            kernel[xIndex, yIndex] = gaussian2D(xIndex, yIndex, x_, y_, gaussianAccent)

    return kernel

def gaussian2D(x, y, x_, y_, accent):
    squareX = (1.*(x-x_)/x_)**2
    squareY = (1.*(y-y_)/y_)**2
    return np.exp(-accent * (squareX + squareY)**(0.5))


