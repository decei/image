# desei - Viestin salaus kuvan pikseleitä muuttamalla
# versio 1.0 - PIL

# 10.15.2020
# Kuvatiedoston luonti ja kuvan pikseleiden ja koon luku onnistuu
# Toiminnan valitseminen
# Ohjelmasta poistuminen
# Muuttaa kirjaimet binääriksi

# 11.5.2020
# Kryptaus (E) lähestulkoon  onnistuu, luo kuvan mutta pikselit...?!?!?
# Muutettiin binääriluvut -> str, yksinkertaisempaa
# Uusi kuva alkuperäisen kopio
# Poistaa viestin kryptauksen jälkeen
# Pikselilistat ok

#TODO:
# Aseta rajat kuvan resoluutiolle? (min)
# Kuvat numerolla vai nimellä?
# Kuvan poisto dekryptauksen jälkeen?
# Automaattinen vastauksen kirjoitus?
# Tekstin tarkistus
# to_text - jos ei sopiva kirjain -> lopeta
# Ei muuta seuraavaa pikseliä


import string
from PIL import Image


PIC_NAME = 'IMG_0909.jpeg'
ALPH = list(string.ascii_lowercase)
for z in range(0, 10):
    ALPH.append(str(z))
ALPH.append("-")
X = ['000', '001', '010', '011', '100', '101', '110', '111']
Z = []
for y in X[:6]:
    for x in X[1:]:
        Z.append([x, y])
del Z[37:]


# Tarkista onko kuva olemassa ja luo kuvatiedosto.
def read_pic(vrs):
    if vrs == 1:
        pic_name = input("Write the name of the image to be processed: ")
    elif vrs == 2:
        pic_name = input("Write the name of the original image: ")
    else:
        print("Wrong parameter.")
        return

    try:
        return Image.open(pic_name)
    except FileNotFoundError:
        print("File not found.")


# Luo asetukset kuvalle.
def setup(vrs):
    pic = read_pic(vrs)

    try:
        width = pic.size[0]
        height = pic.size[1]
        pxls_to_read_x = []
        pxls_to_read_y = []
        a = 0
        b = 0

        while a < width-1:
            pxls_to_read_x.append(a)
            a += 50
        while b < height:
            pxls_to_read_y.append(b)
            b += 50

    except AttributeError:
        return

    if vrs == 1:
        return pic, pxls_to_read_x, pxls_to_read_y
    if vrs == 2:
        return pic


# Kryptaus
def encrypt():
    msg = input("Write the message to be encrypted:\n")
    listed_msg = list(msg.lower())
    encrypted = []

    for j in range(0, len(listed_msg)):
        if listed_msg[j] == ' ':
            listed_msg[j] = '-'
        elif listed_msg[j] not in ALPH:
            print("Unknown character. Use only basic alphabets and numbers.")
            return

        bin_char = to_code(listed_msg[j])
        encrypted.append(bin_char)

    # Alkuperäisen kuvan luonti, uuden kopiointi
    [pic, xs, ys] = setup(1)
    pixel_map = pic.load()
    new_pic = Image.new(pic.mode, pic.size)
    pixel_map_new = new_pic.load()

    done = False

    for j in range(pic.size[1]):
        for i in range(pic.size[0]-1):
            if pixel_map_new[i, j] != (0, 0, 0):
                continue

            pixel_map_new[i, j] = pixel_map[i, j]
            pixel_map_new[i+1, j] = pixel_map[i+1, j]

            if i in xs and j in ys and not done:
                binx = encrypted[0]
                bin_1 = binx[0]
                bin_2 = binx[1]

                col_list = list(pixel_map_new[i, j])
                for k in range(3):
                    col_list[j] += int(bin_1[j])
                pixel_map_new[i, j] = tuple(col_list)

                if bin_2 != '000':
                    col_list_2 = list(pixel_map_new[i+1, j])
                    for m in range(3):
                        col_list_2[m] += int(bin_2[m])

                    pixel_map_new[i+1, j] = tuple(col_list_2)

                del encrypted[0]

                if len(encrypted) == 0:
                    done = True

    new_name = input("Write the name of the encrypted file: ")
    new_pic.save(new_name, quality=92)
    new_pic.close()
    pic.close()
    print("Message encrypted, to be found from the file: ", new_name, ".\n",
          sep="")


# Pikselin muuttaminen binäärien avulla
def change_pix(new_map, px, py, bin_1, bin_2):
    col_tuple = new_map[px, py]
    col_list = list(col_tuple)

    for j in range(3):
        col_list[j] += int(bin_1[j])

    if bin_2 != '000':
        col_tuple_2 = new_map[px+1, py]
        col_list_2 = list(col_tuple_2)

        for k in range(3):
            col_list_2[k] += int(bin_2[k])

        new_map[px+1, py] = tuple(col_list_2)

    return tuple(col_list)


# Etsi ja palauta vastaava binääriarvo annetulle merkille.
def to_code(char):
    ix = ALPH.index(char)
    return Z[ix]


# Dekryptaus
def decrypt():
    msg = ""

    [enc_pic, enc_x, enc_y] = setup(1)
    og_pic = setup(2)

    pixel_map_enc = enc_pic.load()
    pixel_map_og = og_pic.load()

    done = False

    while True and not done:
        for pixel_y in enc_y:
            for pixel_x in enc_x:

                print(pixel_x, pixel_y)
                print(pixel_map_og[pixel_x, pixel_y])
                print(pixel_map_enc[pixel_x, pixel_y])
                binx = compare(pixel_map_enc, pixel_map_og, pixel_x, pixel_y)

                if binx == ['000', '000']:
                    done = True
                    break

                print(binx, msg)    #poista
                msg = to_text(binx, msg)
            if done:
                break

    enc_pic.close()
    og_pic.close()
    print("The decrypted message:\n", msg, sep="")


# Etsi ja palauta merkki vastaavan pikselin muutokselle (str to str)
def to_text(bin_list, msg):
    bin_1 = bin_list[0]
    bin_2 = bin_list[1]
    for b in Z:
        if bin_1 == b[0]:
            if bin_2 == b[1]:
                charx = Z.index([bin_1, bin_2])
                msg = msg + ALPH[charx]
                return msg
    print("Message contains unknown characters. Unable to read.")


def compare(map_enc, map_og, px, py):
    if map_enc[px, py] == map_og[px, py]:
        return ['000', '000']

    pxl_1_str = ""
    pxl_1_enc = list(map_enc[px, py])
    pxl_1_og = list(map_og[px, py])
    for j in range(3):
        diff = pxl_1_enc[j] - pxl_1_og[j]
        pxl_1_str += str(diff)

    if map_enc[px+1, py] == map_og[px+1, py]:
        return [pxl_1_str, '000']

    pxl_2_str = ""
    pxl_2_enc = list(map_enc[px+1, py])
    pxl_2_og = list(map_og[px+1, py])
    for j in range(3):
        diff = pxl_2_enc[j] - pxl_2_og[j]
        pxl_2_str += str(diff)

    return [pxl_1_str, pxl_2_str]


# Kysy haluttu toimenpide ja toteuta.
def menu():
    while True:
        choice = input("Encrypt (E) / Decrypt (D) / Quit (Q): ")

        if choice == "E" or choice == "e":
            encrypt()
        elif choice == "D" or choice == "d":
            decrypt()
        elif choice == "Q" or choice == "q":
            break
        else:
            print("- Unknown command. Use E, D or Q.")


def main():
    menu()


main()
