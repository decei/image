import imageio
import numpy
from PIL import Image


def read_pic_io(vrs):
    if vrs == 1:
        pic_name = input("Write the name of the image to be encrypted: ")
    elif vrs == 2:
        pic_name = input("Write the name of the image to be decrypted: ")
    else:
        pic_name = input("Write the name of the original image: ")

    try:
        if pic_name.endswith('.jpeg') or pic_name.endswith('.jpg'):
            pic = Image.open(pic_name)
            parts = pic_name.split('.')
            pic_name = parts[0] + '.png'
            print("Converting into a PNG-image...")
            pic.save(pic_name)
            pic.close()

        pic = imageio.imread(pic_name)

        if vrs == 2:
            return pic, pic_name

        return pic

    except FileNotFoundError:
        print("- File not found.")
        return None


def setup_io(vrs):
    if vrs == 2:
        [pic, pic_name] = read_pic_io(vrs)
    else:
        pic = read_pic_io(vrs)

    try:
        height = int(pic.shape[0])
        width = int(pic.shape[1])

        pixels_x = []
        pixels_y = []
        x = 0
        y = 0

        while x < width - 1:
            pixels_x.append(x)
            x += 50
        while y < height:
            pixels_y.append(y)
            y += 50

        if vrs == 1:
            return pic, pixels_x, pixels_y

        elif vrs == 2:
            return pic, pixels_x, pixels_y, pic_name

        elif vrs == 3:
            return pic

    except AttributeError:
        raise TypeError


def change_pix(pic, px, py, binx):
    col_list = pic[px, py]

    for j in range(3):
        col_list[j] += int(binx[j])

    return numpy.array(col_list)


def save_new(new_pic):
    new_pic_name = input("Write the name of the new image: ")
    if not new_pic_name.endswith('.png'):
        parts = new_pic_name.split('.')
        new_pic_name = parts[0] + '.png'

    print("Encrypting...")
    imageio.imwrite(new_pic_name, new_pic)
