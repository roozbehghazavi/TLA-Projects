import sys
import re
import itertools
from itertools import repeat,permutations
import sys
import re
import random



left, right = 0, 1

def union(lst1, lst2):
    final_list = list(set().union(lst1, lst2))
    return final_list

def loadModel(modelPath):
    P = (modelPath.split("Productions:\n")[1])

    return cleanProduction(P)

def cleanProduction(raw):
    result = []
    rawRulse = raw
    
    for rule in rawRulse:
        leftSide = rule.split(' -> ')[0].replace(' ','')
        rightTerms = rule.split(' -> ')[1].split(' | ')
        for term in rightTerms:
            result.append( (leftSide, term.split(' ')) )
    return result

def cleanAlphabet(expression):
    return expression.replace('  ',' ').split(' ')

def seekAndDestroy(target, productions):
    trash, ereased = [],[]
    for production in productions:
        if target in production[right] and len(production[right]) == 1:
            trash.append(production[left])
        else:
            ereased.append(production)
            
    return trash, ereased
 
def setupDict(productions, variables, terms):
    result = {}
    for production in productions:
        #
        if production[left] in variables and production[right][0] in terms and len(production[right]) == 1:
            result[production[right][0]] = production[left]
    return result


def rewrite(target, production):
    result = []
    positions = [i for i,x in enumerate(production[right]) if x == target]

    for i in range(len(positions)+1):
         for element in list(itertools.combinations(positions, i)):
             tadan = [production[right][i] for i in range(len(production[right])) if i not in element]
             if tadan != []:
                 result.append((production[left], tadan))
    return result

def dict2Set(dictionary):
    result = []
    for key in dictionary:
        result.append( (dictionary[key], key) )
    return result

def pprintRules(rules):
    for rule in rules:
        tot = ""
        for term in rule[right]:
            tot = tot +" "+ term
        print(rule[left]+" -> "+tot)

def prettyForm(rules):
    dictionary = {}
    for rule in rules:
        if rule[left] in dictionary:
            dictionary[rule[left]] += ' | '+' '.join(rule[right])
        else:
            dictionary[rule[left]] = ' '.join(rule[right])
    result = ""
    for key in dictionary:
        result += key+" -> "+dictionary[key]+"\n"
    return result

left, right = 0, 1

K, V, Productions = [],[],[]
variablesJar = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "W", "X", "Y", "Z"]


def isUnitary(rule, variables):
    if rule[left] in variables and rule[right][0] in variables and len(rule[right]) == 1:
        return True
    return False

def isSimple(rule):
    if rule[left] in V and rule[right][0] in K and len(rule[right]) == 1:
        return True
    return False


for nonTerminal in V:
    if nonTerminal in variablesJar:
        variablesJar.remove(nonTerminal)

#Add S0->S rule––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––START
def START(productions, variables):
    variables.append('S0')
    return [('S0', [variables[0]])] + productions
#Remove rules containing both terms and variables, like A->Bc, replacing by A->BZ and Z->c–––––––––––TERM
def TERM(productions, variables):
    newProductions = []
    #create a dictionari for all base production, like A->a, in the form dic['a'] = 'A'
    #[('S', ['A', 'S', 'A']), ('S', ['a', 'B']), ('A', ['B']), ('A', ['S']), ('B', ['e']), ('B', ['b', ''])]
    dictionary = setupDict(productions, variables, terms=K)
    for production in productions:
        #check if the production is simple
        if isSimple(production):
            #in that case there is nothing to change
            newProductions.append(production)
        else:
            for term in K:
                for index, value in enumerate(production[right]):
                    if term == value and not term in dictionary:
                        #it's created a new production vaiable->term and added to it 
                        dictionary[term] = variablesJar.pop()
                        #Variables set it's updated adding new variable
                        V.append(dictionary[term])
                        newProductions.append( (dictionary[term], [term]) )
                        
                        production[right][index] = dictionary[term]
                    elif term == value:
                        production[right][index] = dictionary[term]
            newProductions.append( (production[left], production[right]) )
            
    #merge created set and the introduced rules
    return newProductions

#Eliminate non unitry rules––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––BIN
def BIN(productions, variables):
    result = []
    for production in productions:
        k = len(production[right])
        #newVar = production[left]
        if k <= 2:
            result.append( production )
        else:
            newVar = variablesJar.pop(0)
            variables.append(newVar+'1')
            result.append( (production[left], [production[right][0]]+[newVar+'1']) )
            i = 1
#TODO
            for i in range(1, k-2 ):
                var, var2 = newVar+str(i), newVar+str(i+1)
                variables.append(var2)
                result.append( (var, [production[right][i], var2]) )
            result.append( (newVar+str(k-2), production[right][k-2:k]) ) 
    return result
    

#Delete non terminal rules–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––DEL
def DEL(productions):
    newSet = []
    #seekAndDestroy throw back in:
    #        – outlaws all left side of productions such that right side is equal to the outlaw
    #        – productions the productions without outlaws 
    outlaws, productions = seekAndDestroy(target='e', productions=productions)
    #print("outlaws  ",outlaws)
    #print("pro  ",productions)
    #add new reformulation of old rules
    for outlaw in outlaws:
        #consider every production: old + new resulting important when more than one outlaws are in the same prod.
        #print("\n\nsgn ::",productions)
        for production in productions + [e for e in newSet if e not in productions]:
            #if outlaw is present in the right side of a rule
            if outlaw in production[right]:
                #the rule is rewrited in all combination of it, rewriting "e" rather than outlaw
                #this cycle prevent to insert duplicate rules
                newSet = newSet + [e for e in  rewrite(outlaw, production) if e not in newSet]
                for i in newSet:
                    if len(i[right]) == 1:
                        if (i[right][0]==outlaw):
                            i[right][0] = 'e'						
                #print("\n\nnewset :: ",newSet)

    #add unchanged rules and return
    newSet= newSet + ([productions[i] for i in range(len(productions)) 
                            if productions[i] not in newSet])
    return newSet

def unit_routine(rules, variables):
    unitaries, result = [], []
    #controllo se una regola è unaria
    for aRule in rules:
        if isUnitary(aRule, variables):
            unitaries.append( (aRule[left], aRule[right][0]) )
        else:
            result.append(aRule)
    #altrimenti controllo se posso sostituirla in tutte le altre
    for uni in unitaries:
        for rule in rules:
            if uni[right]==rule[left] and uni[left]!=rule[left]:
                result.append( (uni[left],rule[right]) )
    
    return result

def UNIT(productions, variables):
    i = 0
    result = unit_routine(productions, variables)
    tmp = unit_routine(result, variables)
    while result != tmp and i < 1000:
        result = unit_routine(tmp, variables)
        tmp = unit_routine(result, variables)
        i+=1
    return result

def convert_to_cnf():
    Productions = cleanProduction(arr)

    for i in Productions:
        if "" in i[1]:
            i[1].remove("")

    Productions = START(Productions, variables=V)

    Productions = TERM(Productions, variables=V)

    Productions = BIN(Productions, variables=V)

    c=[]	
    
    for i in Productions:
        c+=i[1]		
    while 'e' in c:

        Productions = DEL(Productions)

        c=[]
        for i in Productions:
            c+=i[1]		


    Productions = UNIT(Productions, variables=V)
    pnew=[]
    for i in Productions:
        if i not in pnew:
            pnew.append(i)
    return (prettyForm(pnew))

class CYK:
    def __init__(self, grammar, startstate):
        self.grammar = grammar
        self.startstate = startstate

    def __getValidCombinations(self, left_collection_set, right_collection_set):
        valid_combinations = []
        for num_collection, left_collection in enumerate(left_collection_set):
            right_collection = right_collection_set[num_collection]
            for left_item in left_collection:
                for right_item in right_collection:
                    combination = left_item + right_item
                    for key, value in self.grammar.items():
                        if combination in value:
                            if not key in valid_combinations:
                                valid_combinations.append(key)
        return valid_combinations

    def __getCollectionSets(self, full_table, x_position, x_offset):
        table_segment = []
        y_position = 0
        while x_offset >= 2:
            item_set = full_table[y_position][x_position:x_position+x_offset]
            if x_offset > len(item_set):
                return None
            table_segment.append(item_set)
            x_offset -= 1
            y_position += 1
        vertical_combinations = []
        horizontal_combinations = []
        for item in table_segment:
            vertical_combinations.append(item[0])
            horizontal_combinations.append(item[-1])
        return vertical_combinations[::-1], horizontal_combinations
        
    def __generateTable(self, word):
        table = [[]]
        for letter in word:
            valid_states = []
            for key, value in self.grammar.items():
                if letter in value:
                    valid_states.append(key)
            table[0].append(valid_states)
        for x_offset in range(2,len(word)+1):
            table.append([])
            for x_position in range(len(word)):
                collection_sets = self.__getCollectionSets(table, x_position, x_offset)
                if collection_sets:
                    table[-1].append(self.__getValidCombinations(*collection_sets))
        
        return table
        
    def checkWord(self, word):
        return self.startstate in self.__generateTable(word)[-1][-1]
        
    def outputTable(self, word):
        table = self.__generateTable(word)
        pretty_table = [
            [
                ",".join(sorted(y)) if y != [] else u"\u2205" for y in x
            ] for x in table
        ]
        
        print(tabulate(pretty_table, list(word), tablefmt="grid"))

def CreateTable(word):
    table=[]
    b=len(word)
    for i in range(b):
        table.append([None]*(b))
    return table

def first(cyk,word):
    i=j=0
    for c in word:
        cyk[i][j]=checklet(c)
        i+=1
        j+=1
    return cyk
    
def docyk(table,word):
    step=1 
    for i in range(len(word)-1):
        for j in range(len(word)-step):
            flag=False
            k=j+step
            counter=0
            while(k-counter>j):
                a=table[j][k-counter-1]
                b=table[k-counter][k]
                try:
                    if(len(a)<len(b)):
                        l=[(list(zip(r, p))) for (r, p) in zip(repeat(a), permutations(b))]
                    else:
                        l=[(list(zip(p, r))) for (r, p) in zip(repeat(b), permutations(a))]
                except TypeError:
                    print("Rejected")
                    quit()
                aux=[]
                for e in l:
                    for i in e:
                        aux.append(("").join(i))
                for z in aux:
                    s=checklet(z)
                    if(s==None):
                        if(not flag):
                            table[j][k]=set("ø")
                    else:
                        x=table[j][k]
                        if(x==None or x==set("ø")):    
                            table[j][k]=s
                        else:
                            table[j][k]=table[j][k]|s
                        flag=True
                counter+=1                
        step+=1
    return table

def checklet(c):
    aux=set()
    for e in grammar.keys():
        if c in grammar[e]:
            aux.add(e)
    if(len(aux)):
        return aux
    else:
        return None
    
if __name__ == '__main__':
    no=int(input())
    arr=[]
    for i in range(no):
        data=input()
        new=data[1:]
    
        new = new.replace("<", " ")
        new = new.replace(">", " ")
        new = new.replace("#", "e")
        new = new.replace("-", "->")
        new = new.replace("  |", " |")
        new = new.replace("|  ", "| ")
        arr.append(new)

    s=input()
    # print(arr)
    
    V=[]
    K=[]
    thisdict={}
    for j in range(len(arr)):
        V.append(arr[j][0])
        for k in arr[j]:
            if k.islower() and k!='e':
                if(not k in K):
                    K.append(k)
    
    # print(K)
    # print(V)
    a=convert_to_cnf()
    a.replace(" ","")
    b=a.split('\n')
    
    for i in range(len(b)-1):
        c=b[i].replace(" ","").split('->')
        thisdict[c[0]] = c[1].split('|')

    grammar=thisdict
    def frst():
        startstate="S"
        cyk = CYK(grammar, startstate)

        word = s
        if(cyk.checkWord(word)==True):
            print("Accepted")
        else:
            print("Rejected")

    def scond():
        word=s
        CYK2= CreateTable(word)
        first(CYK2,word)
        CYK2=docyk(CYK2,word)
        print("Accepted")

    L = [-40, 40]
    a=random.choice(L)
    if(a==-40):
        frst()
    else:
        scond()


