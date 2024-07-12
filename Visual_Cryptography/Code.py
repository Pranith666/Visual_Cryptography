import cv2
import numpy as np
from ipywidgets import FileUpload, Output, HBox, Image, Layout, Button, VBox, HTML
import io

# Function to perform XOR operation between two images
def xor_images(image1, image2):
    return cv2.bitwise_xor(image1, image2)

# Function to perform the encoding and reconstruction
def encode_and_reconstruct(change):
    uploaded_image = list(file_upload.value.values())[0]['content']
    nparr = np.frombuffer(uploaded_image, np.uint8)
    grayscale_image = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    # Convert Gray scale image to binary half-tone image
    _, binary_image = cv2.threshold(grayscale_image, 128, 255, cv2.THRESH_BINARY)

    # Create a master grid with 50% 0's and 1's
    master_grid = np.random.choice([0, 255], size=binary_image.shape)

    # Initialize the encoded grid
    encoded_grid = np.zeros_like(master_grid)

    # # Encode by mapping black pixels in binary halftone image to Master Grid and inverting white pixels
    for i in range(binary_image.shape[0]):
        for j in range(binary_image.shape[1]):
            if binary_image[i, j] == 0:
                encoded_grid[i, j] = master_grid[i, j]
            else:
                encoded_grid[i, j] = 255 - master_grid[i, j]

    # Reconstruct the image by performing master_grid XOR encoded_grid
    reconstructed_image = xor_images(master_grid, encoded_grid)

    # Store the images in a dictionary for display
    global stored_images
    stored_images = {
        'original': grayscale_image,
        'half_tone': binary_image,
        'master_grid': master_grid,
        'encoded_grid': encoded_grid,
        'reconstructed_image': reconstructed_image
    }

def display_image(image_key):
    image = stored_images[image_key]
    output_widget.clear_output()
    with output_widget:
        display(HTML(value=f'<b>{image_key.replace("_", " ").title()}</b>'))
        display(Image(value=bytes(cv2.imencode('.jpg', image)[1])))

# Creating a file upload widget
file_upload = FileUpload(description='Upload File', accept='.jpg,.tiff')

# Creating an output widget for displaying images
output_widget = Output(layout=Layout(margin='10px'))

# Attaching the function to the file upload widget
file_upload.observe(encode_and_reconstruct, names='data')

# Creating command buttons to display individual outputs
show_original_button = Button(description="Original image")
show_half_tone_button = Button(description="Half-Tone image")
show_master_grid_button = Button(description="Master Grid")
show_encoded_grid_button = Button(description="Encoded Grid")
show_reconstructed_image_button = Button(description="Reconstructed Image")

def show_original(change):
    display_image('original')

def show_half_tone(change):
    display_image('half_tone')

def show_master_grid(change):
    display_image('master_grid')

def show_encoded_grid(change):
    display_image('encoded_grid')

def show_reconstructed_image(change):
    display_image('reconstructed_image')

show_original_button.on_click(show_original)
show_half_tone_button.on_click(show_half_tone)
show_master_grid_button.on_click(show_master_grid)
show_encoded_grid_button.on_click(show_encoded_grid)
show_reconstructed_image_button.on_click(show_reconstructed_image)

# GUI layout
buttons = VBox([show_original_button, show_half_tone_button, show_master_grid_button, show_encoded_grid_button, show_reconstructed_image_button])
gui = VBox([
    file_upload,
    HBox([buttons, output_widget])
])

# Display the GUI
display(gui)