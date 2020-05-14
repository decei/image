import imageio
import numpy
import string


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


def get_msg():
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

    return encrypted            # Palauttaa [str, str]


def change_pix(pic_pix, binx):
    col_list = list(pic_pix)

    for j in range(3):
        col_list[j] += int(binx[j])

    return numpy.array(col_list)


def encrypt():  # TODO
    encrypted = []
    while True and not encrypted:
        encrypted = get_msg()

    seed = int(input("Enter code number: "))       # TODO: lisää tarkistus onko
    done = False

    numpy.random.seed(seed)
    rnd_pix = numpy.random.randint(256, size=(10, 10, 3)).astype(numpy.uint8)
    mesg_pix = numpy.ones((10, 10, 3))

    for j in range(mesg_pix.shape[0]):
        if j % 2 != 0:
            continue

        for i in range(mesg_pix.shape[1]):
            if i % 2 != 0:
                continue

            bin_1 = encrypted[0][0]
            bin_2 = encrypted[0][1]

            mesg_pix[j, i] = change_pix(mesg_pix[j, i], bin_1)

            if bin_2 != '000':
                mesg_pix[j, i + 1] = change_pix(mesg_pix[j, i + 1],
                                                bin_2)

            del encrypted[0]

            if len(encrypted) == 0:
                done = True
                break

        if done:
            break

    enc_pix_1 = numpy.multiply(rnd_pix, mesg_pix)
    enc_pix_2 = numpy.divide(enc_pix_1, seed)

    pic_name = input("Enter the name of the encrypted image: ")
    imageio.imwrite(pic_name, enc_pix_2.astype(numpy.uint8))

    #while are_same(pic, new_pic):
        #new_pic = Picture(4, new_pic)

    #print("- Encryption success. To be found from ", new_pic.get_name()
          #, ".\n", sep="")

    #pic.delete()
    #new_pic.delete()
    #return


def menu():
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
            print("- Unknown command. Use E, D or Q.\n")


def main():
    menu()


main()
