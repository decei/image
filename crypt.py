# decei - Encryption / decryption of a message by changing the pixels.
# Version 3.1 - imageio, objects, processed pixels to landscape

# 14.5.2020
# Encrypting quite time consuming due to high quality
# Set a quality limit for the image?

import string
import os
import imageio
import numpy
from PIL import Image


# Creation of lists of the characters and corresponding
# binary codes and the INFO-texts.
ALPH = list(string.ascii_lowercase)
for z in range(0, 10):
    ALPH.append(str(z))
ALPH.extend([" ", ",", ".", ":", "(", ")", "ä", "ö"])
X = ['000', '001', '010', '011', '100', '101', '110', '111']
Z = []
for x2 in X[:7]:
    for x1 in X[1:]:
        Z.append([x1, x2])
del Z[44:]
INFO = "- Program encrypts a message into a selected image and creates\n" \
       "  a new image with the message. You can also decrypt an existing\n" \
       "  message from an image if you have the original image as well.\n" \
       "  Quit by entering 'Q' or 'q'.\n"
INFO2 = "- Legal characters are basic alphabets, numbers, white space and\n" \
        "  [, . : ( ) ä ö].\n" \
        "- The original image should be PNG_image. Program will convert\n" \
        "  to PNG if not. Same for the encrypted image.\n" \
        "- If given image is not found, program will print an error\n" \
        "  message both while encrypting and decrypting.\n" \
        "- After successful decryption, program deletes the encrypted image.\n"


class Picture:
    """Class either reads or writes an image and returns information of it."""

    def __init__(self, version, pixels):
        self.__name = ""
        self.__pixels = numpy.empty(0)
        self.ask_name(version)

        if version == 4:
            self.__pixels = pixels
            self.write_image()
        else:
            self.open_image()

    def ask_name(self, vrs):
        """Ask name for the image and set it to self.__name."""
        if vrs == 1:
            pic_name = input("Write the name of the image to be encrypted: ")
        elif vrs == 2:
            pic_name = input("Write the name of the image to be decrypted: ")
        elif vrs == 3:
            pic_name = input("Write the name of the original image: ")
        else:
            pic_name = input("Write the name of the new image: ")

        if pic_name == "" or pic_name == " ":
            self.ask_name(vrs)

        self.__name = pic_name

    def open_image(self):
        """Read given image and save data to self.__pixels."""
        try:
            if self.__name.endswith('.jpeg') or self.__name.endswith('.jpg'):

                pic = Image.open(self.__name)
                parts = self.__name.split('.')
                self.__name = parts[0] + '.png'
                print("Converting into a PNG-image...")
                pic.save(self.__name)
                pic.close()

            self.__pixels = imageio.imread(self.__name)

        except (ValueError, FileNotFoundError):
            print("- File not found.")
            self.__pixels = None

    def write_image(self):
        """Write new image from the existing data."""
        if not self.__name.endswith('.png'):
            print("Sorry, giving you a PNG-version...")
            parts = self.__name.split('.')
            self.__name = parts[0] + '.png'

        print("Encrypting...")
        imageio.imwrite(self.__name, self.__pixels)

    def get_data(self):
        """Return pixel data (numpy.array)."""
        return self.__pixels

    def get_name(self):
        """Return name of the image (str)."""
        return self.__name

    def get_x_y(self):
        """Return lists of the coordinates of the wanted pixels ([int])."""
        height = int(self.__pixels.shape[0])
        width = int(self.__pixels.shape[1])

        pixels_x = []
        pixels_y = []
        px = 0
        py = 0

        while px < width - 1:
            pixels_x.append(px)
            px += 50
        while py < height:
            pixels_y.append(py)
            py += 50

        return pixels_x, pixels_y

    def exist(self):
        """Check if Picture-object has any pixel data (bool)."""
        if self.__pixels is None:
            return False
        else:
            return True

    def delete(self):
        """Delete the Picture-object."""
        del self


def to_code(char):
    """Convert the given character to corresponding binary code ([str])."""
    try:
        return Z[ALPH.index(char)]
    except ValueError:
        print("- Unknown character. Use only basic alphabets, numbers and "
              "[, . : ( )].")
        return []


def to_text(bin_list):
    """Convert the given binary code to corresponding character (str)."""
    try:
        return ALPH[Z.index([bin_list[0], bin_list[1]])]
    except ValueError:
        print("- Decryption failure. Wrong decryption code or image pair.\n")
        return "?"


def get_msg():
    """Ask for a message and return it in binary form ([[str, str], ...])"""
    msg = input("Write the message to be encrypted: ")

    if msg == "":
        return

    listed_msg = list(msg.lower())
    encrypted = []

    for i in range(0, len(listed_msg)):
        binar = to_code(listed_msg[i])

        if not binar:
            return encrypted == []

        encrypted.append(binar)

    return encrypted


def compare(enc_pix, og_pix):
    """Compare the two given pixels and return the difference (str)."""
    pxl_enc = list(enc_pix)
    pxl_og = list(og_pix)

    if pxl_enc == pxl_og:
        pxl_str = "000"

    else:
        pxl_str = ""
        for j in range(3):
            diff = int(pxl_enc[j]) - int(pxl_og[j])
            pxl_str += str(diff)

    return pxl_str


def are_same(og, enc):
    """Check if the two Picture-objects are the same (bool)."""
    if og.get_name() == enc.get_name():
        print("- The encrypted/decrypted image can't be the same as "
              "the original.")
        return True
    else:
        return False


def change_pix(pix, binx):
    """Change the wanted pixel by given amount (numpy.array(3))."""
    col_list = list(pix)

    for j in range(3):
        col_list[j] += int(binx[j])

    return numpy.array(col_list)


def encrypt():
    """Perform the encryption when called."""
    encrypted = []
    while True and not encrypted:
        encrypted = get_msg()

    while True:
        pic = Picture(1, None)

        if not pic.exist():
            pic.delete()
            continue

        [pic_xs, pic_ys] = pic.get_x_y()
        new_pic_pix = pic.get_data()

        done = False

        for j in pic_ys:
            for i in pic_xs:
                bin_1 = encrypted[0][0]
                bin_2 = encrypted[0][1]

                new_pic_pix[j, i] = change_pix(new_pic_pix[j, i], bin_1)

                if bin_2 != '000':
                    new_pic_pix[j, i + 1] = change_pix(new_pic_pix[j, i + 1],
                                                       bin_2)

                del encrypted[0]

                if len(encrypted) == 0:
                    done = True
                    break

            if done:
                break

        new_pic = Picture(4, new_pic_pix)

        while are_same(pic, new_pic):
            new_pic = Picture(4, new_pic)

        print("- Encryption success. To be found from ", new_pic.get_name(),
              ".\n", sep="")

        pic.delete()
        new_pic.delete()
        return


def decrypt():
    """Perform the decryption when called."""
    msg = ""
    while True:
        enc_pic = Picture(2, None)

        if not enc_pic.exist():
            enc_pic.delete()
            continue

        while True:
            og_pic = Picture(3, None)

            if not og_pic.exist() or are_same(og_pic, enc_pic):
                og_pic.delete()
                continue

            done = False

            [pic_xs, pic_ys] = enc_pic.get_x_y()
            enc_pix = enc_pic.get_data()
            og_pix = og_pic.get_data()

            print("Decrypting...")

            for j in pic_ys:
                for i in pic_xs:
                    px_1 = compare(enc_pix[j, i], og_pix[j, i])

                    if px_1 == "000":
                        done = True
                        break

                    px_2 = compare(enc_pix[j, i + 1], og_pix[j, i + 1])

                    charx = to_text([px_1, px_2])
                    if charx == "?":
                        return

                    msg += charx

                if done:
                    break

            os.remove(enc_pic.get_name())
            enc_pic.delete()
            og_pic.delete()
            print("- The decrypted message:\n", msg, sep="")
            print("- Decryption success.\n")
            return


def give_info():
    """Print the info when called."""
    print(INFO)

    while True:
        more = input("More info? (Y/N): ")
        if more == "Y" or more == "y":
            print(INFO2)
            return

        elif more == "N" or more == "n":
            print()
            return

        else:
            print("- Unknown command. Use Y or N.")
            continue


def menu():
    """Ask for the operation until asked to quit."""
    while True:
        choice = input("Encrypt (E) / Decrypt (D) / Info (I) / Quit (Q): ")

        if choice == "E" or choice == "e":
            encrypt()

        elif choice == "D" or choice == "d":
            decrypt()

        elif choice == "I" or choice == "i":
            give_info()

        elif choice == "Q" or choice == "q":
            print("- Goodbye.")
            break

        else:
            print("- Unknown command. Use E, D, I or Q.\n")


def main():
    menu()


main()
