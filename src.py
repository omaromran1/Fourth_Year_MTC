import torch
from torchvision import models, transforms
from PIL import Image
import matplotlib.pyplot as plt

# Load the entire model (architecture + weights)
resnet = torch.load('../model/resnet_full_model.pth', map_location=torch.device('cpu'))

# Set the model to evaluation mode (important for inference)
resnet.eval()

# Define the necessary image transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # Resize the image to 224x224
    transforms.ToTensor(),  # Convert the image to a Tensor
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # Normalize
])

# Load the image you want to test
image_path = "../img/OIP.jpg"  # Replace with your image path
img = Image.open(image_path)

# Apply the transformations to the image
img_tensor = transform(img)
img_tensor = img_tensor.unsqueeze(0)  # Add a batch dimension (for a single image)

# Define the class labels (your dictionary)
classes = {
    0:'Speed limit (20km/h)', 1:'Speed limit (30km/h)', 2:'Speed limit (50km/h)', 
    3:'Speed limit (60km/h)', 4:'Speed limit (70km/h)', 5:'Speed limit (80km/h)', 
    6:'End of speed limit (80km/h)', 7:'Speed limit (100km/h)', 8:'Speed limit (120km/h)', 
    9:'No passing', 10:'No passing veh over 3.5 tons', 11:'Right-of-way at intersection', 
    12:'Priority road', 13:'Yield', 14:'Stop', 15:'No vehicles', 16:'Veh > 3.5 tons prohibited', 
    17:'No entry', 18:'General caution', 19:'Dangerous curve left', 20:'Dangerous curve right', 
    21:'Double curve', 22:'Bumpy road', 23:'Slippery road', 24:'Road narrows on the right', 
    25:'Road work', 26:'Traffic signals', 27:'Pedestrians', 28:'Children crossing', 
    29:'Bicycles crossing', 30:'Beware of ice/snow', 31:'Wild animals crossing', 
    32:'End speed + passing limits', 33:'Turn right ahead', 34:'Turn left ahead', 
    35:'Ahead only', 36:'Go straight or right', 37:'Go straight or left', 38:'Keep right', 
    39:'Keep left', 40:'Roundabout mandatory', 41:'End of no passing', 
    42:'End no passing veh > 3.5 tons'
}

# Make the prediction
with torch.no_grad():  # No need to track gradients for inference
    outputs = resnet(img_tensor)  # Perform a forward pass through the model
    _, predicted_class = torch.max(outputs, 1)  # Get the index of the class with the highest score

# Get the human-readable label from the classes dictionary
predicted_label = classes[predicted_class.item()]

# Print the predicted class index and class label
print(f"Predicted Class Index: {predicted_class.item()}")
print(f"Predicted Class Label: {predicted_label}")

# Display the image with the predicted class
plt.imshow(img)
plt.title(f"Predicted: {predicted_label}")
plt.show()
