
#int counterFunctionCalls

	
def max3(x,y,z):
#{
    #int m
    global counterFunctionCalls
    counterFunctionCalls = counterFunctionCalls + 1
    if x>y:
        m = x
    elif y>x:
        m = y
    else:
        m = z
    return m
#}


def fib(x):
#{
    global counterFunctionCalls
    counterFunctionCalls = counterFunctionCalls + 1
    if x<0:
        return -1
    elif x==0 or x==1:
        return 1
    else:
        return fib(x-1)+fib(x-2)
#}
     
     
def isPrime(x):
#{
    ## declarations for isPrime ##
    #int i

    def divides(x,y):
    #{
        ## body of divides ##
        global counterFunctionCalls
        counterFunctionCalls = counterFunctionCalls + 1
        if y == (y//x)*x:
            return 1
        else:
            return 0
    #}

    ## body of isPrime ##
    global counterFunctionCalls
    counterFunctionCalls = counterFunctionCalls + 1
    i = 2
    while i < x:
    #{
        if divides(i,x) == 1:
            return 0
        i = i + 1
    #}
    return 1
#}

     
def quad(x):
#{
    #int y
    
    ## nested function sqr ##
    def sqr(x):
    #{
        ## body of sqr ##
        global counterFunctionCalls
        counterFunctionCalls = counterFunctionCalls + 1
        return x*x
    #}
    
    ## body of quad ##
    global counterFunctionCalls
    counterFunctionCalls = counterFunctionCalls + 1
    y = sqr(x)*sqr(x)
    return y
#}


def leap(year):
## returns 1 if year is a leap year, otherwise it returns 0 ##
#{
    global counterFunctionCalls
    counterFunctionCalls = counterFunctionCalls + 1
    if year%4==0:
        return 1
    else:
        return 0 
#}        


        
#def main
#int i
#int a
#int b
#int f
#int q


    if i < x and i == 0 or a == 1:
    #{
        a = 3
        print(x)
        a = int(input())
    #}
    elif a == 0:
    	a = 1
    else:
    	a = 3

i = 6
