from ngram_score import ngram_score
import random
from pycipher import *
import utils
import os

alphabet2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
path = os.path.dirname(os.path.realpath(__file__))


def decrypt_substitution(alphabet, ciphertext):
    return SimpleSubstitution(alphabet).decipher(ciphertext)


def bruteforce_sub(ciphertext):
    fitness = ngram_score(path + "/english_quadgrams.txt")
    m = list(alphabet2)
    mScore = -99e9
    p1, p2 = mScore, m[:]
    i = 1
    best_keys = []
    for i in range(5):
        i += 1
        random.shuffle(p2)
        plain = decrypt_substitution(p2, ciphertext)
        pScore = fitness.score(plain)
        count = 0
        while count < 1000:
            a, b = random.randint(0, 25), random.randint(
                0, 25
            )  # select random letters to switch in the alphabet
            c = p2[:]
            c[a], c[b] = c[b], c[a]
            plain = decrypt_substitution(c, ciphertext)
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
                f'Best key: {"".join(m)} - {decrypt_substitution(m, ciphertext)[:20]}'
            )
            best_keys.append(m)
    return best_keys


def decrypt_periodic_substitution(ciphertext, keys, length):
    columns = utils.columns(ciphertext, length)
    plaintext = []
    for i in range(len(keys)):
        plaintext.append(decrypt_substitution(keys[i], columns[i]))

    # return first element of each list, then second, etc.
    return "".join(
        [
            plaintext[i][j]
            for i in range(len(plaintext))
            for j in range(len(plaintext[i]))
        ]
    )


def bruteforce_periodic_sub(ciphertext, lengths=[6]):
    for length in lengths:
        fitness = ngram_score("english_quadgrams.txt")
        m = [list(alphabet2) for _ in range(length)]
        mScore = -99e9
        p1, p2 = mScore, [j[:] for j in m]
        best_keys = []
        for i in range(5):
            for j in range(length):
                random.shuffle(p2[j])
            plain = decrypt_periodic_substitution(p2, ciphertext)
            pScore = fitness.score(plain)
            count = 0
            while count < 1000:
                d = random.randint(0, length - 1)
                a, b = random.randint(0, 25), random.randint(
                    0, 25
                )  # select random letters to switch in the alphabet
                c = p2[:]
                c[a], c[b] = c[b], c[a]
                plain = decrypt_periodic_substitution(c, ciphertext)
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
                    f'Best key: {"".join(m)} - {decrypt_periodic_substitution(m, ciphertext)[:20]}'
                )
                best_keys.append(m)
