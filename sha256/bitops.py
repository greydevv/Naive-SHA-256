from sha256.const.tables import ASCII
from sha256.const import H, K
from functools import reduce

def binary(n):
    if n == 0:
        return [0]
    elif n < 0:
        return binary(abs(n))
    bit_arr = []
    while n != 0:
        bit_arr.append(n % 2)
        n = n // 2
    
    return bit_arr[::-1]

def prepad(bits):
    rem = len(bits) % 32
    if rem > 0:
        bits = [0]*(32-rem) + bits
    
    return bits

def add(a,b):
    # bits added from left to right, start at rightmost index
    i = len(a)-1
    carry = False
    result = []
    while i >= 0:
        x,y = a[i], b[i]
        if x and y:
            result.append(1 if carry else 0)
            carry = True
        elif x or y:
            result.append(0 if carry else 1)
        else:
            result.append(1 if carry else 0)
            carry = False

        i -= 1

    return result[::-1]

def twos(bits):
    # flip bits
    bits = [1-bit for bit in bits]
    other = [0]*(len(bits)-1) + [1]  
    # add bits to 1
    return add(bits, other)
