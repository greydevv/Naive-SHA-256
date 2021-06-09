from sha256.core.bitops import binary, prepad, twos
from sha256.const.tables import HEX
from functools import reduce

def xor(*bit_arrs):
    result = reduce(UBitArray32.__xor__, bit_arrs)
    return result

def choice(a, b, c):
    result = []
    for model, y, z in zip(a, b, c):
        result.append(y if model else z)
    return UBitArray32(result)

def majority(*bit_arrs):
    result = []
    for bits in zip(*bit_arrs):
        result.append(max(bits, key=bits.count))
    return UBitArray32(result)

class UBitArray32:
    def __init__(self, bits):
        if not bits:
            raise ValueError(f"cannot create empty {self.__class__.__name__}")
        elif len(bits) > 32 and 1 in bits[0:-32]:
            raise ValueError(f"maximum value of 4294967295 exceeded")
        elif len(bits) > 32:
            # only take first 32 bits
            bits = bits[-32:]
        elif len(bits) < 32:
            # pad with zeros to 32 bits
            bits = [0]*(32-len(bits)) + bits
        
        self.bits = bits

    @classmethod
    def fromint(cls, n):
        if n > 4294967295:
            raise ValueError(f"maximum value of 4294967295 exceeded")
        elif n < 0:
            bits = binary(n*-1)
            bits = twos(prepad(bits))
        else:
            bits = binary(n)
            bits = prepad(bits)

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

    def rshift(self, n):
        if n >= len(self):
            return self.__class__([0]*len(self))
        else:
            # chop last n bits, prepend n '0's
            result = [0]*n + self.bits[:-n]
            return self.__class__(result)
    
    def rotr(self, n):
        n = n % len(self)
        # chop last n bits, prepend them
        result = self.bits[-n:] + self.bits[:-n]
        return self.__class__(result)

    def __xor__(self, other):
        result = []
        for x,y in zip(self.bits, other.bits):
            result.append((x + y) % 2)

        return self.__class__(result)

    def __add__(self, other):
        i = len(self)-1
        carry = False
        result = []
        while i >= 0:
            x,y = self[i], other[i]
            if x and y:
                result.append(1 if carry else 0)
                carry = True
            elif x or y:
                result.append(0 if carry else 1)
            else:
                result.append(1 if carry else 0)
                carry = False

            i -= 1

        return self.__class__(result[::-1])

    def __eq__(self, other):
        # assume that other is UBitArray32
        return self.bits == other.bits

    def __getitem__(self, i):
        if isinstance(i, int):
            return self.bits[i]
        elif isinstance(i, slice):
            if not self.bits[i]:
                raise ValueError(f"slice results in empty {self.__class__.__name__}")
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
