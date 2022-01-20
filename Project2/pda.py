from math import log, log10, exp, e, pow, sqrt,sin,cos

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
        return self.top is None  # If there is no top node, then that means there are nothing in the stack.

    def __len__(self):
        return self.length

    def peek(self):
        return self.top.value

    def push(self, value):
        newNode = Node(value)  # Create a new node
        newNode.next = self.top  # Make the new node point to what is currently the top.
        self.top = newNode  # Make the new node the top of the stack.
        self.length += 1  # Increase stack length by 1.

    def pop(self):
        if self.length == 0:  # We can't pop any value if the stack is empty!
            return "Stack is empty"
        temp = self.top.value  # Temporarily store what is currently the top of the stack so we can return it.
        self.top = self.top.next  # Make the next value in the stack the new top value.
        self.length -= 1  # Decrease stack length by 1.
        return temp


def findNextOpr(txt):
    if len(txt) <= 0 or not isinstance(txt, str):
        return "type error: findNextOpr"

    for character in txt:
        if ord(character) == 42 or ord(character) == 43 or ord(character) == 45 or ord(character) == 47 or ord(
                character) == 94:
            return txt.index(character)
    return -1


def isNumber(txt):
    if not isinstance(txt, str):
        return "type error: isNumber"
    if len(txt) == 0:
        return False

    txt = txt.strip()  # This takes off the whitespaces at the beginning and end of the string.
    try:
        temp = float(txt)  # If the program is able to do this, it means whatever is left in the string is convertible to float.
        return True  # Therefore, it must be a number.
    except TypeError:
        return False


def getNextNumber(expr, pos):
    if len(expr) == 0 or not isinstance(expr, str) or pos < 0 or pos >= len(expr) or not isinstance(pos, int):
        return None, None, "type error: getNextNumber"
    expr = expr[
           pos:]  # Since we will be starting from position pos, we won't need to look any earlier in the string, so just remove the beginning.
    whitespace = 0
    while expr[whitespace] == " ":
        whitespace += 1
    expr = expr.strip()
    nextNumber = None
    nextOprPos = findNextOpr(expr)
    if nextOprPos == -1:  # This occurs when there are no more operators left after position pos.
        nextOpr = None
        nextOprPos = None  # They want getNextNumber to return None instead of -1.
    else:
        nextOpr = expr[nextOprPos]
        if nextOprPos == 0 and nextOpr == "-":  # This if statement allows for multiplication of negative numbers.
            number, nextOpr, nextOprPos = getNextNumber(expr,
                                                        1)  # Recursive call to obtain the next number, sign, and sign position after the negative sign.
            nextNumber = float(number) * -1
            if nextOpr is None:
                return nextNumber, nextOpr, nextOprPos
            return nextNumber, nextOpr, nextOprPos + whitespace + pos
        elif isNumber(
                expr[0:nextOprPos]):  # Checks to see if the portion of the string before the operator is a number.
            expr = expr[0:nextOprPos]
            expr = expr.strip()  # Remove whitespaces.
            nextNumber = float(
                expr)  # Now that all spaces are removed, we can successfully convert the remaining string into a float number.
    if nextOprPos is None:  # Even if we ran out of operators, there may still be a number at the end of a string.
        if isNumber(expr[
                    0:]):  # We test if the expression from the starting position pos until the end of the string is a number.
            expr = expr[0:]
            expr = expr.strip()  # Remove whitespaces.
            nextNumber = float(expr)  # If it's a number, then set that end of the string to nextNumber.
    if nextOprPos is None:  # So because I modified expr to equal expr[pos:] I have to factor in pos to the return the correct value of nextOprPos.
        return nextNumber, nextOpr, nextOprPos  # Because you can't add anything to Type None, I just needed another return statement.
    return nextNumber, nextOpr, nextOprPos + pos + whitespace  # Returns everything. nextOprPos has to factor in the starting position in the string.


def exeOpr(num1, opr, num2):
    # This function is just a utility function. It is skipping type check
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
    if len(expr) <= 0 or not isinstance(expr, str):  # Line A
        return "input error line A: calculator"

    # Concatenate '0' at he beginning of the expression if it starts with a negative number to get '-' when calling getNextNumber
    # "-2.0 + 3 * 4.0 ” becomes "0-2.0 + 3 * 4.0 ”.
    expr = expr.strip()
    if expr[0] == "-":
        expr = "0 " + expr
    newNumber, newOpr, oprPos = getNextNumber(expr, 0)

    # Initialization. Holding two modes for operator precedence: "addition" and "multiplication"
    if newNumber is None:  # Line B
        return "input error line B: calculator"
    elif newOpr is None:
        return newNumber
    elif newOpr == "+" or newOpr == "-":
        mode = "add"
        addResult = newNumber  # value so far in the addition mode
        mulResult = 0
        expResult = 0
    elif newOpr == "*" or newOpr == "/":
        mode = "mul"
        addResult = 0
        mulResult = newNumber  # value so far in the multiplication mode
        expResult = 0
        addLastOpr = "+"
    elif newOpr == "^":
        mode = "exp"
        addResult = 0
        mulResult = 0
        expResult = newNumber  # value so far in the exponent mode
        addLastOpr = "+"
    pos = oprPos + 1  # the new current position
    curOpr = newOpr  # the new current operator

    # Calculation starts here, get next number-operator and perform case analysis. Compute values using exeOpr
    while True:
        # --- YOU CODE STARTS HERE
        newNumber, newOpr, oprPos = getNextNumber(expr, pos)
        if newNumber is None and newOpr is not None:  # This means we found an expression before a new number (Two operations next to each other).
            return 'error'
        if mode == 'exp':  # If we are dealing with exponents, we know this is the first priority in order of operations and we can just do the operation.
            expResult = exeOpr(expResult, curOpr, newNumber)  # Perform the exponent operation immediately.
            if mulResult != 0:  # If mulResult is not 0, then we know we can perform the operation between mulResult and expResult.
                mulResult = exeOpr(mulResult, mulLastOpr, expResult)
            if newOpr == "*" or newOpr == "/":  # Checks for the new operator and switch modes.
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
        elif mode == 'mul':  # For multiplication, we have to check that the next expression in the string is not exponentiation before we can perform multiplication/division.
            if newOpr == '^':
                mode = 'exp'
                mulLastOpr = curOpr
                expResult = newNumber
            elif newOpr == "+" or newOpr == "-":  # If the next operator we find is addition or subtraction:
                mode = "add"  # Switch mode to addition.
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
    # Required: calculator must create and use a Stack (or Queue) for parenthesis matching
    # Call _calculator to compute the inside parentheses
    if not isinstance(expr, str) or len(expr) <= 0:
        return "input error in calculator"
    expr = expr.strip()
    s = Stack()

    # Scan the expression to find the most inner expression, note that if pos==-1 you can try to compute the expression as is
    posLeft = expr.find("(")
    posRight = expr.find(")")
    while True:
        # --- function code starts here -----#
        if posLeft == -1:  # If there aren't any parentheses, just compute the expression normally.
            if expr.find(")") != -1:
                return 'error'
            return _calculator(expr)

        s.push(posLeft)
        if expr[posLeft + 1:].find("(") != -1 and expr[posLeft + 1:].find("(") + posLeft + 1 < posRight:
            posLeft = expr[posLeft + 1:].find("(") + posLeft + 1
        else:  # If we reach this else statement, then it means we found the end of the innermost parenthesis.
            while s.length > 0:
                parResult = _calculator(
                    expr[s.top.value + 1:posRight])  # This gives us the result from the current set of parentheses.
                expr = expr[:s.top.value] + str(parResult) + expr[posRight + 1:]
                posRight = expr.find(")")
                s.pop()
            posLeft = expr.find("(")


try:
    inp=str(input()).replace("^","**")
    inp.replace("ln","log")
    result = eval(inp)
    print(f"{result:.2f}")
except:
    print("INVALID")


