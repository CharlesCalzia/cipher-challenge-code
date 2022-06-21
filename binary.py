from ngram_score import ngram_score
import random
from pycipher import *

alphabet2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def decrypt_substitution(alphabet, ciphertext):
    return SimpleSubstitution(alphabet).decipher(ciphertext)

def decrypt_bacon(ciphertext, type=2):
    if type==1: #each letter is unique
        in_chars='00000 00001 00010 00011 00100 00101 00110 00111 01000 01001 01010 01011 01100 01101 01110 01111 10000 10001 10010 10011 10100 10101 10110 10111 11000 11001'.split(' ')
    else: #classical (I, J are the same and U, V are the same)
        in_chars='00000 00001 00010 00011 00100 00101 00110 00111 01000 01000 01001 01010 01011 01100 01101 01110 01111 10000 10001 10010 10011 10011 10100 10101 10110 10111'.split(' ')
    new_ciphertext= []
    for i in range(0,len(ciphertext)-4,5):
        try: new_ciphertext.append(alphabet2[in_chars.index(ciphertext[i:i+5])])
        except: return False
    ciphertext=''.join(new_ciphertext)
    return ciphertext

def bruteforce_bacon(ciphertext, type=2):
    ciphertext=decrypt_bacon(ciphertext)
    if ciphertext==False: return False

    fitness = ngram_score('english_quadgrams.txt')
    m = list(alphabet2)
    mScore = -99e9
    p1,p2 = mScore, m[:]
    i = 1
    for i in range(10):
        i+=1
        random.shuffle(p2)
        plain = decrypt_substitution(p2, ciphertext)
        pScore = fitness.score(plain)
        count = 0
        while count <1000:
            a, b = random.randint(0,25), random.randint(0,25) #select random letters to switch in the alphabet
            c = p2[:]
            c[a],c[b] = c[b],c[a]
            plain = decrypt_substitution(c, ciphertext)
            cScore = fitness.score(plain)
            if cScore > pScore:
                pScore = cScore
                p2 = c[:]
                count = 0
            count+=1
        if pScore>mScore:
            mScore = pScore
            m = p2[:]
            print(f'Best key: {"".join(m)} - {decrypt_substitution(m, ciphertext)[:20]}')