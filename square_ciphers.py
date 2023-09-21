from secretpy.ciphers import nihilist
from ngram_score import ngram_score
import random
from pycipher import *
from secretpy import Nihilist
from utils import blocks

alphabet2 = "ABCDEFGHIKLMNOPQRSTUVWXYZ"


def decrypt_polybius(ciphertext, alphabet="ABCDEFGHIZKLMNOPQRSTUVWXY", chars="ABCDE"):
    return PolybiusSquare("".join(alphabet), 5, chars).decipher(ciphertext)


def bruteforce_polybius(ciphertext, in_chars="12345", out_chars="ABCDE"):
    for i in range(5):
        ciphertext = ciphertext.replace(in_chars[i], out_chars[i])

    fitness = ngram_score("english_quadgrams.txt")
    m = list(alphabet2)
    mScore = -99e9
    p1, p2 = mScore, m[:]
    i = 1
    for i in range(5):
        i += 1
        random.shuffle(p2)
        plain = decrypt_polybius(ciphertext, p2)
        pScore = fitness.score(plain)
        count = 0
        while count < 1000:
            a, b = random.randint(0, 24), random.randint(
                0, 24
            )  # select random letters to switch in the alphabet
            c = p2[:]
            c[a], c[b] = c[b], c[a]
            plain = decrypt_polybius(ciphertext, c)
            cScore = fitness.score(plain)
            if cScore > pScore:
                pScore = cScore
                p2 = c[:]
                count = 0
            count += 1
        if pScore > mScore:
            mScore = pScore
            m = p2[:]
            print(f'Best key: {"".join(m)} - {decrypt_polybius(ciphertext, m)[:20]}')


def decrypt_nihilist(ciphertext, key):
    nihilist = Nihilist()
    alphabet = "A B C D E F G H J Z K L M N O P Q R S T U V W X Y".split(" ")
    try:
        return nihilist.decrypt(ciphertext, "".join(key), alphabet)
    except:
        return False


def decrypt_nihilist2(ciphertext, key):
    alphabet = "A B C D E F G H I Z K L M N O P Q R S T U V W X Y".split(" ")
    poly = decrypt_polybius(alphabet, ciphertext)


def bruteforce_nihilist(
    ciphertext, lengths=list(range(2, 9))
):  # Not really functioning
    # ciphertext = ' '.join(blocks(ciphertext2,2))
    for length in lengths:
        # ciphertext=ciphertext.upper()
        fitness = ngram_score("english_quadgrams.txt")
        m = list(alphabet2)
        mScore = -99e9
        p1, p2 = mScore, ["A" for i in range(length)]
        i = 1
        for i in range(3):
            i += 1
            random.shuffle(p2)
            plain = decrypt_nihilist(ciphertext, p2)
            if not plain:
                continue
            pScore = fitness.score(plain)
            count = 0
            while count < 1000:
                a, b = random.randint(0, length - 1), random.randint(0, 24)
                c = p2[:]
                c[a] = alphabet2[b]
                plain = decrypt_nihilist(ciphertext, c)
                if not plain:
                    continue
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
                    f"Length {length} best key: {m} - {decrypt_nihilist(ciphertext,m)[:20]}"
                )


def decrypt_playfair(alphabet, ciphertext):
    return Playfair(key=alphabet).decipher(ciphertext)


def bruteforce_playfair(ciphertext):  # Not really functioning
    fitness = ngram_score("english_quadgrams.txt")
    m = list("EXAMPLBCDFGHIKNOQRSTUVWYZ")
    mScore = -99e9
    p1, p2 = mScore, m[:]
    i = 1
    for i in range(10):
        i += 1
        random.shuffle(p2)
        plain = decrypt_playfair(p2, ciphertext)
        print(plain)

        pScore = fitness.score(plain)
        count = 0
        while count < 1000:
            a, b = random.randint(0, 24), random.randint(0, 24)
            c = p2[:]
            c[a], c[b] = c[b], c[a]
            plain = decrypt_playfair(c, ciphertext)
            cScore = fitness.score(plain)
            if cScore > pScore:
                pScore = cScore
                p2 = c[:]
                count = 0
            count += 1
        if pScore > mScore:
            mScore = pScore
            m = p2[:]
            print(f'Best key: {"".join(m)} - {decrypt_playfair(m, ciphertext)[:20]}')


def decrypt_two_square(ciphertext, key1, key2):  # Not functioning
    return decrypt_playfair(key1, decrypt_playfair(key2, ciphertext))


def bruteforce_two_square(ciphertext):  # Not functioning
    fitness = ngram_score("english_quadgrams.txt")
    m = list(alphabet2)
    mScore = -99e9
    p1, p2 = mScore, m[:]
    i = 1
    for i in range(5):
        i += 1
        random.shuffle(p2)
        plain = decrypt_two_square(ciphertext, p2)
        pScore = fitness.score(plain)
        count = 0
        while count < 1000:
            a, b = random.randint(0, 24), random.randint(0, 24)
            c = p2[:]
            c[a], c[b] = c[b], c[a]
            plain = decrypt_two_square(ciphertext, c)
            cScore = fitness.score(plain)
            if cScore > pScore:
                pScore = cScore
                p2 = c[:]
                count = 0
            count += 1
        if pScore > mScore:
            mScore = pScore
            m = p2[:]
            print(f'Best key: {"".join(m)} - {decrypt_two_square(ciphertext, m)[:20]}')
