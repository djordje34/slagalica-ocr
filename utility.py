import re
import pandas as pd
import difflib
import time
from io import StringIO


with open('recnik.txt') as f:
    recnik= f.read().lower().split("\n")

def mostSimilarList(x):
    
    return difflib.get_close_matches(x,recnik,n=2)

def similar(a, b):
    
    return any([difflib.SequenceMatcher(None, a, x).ratio() >0.75 for x in b])

def checker(x):     #PANDAS NE PODRZAVA CIRILICU, POTREBNO OVAKO PROCITATI KROZ TXT CYR
    with open('recnik.txt') as f:
        if x in recnik:
            return True
    return False;


def splitter(x):
    return x.split(' - ')[1]

def cutter(x):
    x=str(x)
    return re.sub(r'^\s+|\s+$' , "" , x).lower()

def controller(x):
    x=cutter(x)
    
    if not checker(x):
        return (''.join([w+'|!' for w in m])+x).split("|!") if similar(x,(m:=mostSimilarList(x))) else 'MANUELNO PROVERITI'
    return x

#ako nije u recniku vratiti 2 moguca resenja i sta nije u recniku

start_time = time.time()


search = pd.read_csv('out/c160e05a.txt')
search.columns = ['toCheck']
mocker = search.loc[search['toCheck'].str.contains(' - ')]['toCheck'].apply(splitter).apply(controller)
print(mocker)
print(print("%s sekundi exec vreme" % (time.time() - start_time)))