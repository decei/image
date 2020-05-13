# decei - Viestin salaus kuvan pikseleitä muuttamalla
# versio 2.0 - imageio

# 12.5.2020
# Kryptaus ok, kestää pitkään, rajoita kuvan kokoa?
# Toimiva ohjelma, salaa pitkään


import string
from copy import copy
from helps import setup_io, change_pix, save_new
import os
import imageio
import numpy
from PIL import Image


ALPH = list(string.ascii_lowercase)
for z in range(0, 10):
    ALPH.append(str(z))
ALPH.extend([" ", ",", ".", ":", "(", ")", "ä", "ö"])
X = ['000', '001', '010', '011', '100', '101', '110', '111']
Z = []
for y in X[:7]:
    for x in X[1:]:
        Z.append([x, y])
del Z[44:]
INFO = "Program encrypts a message into a selected image (PNG) and creates\n" \
       "a new image with the message. You can also decrypt an existing\n" \
       "message from an image if you have the original image as well.\n" \
       "If there's no message encrypted or the image pair is wrong,\n" \
       "proogram returns an error message. Quit by entering 'Q' or 'q'.\n"


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


# Muuta yksittäinen merkki listaksi ['xxx', 'xxx']
def to_code(char):
    ix = ALPH.index(char)
    return Z[ix]


# Pyydä ja käännä haluttu viesti, palauta käännetty lista
def get_msg():
    msg = input("Write the message to be encrypted:\n")
    listed_msg = list(msg.lower())
    encrypted = []

    for i in range(0, len(listed_msg)):
        if listed_msg[i] not in ALPH:
            print("- Unknown character. Use only basic alphabets, numbers and"
                  "[, . : ( )].")
            return get_msg()

        binar = to_code(listed_msg[i])
        encrypted.append(binar)

    return encrypted


# Muuttaa annetun listan ['xxx', 'xxx'] yksittäiseksi merkiksi
def to_text(bin_list):
    bin_1 = bin_list[0]
    bin_2 = bin_list[1]
    for b in Z:
        if bin_1 == b[0]:
            if bin_2 == b[1]:
                index_bin = Z.index([bin_1, bin_2])
                return ALPH[index_bin]
    print("- Decryption failure. Wrong decryption code or image pair.\n")
    return "?"


# Vertaa pikselien eroa ja palauttaa vastaavan merkin
def compare(enc_pic, og_pic, px, py):
    pxl_1_enc = list(enc_pic[px, py])
    pxl_1_og = list(og_pic[px, py])

    if pxl_1_enc == pxl_1_og:
        charx = ""

    else:
        pxl_1 = ""
        for j in range(3):
            diff_1 = pxl_1_enc[j] - pxl_1_og[j]
            pxl_1 += str(diff_1)

        pxl_2_enc = list(enc_pic[px + 1, py])
        pxl_2_og = list(og_pic[px + 1, py])

        if pxl_2_enc == pxl_2_og:
            pxl_2 = '000'

        else:
            pxl_2 = ""
            for k in range(3):
                diff_2 = pxl_2_enc[k] - pxl_2_og[k]
                pxl_2 += str(diff_2)

        charx = to_text([pxl_1, pxl_2])

    return charx


# Salaa viesti
def encrypt():
    # Pyydetään salattava teksti ja muutetaan binäärimuotoon
    encrypted = get_msg()

    while True:
        # Luodaan kuva ja listat pikseleistä, joita muokataan
        try:
            [pic, pic_xs, pic_ys] = setup_io(1)
            new_pic = copy(pic)

            done = False

            for j in pic_ys:
                for i in pic_xs:
                    binx = encrypted[0]
                    bin_1 = binx[0]
                    bin_2 = binx[1]

                    new_pic[i, j] = change_pix(pic, i, j, bin_1)

                    if bin_2 != '000':
                        new_pic[i + 1, j] = change_pix(pic, i + 1, j, bin_2)

                    del encrypted[0]

                    if len(encrypted) == 0:
                        done = True
                        break
                if done:
                    break

            # Luodaan ja tallennetaan uusi kuva
            save_new(new_pic)
            print("- Encryption success.\n")
            return

        except TypeError:
            continue
        except ValueError:
            continue


# Pura salaus
def decrypt():
    msg = ""
    ok = False

    while True:
        try:
            if not ok:
                [enc_pic, xs, ys, pic_name] = setup_io(2)
            ok = True
            og_pic = setup_io(3)

            done = False
            print("Decrypting...")

            for pix_y in ys:
                for pix_x in xs:
                    charx = compare(enc_pic, og_pic, pix_x, pix_y)

                    if charx == "":
                        done = True
                        break

                    elif charx == "?":
                        return

                    msg += charx

                if done:
                    break

            print("The decrypted message:\n", msg, sep="")
            os.remove(pic_name)
            print("- Decryption success.\n")
            return

        except TypeError:
            continue


def menu():
    print(INFO)
    while True:
        choice = input("Encrypt (E) / Decrypt (D) / Quit (Q): ")

        if choice == "E" or choice == "e":
            encrypt()

        elif choice == "D" or choice == "d":
            decrypt()

        elif choice == "Q" or choice == "q":
            print("- Goodbye.")
            break

        else:
            print("- Unknown command. Use E, D or Q.\n")


def main():
    menu()


main()
