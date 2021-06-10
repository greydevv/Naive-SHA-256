from sha256.const.tables import ASCII
from sha256.const import H, K

def binary(n):
    if n == 0:
        return [0]
    elif n < 0:
        return binary(n*-1)
    bit_arr = []
    while n != 0:
        bit_arr.append(n % 2)
        n = n // 2
    
    return bit_arr[::-1]

def prepad(bits, to=32):
    if to == 0: return bits

    rem = len(bits) % to
    if rem > 0:
        bits = [0]*(to-rem) + bits
    
    return bits

def add(a,b):
    carry = False
    result = []
    # bits added from right to left (iterate backwards)
    for i in range(len(a)-1,-1,-1):
        x,y = a[i], b[i]
        if x and y:
            result.append(1 if carry else 0)
            carry = True
        elif x or y:
            result.append(0 if carry else 1)
        else:
            result.append(1 if carry else 0)
            carry = False

    if carry: result.append(1)

    return result[::-1]

def twos(bits):
    # 1-bit flips the bit (1-0=1, 1-1=0)
    bits = [1-bit for bit in bits]
    other = [0]*(len(bits)-1) + [1]  

    return add(bits, other)
