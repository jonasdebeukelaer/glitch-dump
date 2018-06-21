import sys, time
from PIL import Image
import imageio

#wrap pixels around edges of the 
def wrap(maxPosition, position):
  if position > maxPosition:
    return position - maxPosition
  elif position < 0:
    return maxPosition + position
  else:
    return position


def displayPercentage( msg, i, total):
  progress = i / (1. * total)
  barLength = 20 # Modify this to change the length of the progress bar
  status = ""
  if isinstance(progress, int):
    progress = float(progress)
  if not isinstance(progress, float):
    progress = 0
    status = "error: progress var must be float\r\n"
  if progress < 0:
    progress = 0
    status = "Halt...\r\n"
  if progress >= 1:
    progress = 1
    status = "Done...\r\n"
  block = int(round(barLength*progress))
  text = msg + "\r[{0}] {1}% {2}".format( "="*block + " "*(barLength-block), int(progress*100), status)
  sys.stdout.write(text)
  sys.stdout.flush()


def saveNewGif(gifImgs, fileName):
  print ""
  print "renormalise and save..."
  fileName = "%s_%s" % (fileName, time.strftime("%y-%m-%d %H_%M_%S"))
  gifImgs = [255. * imageArray / imageArray.max() for imageArray in gifImgs]

  imageio.mimsave("pic_archive/%s.gif" % (fileName), gifImgs, fps=24)

def saveNewFile(imageArray, fileName):
  print ""
  print "renormalise and save..."
  imageArray = 255. * imageArray / imageArray.max()

  if not isForGif:
    fileName = "%s_%s" % (fileName, time.strftime("%y-%m-%d, %H:%M:%S"))

  smooshFaceImage = Image.fromarray(imageArray.astype('uint8'))
  smooshFaceImage.save("pic_archive/%s.png" % (fileName))