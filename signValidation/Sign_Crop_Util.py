import cv2 as cv
import numpy as np

class Signature:
    def __init__(self, imageName):
        self.imageName = imageName

    def processing(self):

        img = cv.imread(self.imageName, cv.IMREAD_UNCHANGED)

        if np.sum(img) == 0:
            return img

        img = cv.copyMakeBorder(img,5,5,5,5,cv.BORDER_CONSTANT,value=[0,0,0])

        if(len(img.shape) > 2):
            if(img.shape[2] == 4):
                # make a mask of where the transparent pixels are
                trans_mask = img[:, :, 3] == 0

                # replace transparent area with white background
                img[trans_mask] = [255, 255, 255, 255]

                # remove alpha channel from image
                img = cv.cvtColor(img.copy(), cv.COLOR_BGRA2BGR)

            # make the image grayscale
            img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # thresholding and finding contours
        _, thresh = cv.threshold(img, 75, 255, cv.THRESH_BINARY)
        contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        # remove the first contour i.e. the image boundary
        contours.remove(contours[0])

        # store x and y coordinates of the bounding rectangles corresponding to all contours
        min_x = img.shape[1]
        min_y = img.shape[0]
        max_x = 0
        max_y = 0

        for cnt in contours:
            x, y, w, h = cv.boundingRect(cnt)
            if x < min_x:
                min_x = x
            if x+w > max_x:
                max_x = x+w
            if y < min_y:
                min_y = y
            if y+h > max_y:
                max_y = y+h

        # pad the bounding rectangles with 5 pixel thick margin
        if min_y-5 > 0:
            min_y = min_y-5
        else:
            min_y = 0

        if min_x-5 > 0:
            min_x = min_x-5
        else:
            min_x = 0

        if max_y+5 > img.shape[0]:
            max_y = img.shape[0]
        else:
            max_y = max_y+5

        if max_x+5 > img.shape[1]:
            max_x = img.shape[1]
        else:
            max_x = max_x+5

        # crop the image by selecting the extrema dimensions from the set of all bounding rectangles
        thresh = thresh[min_y:max_y, min_x:max_x]
        return thresh