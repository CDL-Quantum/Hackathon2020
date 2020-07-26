# This file contains functions which have to do with manipulating RGB images
from PIL import Image
import numpy as np
from math import pi, floor

# the number of possible RGB values used (default would be 256)
r_num = 16
g_num = r_num ** 2
b_num = r_num ** 3

# this function doubles the size of an image with 4 colors, because a 2x2 pixel image is very small
def double_size(im):

	rows = len(im)
	cols = len(im[0])

	new_im = np.zeros(((rows * 2, cols * 2, 3)))

	r = im[0]
	first = r[0]
	second = r[int(cols/2)]

	for i in range(rows):
		for j in range(cols):
			for k in range(3):
				new_im[i][j][k] = first[k]
		for j in range(cols, cols * 2):
			for k in range(3):
				new_im[i][j][k] = second[k]

	r = im[int(rows/2)]
	first = r[0]
	second = r[int(cols/2)]

	for i in range(rows, rows * 2):
		for j in range(cols):
			for k in range(3):
				new_im[i][j][k] = first[k]
		for j in range(cols, cols * 2):
			for k in range(3):
				new_im[i][j][k] = second[k]

	return new_im

# given an rgb image as a regular python list, converts it into a numpy array image
def make_image(rgbs):

	rows = len(rgbs)
	cols = len(rgbs[0])

	new_im = np.zeros(((rows, cols, 3)))

	# convert to numpy array and scale the image back up
	for i in range(rows):
		for j in range(cols):
			for k in range(3):
				new_im[i][j][k] = rgbs[i][j][k]

	new_im = scale_up(new_im)

	return new_im

# This function displays an image and saves it to the current directory
def show_image(pixels):

	# Create a PIL image from the NumPy array
	image = Image.fromarray(pixels.astype('uint8'), 'RGB')

	image.show()

# This function takes an image as a list of RGB values and converts it to a numpy array of RGB values and scales up the values
def scale_up(image):

	rows = len(image)
	cols = len(image[0])
	scale = 256/r_num
	new_im = np.zeros(((rows, cols, 3)))

	for i in range(rows):
		for j in range(rows):
			for k in range(3):
				new_im[i][j][k] = image[i][j][k] * scale

	return new_im

# this function takes an RGB triplet and converts it to an angle in [0, pi/2]
def rgb_to_theta(rgb):

	r, g, b = rgb
	theta = (pi/2) * ((r/r_num) + (g/g_num) + (b/b_num))
	return theta

# this function takes an angle and converts it to an RGB triplett
def theta_to_rgb(theta):

	r = floor(theta/(pi/(r_num * 2)))
	theta = theta - r*(pi/(r_num * 2))

	g = floor(theta/(pi/(g_num * 2)))
	theta = theta - g*(pi/(g_num * 2))

	b = floor(theta/(pi/(b_num * 2)))

	return [r,g,b]

# this function has the image which will be stored and recovered
def get_image():

	pixels = np.array([[[17, 17, 17], [240, 17, 17]], [[17, 240, 17], [17, 17, 240]]])
	scale = 256/r_num

	for i in range(2):
		for j in range(2):
			for k in range(3):
				pixels[i][j][k] = floor(pixels[i][j][k] / scale)

	return pixels