import requests as rq
import cv2
import numpy as np

class ImageGetter:
    #Used to close the camera again, when getting picture from PC camera
    cap = None

    def getMobilePicture(self, pictureUrl):
        """
        Gets the current picture from the stream provided by the app "IP Webcam"
        Input: The url specified in the app on your phone
        Output: OpenCV compatible picture
        """
        
        #Set the url to which you wnat to send a request
        url = pictureUrl + "/shot.jpg" 

        #Request the picture and format it to make it compatible with opencv
        imgResp =  rq.get(url)  
        imgNp = np.array(bytearray(imgResp.content), dtype=np.uint8) 
        img = cv2.imdecode(imgNp, -1) 

        return img

    def getPCPicture(self, cam=0):
        """
        VideoCapture connects with a camera on your PC and can therefore read the images
        Input: cam = Camera ID (0 = default camera)
        Output: OpenCV compatible picture
        """
        if self.cap == None:
            self.cap = cv2.VideoCapture(cam)

        _, frame = self.cap.read()
        
        return frame

    def getFilePicture(self, filePath):
        """
        Get a picture located on your computer (maybe it must be inside your working folder)
        Input: filePath = filename of picture such as "smartphone.jpg" or the total filePath
        Output: OpenCV compatible picture
        """
        return cv2.imread(filePath)

    def closeAll(self):
        if self.cap != None:
            self.cap.release()
            self.cap = None

