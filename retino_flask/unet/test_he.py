import tensorflow as tf
import cv2
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage.measurements import label
from PIL import Image
from scipy.special import expit
from keras.models import load_model
from imageio import imread


IMAGE_SIZE = 512

def BCE(y_pred, y_true):
    # weight ratio = 9:1
    # 9-1=8
    class_weights = tf.constant([8],dtype=tf.float32)
    tensor_one = tf.constant([1],dtype=tf.float32)

    pred_flat = tf.reshape(y_pred, [-1, 1])
    true_flat = tf.reshape(y_true, [-1, 1])

    weight_map = tf.multiply(true_flat, class_weights)
    weight_map = tf.add(weight_map, tensor_one)

    loss_map = tf.nn.sigmoid_cross_entropy_with_logits(logits=pred_flat, labels=true_flat)
    loss_map = tf.multiply(loss_map, weight_map)
    loss = tf.reduce_mean(loss_map)
    return loss

def IOU(y_pred, y_true):
    """Returns a (approx) IOU score

    intesection = y_pred.flatten() * y_true.flatten()
    Then, IOU = 2 * intersection / (y_pred.sum() + y_true.sum() + 1e-7) + 1e-7

    Args:
        y_pred (4-D array): (N, H, W, 1)
        y_true (4-D array): (N, H, W, 1)

    Returns:
        float: IOU score
    """
    H, W, _ = y_pred.get_shape().as_list()[1:]

    pred_flat = tf.reshape(y_pred, [-1, H * W])
    true_flat = tf.reshape(y_true, [-1, H * W])

    intersection = 2 * tf.reduce_sum(pred_flat * true_flat, axis=1) + 1e-7
    denominator = tf.reduce_sum(
        pred_flat, axis=1) + tf.reduce_sum(
            true_flat, axis=1) + 1e-7

    return tf.reduce_mean(intersection / denominator)

smooth = 1e-15
def dice_coef(y_true, y_pred):
    y_true = tf.keras.layers.Flatten()(y_true)
    y_pred = tf.keras.layers.Flatten()(y_pred)
    intersection = tf.reduce_sum(y_true * y_pred)
    return (2. * intersection + smooth) / (tf.reduce_sum(y_true) + tf.reduce_sum(y_pred) + smooth)



model = load_model('unet/he_model/hemo_model_124.h5' , custom_objects={"IOU": IOU,"dice_coef":dice_coef})



def read_image(path):
    x = imread(path)
    # print(x)
    # x = cv2.cvtColor(x, cv2.COLOR_BGR2RGB)
    # x = cv2.resize(x, (IMAGE_SIZE, IMAGE_SIZE))
    x = x/255.0
    return x



def predict_he(path):
    x = read_image(path)
    predicted_image = np.zeros((2848, 4288), dtype=float)
    for i in range(6):
        for j in range(9):
            top_y = i*512
            if (i==5):
                top_y = 2336
            top_x = j*512
            if (j==8):
                top_x = 3776

            image_crop = x[top_y:top_y+512, top_x:top_x+512]
            predicted_crop = model.predict(np.expand_dims(image_crop, axis=0))[0]
            predicted_crop =np.squeeze(predicted_crop)
            predicted_image[top_y:top_y+512, top_x:top_x+512] = np.maximum(predicted_image[top_y:top_y+512, top_x:top_x+512], predicted_crop)
    predicted_mask = ((predicted_image*255).astype('uint8'))
    x = ((x*255).astype('uint8'))
    predicted_mask = np.stack((predicted_mask,)*3, -1)
    output_image = np.maximum(predicted_mask, x)
    output_save = Image.fromarray(output_image)
    
    return output_save





# def pipeline(image, sess, X, mode, pred):
#     image_WH=(512, 512)
#     image = np.copy(image)
#     H, W, C = image.shape
    
#     if (W, H) != image_WH:
#         image = cv2.resize(image, image_WH)
    
#     mask_pred = sess.run(pred, feed_dict={X: np.expand_dims(image, 0),
#                                           mode: False})
    
#     mask_pred = np.squeeze(mask_pred)
#     mask_pred = expit(mask_pred)
#     return mask_pred

# def predict_he(image):
# 	saver = tf.compat.v1.train.import_meta_graph("unet/he_model/model.ckpt.meta")
# 	sess = tf.compat.v1.InteractiveSession()
# 	saver.restore(sess, "unet/he_model/model.ckpt")
# 	X, mode = tf.compat.v1.get_collection("inputs")
# 	pred = tf.compat.v1.get_collection("outputs")[0]

# 	#image = np.array(image)

# 	predicted_image = np.zeros((2848, 4288), dtype=float)
# 	for i in range(10):
# 		for j in range(16):
# 			top_y = i*256
# 			if (i==9):
# 				top_y = 2336
# 			top_x = j*256
# 			if (j==15):
# 				top_x = 3776

# 			image_crop = image[top_y:top_y+512, top_x:top_x+512]
# 			predicted_crop = pipeline(image_crop, sess, X, mode, pred)
# 			predicted_image[top_y:top_y+512, top_x:top_x+512] = np.maximum(predicted_image[top_y:top_y+512, top_x:top_x+512], predicted_crop)
# 	threshold = 0.5
# 	predicted_image = predicted_image > threshold
# 	predicted_mask = (predicted_image.astype('uint8'))*255
# 	predicted_mask = np.stack((predicted_mask,)*3, -1)
# 	output_image = np.maximum(predicted_mask, image)
# 	output_save = Image.fromarray(output_image)
	
# 	return output_save

# # image_path = "IDRiD_14.jpg"
# # image = Image.open(image_path)
# # output_save = predict_he(image)
# # output_save.save("predicted_he.jpg", "JPEG")