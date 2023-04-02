import re
import pandas as pd
import difflib
import time
from io import StringIO
import sys

#EPSILON = 1e-
def run(file):
    
    #/home/djordje/Documents/GitHub/slagalica-ocr/out/c084e09a'
    
    rel_file = file.split('/')[-1]
    
    with open('recnik.txt') as f:
        recnik= f.read().lower().split("\n")
    recnik = recnik[::-1]

    def mostSimilarList(x):
        
        
        if '.' in x:
            return difflib.get_close_matches(x,filter(lambda y: len(y) >= len(x), recnik),n=1)
        
        fst = difflib.get_close_matches(x,recnik,n=1)
        snd = difflib.get_close_matches(x,filter(lambda y: len(y) == len(x), recnik),n=1)
        
        if not (fst or snd):
            return x
        
        tempX = ([z for z in x if not z.isdigit()])
        return snd if (difflib.SequenceMatcher(None, snd[0], tempX).ratio() >= difflib.SequenceMatcher(None, fst[0], tempX).ratio()) else fst
        
    def similar(a, b):
        
        return any([difflib.SequenceMatcher(None, a, x).ratio() >0.5 for x in b])

    def checker(x):     #PANDAS NE PODRZAVA CIRILICU, POTREBNO OVAKO PROCITATI KROZ TXT CYR
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
            return [m[0],x] if similar(x,(m:=mostSimilarList(x))) else x
        return x

    #ako nije u recniku vratiti 2 moguca resenja i sta nije u recniku

    start_time = time.time()

#'out/c105e18a.txt'
    search = pd.read_csv(file)
    search.columns = ['toCheck']
    mocker = search.loc[search['toCheck'].str.contains(' - ')]['toCheck'].apply(splitter).apply(controller)
    print("%s sekundi exec vreme" % (time.time() - start_time))
    

    for mini in mocker:
        
        if len(mini)==2:
            if len(mini[0])>1 and len(mini[1]) > 1:
                search = search.replace(mini[1].upper(),mini[0].upper(), regex=True)
                print(mini[1].upper(),mini[0].upper())
    search.columns = [''] * len(search.columns)
    
    search.to_csv(f'banished/{rel_file}',index=None)
    for x in search.values:
        print(x)
def main():
    #run(sys.argv[1])
    run("/home/djordje/Documents/GitHub/slagalica-ocr/out/c084e09a.txt")
    
if __name__=="__main__":
    main()