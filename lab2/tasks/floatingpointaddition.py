import sys, os
sys.path.append(os.path.dirname(sys.path[0]))
from MyToolslib import ALU, register_to_int

#to check our algorithm we should use true ieee754 SINGLE precision
#python by default use float64, we need float32, so we need this import
import numpy as np


import struct
#return binary representation of float number as string
def get_float_binary_str(num):
    return ''.join([bin(c).replace('0b', '').rjust(8, '0') for c in struct.pack('!f', num)])

# convivient way to print binary        
def bin_str(a):
    s = ""
    for i in range(len(a)):
        s = s + str(a[i])
    return s

#IEEE 754 single precision floating point numbers (32 bits)
#we are going to sum a and b
a = None
b = None
sumresult = None

print("We are going to sum a and b in floating point 32 bit")
a0 = float(input("Enter a: "))
b0 = float(input("Enter b: "))

#convert numbers to lists of length 32
a = [ 1 if(c == '1') else 0 for c in list(get_float_binary_str(a0))]
b = [ 1 if(c == '1') else 0 for c in list(get_float_binary_str(b0))]
sumresult = [0 for i in range(32)]

print("binary a: "+bin_str(a)[0]+ " "+bin_str(a)[1:9] + " " + bin_str(a)[9:32])
print("binary b: "+bin_str(b)[0]+ " "+bin_str(b)[1:9] + " " + bin_str(b)[9:32])

#find difference in exponents in int representation
exp_diff = register_to_int(ALU.subtract([0]+a[1:9],[0]+b[1:9]))
print("difference in exponents in int representation: "+str(exp_diff)+" (base 10) ")

#number with bigger exponent is "a"
if(exp_diff < 0):
    tmp = a
    a = b
    b = tmp
    exp_diff = -exp_diff

#set initially sign and exponent of result same as in "a"
sumresult[0] = a[0]
sumresult[1:9] = a[1:9]

#add two "zeroes" and "one" at the beginning so we can easily add or substract mantissas 
# (one "zero" for sign, one "zero" for overflow situation, "one" for implicit 1 befor decimal point)
# add three zeroes at the end to do rounds later
a_mantissa = [0,0,1] + a[9:32] + [0,0,0]
b_mantissa = [0,0,1] + b[9:32] + [0,0,0]

#if "a" or "b" was absolute zero then we shouldnt add implicit 1
if(a[1:9] == [0,0,0,0,0,0,0,0]):
    a_mantissa[2] = 0
if(b[1:9] == [0,0,0,0,0,0,0,0]):
    b_mantissa[2] = 0

# shift number with lower exponent to align mantisas
b_mantissa = ALU.shift(b_mantissa,-exp_diff)

print("shift mantissa of lower number so that with same exponent decimal point will be in same position")
print("mantissa a       : "+ str(a_mantissa[2])+"."+bin_str(a_mantissa[3:26]))
print("mantissa b       : "+ str(b_mantissa[2])+"."+bin_str(b_mantissa[3:26]))
print("perform addition")

if(a[0] != b[0]):
    #signs are different
    sum_result_mantissa = ALU.subtract(a_mantissa,b_mantissa)
else:
    #signs are same
    sum_result_mantissa = ALU.sum(a_mantissa,b_mantissa)


print("mantissa result: "+("1" if sum_result_mantissa[1] == 1 else "")+str(sum_result_mantissa[2])+"."+bin_str(sum_result_mantissa[3:26]))

#case when exponents were same but "a" turned up less then "b"
#result of subtraction mantissas is negative so we need to switch the sign of result
if(sum_result_mantissa[0] == 1):
    sum_result_mantissa = ALU.negatiate(sum_result_mantissa)
    sumresult[0] = (sumresult[0] + 1) % 2

# round result 
#if(sumresult[0] == 0):
for i in range(5):
    if sum_result_mantissa[i] == 1:
        if sum_result_mantissa[i+24] == 1:
            sum_result_mantissa = ALU.sum(sum_result_mantissa,[1]+[0 for j in range(4-i)])
        break


#adjusting mantissa and exponent
#find adjusting shift value which determines how we should change exponent
exp_adjusting_val0 = 2
for bit in sum_result_mantissa:
    if(bit != 1):
        exp_adjusting_val0 -= 1
    else:
        break


sum_result_exp = [0,0] + sumresult[1:9]
exp_adjusting_val = [ 1 if ch == '1' else 0 for ch in list("{0:b}".format(abs(exp_adjusting_val0)))]
if(exp_adjusting_val0 > 0):
    sum_result_exp = ALU.sum(sum_result_exp, exp_adjusting_val)
if(exp_adjusting_val0 < 0):
    sum_result_exp = ALU.subtract(sum_result_exp, exp_adjusting_val)

#exponent becomes negative means absolute zero (or mantissa contains all zeroes when for example we sentract same float numbers)
if(sum_result_exp[0] == 1 or exp_adjusting_val0 == -24):
    sum_result_exp = [0,0,0,0,0,0,0,0,0]  #exponent for absolute zero

#exponent becomes greater then maximum possible value means infinity
if(sum_result_exp[1] == 1):
    sum_result_exp = [1,1,1,1,1,1,1,1,1]  #exponent for infinity

print("add to exponent (" + str(exp_adjusting_val0)+") to adjust it")
print("adjusted exponent:" + bin_str(sum_result_exp[-8:]))

#prepare mantissa of result
sum_result_mantissa = sum_result_mantissa[3-exp_adjusting_val0:][:23]
sum_result_mantissa = sum_result_mantissa + [0 for i in range(23 - len(sum_result_mantissa))]


print("perform mantissa normalization")
print("mantissa result:   1."+bin_str(sum_result_mantissa))

#set resulting exponent and mantisa
sumresult[1:9] = sum_result_exp[-8:]
sumresult[9:32] = sum_result_mantissa

#output result
print("result: "+bin_str(sumresult)[0]+" "+bin_str(sumresult)[1:9]+" "+bin_str(sumresult)[9:32])

if(bin_str(sumresult) == get_float_binary_str(np.float32(a0)+np.float32(b0))):
    print("result :" + str(np.float32(a0)+np.float32(b0)))
    print("Answer verified")
else:
    print("WRONG ANSWER DETECTED!!!")
    print("Expected:")
    resstr = get_float_binary_str(np.float32(a0)+np.float32(b0))
    print("result: "+resstr[0]+" "+resstr[1:9]+" "+resstr[9:32])
    print("expected result :" + str(np.float32(a0)+np.float32(b0)))













