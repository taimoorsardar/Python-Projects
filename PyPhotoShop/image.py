import os
import numpy as np
import png

class Image:
    def __init__(self, x_pixels=0, y_pixels=0, num_channels=0, filename=''):
        # Set correct input and output paths
        self.input_path = os.path.join(os.getcwd(), "input")
        self.output_path = os.path.join(os.getcwd(), "output")
        
        if x_pixels and y_pixels and num_channels:
            self.x_pixels = x_pixels
            self.y_pixels = y_pixels
            self.num_channels = num_channels
            self.array = np.zeros((x_pixels, y_pixels, num_channels))
        elif filename:
            self.array = self.read_image(filename)
            self.x_pixels, self.y_pixels, self.num_channels = self.array.shape
        else:
            raise ValueError("You need to input either a filename OR specify the dimensions of the image")

    def read_image(self, filename, gamma=2.2):
        '''
        Read PNG RGB image, return 3D numpy array organized along Y, X, channel.
        Values are float, gamma is decoded.
        '''
        # Construct the correct file path
        file_path = os.path.join(self.input_path, filename)
        print(f"Trying to read file: {file_path}")  # Debug print
        
        try:
            im = png.Reader(file_path).asFloat()
            resized_image = np.vstack(list(im[2]))
            resized_image.resize(im[1], im[0], 3)
            resized_image = resized_image ** gamma
            return resized_image
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            raise

    def write_image(self, output_file_name, gamma=2.2):
        '''
        3D numpy array (Y, X, channel) of values between 0 and 1 -> write to png.
        '''
        im = np.clip(self.array, 0, 1)
        y, x = self.array.shape[0], self.array.shape[1]
        im = im.reshape(y, x * 3)
        writer = png.Writer(x, y)
        output_file_path = os.path.join(self.output_path, output_file_name)
        
        with open(output_file_path, 'wb') as f:
            writer.write(f, 255 * (im ** (1 / gamma)))

        self.array.resize(y, x, 3)  # Reset array shape after mutation

if __name__ == '__main__':
    # Ensure this file exists at this location
    im = Image(filename='lake.png')
    im.write_image('test.png')
