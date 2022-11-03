import wordninja
from langdetect import detect
import collections
import matplotlib.pyplot as plt
from ngram_score import ngram_score
from nltk.util import ngrams
import operator

path = '/home/ctc/OneDrive/Charles/Projects/Codebreaking/Python/'
alphabet1, alphabet2 = 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def check_english(n): #check if n makes sense
    try:
        crib = "the"
        n = n.lower()
        if detect(n)=='en' and "t" in n and "e" in n and crib.lower() in n[:60]: return True 
        else: return False
    except: return False

def key2alpha(keyword, shift=False): #converts keyword into alphabet
    keyword=keyword.lower()
    alphabet2= list(alphabet1)
    alphabet = []
    for i in keyword:
        if i not in alphabet:
            alphabet.append(i)
            alphabet2.remove(i)
    if not shift:
        alphabet+=alphabet2
        return ''.join(alphabet)
        
    else:
        alphabet3s = []
        for j in range(26):
            alphabet3=alphabet2[:j]
            alphabet3+=alphabet
            alphabet3+=alphabet2[j:]
            alphabet3s.append(''.join(alphabet3))
        return alphabet3s
    
    
def split_text(text): #put spaces between words (using wordninja library)
    x = wordninja.split(text)
    print(' '.join(x))
    return x

def anagram(x): #find anagrams of x
    y=sorted(list(x.lower()))
    v=[]
    with open(path+'dictionary1.txt','r') as file:
        for i in file:
            i=list((i.lower()).rstrip())
            if sorted(i)==y:
                v.append("".join(i))
    return v

def factorise(x): #prime factors of x
    nums = [i for i in range(2,x) if x%i==0]
    return nums

def base_convert(number, in_base, out_base):
    return base(number,in_base,out_base,string=True)
    
def reverse(ciphertext):
    x = ciphertext[::-1]
    return x
        
def ngram_plot(x,ciphertext,sub,plot=True):
    d = {}
    d2={}
    a = list(ngrams(ciphertext,x))
    b = collections.Counter(a)
    d2 = [''.join(i) for i in b]
    b = [list(i) for i in b.most_common(10)]
    
    #for i in c:
     #   d2["".join(i[0])] = i[1]
    if plot==True:
        for i in b:
            d["".join(i[0])] = i[1]
        plt.subplot(4,1,sub)
        plt.bar(list(d.keys()), list(d.values()))
    print(len(d2[0]), len(d2))
    return b

def ioc(ciphertext): #IOC
    english_ioc = 0.068
    ics = []
    freqsum = 0.0
    IC=0
    N = len(ciphertext)
    freqs  = collections.Counter(ciphertext.upper())
    for letter in alphabet2:
        freqsum += (freqs[ letter ] * ( freqs[ letter ] - 1 )) / (N * (N - 1))
    return freqsum


def frequency(ciphertext):
    ciphertext=ciphertext.lower()
    letter_frequencies = {"e":0.1202,"t":0.0910,"a":0.0812,"o":0.0768,"i":0.0731,"n":0.0695,"s":0.0628,"r":0.0602,"h":0.0592,"d":0.0432,"l":0.0398,"u":0.0288,"c":0.0271,"m":0.0261,"f":0.0230,"y":0.0211,"w":0.0209,"g":0.0203,"p":0.0182,"b":0.0149,"v":0.0111,"k":0.0069,"x":0.0017,"q":0.0011,"j":0.0010,"z":0.0007}
    a = ''.join(e for e in ciphertext if e.isalpha())
    total = 0
    for value in letter_frequencies:
        letter_frequencies[value] *= len(ciphertext)
    for value in letter_frequencies:
        total += letter_frequencies[value]
    all_freq = {}
    for i in ciphertext:
        if i in all_freq:
            all_freq[i] += 1
        else:
            all_freq[i] = 1
    for i in 'abcdefghijklmnopqrstuvwxyz':
        if i not in all_freq:
            all_freq[i] = 0        
    all_freq = sorted(all_freq.items(), key=operator.itemgetter(1))
    sorted_freq = collections.OrderedDict(all_freq)
    letter_frequencies = collections.OrderedDict(letter_frequencies)
    ngram_plot(2,ciphertext,2)
    plt.subplot(4,1,2)
    plt.bar(letter_frequencies.keys(), letter_frequencies.values(), width = 0.3, color='r',align='edge')
    ngram_plot(3,ciphertext,3)
    ngram_plot(4,ciphertext,4)
    plt.subplot(4,1,1)
    plt.bar(sorted_freq.keys(), sorted_freq.values(), width = 0.3, color='g',align='center')
    plt.bar(letter_frequencies.keys(), letter_frequencies.values(), width = 0.3, color='r',align='edge')
    plt.show()
    return sorted_freq

def blocks(ciphertext, n=2):
    blocks = [ciphertext[i:i+n] for i in range(0, len(ciphertext), n)]
    return blocks

def columns(ciphertext, n=2):
    columns = [ciphertext[i::n] for i in range(n)]
    return columns
