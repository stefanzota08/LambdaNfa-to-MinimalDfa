def Remove(duplicate):
    for a in duplicate:
        for b in a:
            while a.count(b) > 1:
                a.remove(b)
    return duplicate

class Automat:
    def __init__(self, fisier):
        self.tata = []
        self.k = open(fisier, 'r')
        self.q = int(self.k.readline())
        self.f = int(self.k.readline())
        self.F = self.k.readline()
        self.F = self.F.split()
        self.F = [int(self.x) for self.x in self.F]
        self.v = int(self.k.readline())
        self.V = self.k.readline()
        self.V = self.V.split()
        self.g = int(self.k.readline())
        self.G = []
        for self.i in range(self.g):
            self.aux = self.k.readline()
            self.aux = self.aux.split()
            self.aux[0] = int(self.aux[0])
            self.aux[2] = int(self.aux[2])
            self.G = self.G + [self.aux]


def lambdanfa_to_nfa(automat1):
    vect = []
    for i in range(automat1.q):
        vect = vect + [[i]]
    l = []
    for i in range(automat1.q):
        l = l + [[i]]

    for i in automat1.G:
        if i[1] == '$':
            if i[2] not in l[i[0]]:
                l[i[0]] = l[i[0]] + [i[2]]

    for i in automat1.G:
        if i[1] == '$':
            if i[2] not in vect[i[0]]:
                vect[i[0]] = vect[i[0]] + [i[2]]
    ################# lambda inchiderea automatului #####################

    for u in range(automat1.q):
        for i in range(0, len(l)):
            for j in range(1, len(l[i])):
                l[i] = l[i] + l[l[i][j]]
            for b in l[i]:
                while l[i].count(b) > 1:
                    l[i].remove(b)
    for x in l:
        x.sort()
    # print(l)
    ######################################################################
    for nr in automat1.V:
        automat1.tata = automat1.tata + [[]]

    for cIndex in range(0, automat1.v):

        #### reuniune stari accesibile prin caracterul 'a' #################
        a = []
        for i in range(automat1.q):
            a = a + [[]]

        for index in range(0, len(l)):
            for elem in l[index]:
                for tranzitie in automat1.G:
                    if tranzitie[0] == elem and tranzitie[1] == automat1.V[cIndex]:
                        a[index] = a[index] + [tranzitie[2]]
            for b in a[index]:
                while a[index].count(b) > 1:
                    a[index].remove(b)
        ###########################################################################
        for i in range(automat1.q):
            automat1.tata[cIndex] = automat1.tata[cIndex] + [[]]

        for indice in range(0, len(a)):
            for element in a[indice]:
                automat1.tata[cIndex][indice] = automat1.tata[cIndex][indice] + l[element]

        automat1.tata[cIndex] = Remove(automat1.tata[cIndex])
        automat1.tata[cIndex] = Remove(automat1.tata[cIndex])
        for lista in automat1.tata[cIndex]:
            lista.sort()

    starifinale = []
    for multime in automat1.tata:
        for index in range(0, len(multime)):
            for elem in automat1.F:
                if elem in multime[index] and index not in starifinale:
                    starifinale = starifinale + [index]

    ##############################################################################
    StariDeSters = []
    i = 0
    while i < automat1.q:
        j = i + 1
        while j < automat1.q:
            if automat1.tata[0][i] == automat1.tata[0][j]:
                ok = 1
                for key in range(1, automat1.v):
                    if automat1.tata[key][i] != automat1.tata[key][j]:
                        ok = 0
                if ok == 1:
                    for m in automat1.tata:
                        for n in m:
                            if j in n:
                                n.remove(j)
                                if i not in n:
                                    n.append(i)
                                    n.sort()
                        m[j] = []
                        if j not in StariDeSters:
                            StariDeSters = StariDeSters + [j]
            j = j + 1
        i = i + 1


    StariDeSters.sort(reverse=True)
    for index in range(0, len(automat1.tata)):
        dict = {i: automat1.tata[index][i] for i in range(0, len(automat1.tata[index]))}
        automat1.tata[index] = dict
    for multimi in automat1.tata:
        for i in StariDeSters:
            del multimi[i]
    for i in StariDeSters:
        if i in starifinale:
            starifinale.remove(i)
    automat1.q = automat1.q - len(StariDeSters)
    automat1.F = starifinale
    automat1.f = len(starifinale)
    print("Dupa transformarea din $-NFA in NFA:")
    for index in range(0, len(automat1.tata)):
        print("Caracterul " + automat1.V[index] + " -> " + str(automat1.tata[index]))
    print("Stari finale : " + str(automat1.F))
    print("\n")

def nfa_to_dfa(automat2):
    stariNoi = []
    for dict in automat2.tata:
        for valoare in dict.values():
            if len(valoare) > 1 and valoare not in stariNoi:
                stariNoi = stariNoi + [valoare]
    ultimastare = list(automat2.tata[0].keys())[-1] + 1
    stariNoi = {i: stariNoi[i - ultimastare] for i in range(ultimastare, ultimastare + len(stariNoi))}
    for stare in stariNoi.keys():
        for index in range(0, len(automat2.tata)):
            l = []
            for elem in stariNoi[stare]:
                l = list(set(l) | set(automat2.tata[index][elem]))
            automat2.tata[index][stare] = l
    starifinale = []
    for dict in automat2.tata:
        for valoare in dict.values():
            for starefinala in automat2.F:
                if starefinala in valoare and valoare not in starifinale:
                    starifinale = starifinale + [valoare]

    for x in range(0, len(starifinale)):
        for val in stariNoi.keys():
            if starifinale[x] == stariNoi[val]:
                starifinale[x] = [val]

    starifinale = [i for [i] in starifinale]
    for dict in automat2.tata:
        for key in dict.keys():
            for stare, val in stariNoi.items():
                if dict[key] == val:
                    dict[key] = [stare]
    for dict in automat2.tata:
        for i in dict.keys():
            if dict[i] == []:
                dict[i] = None
            else: dict[i] = list(dict[i])[0]
    automat2.q = automat2.q + len(stariNoi)
    automat2.F = starifinale
    automat2.f = len(starifinale)
    print("Dupa transformarea din NFA in DFA:")
    for index in range(0, len(automat2.tata)):
        print("Caracterul " + automat2.V[index] + " -> " + str(automat2.tata[index]))
    print("\n")

def dfa_to_dfamin(automat3):
    maxstare = max(automat3.tata[0].keys()) + 1
    ListaDeStari = list(automat3.tata[0].keys())
    a = [0] * maxstare

    for i in range(0, maxstare):
        if i in ListaDeStari:
            l = []
            for j in range(0, maxstare):
                if j in ListaDeStari:
                    l = l + ['TRUE']
                else: l = l + [0]
            a[i] = l
        else:
            l = [0]*maxstare
            a[i] = l

    for i in range(0, maxstare):
        for j in range(0, maxstare):
            if i in ListaDeStari and j in ListaDeStari:
                if i in automat3.F and j not in automat3.F:
                    a[i][j] = 'FALSE'
                    a[j][i] = 'FALSE'
    ok = 1
    for i in range(0, maxstare):
        for j in range(0, maxstare):
            if i in ListaDeStari and j in ListaDeStari:
                for index in range(0, len(automat3.V)):
                    if automat3.tata[index][i] != None and automat3.tata[index][j] != None:
                        if a[automat3.tata[index][i]][automat3.tata[index][j]] == 'FALSE':
                            a[i][j] = 'FALSE'
    tranzitii = []
    for i in range(0, maxstare):
        nou = []
        for j in range(0, maxstare):
            if i in ListaDeStari and j in ListaDeStari:
                if a[i][j] == 'TRUE':
                    nou = nou + [j]
        if nou not in tranzitii:
            tranzitii = tranzitii + [nou]

    d = [{} for i in range(automat3.v)]
    for tran in range(0, len(tranzitii)):
        for elem in tranzitii[tran]:
            for index in range(0, automat3.v):
                x = automat3.tata[index][elem]
                for tran2 in tranzitii:
                    if x in tran2:
                        d[index][tran] = tran2
    starifinale = []
    for stare in automat3.F:
       for index in range(0, len(tranzitii)):
           if stare in tranzitii[index] and index not in starifinale:
               starifinale = starifinale + [index]
    for index in range(automat3.v):
        for key in d[index].keys():
            for i in range(0, len(tranzitii)):
                if d[index][key] == tranzitii[i]:
                    d[index][key] = i
    for key in list(d[0].keys()):
        ok = 0
        for index in range(automat3.v):
            if key in starifinale:
                ok = 1
            elif d[index][key] in starifinale:
                ok = 1
            elif key != d[index][key]:
                ck = d[index][key]
                valid = 1
                while valid == 1:
                    if d[index][ck] == ck:
                        valid = 0
                    elif d[index][ck] in starifinale:
                        ok = 1
                        valid = 0
                    else: ck = d[index][ck]
        if ok == 0:
            for index in d:
                for i in index.keys():
                    if index[i] == key:
                        index[i] = None
                del index[key]


    for elem in list(d[0].keys()):
        ok = 0
        for index in range(automat3.v):
            if elem in list(d[index].values()):
                ok = 1
        if ok == 0:
            for index in d:
                del index[elem]
    automat3.tata = d
    automat3.F = starifinale
    automat3.q = len(list(automat3.tata[0].keys()))
    automat3.f = len(automat3.F)

    print("Dupa transformarea din DFA in DFA-minimal:")
    for index in range(automat3.v):
        print("Caracterul " + automat3.V[index] + " -> " + str(automat3.tata[index]))

steff = Automat("test.txt")
lambdanfa_to_nfa(steff)
nfa_to_dfa(steff)
dfa_to_dfamin(steff)
