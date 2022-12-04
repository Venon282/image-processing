# -*- coding: utf-8 -*-
"""Td2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oF9dTSevbgdOeSt7Jl_zg2EK5OyVp78F
"""

from math import *
import random
import numpy as np
import matplotlib.pyplot as plt

def display(imglist,size=5, shape=True):
   cols = len(imglist)
   fig = plt.figure(figsize=(size*cols,size*cols))
   for i in range(0,cols):
      a = fig.add_subplot(1, cols, i+1)
      if len(imglist[i].shape) > 2 :
         subfig = plt.imshow(imglist[i], vmin=0.0, vmax=1.0)
      else :
         subfig = plt.imshow(imglist[i],cmap="gray",vmin=0.0, vmax=1.0)
      subfig.axes.get_xaxis().set_visible(False)
      subfig.axes.get_yaxis().set_visible(False)
      if shape == True:
        a.set_title(str(imglist[i].shape))
   plt.show()

def clamp(pixel):
 """Fonction qui retourne une nouveau pixel dans lequel
 les composantes du pixel passé en argument sont
 replacées dans l'intervalle [0,1]"""
 pix = np.copy(pixel)
 for i in range(0,len(pix)):
  if pix[i]<0:
   pix[i] = 0
  else:
   if pix[i]>1:
    pix[i] = 1
 return(pix)

def greyscale(img):
  plt.imsave("images/greyscale.png", img)
  img = plt.imread("images/greyscale.png")
  cols = len(img)
  matrice = np.mat('[0.2126 0.7152 0.0722 ; 0.2126 0.7152 0.0722 ; 0.2126 0.7152 0.0722 ]')
  for i in range(0,cols):
    for j in range(0,cols):
      p = img[i,j]
      matricePixel = np.mat('['+str(p[0])+' ; '+str(p[1])+' ; '+str(p[2])+'')
      calculMatrice = np.dot(  matrice ,  matricePixel  )
      for p2 in range(0,3):
        img[i,j,p2]= calculMatrice[p2]
  return img

def sepia(img):
  plt.imsave("images/sepia.png", img)
  img = plt.imread("images/sepia.png")
  cols = len(img)
  matrice = np.mat('[0.393 0.769 0.189 ; 0.349 0.686 0.168 ; 0.272 0.534 0.131 ]')
  for i in range(0,cols):
   for j in range(0,cols):
     p = img[i,j]
     matricePixel = np.mat('['+str(p[0])+' ; '+str(p[1])+' ; '+str(p[2])+'')
     calculMatrice = np.dot(  matrice ,  matricePixel  )
     for p2 in range(0,3):
       img[i,j,p2]= clamp(calculMatrice[p2])
  return img

def mix(img,img2,factor):
  plt.imsave("images/mix.png", img)
  img = plt.imread("images/mix.png")
  cols = len(img)
  for i in range(0,cols):
   for j in range(0,cols):
     p,p2 = img[i,j],img2[i,j]
     matricePixel, matricePixel2 = np.mat('['+str(p[0])+' ; '+str(p[1])+' ; '+str(p[2])+''), np.mat('['+str(p2[0])+' ; '+str(p2[1])+' ; '+str(p2[2])+'')
     calculMatrice = factor*matricePixel + (1-factor)*matricePixel2
     for p3 in range(0,3):
       img[i,j,p3]= calculMatrice[p3]
  return img

def multiply(img,img2):
  plt.imsave("images/multiply.png", img)
  img = plt.imread("images/multiply.png")
  cols = len(img)
  for i in range(0,cols):
   for j in range(0,cols):
     p,p2 = img[i,j],img2[i,j]
     matricePixel, matricePixel2 = np.mat('['+str(p[0])+' ; '+str(p[1])+' ; '+str(p[2])+''), np.mat('['+str(p2[0])+' ; '+str(p2[1])+' ; '+str(p2[2])+'')
     for p3 in range(0,3):
       img[i,j,p3]= matricePixel[p3]*matricePixel2[p3]
  return img

img = plt.imread("./images/solo-256px.png")
img2 = plt.imread('./images/logo-starwars-256px.png')

display([img, greyscale(img)], 5)
display([img, sepia(img)], 5)
display([img, mix(img,img2,0.5), img2], 5)
display([img, multiply(img,img2), img2], 5)

#
# RGB to HSL conversion function
# http://www.rapidtables.com/convert/color/rgb-to-hsl.htm
#
# Parameter:
# - pixel: array containing red, green and blue values
#
# Returns:
# array containing hue, saturation and lightness values
#
def rgb2hsl(pixel):
 r=pixel[0]
 g=pixel[1]
 b=pixel[2]

 cmax=max(r,g,b)
 cmin=min(r,g,b)
 delta=cmax-cmin

 # Lightness calculation
 l=(cmax+cmin)/2

 # Saturation calculation
 s=0
 if delta!=0:
  s=delta/(1-abs(2*l-1))
 
 # Hue calculation
 h=0
 if delta!=0:
  if cmax==r:
    h=(((g-b)/delta)%6)*60

 if cmax==g:
  h=(2+(b-r)/delta)*60

 if cmax==b:
  h=(4+(r-g)/delta)*60

 return([h,s,l])

#
# HSL to RGB conversion function
# http://www.rapidtables.com/convert/color/hsl-to-rgb.htm
#
# Parameter:
# - pixel: array containing hue, saturation and lightness values
#
# Returns:
# array containing red, green and blue values
#
def hsl2rgb(pixel):
 h=pixel[0]
 s=pixel[1]
 l=pixel[2]

 c=(1-abs(2*l-1))*s
 x=c*(1-abs((h/60)%2-1))

 r=0
 g=0
 b=0

 if h>=0 and h<60:
  r=c
  g=x

 if h>=60 and h<120:
  r=x
  g=c

 if h>=120 and h<180:
  g=c
  b=x

 if h>=180 and h<240:
  g=x
  b=c

 if h>=240 and h<300:
  r=x
  b=c

 if h>=300 and h<360:
  r=c
  b=x

 m=l-c/2
 return clamp([r+m,g+m,b+m])

def colorize(img,hue):
  #plt.imsave("images/colorize.png", img)
  #img = plt.imread("images/colorize.png")
  imgnew = img.copy()
  cols = len(img)
  for i in range(0,cols):
   for j in range(0,cols):
     hsl = rgb2hsl(img[i,j])
     imgnew[i,j] = hsl2rgb([hue,hsl[1],hsl[2]])
  return imgnew

def saturation(img,m):
  #plt.imsave("images/colorize.png", img)
  #img = plt.imread("images/colorize.png")
  imgnew = img.copy()
  cols = len(img)
  for i in range(0,cols):
   for j in range(0,cols):
     hsl = rgb2hsl(img[i,j])
     imgnew[i,j] = hsl2rgb([hsl[0],m,hsl[2]])
  return imgnew

def gradient(img,centerx,centery,radius):
  imgnew = img.copy()
  cols = len(img)
  for i in range(0,cols):
   for j in range(0,cols):  
     hsl = rgb2hsl(img[i,j])
     l=1-(sqrt(((i-centerx)**2)+(j-centery)**2))/radius
     if hsl[1]<l:
       l=hsl[1]
     imgnew[i,j] = hsl2rgb([hsl[0],hsl[1],l])
  return imgnew

img = plt.imread("./images/solo-256px.png")
img2 = plt.imread('./images/logo-starwars-256px.png')

display([colorize(img,350),colorize(img,200)],5)
display([img,saturation(img,0.5),saturation(img,2)],5)
display([img,gradient(img,90,60,55)],5)

def rgb2cmyb(pixel):
  matriceDe1 = np.mat('[1.0 1.0 1.0  ]')
  matriceRGB = np.mat('['+str(pixel[0])+' '+str(pixel[1])+' '+str(pixel[2])+']')
  resultat = matriceDe1-matriceRGB
  b=resultat[0,0]
  for i in range(0,3):
    if resultat[0,i]<b:
      b=resultat[0,i]
  if b==1:
    for i in range(0,3):
      resultat[i]=0
  else:
    matriceB = np.mat('['+str(b)+' '+str(b)+' '+str(b)+']')
    for i in range(0,3):
      resultat = resultat - matriceB
  return resultat

p1 = [0.2,0.8,0.6]
p2 = rgb2cmyb(p1)
print(p2)