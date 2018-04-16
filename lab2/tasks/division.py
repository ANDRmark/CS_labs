import sys, os
sys.path.append(os.path.dirname(sys.path[0]))
from MyToolslib import ALU, register_to_int

# convivient way to print binary        
def bin_str(a):
    s = ""
    for i in range(len(a)):
        s = s + str(a[i])
    return s


remainder = None
divisor = None
quotient = None

#-------------------division---------------------
#read input numbers to do multiplication
divident0 = int(input("Enter divident:"))
divisor0 = int(input("Enter divisor:"))

#convert numbers to binary lists (like number 5 will be [1, 0, 1])
#this algorithm of division imply to initially write dividend in remainder register
remainder = [ 1 if ch == '1' else 0 for ch in list("{0:b}".format(abs(divident0)))]
divisor = [ 1 if ch == '1' else 0 for ch in list("{0:b}".format(abs(divisor0)))]

#set 32 bits for quotient and 64 for divisor and remainder
#in fact lists are of lengths of 32 and 64
basicRegLen = 32
remainder = remainder[-basicRegLen*2:] if len(remainder) > basicRegLen*2 else [ 0 for i in  range(basicRegLen*2 - len(remainder))] + remainder
divisor = (divisor[-basicRegLen:] if len(divisor) > basicRegLen else [ 0 for i in  range(basicRegLen - len(divisor))] + divisor) + ([ 0 for i in range(basicRegLen)])
quotient = [ 0 for i in range(basicRegLen)]

#start process and output
#display entered data
print("information about each iteration shows state after executing all actions in that iteration")
print("sign of result is considered at the end, operations done over positive numbers")
print("initial state:")
print("Divisor:   ",end="")
print(bin_str(divisor))
print("Remainder: ",end="")
print(bin_str(remainder))
print("Quotient:  ",end="")
print(bin_str(quotient))

#starting main loop where will be n iterations done 
for i in range(basicRegLen):
     print("iteration " + str(i+1) +": ")
     divisor = ALU.shift(divisor, -1)
     print("shift divisor right by 1; ")
     quotient = ALU.shift(quotient,1)
     print("shift quotient left by 1; ")
     remainder = ALU.subtract(remainder,divisor)
     print("subtract divisor from remainder; ")
     if(remainder[0] == 1):
         remainder = ALU.sum(remainder,divisor)
         print("remainder becomes negative, so add divisor to remainder back; ")
     else:
        quotient[len(quotient) -1] = 1
        print("remainder not negative, so set last quotient bit to 1; ")
     print("Divisor:   ",end="")
     print(bin_str(divisor))
     print("Remainder: ",end="")
     print(bin_str(remainder))
     print("Quotient:  ",end="")
     print(bin_str(quotient))


#restore signs of numbers
if((divisor0 < 0 and divident0 > 0) or (divisor0 > 0 and divident0 < 0)):
    quotient =  ALU.negatiate(ALU.sum(quotient,[1]))
    remainder = ALU.subtract(divisor, remainder)
if(divisor0 < 0 ):
    remainder = ALU.negatiate(remainder)

#Output results
print("Result:")
answerquotient = register_to_int(quotient)
answerremainder = register_to_int(remainder)


print("Quotient with sign    : ",end="")
print(bin_str(quotient))
print("Reminder with sign    : ",end="")
print(bin_str(remainder))
print("Answer:  quotient = " + str(answerquotient) +";  remainder = ", str(answerremainder))
if(answerquotient != divident0 // divisor0 or answerremainder != divident0 % divisor0):
    print("WRONG ANSWER DETECTED!!!")
    print("Expected quotient: "+str(divident0 // divisor0))
    print("Expected remainder: "+str(divident0 % divisor0))
else:
    print("Answer verified")



