class ALU:
    @classmethod   
    def sum(cls,a,b,ignoreoverflow = True):
        carry = 0
        if (len(a) != len(b)):
            # normalize a and b to same length 
            a = [ 0 for i in range(len(b) - len(a))] + a
            b = [ 0 for i in range(len(a) - len(b))] + b
        # prepare result massive and fill it with 0's
        result = [ 0 for i in range(len(a))]
        #
        l = len(a)
        for i in range(l):
            result[len(result)-i-1] = (a[l-i-1] + b[l-i-1] + carry) % 2
            carry = (a[l-i-1] + b[l-i-1] + carry) // 2
        if(not ignoreoverflow and carry != 0):
            result = [carry] + result
        return result

    @classmethod
    def subtract(cls,minuend,subtrahend):
        if (len(minuend) != len(subtrahend)):
            # normalize a and b to same length
            minuend = [ 0 for i in range(len(subtrahend) - len(minuend))] + minuend
            subtrahend = [ 0 for i in range(len(minuend) - len(subtrahend))] + subtrahend
        result = cls.sum(minuend, cls.negatiate(subtrahend))
        return result
    # det additional code for negativ number
    @classmethod 
    def negatiate(cls,a):
        result = [0 for i in range(len(a))]
        for i in range(len(a)):
            result[i] = 1 if(a[i] == 0) else 0
        return ALU.sum(result,[1])

    #positiv n means shift left by n position
    #negativ n means shift right by |n| position
    @classmethod 
    def shift(cls,a,n):
        if(n > 0):
            a = a[n:] + [0 for i in range(min(n,len(a)))]
        if(n < 0):
            a = [0 for i in range(min(abs(n),len(a)))] + a[:n]
        return a

def register_to_int(a, signSensitive=True):
    rez = 0
    negative = False
    if(signSensitive and a[0] == 1):
        negative = True
        a = ALU.negatiate(a)
    for i in a:
        rez = rez << 1
        if(i == 1):
            rez+=1
    if(negative):
        rez = -rez
    return rez

