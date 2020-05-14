# decei - Encryption / decryption of a message by changing pixels of
# a random generated image. Parts from crypt.py.
# Version 1.0 - imageio, functions

import imageio
import numpy
import string
import os


# Creation of lists of the characters and corresponding binary codes.
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
        print("- Decryption failure. Wrong decryption code.\n")
        return "?"


def get_msg():
    """Ask for a message and return it in binary form ([[str, str], ...])"""
    msg = input("Write the message to be encrypted: ")
    encrypted = []

    if msg != "":
        listed_msg = list(msg.lower())

        for i in range(0, len(listed_msg)):
            binar = to_code(listed_msg[i])

            if not binar:
                encrypted = []
                break

            encrypted.append(binar)

    return encrypted


def change_pix(pic_pix, binx):
    """Change the wanted pixel by given amount (numpy.array(3))."""
    col_list = list(pic_pix)

    for j in range(3):
        col_list[j] += int(binx[j])

    return numpy.array(col_list)


def ask_details(vrs):
    """Ask for and return seed value and the image shape (int)."""
    try:
        seed = int(input("Enter the code number: "))

        if vrs == 1:
            height = int(input("Enter the height of the image: "))
            width = int(input("Enter the width of the image: "))

            if seed >= 0 and height > 0 and width > 0:
                return seed, height, width

        if vrs == 2:
            if seed >= 0:
                return seed

        raise ValueError

    except ValueError:
        print("- Values must be positive numbers.")
        return ask_details(vrs)


def close_matrix(seed, msg_pix, h, w):
    """Operate the given matrix to the encrypted version (numpy.array)."""
    numpy.random.seed(seed)
    rnd_pix = numpy.random.randint(1, 128, size=(h, w, 3)).astype(numpy.uint8)

    enc_pix = numpy.multiply(rnd_pix, msg_pix)
    enc_pix = numpy.add(rnd_pix, enc_pix)
    return enc_pix


def write_image(enc_pix):
    """Write the wanted image with correct name."""
    pic_name = ""

    while pic_name == "" or pic_name == " ":
        pic_name = input("Enter the name of the encrypted image: ")

    if not pic_name.endswith('.png'):
        print("- Sorry, giving you a PNG-version...")
        parts = pic_name.split('.')
        pic_name = parts[0] + '.png'

    print("Encrypting...")
    imageio.imwrite(pic_name, enc_pix.astype(numpy.uint8))


def open_matrix(seed, pix, h, w):
    """Operate the given matrix to the decrypted version (numpy.array)."""
    numpy.random.seed(seed)
    rnd_pix = numpy.random.randint(1, 128, size=(h, w, 3)).astype(numpy.uint8)

    dec_pix = numpy.subtract(pix, rnd_pix)
    dec_pix = numpy.divide(dec_pix, rnd_pix)
    return dec_pix


def read_image():
    """Read the given image if found and return data ([numpy.array, str])."""
    pic_name = ""

    while pic_name == "" or pic_name == " ":
        pic_name = input("Enter the name of the encrypted image: ")

    try:
        pix = imageio.imread(pic_name)
        return pix, pic_name

    except (ValueError, FileNotFoundError):
        print("- File not found.")
        read_image()


def to_str(pix):
    """Convert the given list of ints to corresponding string (str)."""
    p_str = ""
    for i in range(3):
        p_str += str(int(pix[i]))
    return p_str


def encrypt():
    """Perform the encryption when called."""
    encrypted = []
    while True and not encrypted:
        encrypted = get_msg()

    [seed, height, width] = ask_details(1)

    if height * (width - 1) / 4 < len(encrypted):
        print("Image size too small for the message.\n")
        return

    msg_pix = numpy.zeros((height, width, 3))

    done = False
    j = 0
    i = 0

    while j <= height and not done:
        while i < width and not done:

            bin_1 = encrypted[0][0]
            bin_2 = encrypted[0][1]

            msg_pix[j, i] = change_pix(msg_pix[j, i], bin_1)

            if bin_2 != '000':
                msg_pix[j, i + 1] = change_pix(msg_pix[j, i + 1], bin_2)

            del encrypted[0]

            if len(encrypted) == 0:
                done = True

            i += 2

        j += 2
        i = 0

    enc_pix = close_matrix(seed, msg_pix, height, width)
    write_image(enc_pix)

    print("- Encryption success.\n", sep="")
    return


def decrypt():
    """Perform the decryption when called."""
    msg = ""

    seed = ask_details(2)

    [pix, pic_name] = read_image()
    height = pix.shape[0]
    width = pix.shape[1]

    print("Decrypting...")
    dec_pix = open_matrix(seed, pix, height, width)

    done = False
    i = 0
    j = 0

    while j <= height and not done:
        while i < width and not done:

            px_1 = to_str(list(dec_pix[j, i]))

            if px_1 == "000":
                done = True
                break

            px_2 = to_str(list(dec_pix[j, i + 1]))

            charx = to_text([px_1, px_2])
            if charx == "?":
                return

            msg += charx
            i += 2

        j += 2
        i = 0

    print("- The decrypted message:\n", msg, sep="")
    print("- Decryption success.\n")
    os.remove(pic_name)
    return


def menu():
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
