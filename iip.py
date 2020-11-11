# Program for Basic Image Editing!
## IIP Project!

import cv2
import numpy as np
import tkinter
from tkinter import filedialog
from tkinter import *
import os
from PIL import Image
import tkinter.messagebox
import time

BASE_DIR = os.getcwd()

my_image = "WELCOME.jpg"				# Place the name of your image here.
img_path = os.path.join(BASE_DIR, my_image)

# -> Features!
# 1. Histogram Equalization for auto enhancement
# 2. Unsharp Masking for sharpening
# 3. Median Filter	for noise removal
# 4. Simple Averaging Filter 3x3 for smoothening
# 5. Image Negative	for cool image.

def get_mse(imageA):
	global ref_img
	err = np.sum((imageA.astype("float") - ref_img.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	err = round(err, 2)
	return err

def get_File():
	try:
		global img_path, img, board_img, my_board, ref_img, error
		path = tkinter.filedialog.askopenfilename(initialdir =  "/", title = "Select A File", filetype =(("jpeg files","*.jpg"),("png files","*.png"),("all files","*.*")))
		img_path = path
		img = cv2.imread(img_path) 
		ref_img = img.copy()
		cv2.imwrite("temp.png", img)
		error.config(text="SNR: 0")
		board_img = tkinter.PhotoImage(file = img_path)
		my_board.configure(image=board_img)
	except:
		tkinter.messagebox.showinfo("Open Failed!", "Unable to read the image.")

# Histogram Equlaization!
def auto_set():
	global img, my_board, board_img, error
	stack.append(img)
	b,g,r = cv2.split(img)	# Spilliting into 3 components
	eq1 = cv2.equalizeHist(b)
	eq2 = cv2.equalizeHist(g)
	eq3 = cv2.equalizeHist(r)
	hist_eq = cv2.merge((eq1, eq2, eq3))
	mse = get_mse(hist_eq)
	error.config(text = "SNR: " + str(mse))
	img = hist_eq
	cv2.imwrite("temp.png", img)
	board_img = tkinter.PhotoImage(file=r'temp.png')
	my_board.configure(image=board_img)

# Simple Averaging Filter 3x3
def smoothening():
	global img, my_board, board_img, error
	stack.append(img)
	kernel = np.ones((3,3),np.float32)/9
	dst = cv2.filter2D(img,-1,kernel)
	mse = get_mse(dst)
	error.config(text = "SNR: " + str(mse))
	img = dst
	cv2.imwrite("temp.png", img)
	board_img = tkinter.PhotoImage(file=r'temp.png')
	my_board.configure(image=board_img)
	return dst

# Unsharp Masking
def sharpening():
	global img, my_board, board_img, error
	my_img = img
	stack.append(img)
	blur = smoothening()
	mask = cv2.subtract(my_img, blur)
	fin = cv2.add(my_img, mask)
	mse = get_mse(fin)
	error.config(text = "SNR: " + str(mse))
	img = fin
	cv2.imwrite("temp.png", img)
	board_img = tkinter.PhotoImage(file=r'temp.png')
	my_board.configure(image=board_img)

# Median Filter
def noise():
	global img, my_board, board_img, error
	stack.append(img)
	med = cv2.medianBlur(img, 3)
	mse = get_mse(med)
	error.config(text = "SNR: " + str(mse))
	#print(mse)
	img = med
	cv2.imwrite("temp.png", img)
	board_img = tkinter.PhotoImage(file=r'temp.png')
	my_board.configure(image=board_img)

# Exit
def exiter():
	return exit()

# Performs Image Negative
def neg():
	global img, my_board, board_img, error
	stack.append(img)
	neg = 1 - img
	mse = get_mse(neg)
	error.config(text = "SNR: " + str(mse))
	cv2.imwrite("temp.png", neg)
	board_img = tkinter.PhotoImage(file=r'temp.png')
	my_board.configure(image=board_img)
	img = neg

# Undo the last effect
def undo():
	global img, my_board, board_img, error
	if(len(stack)==0):
		tkinter.messagebox.showinfo("Undo Failed!", "All operations have been reverted")
		stack.append(img)
		error.config(text = "SNR: 0")
	else:
		img = stack.pop()
		cv2.imwrite("temp.png", img)
		board_img = tkinter.PhotoImage(file=r'temp.png')
		mse = get_mse(img)
		error.config(text="SNR: " +str(mse))
		my_board.configure(image=board_img)


# Save the Image
def saver():
	global img, my_board, board_img
	dir = os.getcwd()
	cv2.imwrite("new_img.png", img)
	tkinter.messagebox.showinfo("Saved!", "Image has been Sucessfully saved at " + str(dir))

def add_noise():
	global img, my_board, board_img, error
	stack.append(img)
	gauss =  np.random.normal(0, 1, img.size)
	gauss = gauss.reshape(img.shape[0], img.shape[1], img.shape[2]).astype('uint8')
	img_gauss = cv2.add(img, gauss)
	cv2.imwrite("temp.png", img_gauss)
	board_img = tkinter.PhotoImage(file=r'temp.png')
	my_board.configure(image=board_img)
	mse = get_mse(img_gauss)
	error.config(text="SNR: " + str(mse))
	img = img_gauss

stack = []

# Reading the image initially
img = cv2.imread(img_path)
ref_img = img.copy() 
cv2.imwrite("temp.png", img)

# Initializing our window
window = tkinter.Tk()
window.title("Image Editor")

# Dividing the image into two frames
functional_frame = tkinter.Frame(window).pack(side='left')
img_frame = tkinter.Frame(window).pack(side = 'right')
browse_frame = tkinter.Frame(window).pack(side="top")

# Our Image will load in this frame.
board_img = tkinter.PhotoImage(file = os.path.join(BASE_DIR, "temp.png"))
my_board = tkinter.Label(img_frame, image = board_img)
my_board.pack(side = 'right')
error = tkinter.Label(img_frame, text="SNR=0", font=('Candara 15 bold'))
error.place(x=250, y=35)

# All Buttons
welcome = tkinter.Label(browse_frame, text="IIP Project!", font=('Candara 18 bold')).pack()
auto = tkinter.Button(functional_frame, text = "Histogram Equalization", command=lambda: auto_set(), bd=5, width=30, height=2, activebackground='orange').pack()
smooth = tkinter.Button(functional_frame, text = "Averaging Filter", command=lambda: smoothening(), bd=5, width=30, height=2, activebackground='orange').pack()
median = tkinter.Button(functional_frame, text = "Median Filter", command=lambda: noise(), bd=5, width=30, height=2, activebackground='orange').pack()
sharp = tkinter.Button(functional_frame, text = "Unsharp Masking", command=lambda: sharpening(), bd=5, width=30, height=2, activebackground='orange').pack()
negation = tkinter.Button(functional_frame, text = "Negative Image", command=lambda: neg(), bd=5, width=30, height=2, activebackground='orange').pack()
noiser = tkinter.Button(functional_frame, text = "Add Noise", command=lambda: add_noise(), bd=5, width=30, height=2, activebackground='orange').pack()
undoer = tkinter.Button(functional_frame, text = "Undo", command=lambda: undo(), bd=5, width=30, height=2, activebackground='orange').pack()
ss = tkinter.Button(functional_frame, text = "Save", command=lambda: saver(), bd=5, width=30, height=2, activebackground='orange').pack()
end = tkinter.Button(functional_frame, text = "Exit", command=lambda: exiter(), bd=5, width=30, height=2, activebackground='orange').pack()
spacing = tkinter.Label(functional_frame, text=" ", font=('Candara 8')).pack()
browse = tkinter.Button(browse_frame, text = "Browse", command=lambda : get_File(), bd=5, width=15, height=2, activebackground='orange').pack()

# Name of Developers!
spacing = tkinter.Label(functional_frame, text=" ", font=('Candara 8')).pack()
Auth = tkinter.Label(functional_frame, text="Developers: ", font=('Candara 10 bold')).pack()
Dev1 = tkinter.Label(functional_frame, text="Abhay Gupta (17ucc003)", font=('Candara 9')).pack()
Dev2 = tkinter.Label(functional_frame, text="Abhishek Choyal (17ucc005)", font=('Candara 9')).pack()
Dev3 = tkinter.Label(functional_frame, text="Vasundhara Shukla (17ucc065)", font=('Candara 9')).pack()
Dev4 = tkinter.Label(functional_frame, text="Saurabh Sharma (17uec125)", font=('Candara 9')).pack()

# Running our Window
window.mainloop()