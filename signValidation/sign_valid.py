import cv2 as cv
import os
import signValidation.Sign_Crop_Util as signature
import numpy as np

class Sign_Valid:
	def __init__(self, path):
		self.path = path

	def process(self):

		images = [img for img in os.listdir(self.path) if img.endswith(".png")]

		images.sort()

		solidity = []
		pixel_density = []

		for image in images:

			cnt_area = 0
			hull_area = 0
				
			sign = signature.Signature(os.path.join(self.path, image))

			im = sign.processing()

			if np.sum(im) == 0:
				continue

			#im = cv.resize(im, (350,150))

			contours, _ = cv.findContours(im, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

			# remove the first contour i.e. the image boundary
			contours.remove(contours[0])

			for cnt in contours:
				cnt_area = cnt_area + cv.contourArea(cnt)
				hull = cv.convexHull(cnt)
				hull_area = hull_area + cv.contourArea(hull)

			if hull_area == 0:
				solidity.append(1)
			else:
				solidity.append(float(cnt_area)/float(hull_area))

			dim = im.shape[0]*im.shape[1]
			pixel_density.append(float(dim - cv.countNonZero(im))/float(dim))

			#print(image, '\t', solidity, '\t\t\t', pixel_density, end = '\n\n')

		features = list(zip(solidity, pixel_density))
		return features
