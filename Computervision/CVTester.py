import cv2
from Computervision.GetPicture import ImageGetter
from Computervision.ColorRecognizer import ColorRecognizer
import time

ColorSetter = ColorRecognizer()

url = "http://192.168.87.123:8080"
picture_path = "Test.jpg"

color = ColorSetter.getColorFromSelectedPart(getPictureFrom="mobile", pictureUrl=url)
colorRange = [int(x)-5 for x in color] + [int(x)+5 for x in color]
vals = ColorSetter.getColorWithTrackbars(getPictureFrom="mobile", pictureUrl=url, initialColorRange=colorRange) 
#vals = ColorSetter.getColorFromSelectedPart(getPictureFrom="file", fileName=picture_path)
print(vals)