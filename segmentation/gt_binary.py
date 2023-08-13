#!/usr/bin/env python

from PIL import Image
import numpy as np
#from resizeimage import resizeimage
import os, sys
import operator

def resizeImage(infile, output_dir="", size=(4288,2848)):
     outfile = os.path.splitext(infile)[0]
     extension = os.path.splitext(infile)[1]
    

     if (operator.eq(extension, ".jpg")):
        return

     if infile != outfile:
        try:
            im = Image.open(os.path.join("mask",infile))
           
            #print(imarray)
            gray = im.convert('L')
            bw = gray.point(lambda x: 0 if x<50 else 255, '1')
            # im = resizeimage.resize_cover(im, [960, 640])
            bw.save(output_dir+infile[:-3]+".jpg",quality=100)
        except IOError:
            print ("cannot reduce image for ", infile)


if __name__=="__main__":
    output_dir = "binary_ground_truth/"
    dir = os.getcwd()
    #print(dir)
    if not os.path.exists(os.path.join(dir,output_dir)):
        os.mkdir(output_dir)

    for file in os.listdir("mask"):
        resizeImage(file,output_dir)
       


