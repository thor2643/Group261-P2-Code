import cv2
from Computervision.GetPicture import ImageGetter
import time
import numpy as np

class ColorRecognizer:
    """
    This class provides useful methods to determine the correct color ranges of objects.
    In general the methods return the color values in HSV format (Hue, Saturation and Value)
    """
    ImgGetter = ImageGetter()

    HSVColorRange = [[0, 0, 0, 255, 255, 255]]


    def getColorWithTrackbars(self, getPictureFrom = "pc", fileName = None, PCCamID = 0, pictureUrl = None, initialColorRange = [0, 0, 0, 255, 255, 255]):
        """
        This method makes it easy to try out and retrieve different HSV value ranges
        Inputs:
            @param getPictureFrom can be set to either "pc", "mobile" or "file" depending on how to get the image
            @param initialColorRange array with  with 3 numbers for lower HSV boundaries and 3 number for upper boundary
            @param rest depends on how to get the image

        returns array with color range [LH, LS, LV, UH, US, UV]
        """
        getPictureFrom = getPictureFrom.lower()
        done = False
        colorRange = initialColorRange

        if getPictureFrom == "pc":
            def getImage():
                frame = self.ImgGetter.getPCPicture(PCCamID)
                return frame
        elif getPictureFrom == "mobile":
            def getImage():
                frame = self.ImgGetter.getMobilePicture(pictureUrl)
                return frame
        elif getPictureFrom == "file":
            def getImage():
                frame = self.ImgGetter.getFilePicture(fileName)
                return frame
        else:
            print("Invalid arguments please check your function call")
            return None

        def updateTrackVal(_):
            colorRange[0] = cv2.getTrackbarPos("LH", 'tracking') #får fat i værdien af vores trackbars
            colorRange[1] = cv2.getTrackbarPos("LS", 'tracking')
            colorRange[2] = cv2.getTrackbarPos("LV", 'tracking')

            colorRange[3] = cv2.getTrackbarPos("UH", 'tracking')
            colorRange[4] = cv2.getTrackbarPos("US", 'tracking')
            colorRange[5] = cv2.getTrackbarPos("UV", 'tracking')
        
        def breakLoop(_):
            nonlocal done
            done = True


        names = ["LH", "LS", "LV", "UH", "US", "UV"]
        cv2.namedWindow('tracking')

        for i in range(len(names)):
            cv2.createTrackbar(names[i], "tracking", initialColorRange[i], 255, updateTrackVal)

        cv2.createTrackbar("Save/close", "tracking", 0,1, breakLoop)

        while not done:
            #Get picture and convert to HSV color format
            img = getImage()
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
            #Set upper and lower boundaries
            l_b = np.array([colorRange[0], colorRange[1], colorRange[2]]) 
            u_b = np.array([colorRange[3], colorRange[4], colorRange[5]]) 
        
            #Create the mask according to the tresholds set above (returns 1 if pixel is inside interval and 0 if otherwise)
            mask = cv2.inRange(hsv, l_b, u_b) 

            #compare the original image with the mask by making and bitwise "and" operation
            res = cv2.bitwise_and(img, img, mask=mask)

            cv2.imshow('mask', mask)
            cv2.imshow('res', res)

            key = cv2.waitKey(1)
            if key == 27:
                break
        

        self.ImgGetter.closeAll()
        cv2.destroyWindow("mask")
        cv2.destroyWindow("res")
        cv2.destroyWindow("tracking")

        return colorRange

    
    def getColorFromSelectedPart(self, getPictureFrom = "pc", fileName = None, PCCamID = 0, pictureUrl = None):
        """
        Takes the average HSV value ranges from part of the picture specfied by the mouse.
        Specify the area by dragging the mouse over the wished selection
        Inputs:
            @param getPictureFrom can be set to either "pc", "mobile" or "file" depending on how to get the image
            @param rest depends on how to get the image

        Returns a 3d-array with the average HSV values

        """
        def snap(x):
            nonlocal processing
            processing = True

        def checkForContinue(x):
            nonlocal val, processing
            try:
                cv2.destroyWindow("Cropped image")
                cv2.destroyWindow("tracking")
            except:
                print("No windows open") 
            val = "continue"
            processing = False 

        def checkForDone(x):
            nonlocal done, val
            try:
                cv2.destroyWindow("tracking")
                cv2.destroyWindow("Cropped image")
            except:
                print("No windows open") 
            val = "done"
            done = 1

        def saveColors(x):
            nonlocal cropped_image, HSV_values
            hsv = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2HSV)
            h = 0
            s = 0
            v = 0
            for rows in hsv:
                for col in rows:
                    h += col[0]
                    s += col[1]
                    v += col[2]

            pixels = (hsv.shape[0]*hsv.shape[1])
            avg_h = h/pixels
            avg_s = s/pixels
            avg_v = v/pixels

            HSV_values.append([avg_h, avg_s, avg_v])

        def click_event(event, x, y, flags, param):
            nonlocal x1,y1, img, x2, y2, done, HSV_values, val, cropped_image, processing
            
            val = None
            img2 = img.copy()

            if event == cv2.EVENT_LBUTTONDOWN and processing:
                print("click")
                x1 = x
                y1 = y
            elif event == cv2.EVENT_MOUSEMOVE and x1 >= 0 and x2 < 0:
                cv2.rectangle(img2, (x1,y1), (x, y), (0,255,0), 2)
            elif event == cv2.EVENT_LBUTTONUP and processing:
                cv2.rectangle(img2, (x1,y1), (x, y), (0,255,0), 2)
                x2 = x
                y2 = y

                cropped_image = img[y1:y2, x1:x2]

                cv2.namedWindow('tracking')
                cv2.createTrackbar("Save?", "tracking", 0,1, saveColors)
                cv2.createTrackbar("Continue?", "tracking", 0,1, checkForContinue)
                cv2.createTrackbar("Done?", "tracking", 0,1, checkForDone)

                cv2.imshow("Cropped image", cropped_image)
                cv2.waitKey(10)

                #Gives the user decide whether to save the colors of the specified part or not
                while val == None:
                    cv2.waitKey(1)

                #Reset so another part can be chosen
                if val == "continue":
                    x1, y1, x2, y2 = [-1, -1, -1, -1]
                    img2 = img.copy() 
                    done = False  
                    cv2.setTrackbarPos("Snap", "Take Picture", 0)  
                    processing = False


            cv2.imshow("image", img2)   


        x1, y1, x2, y2 = [-1, -1, -1, -1]
        HSV_values = []
        val = "continue"
        cropped_image = None
        processing = False
        done = False

        #Here the getimage function is defined according to the specified method
        if getPictureFrom == "pc":
            def getImage():
                frame = self.ImgGetter.getPCPicture(PCCamID)
                return frame
        elif getPictureFrom == "mobile":
            def getImage():
                frame = self.ImgGetter.getMobilePicture(pictureUrl)
                return frame
        elif getPictureFrom == "file":
            def getImage():
                frame = self.ImgGetter.getFilePicture(fileName)
                return frame
        else:
            print("Invalid arguments please check your function call")
            return None


        img = getImage()
        cv2.imshow("image", img)

        #Setup an eventobserver on the image windows
        cv2.setMouseCallback('image', click_event) 

        #Create trackbar to take a picture to work with (OpenCV does not support buttons)
        cv2.namedWindow('Take Picture')
        cv2.createTrackbar("Snap", "Take Picture", 0,1, snap)

        #Runs until "done" trackbar is manipulated
        while not done:
            if processing == False:
                img = getImage()
                cv2.imshow("image", img)
            

            key = cv2.waitKey(1)
            if key == 27:
                break
        
        #Under here the average HSV values are calculated and saved to the values list, which is then returned
        h, s, v = [0,0,0]
        for hsv in HSV_values:
            h += hsv[0]
            s += hsv[1]
            v += hsv[2]

        if len(HSV_values) != 0:
            values = [h/len(HSV_values), s/len(HSV_values), v/len(HSV_values)]
        else:
            values = -1

        self.ImgGetter.closeAll()
        cv2.destroyWindow("image")

        return values





