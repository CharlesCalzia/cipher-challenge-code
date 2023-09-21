from ngram_score import ngram_score
import random
from pycipher import *
import os

alphabet2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
path = os.path.dirname(os.path.realpath(__file__))


def decrypt_vigenere(key, ciphertext):
    return Vigenere(key).decipher(ciphertext)


def bruteforce_vigenere(
    ciphertext, lengths=list(range(2, 12))
):  # needs work to convert it to copy subsitution bruteforce algo
    for length in lengths:
        ciphertext = ciphertext.upper()
        fitness = ngram_score(path + "/english_quadgrams.txt")
        m = list(alphabet2)
        mScore = -99e9
        p1, p2 = mScore, ["A" for i in range(length)]
        i = 1
        for i in range(3):
            i += 1
            random.shuffle(p2)
            plain = decrypt_vigenere(p2, ciphertext)
            pScore = fitness.score(plain)
            count = 0
            while count < 1000:
                a, b = random.randint(0, length - 1), random.randint(
                    0, 25
                )  # select random letters to switch in the alphabet
                c = p2[:]
                c[a] = alphabet2[b]
                plain = decrypt_vigenere(c, ciphertext)
                cScore = fitness.score(plain)
                if cScore > pScore:
                    pScore = cScore
                    p2 = c[:]
                    count = 0
                count += 1
            if pScore > mScore:
                mScore = pScore
                m = p2[:]
                print(
                    f"Length {length} best key: {m} - {decrypt_vigenere(m, ciphertext)[:20]}"
                )
