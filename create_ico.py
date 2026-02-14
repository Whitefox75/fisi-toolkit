from PIL import Image

# Load the PNG icon
img = Image.open('icon.png')

# Create ICO with multiple sizes
icon_sizes = [(16, 16), (32, 32), (48, 48), (256, 256)]
img.save('icon.ico', format='ICO', sizes=icon_sizes)

print("ICO file created: icon.ico")
