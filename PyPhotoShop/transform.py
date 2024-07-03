from image import Image
import numpy as np

def brighten(image, factor):
    '''
    when we brighten, we just want to make each channel higher by some amount 
    factor is a value > 0, how much you want to brighten the image by (< 1 = darken, > 1 = brighten)
    '''
    x_pixel, y_pixel, num_channels = image.array.shape
    # make an empty image so we dont actually the modify the original one
    new_im = Image(x_pixels=x_pixel, y_pixels=y_pixel,num_channels=num_channels)
    new_im.array = image.array * factor

    return new_im
def adjust_contrast(image, factor, mid = 0.5):
    '''
    adjust the contrast by increasing the difference
    from the user-defined midpoint by factor amount
    '''
    x_pixel, y_pixel, num_channels = image.array.shape
    new_im = Image(x_pixels=x_pixel, y_pixels=y_pixel,num_channels=num_channels)
    new_im.array = (((image.array) - mid )* factor) + mid
    
    return new_im

def blur(image, kernel_size):
    '''
    kernel size is the number of pixels to take into account when applying the blur
    (ie kernel_size = 3 would be neighbors to the left/right, top/bottom, and diagonals)
    kernel size should always be an *odd* number
    '''
    x_pixel, y_pixel, num_channels = image.array.shape
    # make an empty image so we dont actually the modify the original one
    new_im = Image(x_pixels=x_pixel, y_pixels=y_pixel,num_channels=num_channels)
    
    neighbor_range = kernel_size // 2

    for x in range(x_pixel):
        for y in range(y_pixel):
            for c in range(num_channels):
                total = 0
                for x_i in range(max(0,x-neighbor_range), min(new_im.x_pixels-1, x+neighbor_range)+1):
                    for y_i in range(max(0,y-neighbor_range), min(new_im.y_pixels-1, y+neighbor_range)+1):
                        total += image.array[x_i, y_i, c]
                new_im.array[x, y, c] = total / (kernel_size ** 2)
    return new_im

def apply_kernel(image, kernel):
    '''
    the kernel should be a numpy 2D array that represents the kernel we'll use!
    for the sake of simiplicity of this implementation, let's assume that the kernel is SQUARE
    for example the sobel x kernel (detecting horizontal edges) is as follows:
    [1 0 -1]
    [2 0 -2]
    [1 0 -1]
    '''
    x_pixel, y_pixel, num_channels = image.array.shape
    # make an empty image so we dont actually the modify the original one
    new_im = Image(x_pixels=x_pixel, y_pixels=y_pixel,num_channels=num_channels)
    kernel_size = kernel.shape[0]
    neighbor_range = kernel_size // 2

    for x in range(x_pixel):
        for y in range(y_pixel):
            for c in range(num_channels):
                total = 0
                for x_i in range(max(0,x-neighbor_range), min(new_im.x_pixels-1, x+neighbor_range)+1):
                    for y_i in range(max(0,y-neighbor_range), min(new_im.y_pixels-1, y+neighbor_range)+1):
                        # we need to find which value of the kernel this corresponds to
                        x_k = x_i + neighbor_range - x
                        y_k = y_i + neighbor_range - y
                        kernel_val = kernel[x_k, y_k]
                        total+=image.array[x_i, y_i,c] *kernel_val
                new_im.array[x,y,c] = total
    return new_im

def combine_images(image1, image2):
    '''
    combine two images using the squared sum of squares: value = sqrt(value_1**2, value_2**2)
    size of image1 and image2 MUST be the same
    '''
    x_pixel, y_pixel, num_channels = image1.array.shape # or image2 as size is same
    # make an empty image so we dont actually the modify the original one
    new_im = Image(x_pixels=x_pixel, y_pixels=y_pixel,num_channels=num_channels)

    for x in range(x_pixel):
        for y in range(y_pixel):
            for c in range(num_channels):
                new_im.array[x,y,c] = (image1.array[x,y,c]**2 +image2.array[x,y,c]**2) **0.5
    return new_im
if __name__ == '__main__':
    lake = Image(filename='lake.png')
    city = Image(filename='city.png')

    '''brighten_lake = brighten(lake, 3)
    brighten_lake.write_image('brightened_lake.png')'''
    # similarly we can darken the image if make the factor < 1 inplace of 3

    '''incr_contrast_lake = adjust_contrast(lake,0.5,0.5)
    incr_contrast_lake.write_image('incr_contrast_lake.png')'''
    # similarly we can decrement the contrast by decreasing the difference in the factor and mid parameters
    # decreased contrast means all the image will be closer to one color

    '''blurred_city = blur(city, 3)
    blurred_city.write_image("blurred_city.png")'''
    
    # sobel edge detection kernel on the x and y axis
    sobel_x_kernel = np.array([[1,2,1],
                               [0,0,0],
                               [-1,-2,-1]])
    sobel_y_kernel = np.array([[1,0,-1],
                               [2,0,-2],
                               [1,0,-1]])
    
    sobel_x = apply_kernel(city,sobel_x_kernel)
    # sobel_x.write_image("sobel_x.png")

    sobel_y = apply_kernel(city,sobel_y_kernel)
    # sobel_y.write_image("sobel_y.png")
    
    # lets combine these to make an edge detection filter
    sobel_xy = combine_images(sobel_x,sobel_y)
    sobel_xy.write_image("edge_xy.png")