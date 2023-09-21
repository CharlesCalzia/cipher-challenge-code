from pycipher import Atbash, Affine
from utils import check_english


def decrypt_atbash(
    ciphertext,
):  # Atbash cipher, also known as the "mirror" cipher: flip value of each letter
    return Atbash().decipher(ciphertext)


def decrypt_affine(a, b, ciphertext):  # Affine cipher, ax+b for each letter
    return Affine(a, b).decipher(ciphertext)


def bruteforce_affine(
    ciphertext,
):  # Affine cipher bruteforce (which includes Caesar cipher: where a = 1 and b is some constant)
    output = []
    for a in [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]:
        for b in range(25):
            ptr = decrypt_affine(a, b, ciphertext)
            if check_english(ptr) == True:
                output.append([a, b, ptr[:20]])
    if len(output) == 0:
        return False
    else:
        return output


def null(ciphertext):  # Null cipher (form of steganography)
    decrypted_message = ""
    for word in ciphertext.split():
        decrypted_message += word[0]

    return decrypted_message
