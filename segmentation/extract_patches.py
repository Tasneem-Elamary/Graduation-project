from PIL import Image
#from resizeimage import resizeimage
import os, sys
import numpy as np
import operator

dir = os.getcwd()
output_dir_data = "patches/"
output_dir_mask = "labels/"
if not os.path.exists(os.path.join(dir,output_dir_data)):
    os.mkdir(output_dir_data)
if not os.path.exists(os.path.join(dir,output_dir_mask)):
    os.mkdir(output_dir_mask)

dir_data = "data/"
dir_mask = "binary_ground_truth/"



# im = Image.open(os.path.join(dir_mask,"IDRiD_06.tif"))
# im_crop = im.crop((2000,0,2000+512,0+256))
# im_crop.show()
# image_np = np.array(im_crop)
# print np.sum(image_np)

negative_patches = []
positive_count = 0

for file in os.listdir(dir_mask):
    original_name=file.split("_E")[0]
    #print(original_name)
    outfile = os.path.splitext(file)[0]
    extension = os.path.splitext(file)[1]
    if (operator.eq(extension, ".jpg")):
        continue

    im = Image.open(os.path.join(dir_mask,file))
    imd = Image.open(os.path.join(dir_data,outfile +'.jpg'))
    # image_np = np.array(im)
    # print np.sum([True, True])
    # im_crop = im.crop((1900,0,1900+512,0+512))
    patch_id = 0
    for i in range(10):
    	for j in range(16):
            top_y = i*256
            if (i==9):
                top_y = 2336
            top_x = j*256
            if (j==15):
                top_x = 3776

            im_crop = im.crop((top_x,top_y,top_x+512,top_y+512))
            imd_crop = imd.crop((top_x,top_y,top_x+512,top_y+512))
            
            im_crop.save(output_dir_mask+outfile+"_p"+str(patch_id)+".jpeg",quality=100)
            imd_crop.save(output_dir_data+outfile+"_p"+str(patch_id)+".jpeg",quality=100)
            if (np.sum(np.array(im_crop)) < 100):
                negative_patches.append(output_dir_mask+outfile+"_p"+str(patch_id)+extension)
            else:
                positive_count += 1

            patch_id += 1
   

negative_patches = np.array(negative_patches)
# np.savetxt("negative.csv", negative_patches, delimiter=",", fmt="%s")

negative_count = negative_patches.size
delete_count = negative_count - 4*positive_count
np.random.shuffle(negative_patches)
split_idx = delete_count
delete_patches = negative_patches[:split_idx]

for idx in range(delete_patches.size):
    os.remove(delete_patches[idx])
    os.remove("patches"+delete_patches[idx][6:])

