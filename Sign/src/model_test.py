import os
import numpy as np
import cv2
import matplotlib.pyplot as plt

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
# Your code follows


model  = tf.keras.models.load_model(r'..\Sign_V1.1.h5')



# Load an example image
image_path = r'..\img\no.jpg'
image = cv2.imread(image_path)


# Label Overview
classes = { 0:'Speed limit (20km/h)',
            1:'Speed limit (30km/h)', 
            2:'Speed limit (50km/h)', 
            3:'Speed limit (60km/h)', 
            4:'Speed limit (70km/h)', 
            5:'Speed limit (80km/h)', 
            6:'End of speed limit (80km/h)', 
            7:'Speed limit (100km/h)', 
            8:'Speed limit (120km/h)', 
            9:'No passing', 
            10:'No passing veh over 3.5 tons', 
            11:'Right-of-way at intersection', 
            12:'Priority road', 
            13:'Yield', 
            14:'Stop', 
            15:'No vehicles', 
            16:'Veh > 3.5 tons prohibited', 
            17:'No entry', 
            18:'General caution', 
            19:'Dangerous curve left', 
            20:'Dangerous curve right', 
            21:'Double curve', 
            22:'Bumpy road', 
            23:'Slippery road', 
            24:'Road narrows on the right', 
            25:'Road work', 
            26:'Traffic signals', 
            27:'Pedestrians', 
            28:'Children crossing', 
            29:'Bicycles crossing', 
            30:'Beware of ice/snow',
            31:'Wild animals crossing', 
            32:'End speed + passing limits', 
            33:'Turn right ahead', 
            34:'Turn left ahead', 
            35:'Ahead only', 
            36:'Go straight or right', 
            37:'Go straight or left', 
            38:'Keep right', 
            39:'Keep left', 
            40:'Roundabout mandatory', 
            41:'End of no passing', 
            42:'End no passing veh > 3.5 tons' }
# Preprocess the image: resize, normalize, and add batch dimension
frame_resized = cv2.resize(image, (30, 30))  # Resize to 30x30 pixels
frame_normalized = frame_resized / 255.0  # Normalize pixel values
frame_batch = np.expand_dims(frame_normalized, axis=0)  # Add batch dimension

# Make a prediction
predictions = model.predict(frame_batch)
predicted_class = np.argmax(predictions, axis=1)[0]

# Assuming you have a list of class names
class_names = [f'Class{i+1}' for i in range(43)]  # Adjust this list to your actual class names


# Get class label from the dictionary
label = classes[predicted_class] 
# Print the predicted class index and name 
print(f"Predicted class label: {label}")
print("Predicted class:", label)

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
plt.imshow(image_rgb)
plt.axis('off')
plt.show()