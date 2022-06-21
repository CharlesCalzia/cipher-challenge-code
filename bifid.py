from pycipher import Bifid
from ngram_score import ngram_score
import random

alphabet2 = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'

def decrypt_bifid(ciphertext, key):
    return Bifid(''.join(key), 5).decipher(ciphertext)

def bruteforce_bifid(ciphertext):
    fitness = ngram_score('english_quadgrams.txt')
    m = list(alphabet2)
    mScore = -99e9
    p1,p2 = mScore, m[:]
    i = 1
    for i in range(5):
        i+=1
        random.shuffle(p2)
        plain = decrypt_bifid(ciphertext, p2)
        pScore = fitness.score(plain)
        count = 0
        while count <1000:
            a, b = random.randint(0,24), random.randint(0,24) #select random letters to switch in the alphabet
            c = p2[:]
            c[a],c[b] = c[b],c[a]
            plain = decrypt_bifid(ciphertext, c)
            cScore = fitness.score(plain)
            if cScore > pScore:
                pScore = cScore
                p2 = c[:]
                count = 0
            count+=1
        if pScore>mScore:
            mScore = pScore
            m = p2[:]
            print(f'Best key: {"".join(m)} - {decrypt_bifid(ciphertext, m)[:20]}')

