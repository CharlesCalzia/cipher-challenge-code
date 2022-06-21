import utils
from pycipher import Railfence, ColTrans
from ngram_score import ngram_score
import random
import square_ciphers

alphabet2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def decrypt_railfence(ciphertext, rails):
    return Railfence(rails).decipher(ciphertext)

def bruteforce_railfence(ciphertext):
    keys = []
    for i in range(2,20):
        if utils.check_english(decrypt_railfence(ciphertext,i))==True:
            keys.append(i)
            try:
                print(decrypt_railfence(ciphertext, i)[:20])
            except:
                print(decrypt_railfence(ciphertext, i))
    return keys

def decrypt_transposition(key, ciphertext, cipher2=False):
    if not cipher2: return ColTrans(key).decipher(ciphertext)
    else: return cipher2(ColTrans(key).decipher(ciphertext))

def bruteforce_transposition(ciphertext, maxLen=10):
    possible_keys = []
    for i in range(2,maxLen+1):
        with open(f'key{i}.txt','r') as file:
            keys = [i.strip() for i in file.readlines()]
        for key in keys:
            if utils.check_english(decrypt_transposition(key,ciphertext))==True:
                possible_keys.append(key)
                try:
                    print(decrypt_transposition(key, ciphertext)[:20])
                except:
                    print(decrypt_transposition(key, ciphertext))
    return keys

def bruteforce_trans(ciphertext, maxLen=10, cipher2=False):
    for keyLen in range(2,maxLen+1):
        fitness = ngram_score('english_quadgrams.txt')
        m = list(alphabet2)[:keyLen]
        mScore = -99e9
        p1,p2 = mScore, m[:]
        i = 1
        for i in range(10):
            i+=1
            random.shuffle(p2)
            plain = decrypt_transposition("".join(p2), ciphertext, cipher2)
            pScore = fitness.score(plain)
            count = 0
            while count <1000:
                a, b = random.randint(0,keyLen-1), random.randint(0,keyLen-1) #select random letters to switch in the alphabet
                c = p2[:]
                c[a],c[b] = c[b],c[a]
                plain = decrypt_transposition("".join(c), ciphertext, cipher2)
                cScore = fitness.score(plain)
                if cScore > pScore:
                    pScore = cScore
                    p2 = c[:]
                    count = 0
                count+=1
            if pScore>mScore:
                mScore = pScore
                m = p2[:]
                print(f'Best key: {"".join(m)} - {decrypt_transposition("".join(m), ciphertext, cipher2)[:20]}')