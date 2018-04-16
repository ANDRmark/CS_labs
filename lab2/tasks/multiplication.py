import sys, os
sys.path.append(os.path.dirname(sys.path[0]))
from MyToolslib import ALU, register_to_int

# convivient way to print binary        
def bin_str(a):
    s = ""
    for i in range(len(a)):
        s = s + str(a[i])
    return s


multiplicand = None
multiplier = None
product = None

#-------------------multiplication---------------------
#read input numbers to do multiplication
multiplicand0 = int(input("Enter multiplicand:"))
multiplier0 = int(input("Enter multiplyer:"))

#convert numbers to binary lists (like number 5 will be [1, 0, 1])
multiplicand = [ 1 if ch == '1' else 0 for ch in list("{0:b}".format(abs(multiplicand0)))]
multiplier = [ 1 if ch == '1' else 0 for ch in list("{0:b}".format(abs(multiplier0)))]

#set 32 bits for multiplyer and 64 for multiplicand and product
#in fact lists are of lengths of 32 and 64
basicRegLen = 32
multiplicand = multiplicand[-basicRegLen*2:] if len(multiplicand) > basicRegLen*2 else [ 0 for i in  range(basicRegLen*2 - len(multiplicand))] + multiplicand
multiplier = multiplier[-basicRegLen:] if len(multiplier) > basicRegLen else [ 0 for i in  range(basicRegLen - len(multiplier))] + multiplier
product = [ 0 for i in range(basicRegLen*2)]


#start process and output
#display entered data
print("information about each iteration shows state after executing all actions in that iteration")
print("sign of result is considered at the end, operations done over positive numbers")
print("initial state:")
print("Multiplier:   ",end="")
print(bin_str(multiplier))
print("Multiplicand: ",end="")
print(bin_str(multiplicand))
print("Product     : ",end="")
print(bin_str(product))

#starting main loop where will be n iterations done 
for i in range(basicRegLen):
    print("iteration " + str(i+1) +": ")
    if(multiplier[len(multiplier)-1] == 1):
        product = ALU.sum(product, multiplicand)
        print("last bit of multiplier is 1 so add multiplicand to product; ")
    multiplicand = ALU.shift(multiplicand,1)
    print("shift multiplicand left by 1; ")
    multiplier = ALU.shift(multiplier,-1)
    print("shift multiplier right by 1; ")
    print("Multiplier:   ",end="")
    print(bin_str(multiplier))
    print("Multiplicand: ",end="")
    print(bin_str(multiplicand))
    print("Product     : ",end="")
    print(bin_str(product))


#restore sign of product
if((multiplicand0 < 0 and multiplier0 > 0) or (multiplicand0 > 0 and multiplier0 < 0)):
    product = ALU.negatiate(product)

#Output
print("Result:")
print("Product with sign     : ",end="")
print(bin_str(product))
answer = register_to_int(product)
print("Answer: " + str(register_to_int(product)))
if (answer != multiplicand0 * multiplier0):
    print("WRONG ANSWER DETECTED!!!")
    print("Expected answer : "+ str(multiplicand0 * multiplier0))
else:
    print("Answer verified")

