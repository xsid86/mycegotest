import os
import sys

from PIL import Image
import math
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPACER = 50

if __name__ == '__main__':
    folders = os.listdir('data')
    print('Available image sources:')
    print('------------------------')

    # Print available folders
    for x in range(len(folders)):
        print(f'{x + 1}. {folders[x]}')

    print('------------------------')

    # Wait for user input
    i = input('Select source folders. Separate folder numbers by comma: ')

    # Clean and convert user input to string array
    i = i.replace(' ', '').strip(',').split(',')

    if not i[0]:
        print('There are no images to process')
        sys.exit()

    user_input = []

    print()
    print('Processing user input...')

    # Convert string array to array of int
    for x in i:
        try:
            x = int(x)
            if x <= len(folders):
                user_input.append(x)
            else:
                print(f'There is no folder with index {x}.')
        except Exception as e:
            print(f'{x} could not be used as folder number. More info: {str(e)}')

    images = []

    # Get image paths from selected directories
    for x in user_input:
        fp = os.path.join(BASE_DIR, f'data/{folders[x - 1]}')
        image_paths = os.listdir(fp)
        for image in image_paths:
            images.append(f'{fp}/{image}')

    if not images:
        print('There are no images to process')
        sys.exit()

    # Calculate number images per row
    per_row = len(images) // int(math.sqrt(len(images)))

    # Calculate rows number
    rows = math.ceil(len(images) / per_row)

    # Concatenate images into single image (suppose all images has the same dimensions, otherwise code need to be modified) # todo attention to image sizes
    # Take dimensions of the first image
    img = Image.open(f'{images[0]}')
    result_image = Image.new('CMYK', (img.width * per_row + SPACER * (per_row + 1), img.height * rows + SPACER * (rows + 1)))
    _col = 0
    x, y = SPACER, SPACER
    for image in images:
        img = Image.open(f'{image}')
        result_image.paste(img, (x, y))
        _col += 1
        x += img.width + SPACER
        if _col == per_row:
            x = SPACER
            y += img.height + SPACER
            _col = 0

    result_image.save(f'output_{datetime.now().timestamp()}.tif')
