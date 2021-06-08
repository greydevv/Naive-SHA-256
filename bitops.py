from functools import reduce
from _ascii import ASCII, HEX
from const import H, K

class BitArray:
    def __init__(self, bits):
        self.bits = bits

    @classmethod
    def fromint(cls, n):
        bits = binary(n)
        bits = prepad(bits)
        return cls(bits)

    @classmethod
    def fromstr(cls, string):
        bits = []
        for char in string:
            char_bits = binary(ASCII[char])
            bits.extend(prepad(char_bits))
        return cls(bits)

    def toint(self):
        # create backwards range for powers
        pows = range(len(self)-1,-1,-1)
        n = 0
        for bit,_pow in zip(self, pows):
            n += bit*(2**_pow)
        return n

    def tohex(self):
        chunks = [self[i:i+4] for i in range(0, len(self), 4)]
        result = ""
        for chunk in chunks:
            hex_value = HEX[chunk.toint()]
            result += hex_value

        return result

    def pad(self):
        bit_len = binary(len(self))
        padding = [1] + [0]*(447-len(self)) + [0]*(64-len(bit_len)) + bit_len
        result = self.bits + padding
        return self.__class__(result)
    
    def rshift(self, n):
        # chop last n bits, prepend n '0's
        result = [0]*n + self.bits[:-n]
        return self.__class__(result)
    
    def rotr(self, n):
        n = n % len(self)
        # chop last n bits, prepend them
        result = self.bits[-n:] + self.bits[:-n]
        return self.__class__(result)

    def __xor__(self, other):
        # assume that other is BitArray and has same length
        result = []
        for a,b in zip(self, other):
            result.append((a + b) % 2)

        return self.__class__(result)

    def __add__(self, other):
        # assume that other is BitArray and has same length
        i = len(self)-1
        result = []
        carry = False
        while i >= 0:
            a,b = self[i], other[i]
            if a and b:
                result.append(1 if carry else 0)
                carry = True
            elif a or b:
                result.append(0 if carry else 1)
            else:
                result.append(1 if carry else 0)
                carry = False
            i -= 1
        return self.__class__(result[::-1]) 

    def __getitem__(self, i):
        if isinstance(i, int):
            return self.bits[i]
        elif isinstance(i, slice):
            return self.__class__(self.bits[i])

    def __iter__(self):
        return iter(self.bits)

    def __len__(self):
        return len(self.bits)

    def __str__(self):
        return "".join([str(bit) for bit in self.bits])
    
    def __repr__(self):
        cls_name = self.__class__.__name__
        bit_repr = " ".join([str(bit) for bit in self.bits])
        return f"{cls_name}[{bit_repr}]"


def prepad(bits):
    rem = len(bits) % 8
    if rem > 0:
        bits = [0]*(8-rem) + bits
    
    return bits

def twos(bits):
    # flip bits
    bits = [1-bit for bit in bits]
    # twos complement

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

def xor(*bit_arrs):
    # assume that there are > 2 arguments passed
    result = reduce(BitArray.__xor__, bit_arrs)
    return result

def choice(a, b, c):
    result = []
    for model, y, z in zip(a, b, c):
        result.append(y if model else z)
    return BitArray(result)

def majority(*bit_arrs):
    result = []
    for bits in zip(*bit_arrs):
        result.append(max(bits, key=bits.count))
    return BitArray(result)

def lsig_0(bit_arr):
    x = bit_arr.rotr(7)
    y = bit_arr.rotr(18)
    z = bit_arr.rshift(3)
    return BitArray(xor(x,y,z))

def lsig_1(bit_arr):
    x = bit_arr.rotr(17)
    y = bit_arr.rotr(19)
    z = bit_arr.rshift(10)
    return BitArray(xor(x,y,z))

def usig_0(bit_arr):
    x = bit_arr.rotr(2)
    y = bit_arr.rotr(13)
    z = bit_arr.rotr(22)
    return BitArray(xor(x,y,z))

def usig_1(bit_arr):
    x = bit_arr.rotr(6)
    y = bit_arr.rotr(11)
    z = bit_arr.rotr(25)
    return BitArray(xor(x,y,z))

def compress(words):
    orig_state = tuple(BitArray.fromint(h) for h in H)
    a,b,c,d,e,f,g,h = orig_state
    import os
    for w,k in zip(words, K):
        k = BitArray.fromint(k)
        t0 = usig_1(e) + choice(e,f,g) + h + k + w
        t1 = usig_0(a) + majority(a,b,c)
        
        b,c,d,e,f,g,h = a,b,c,d,e,f,g
        a = t0 + t1
        e = e + t0

    hash_values = [s0+s1 for s0,s1 in zip(orig_state, (a,b,c,d,e,f,g,h))]
    return hash_values

        









