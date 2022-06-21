## SETUP

from pycipher import *
import matplotlib.pyplot as plt
import sys
from langdetect import detect
import operator
import collections
import time
import pyperclip
from nltk.util import ngrams
#from enigma.machine import EnigmaMachine   #enigma machine
from selenium import webdriver             #web scraping
import pyautogui
import wordninja  #split text into readable format (add spaces)
#from baseconvert import * #base convert
#from secretpy import Trifid
import itertools
from bs4 import BeautifulSoup as bs4
import requests
import random
from ngram_score import ngram_score




## DECRYPT CIPHERS
    
def decrypt_enigma(rotor, reflectors, ring, plugboard, initial, key, ciphertext):
    machine = EnigmaMachine.from_key_sheet(
       rotors=rotor,
       reflector=reflectors,
       ring_settings=ring,
       plugboard_settings=plugboard) #'II IV V', 'b', [1,20,11], 'AV BS CG DL FU HZ IN KM OW RX' - initial setup
    
    machine.set_display(initial) #set starting position- 'WXC'
    msg_key = machine.process_text(key)
    machine.set_display(msg_key) #'KCH'
    return machine.process_text(ciphertext)

def decrypt_railfence(ciphertext, rails):
    return Railfence(rails).decipher(ciphertext)

def bruteforce_railfence(ciphertext):
    keys = []
    for i in range(2,20):
        keys.append(decrypt_railfence(ciphertext,i))
        if check_english(decode_railfence(ciphertext,i))==True:
            keys.append(i)
            try:
                print(decode_railfence(ciphertext, i)[:100])
            except:
                print(decode_railfence(ciphertext, i))
    return keys#"\n".join(keys)
        
def decrypt_vigenere(key, ciphertext):           
    return Vigenere(key).decipher(ciphertext)

def bruteforce_vigenere(ciphertext,file=2):
    x = []
    fo = open(path+"dictionary"+str(file)+".txt") #2 = basic, 1 = very detailed
    words = fo.readlines()
    fo.close()
    d = []
    for word in words:
        word = word.strip()
        try:
            decryptedText = decrypt_vigenere(word, ciphertext)
        except: pass
        if check_english(decryptedText)==True:
                x.append(word)
                v=decryptedText[:40]
                print(v)
                d.append(v)
        #print(word)
    if len(x)>=2:
            return x, d
    elif len(x)==1:
        return decrypt_vigenere(x[0],ciphertext)
    elif x ==[]:
        return False
            
def bruteforce_vigenere_len(ciphertext,length): #bruteforce vigenere of key with certain length
    x = list(itertools.product(alphabet1, repeat = length))
    for i in x:
        decryptedText = decrypt_vigenere(''.join(i), ciphertext)
        if check_english(decryptedText):
            print(decryptedText[:40], i)
    
def vig_rail(ciphertext,file=2): #Vigenere combined with railfence
    x = []
    fo = open(path+"dictionary"+str(file)+".txt") #2 = basic, 1 = very detailed
    words = fo.readlines()
    fo.close()
    d = []
    for word in words:
        word = word.strip()
        decryptedText = decrypt_vigenere(word, ciphertext)
        decryptedText = decrypt_railfence(decryptedText, 47)
        if check_english(decryptedText)==True:
            x.append(word)
            v=decryptedText[:40]
            print(v)
            d.append(v)
            time.sleep(1)
            
    if len(x)>=2:
            return x, d
    elif len(x)==1:
        return decrypt_vigenere(x[0],ciphertext)
    elif x ==[]:
        return False

def xor(key, ciphertext):
    c = ciphertext.split(',')
    c = [int(i) for i in c]
    c = [key^i for i in c]
        
        
def decrypt_substitution(alphabet, ciphertext):
    return SimpleSubstitution(alphabet).decipher(ciphertext)

def bruteforce_sub(ciphertext):
    fitness = ngram_score('english_quadgrams.txt')
    m = list(alphabet2)
    mScore = -99e9
    p1,p2 = mScore, m[:]
    i = 1
    while True:
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
            print(f'Best key: {m}')
            print(decrypt_substitution(m, ciphertext))

def decrypt_keyword_sub(ciphertext, keyword_list, shift=False):
    if shift:
        for i in keyword_list.lower().split(' '):
            try:
                a = key2alpha(i, True)
                for shift in a:
                #a1=a[shift:]+a[:shift]
                    text = decrypt_substitution(shift, ciphertext)
                    if check_english(text):
                        print(shift, text[:20])
            except: pass
            
    if not shift:
        for i in keyword_list.lower().split(' '):
            try:
                a = key2alpha(i)
                print(a)
            except: pass
            text = decrypt_substitution(a, ciphertext)
            if check_english(text):
                print(text[:20])
       
            

def brute_keyword_sub(ciphertext, custom=None, file=2):
    x = []
    if custom!=None:
        words = custom.split(' ')
    else:
        fo = open(path+"dictionary"+str(file)+".txt") #2 = basic, 1 = very detailed
        words = fo.readlines()
        fo.close()
    decrypt_keyword_sub(ciphertext, ' '.join([i.strip() for i in words]), True)
        
    
def setup_online(x,variant):
    browser = webdriver.Chrome(executable_path=r'/home/ctc/Documents/chromedriver')
    browser.get('https://www.guballa.de/'+x+'-solver')
    
    lang = browser.find_element_by_name('lang')
    lang.click()
    pyautogui.press('down')
    pyautogui.press('enter')

    if x=='vigenere':
        if variant=='autokey':
            var = browser.find_element_by_name('variant')
            var.click()
            pyautogui.press('down')
            pyautogui.press('enter')
        elif variant=='beaufort':
            var = browser.find_element_by_name('variant')
            var.click()
            pyautogui.press('down')
            pyautogui.press('down')
            pyautogui.press('enter')
    return browser

def online_guballa(browser, ciphertext):
    text = browser.find_element_by_id('cipher')
    text.send_keys(ciphertext)
    #pyautogui.hotkey('ctrl','v')

    enter = browser.find_element_by_name('break')
    enter.click()

    output = browser.find_element_by_name('clear_text')
    browser.find_element_by_id('cipher').clear()
    return output.text

def setup_dcode(direction,mode): #online transposition solver
    browser = webdriver.Chrome(executable_path=r'/home/ctc/Documents/chromedriver')
    browser.get('https://www.dcode.fr/'+mode+'transposition-cipher')
    time.sleep(1)
    pyautogui.click(x=2689, y=908)
    time.sleep(1)
    pyautogui.scroll(-4)
    time.sleep(1)
    text = browser.find_element_by_id('decipher_transposition_ciphertext')
    text.clear()
    text.send_keys('t')
    pyautogui.press('backspace')
    pyautogui.hotkey('ctrl','v')
    time.sleep(1)
    if direction=='vertical' and mode=='':
        vertical = browser.find_element_by_id('decipher_transposition_direction_vertical')
        if vertical!=None:
            vertical.click()
        #print(vertical)
        time.sleep(1)
        #time.sleep(20)
        #vertical.click()
    if direction=='horizontal' and mode=='columnar-':
        vertical = browser.find_element_by_id('decipher_transposition_direction_horizontal')
        time.sleep(2)
        vertical.click()
    return browser
    
def online_dcode(k, browser, ciphertext):
    time.sleep(1)
    pyautogui.scroll(-3)
    key = browser.find_element_by_id('code_decipher_transposition_permutation')
    key.clear()
    key.send_keys(k)
    pyautogui.press('enter')
    return browser.find_element_by_class_name('result').text
    
def online_vig_trans(n, ciphertext):
    browser = setup_online('horizontal','')
    for i in range(6,n):
        with open((path+"key"+str(i)+".txt"),'r') as fo:
                words = fo.readlines()
        with open(('trans'+str(i)+'.txt'),'w+') as file:
            for x in words:
                file.write(online_dcode(x, browser, ciphertext)[:100]+'\n')
                time.sleep(1)
    pyautogui.hotkey('ctrl','w')
    browser = setup_online('vigenere','')
    for i in range(2,n):
        with open((path+"trans"+str(i)+".txt"),'r') as file:
            words = file.readlines()
        for v in words:
            pyperclip.copy(v)
            print(online_guballa(browser,ciphertext)[:40])    

def rail_vig_online(ciphertext):
    x = bruteforce_railfence(ciphertext)
    """browser1 = setup_online('substitution','')
    for a in x:
        y = online_guballa(browser1,a[:500])
        print(y[:50])
    time.sleep(10)"""
    browser2 = setup_online('vigenere','')
    for b in x:
        z = online_guballa(browser2,b[:500])
        print(z[:50])
    time.sleep(10)
    browser3 = setup_online('vigenere','autokey')
    for c in x:
        t = online_guballa(browser3,c[:500])
        print(t[:50])
    time.sleep(10)
    browser4 = setup_online('vigenere','beaufort')
    for d in x:
        s = online_guballa(browser4,d[:500])
        print(s[:50])

def decrypt_columnar(key,ciphertext): #works
    key2 = ''
    for i in key:
        if i not in key2:
            key2+=i
    key1 = ''.join(sorted(key2))
    #ciphertext = key1 + ciphertext
    columns = []
    k_len = len(key2)
    while len(ciphertext)%k_len!=0:
        ciphertext+='.'
    f=0
    for i in range(0,len(ciphertext),len(ciphertext)//k_len):
        columns.append(key2[f]+ciphertext[i:i+(len(ciphertext)//k_len)])
        f+=1
        
    output = ''
    for char in key1:
        for col in columns:
            if col[0]==char:
                output+=col[1:]
                break
    out = []
    for i in range(len(ciphertext)//k_len):
        out.append(output[i::len(ciphertext)//k_len])
    return ''.join(out)
    

def decrypt_transposition(key, ciphertext): #probably wrong
    x = len(set(key))
    numOfColumns = x
    c = sorted(list(set(key)))
    o = list(set(key))

    plaintext = [''] * numOfColumns
    for i in o:
        plaintext[o.index(i)] += i
    col = 0
    row = 0
    
    for symbol in ciphertext:
        plaintext[col] += symbol
        col += 1  
        if col == numOfColumns:
            col = 0
            row += 1
    plaintext.sort()
    plaintext = [e[1:] for e in plaintext]
    return "".join(plaintext)

def decrypt_transposition(key, ciphertext):
    return ColTrans(key).decipher(ciphertext)
    
def decrypt_transposition_key(key, ciphertext):
    fo = open(path+"key"+str(key)+".txt")
    words = fo.readlines()
    fo.close()
    x =[]
    w = []
    for key in words:
        key = key.strip()
        decryptedText = decrypt_c_transposition(key, ciphertext).lower()
        x = input()
        if x=="":
            print(decryptedText)
            continue


def b_trans_keys(ciphertext):
    global previous
    #w = []
    x = []
    previous = previous.lower()
    r = set(previous.split(" "))
    for i in r:
        u = len(set(list(i)))
        if len(i)>4 and (u%7==0 or u%5==0):
            x.append(i)
    print(x)
    for key in x:
        x = input()
        if x != "":
            break
        else:
            key = key.strip()
            decryptedText = decrypt_c_transposition(key, ciphertext).lower()
            print(decryptedText)  

def t(ciphertext):
    global previous
    x=set(previous.split(' '))
    x.remove('')
    print(x)
    t=[]
    a=[]
    for i in x:
        v = decrypt_c_transposition(i, ciphertext[:500])
        t.append(v)
    browser = setup_online('vigenere','')
    for i in t:
        w = online_guballa(browser, i)
        if check_english(w)==True:
            print(w)
            a.append(w)
    print(a)

def simple_trans(ciphertext,n):
    start=0
    v=[]
    while len(ciphertext)%n!=0:
        ciphertext+='x'
    x = len(ciphertext)
    while True:
        if start==n:
            break
        v.append('')
        for i in range(start,x,n):
            v[start]+=ciphertext[i]
        start+=1
    return ''.join(v)

def rev_simple_trans(ciphertext,n):
    start=0
    v=[]
    r=0
    while len(ciphertext)%n!=0:
        ciphertext+='x' #padding
    x = len(ciphertext)
    while True:
        if start==n:
            break
        v.append('')
        for i in range(start,x,n):
            v[start]+=ciphertext[i]
            if r %2==0:
                v[start] = reverse(v[start])
        start+=1
        r+=1
    return ''.join(v)

def bruteforce_c_transposition(ciphertext,n):
    d = 2
    x =[]
    w = []
    while d<int(n):
        fo = open((path+"key"+str(d)+".txt"),'r')
        words = fo.readlines()
        fo.close()
        file = open((path+"trans"+str(d)+".txt"),'a+')
        for key in words:
            key = key.strip()
            decryptedText = decrypt_c_transposition(key, ciphertext).lower()
            file.write(decryptedText[:300]+'\n')
            """x = input()
            if x=="":
                continue"""
            if check_english(decryptedText)==True:
                x.append(key)
                v= decryptedText[:30]
                print(v)
                #w.append(v)
            #print(key)
        d+=1
        file.close()
    print(x,w)
    if len(x)>=2:
            return x
    elif len(x)==1:
        return x#decrypt_c_transposition(x[0],ciphertext)
    elif x ==[]:
        return False

def columnar_vig(ciphertext, n):
    bruteforce_c_transposition(ciphertext,n)
    browser = setup_online('vigenere','')
    y=[]
    for i in range(2,n):
        with open((path+"trans"+str(i)+".txt"),'r') as file:
            x=file.readlines()
            for v in x:
                v=v.strip()
                w = online_guballa(browser, ciphertext)
                if check_english(w)==True:
                    print(w)
                    y.append(w)
    print(y)
                

def c_trans_vig(n, ciphertext):
    bruteforce_c_transposition(ciphertext, n)
    browser = setup_online('vigenere','')
    v=[]
    for i in range(2,n):
        with open((path+'trans'+str(i)+'.txt'),'r') as file:
            l = file.readlines()
        file1 = open((path+'sub'+str(i)+'.txt'),'a+')
        for v in l:
            x = online_guballa(browser, v)
            #print(x)
            if check_english(x):
                print(x)
                file1.write(x+'\n')
                v.append(x)
        file1.close()
    return v

def bases(ciphertext):
    file=open('test.txt','a+')
    for i in range(3,16): #base
            for j in range(2,16): #split size
                    x=split1(ciphertext[:120],j)
                    r=[]
                    for p in x:
                            try:
                                    v=base_convert(p,i,10)
                                    r.append(chr(int(v)))
                            except: pass
                    try: file.write(''.join(r))
                    except: pass
    file.close()

def decrypt_playfair(key, ciphertext):
    global alpahbet1
    a = set(list(key))
    return Playfair(key=a).decipher(ciphertext)

def decrypt_polybius(alphabet, size, chars,ciphertext):
    return Polybius(alphabet, size, chars).decipher(ciphertext)

def decrypt_porta(key, ciphertext):
    return Porta(key).decipher(ciphertext)

def decrypt_bifid(key,l ,ciphertext):
    return Bifid(key, l).decipher(ciphertext)

def bruteforce_bifid(ciphertext,file=2):
    fo = open(path+"dictionary"+str(file)+".txt") #2 = basic, 1 = very detailed
    words = fo.readlines()
    fo.close()
    d = []
    for i in range(10):
        for word in words:
            word = word.strip()
            decryptedText = decrypt_bifid(key2alpha(word), i,ciphertext)
            if check_english(decryptedText)==True:
                    x.append([word,i])
                    v=decryptedText[:40]
                    print(v)
                    d.append(v)
                    time.sleep(1)
        
    if len(x)>=2:
            return x, d
    elif len(x)==1:
        return decrypt_bifid(x[0][0],x[0][1],ciphertext)
    elif x ==[]:
        return False
    
def bruteforce_porta(ciphertext, file=2):#Porta cipher bruteforce
    x = []
    fo = open(path+"dictionary"+str(file)+".txt") #2 = basic, 1 = very detailed
    words = fo.readlines()
    fo.close()
    d = []
    for word in words:
        word = word.strip()
        decryptedText = decrypt_porta(word, ciphertext)
        if check_english(decryptedText)==True:
                x.append(word)
                v=decryptedText[:40]
                print(v)
                d.append(v)
                time.sleep(1)
    if len(x)>=2:
            return x, d
    elif len(x)==1:
        return decrypt_porta(x[0],ciphertext)
    elif x ==[]:
        return False
    
def split1(ciphertext,x): #splits ciphertext in blocks of x
    v=[]
    for i in range(0,len(ciphertext),x):
        v.append(ciphertext[i:i+x])
    #print(dict(collections.Counter(v)))
    return v

def bi_tri(ciphertext):
    x2 = split1(ciphertext,2)
    x3 = split1(ciphertext,3)
    for i in range(1,17):
        print(str(i)+' : '+ str(len(set(split1(ciphertext,i)))))
    return {k: v for k, v in sorted(x2.items(), key=lambda item: item[1])},{k: v for k, v in sorted(x3.items(), key=lambda item: item[1])}

def distance(ciphertext, letter):
    x = list(ciphertext)
    v = []
    y = []
    r = 0
    for i in x:
        if i==letter:
            v.append(x.index(i)+r)
            r+=1
            x.remove(i)
    for i in range(len(v)-1):
        h = v[i+1]-v[i]
        y.append(h)
    return y
    
def sub_blocks(ciphertext,x): #replace each block of letters (of length x) with a letter in the alphabet and return this dict
    alphabet=list(alphabet1)+list('123456789.')
    r = list(set(split1(ciphertext,x)))
    w = {}
    for i in r:
        w[i] = alphabet[r.index(i)]
    return w

def sub(ciphertext,x): #takes the dictionary and substitutes blocks for letters
    ciphertext1 = split1(ciphertext,x)
    r = sub_blocks(ciphertext,x)
    o = ''
    for i in ciphertext1:
        o+=r[i]
    return o    

def polybius(ciphertext,x): #substitutes the blocks for letters, then uses bruteforce substitution, where x is the greates number of block size to try
    r = []
    y=[]
    for i in range(2,x+1):
        v=sub(ciphertext,i)
        r.append(v[:1000])
    browser = setup_online('substitution','')
    for i in r:
        w = online_guballa(browser,i)[:100]
        y.append(w)
        print(w)
    return y

def l27_sub(ciphertext,b):
    r=[]
    l = list(set(list(split1(ciphertext,b))))
    x=split1(ciphertext,b)
    for i in l:
        y=''.join([t for t in x if t!=i])
        r.append(sub(y,b))
    return r

def sub_list(l):
    browser = setup_online('substitution','')
    y=[]
    for i in l:
        w = online_guballa(browser,i[:200])
        y.append(w[:100])
    print('\n'.join(y))

def replace_bin(ciphertext):
    x=list(itertools.product('012 ',repeat=2))
    file = open('test1.txt','a+')
    for i,j in x:
        ciphertext1=ciphertext.replace(i,j)
        file.write(ciphertext1+'\n')
    file.close()
       
def test1(ciphertext):
    ciphertext2 = split1(ciphertext,2)
    ciphertext3 = split1(ciphertext,3)
    v2 = list(set(ciphertext2))
    v3 = list(set(ciphertext3))
    for i in v2:
        r = []
        for j in ciphertext2:
            if j!=i:
                r.append(j)
        sub(''.join(r),2)
    xs = []
    for i in v3:
        r = []
        for j in ciphertext3:
            if i!=j:
                r.append(j)
        x = sub(''.join(r),3)
        xs.append(x[:500])
    browser = setup_online('substitution','')
    y = []
    for i in xs:
        w = online_guballa(browser,i)[:100]
        y.append(w)
        print(w[:100])
    return y
    
def decrypt_adfgvx(ciphertext, key, keyword):
    return ADFGVX(key=key, keyword=keyword).decipher(ciphertext)

def bruteforce_adfgvx(ciphertext, keyword):
    fitness = ngram_score('english_quadgrams.txt')
    m = list(alphabet2)+list('0123456789')
    mScore = -99e9
    p1,p2 = mScore, m[:]
    i = 1
    while True:
        i+=1
        random.shuffle(p2)
        plain = decrypt_adfgvx(ciphertext, ''.join(p2), keyword)
        pScore = fitness.score(plain)
        count = 0
        while count <1000:
            a, b = random.randint(0,35), random.randint(0,35) #select random letters to switch in the alphabet
            c = p2[:]
            c[a],c[b] = c[b],c[a]
            plain = decrypt_adfgvx(ciphertext, ''.join(c), keyword)
            cScore = fitness.score(plain)
            if cScore > pScore:
                pScore = cScore
                p2 = c[:]
                count = 0
            count+=1
        if pScore>mScore:
            mScore = pScore
            m = p2[:]
            print(f'Best key: {m}')
            print(decrypt_adfgvx(ciphertext, ''.join(m), keyword))
            
def null(ciphertext=1): #Null cipher (form of steganography)
    if ciphertext==1:
        global previous
        ciphertext = previous
    message = ciphertext.upper()

    words_in_message = message.split()

    decrypted_message = ""

    for word in words_in_message:
        decrypted_message += word[0]

    return decrypted_message
   


def automatic(ciphertext):
    print("IOC: {}".format(ioc(ciphertext)))
    print("Possible keys: {}".format(factorise(len(ciphertext))))
    print(f"Ciphertext length: {len(ciphertext)}")
    
    print(f"Atbash: {decrypt_atbash(ciphertext)[:20]}")
    print(bruteforce_affine(ciphertext))

    

    print("Railfence: ")
    for i in bruteforce_railfence(ciphertext):
        print(i[:20])
        
    '''browser = setup_online('substitution','classical')
    print("Substitution: %s"% online_guballa(browser, ciphertext)[:20])
    print("Substitution reversed: %s"%online_guballa(browser, reverse(ciphertext))[:20])
    pyautogui.hotkey('ctrl','w')
    browser = setup_online('vigenere','classical')
    print("Classical Vigenere: %s"%(online_guballa(browser, ciphertext)[:20]))
    print("Classical Vigenere reversed: %s"%(online_guballa(browser, reverse(ciphertext))[:20]))
    pyautogui.hotkey('ctrl','w')
    browser = setup_online('vigenere','autokey')
    print("Autokey Vigenere: %s"%(online_guballa(browser, ciphertext)[:20]))
    print("Autokey Vigenere reversed: %s"%(online_guballa(browser, reverse(ciphertext))[:20]))
    pyautogui.hotkey('ctrl','w')
    browser = setup_online('vigenere','beaufort')
    print("Beaufort Vigenere: %s"%(online_guballa(browser, ciphertext)[:20]))
    print("Beaufort Vigenere reversed: %s"%(online_guballa(browser, reverse(ciphertext))[:20]))
    pyautogui.hotkey('ctrl','w')
    #print(bruteforce_c_transposition(ciphertext,7))
    #setup_dcode('vertical', '')'''
    frequency(ciphertext)
    for i in range(1,15):
        ngram_plot(i,ciphertext,i,False)
    
    
    