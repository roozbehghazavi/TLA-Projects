from math import log, log10, exp, e, pow, sqrt,sin,cos,tan,asin,acos,atan,sinh,cosh,tanh

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __str__(self):
        return "Node({})".format(self.value)

    __repr__ = __str__

class Stack:
    def __init__(self):
        self.top = None
        self.length = 0

    def __str__(self):
        temp = self.top
        out = []
        while temp:
            out.append(str(temp.value))
            temp = temp.next
        out = '\n'.join(out)
        return 'Top:{}\nStack:\n{}'.format(self.top, out)

    __repr__ = __str__

    def isEmpty(self):
        return self.top is None  # agar top node khali bood stack khali ast

    def __len__(self):
        return self.length

    def peek(self):
        return self.top.value

    def push(self, value):
        newNode = Node(value)  # sakht node jadid
        newNode.next = self.top  # newnode barabare bala tarin element stack mishavad
        self.top = newNode  
        self.length += 1  # toole stack 1 adad ezafe mishavad

    def pop(self):
        if self.length == 0:  # stack khali bashad emkan pop vojod nadarad
            return "Stack is empty"
        temp = self.top.value  # zakhire kardane element top e stack
        self.top = self.top.next  # element badi ra top mikonim
        self.length -= 1  # toole stack 1 adad kam mikonim
        return temp


def findNextOpr(txt):
    if len(txt) <= 0 or not isinstance(txt, str):
        return 

    for character in txt:
        if ord(character) == 42 or ord(character) == 43 or ord(character) == 45 or ord(character) == 47 or ord(
                character) == 94:
            return txt.index(character)
    return -1


def isNumber(txt):
    if not isinstance(txt, str):
        return 
    if len(txt) == 0:
        return False

    txt = txt.strip()  #az beyn bordane whitespace ha
    try:
        temp = float(txt)  # agar daroone txt faghat adad bashad anjam mishavad
        return True  
    except TypeError:
        return False #adad nist


def getNextNumber(expr, pos):
    if len(expr) == 0 or not isinstance(expr, str) or pos < 0 or pos >= len(expr) or not isinstance(pos, int):
        return None, None, "type error: getNextNumber"
    expr = expr[
           pos:]  # chon az pos shoro mikonim aval expr ra pak mikonim
    whitespace = 0
    while expr[whitespace] == " ":
        whitespace += 1
    expr = expr.strip()
    nextNumber = None
    nextOprPos = findNextOpr(expr)
    if nextOprPos == -1:  # bad az pos operator vojod nadashte bashad
        nextOpr = None
        nextOprPos = None  
    else:
        nextOpr = expr[nextOprPos]
        if nextOprPos == 0 and nextOpr == "-":  # zarbe adade manfi
            number, nextOpr, nextOprPos = getNextNumber(expr,
                                                        1)  # yaftane adade badi
            nextNumber = float(number) * -1
            if nextOpr is None:
                return nextNumber, nextOpr, nextOprPos
            return nextNumber, nextOpr, nextOprPos + whitespace + pos
        elif isNumber(
                expr[0:nextOprPos]):  # postition ghable operator adad ast ya kheir
            expr = expr[0:nextOprPos]
            expr = expr.strip()  

    if nextOprPos is None: 
        if isNumber(expr[
                    0:]):  
            expr = expr[0:]
            expr = expr.strip()  
            nextNumber = float(expr)  
    if nextOprPos is None:  
        return nextNumber, nextOpr, nextOprPos  
    return nextNumber, nextOpr, nextOprPos + pos + whitespace  


def exeOpr(num1, opr, num2):
    if opr == "+":
        return num1 + num2
    elif opr == "-":
        return num1 - num2
    elif opr == "*":
        return num1 * num2
    elif opr == "/":
        if num2 == 0:
            print("Zero division error")
            return "error"
        else:
            return num1 / num2
    elif opr == "^":
        return num1 ** num2
    else:
        print("error in exeOpr")
        return "error"


def _calculator(expr):
    if len(expr) <= 0 or not isinstance(expr, str):  
        return "input error line A: calculator"

    # Concatenate '0' at he beginning of the expression if it starts with a negative number to get '-' when calling getNextNumber
    # "-2.0 + 3 * 4.0 ” becomes "0-2.0 + 3 * 4.0 ”.
    expr = expr.strip()
    if expr[0] == "-":
        expr = "0 " + expr
    newNumber, newOpr, oprPos = getNextNumber(expr, 0)


    if newNumber is None:  # Line B
        return "input error line B: calculator"
    elif newOpr is None:
        return newNumber
    elif newOpr == "+" or newOpr == "-":
        mode = "add"
        addResult = newNumber  
        mulResult = 0
        expResult = 0
    elif newOpr == "*" or newOpr == "/":
        mode = "mul"
        addResult = 0
        mulResult = newNumber  
        expResult = 0
        addLastOpr = "+"
    elif newOpr == "^":
        mode = "exp"
        addResult = 0
        mulResult = 0
        expResult = newNumber  
        addLastOpr = "+"
    pos = oprPos + 1  
    curOpr = newOpr  

   
    while True:
        newNumber, newOpr, oprPos = getNextNumber(expr, pos)
        if newNumber is None and newOpr is not None:  
            return 'error'
        if mode == 'exp':  #
            expResult = exeOpr(expResult, curOpr, newNumber)  
            if mulResult != 0: 
                mulResult = exeOpr(mulResult, mulLastOpr, expResult)
            if newOpr == "*" or newOpr == "/":  
                if mulResult == 0:
                    mulResult = expResult
                mode = 'mul'
            elif newOpr == "+" or newOpr == "-":
                if addResult == 0:
                    addResult = expResult
                mode = 'add'
            elif newOpr is None:
                if addResult != 0 and mulResult != 0:
                    addResult = exeOpr(addResult, addLastOpr, mulResult)
                    return addResult
                elif addResult != 0 and mulResult == 0:
                    addResult = exeOpr(addResult, addLastOpr, expResult)
                    return addResult
                elif addResult == 0 and mulResult != 0:
                    return mulResult
        elif mode == 'mul': 
            if newOpr == '^':
                mode = 'exp'
                mulLastOpr = curOpr
                expResult = newNumber
            elif newOpr == "+" or newOpr == "-":  
                mode = "add" 
                mulResult = exeOpr(mulResult, curOpr, newNumber)
                addResult = exeOpr(addResult, addLastOpr, mulResult)  # Performs the previous addition operation.
                mulResult = 0  # We're going to eventually be adding everything up, so reset mulResult and keep totals stored in addResult.
            elif newOpr == '*' or newOpr == '/':  # If we have no operators left, we've reached the end of the string and our total is addResult.
                mulResult = exeOpr(mulResult, curOpr, newNumber)
                if newOpr is None:
                    if mulResult != 0:
                        mulResult = exeOpr(mulResult, curOpr, newNumber)
                        addResult = exeOpr(addResult, addLastOpr, mulResult)
                    return addResult
            elif newOpr is None:
                mulResult = exeOpr(mulResult, curOpr, newNumber)
                if addResult == 0 and addLastOpr == '-':
                    return mulResult * -1
                if addResult != 0:
                    addResult = exeOpr(addResult, addLastOpr, mulResult)
                    return addResult
                return mulResult
        elif mode == 'add':  # If we are either adding or subtracting, we need to find a way to tell if we can perform the operation yet.
            if newOpr == '*' or newOpr == '/':  # If we are in adding mode, but the next operator is multiplication, we know that we have to switch to multiplication mode.
                mode = 'mul'
                addLastOpr = curOpr  # We need to keep track of what addition or subtraction operation we will need to perform in the future, so store the plus or minus sign within addLastOpr.
                mulResult = newNumber  # Keep track of the current number that we will be multiplying with.
            elif newOpr == "^":
                mode = 'exp'
                addLastOpr = curOpr
                expResult = newNumber
            elif newOpr == '+' or newOpr == '-':  # If we have addition right before addition again, that means we can perform the operation.
                addResult = exeOpr(addResult, curOpr, newNumber)
            elif newOpr is None:  # If we ran out of operators, we've reached the end of the string and gotten our total.
                if expResult != 0:
                    addResult = exeOpr(expResult, curOpr, newNumber)
                else:
                    addResult = exeOpr(addResult, curOpr, newNumber)
                return addResult
        pos = oprPos + 1  # Update the position as it goes through the expression linearly.
        curOpr = newOpr  # Update the current operator.


def calculator(expr):
    expr = expr.strip()
    return
    s = Stack()
    posLeft = expr.find("(")
    posRight = expr.find(")")
    while True:
        if posLeft == -1: 
            if expr.find(")") != -1:
                return 'error'
            return _calculator(expr)

        s.push(posLeft)
        if expr[posLeft + 1:].find("(") != -1 and expr[posLeft + 1:].find("(") + posLeft + 1 < posRight:
            posLeft = expr[posLeft + 1:].find("(") + posLeft + 1

            while s.length > 0:
                parResult = _calculator(
                    expr[s.top.value + 1:posRight])  
                expr = expr[:s.top.value] + str(parResult) + expr[posRight + 1:]
                posRight = expr.find(")")
                s.pop()
            posLeft = expr.find("(")

def sgn(x):
    return x/abs(x)


try:
    inp=str(input())
    inp2=inp.replace("^","**")
    inp3=inp2.replace("ln","log")
    calculator(inp3)
    # isNumber(inp3)
    # findNextOpr(inp3)
    if(not "//" in inp3):
        result = eval(inp3)
        print(f"{result:.2f}")
    else:
        print("INVALID")


except:
    print("INVALID")

