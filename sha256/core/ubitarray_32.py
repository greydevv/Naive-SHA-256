# ============================================================================ #
# Author: Greyson Murray (greyson.murray@gmail.com)
#
# Description: This file contains UBitArray32 and other auxiliary methods that
#                  deal with various bit computations. 
#
# LICENSE: MIT
# ============================================================================ #

from __future__ import annotations
from typing import List, Union
from collections.abc import Iterator
from functools import reduce
from sha256.core.bitops import binary, prepad, twos, add
from sha256.const.tables import HEX

class UBitArray32:
    """
    (Unsigned 32-Bit Array)
    
    This class is responsible for handling much of the bit computations in the
    hash function. Being an unsigned 32-bit array, the maximum integer value
    that this array should hold is (2**32)-1, or 4294967295. Negative numbers
    will also be converted into their unsigned counterpart.

    """
    
    def __init__(self, bits: List[int]) -> None:
        """
        Args:
            bits: (List[int]) The list of bits to create a UBitArray32 object
                from.

        """

        if not bits:
            raise ValueError(f"cannot create empty {self.__class__.__name__}")
        elif len(bits) > 32:
            # only take first 32 bits
            bits = bits[-32:]
        elif len(bits) < 32:
            # pad with zeros to 32 bits
            bits = [0]*(32-len(bits)) + bits
        
        self.bits = bits

    @classmethod
    def fromint(cls, n: int) -> UBitArray32:
        """
        Creates a UBitArray32 object from an integer. The integer is converted
        into its binary representation and fed back into the
        UBitArray32.__init__ method to create the object.

        Args:
            n: (int) The integer to create a UBitArray32 object from.

        Returns:
           (bits): (UBitArray32) The resulting UBitArray32 object.
        
        Raises:
            (ValueError) The largest number that can be represented in 32-bit is
                (2**32)-1, or 4294967295. For this reason a ValueError is raised
                if and when a number larger than (2**32)-1 is passed to this
                method.

        """

        if n > (2**32)-1:
            raise ValueError(f"maximum value of (2**32)-1, or 4294967295, exceeded")
        elif n < 0:
            bits = binary(n*-1)
            bits = twos(prepad(bits))
        else:
            bits = binary(n)
            bits = prepad(bits)

        return cls(bits)

    def toint(self) -> int:
        """
        Converts the UBitArray32 object back into its (unsigned) integer
        representation.

        Returns:
           (int) The integer representation of the UBitArray32 object. 

        """

        # create backwards range for powers
        pows = range(len(self)-1,-1,-1)
        n = 0
        for bit,_pow in zip(self, pows):
            n += bit*(2**_pow)
        return n

    def tohex(self) -> str:
        """
        Converts the UBitArray32 object into its hexadecimal representation.

        Returns:
            (str) The hexadecimal representation of the UBitArray32
                object.

        """
        
        chunks = [self[i:i+4] for i in range(0, len(self), 4)]
        result = ""
        for chunk in chunks:
            hex_value = HEX[chunk.toint()]
            result += hex_value

        return result

    def rshift(self, n: int) -> UBitArray32:
        """
        Computes a new UBitArray32 object resulting from shifting the bits
        'n' positions rightwards.

        Args:
            n: (int) The amount to shift by.

        Returns:
            (UBitArray32) The resulting UBitArray32 object.

        """

        if n >= len(self):
            return self.__class__([0]*len(self))
        else:
            # chop last n bits, prepend n '0's
            result = [0]*n + self.bits[:-n]
            return self.__class__(result)
    
    def rotr(self, n: int) -> UBitArray32:
        """
        Computes a new UBitArray32 object resulting from rotating the bits
        'n' positions rightwards.

        Args:
            n: (int) The amount to rotate by.

        Returns:
            (UBitArray32) The resulting UBitArray32 object.

        """

        n %= len(self)
        # chop last n bits, prepend them
        result = self.bits[-n:] + self.bits[:-n]
        return self.__class__(result)

    def __xor__(self, other: UBitArray32) -> UBitArray32:
        """
        Computes the bitwise XOR operation with another instance of
        UBitArray32.

        Args:
            other: (UBitArray32) The other instance to compute XOR with. 

        Returns:
            (UBitArray32) The resulting UBitArray32 object.

        """

        result = []
        for x,y in zip(self.bits, other.bits):
            result.append((x + y) % 2)

        return self.__class__(result)

    def __add__(self, other: UBitArray32) -> UBitArray32:
        """
        Computes the bitwise addition operation with another instance of
        UBitArray32.

        Args:
            other: (UBitArray32) The other instance to add to. 

        Returns:
            (UBitArray32) The resulting UBitArray32 object.

        """

        return self.__class__(add(self, other))

    def __eq__(self, other: UBitArray32) -> bool:
        """
        Computes the bitwise addition operation with another instance of
        UBitArray32.

        Args:
            other: (UBitArray32) The other instance to compare to. 

        Returns:
            (bool) True if both 'self' and 'other' have equal bits; otherwise
                False.

        """

        return self.bits == other.bits

    def __getitem__(self, i) -> Union[int, UBitArray32]:
        """
        Gets the bit at the 'i'th index and supports slicing.
        
        Args:
            i: (int or slice) The index or slice to retrieve.

        Returns:
            (int) The bit at the 'i'th postiion (either 0 or 1)
            (UBitArray32) The set of bits retrieved from the slicing operation.

        """

        if isinstance(i, int):
            return self.bits[i]
        elif isinstance(i, slice):
            if not self.bits[i]:
                raise ValueError(f"slice results in empty {self.__class__.__name__}")
            return self.__class__(self.bits[i])

    def __iter__(self) -> Iterator[int]:
        """
        Supports iteration over instances of UBitArray32.

        Returns:
            (list_iterator): An iterator of the set of bits contained by the
                instance of UBitArray32.

        """

        return iter(self.bits)

    def __len__(self) -> int:
        """
        Returns:
            (int) The length of bits.

        """

        return len(self.bits)

    def __str__(self) -> str:
        """
        Returns:
            (str) A simple string representation, for example:
                '00011011110000111000001000110000'
                
        """

        return "".join([str(bit) for bit in self.bits])
    
    def __repr__(self) -> str:
        """
        Returns:
            (str) A string representation for debugging, for example:
                'UBitArray32[0 0 0 1 1 0 1 1 1 1 0 0 0 0 1 1 1 0 0 0 0 0 1 0 0 0 1 1 0 0 0 0]'
                
        """

        cls_name = self.__class__.__name__
        bit_repr = " ".join([str(bit) for bit in self.bits])
        return f"{cls_name}[{bit_repr}]"




def xor(*bitarrays: UBitArray32) -> UBitArray32:
    """
    Computes the bitwise XOR of the input sets of bits.

    Args:
        *bit_arrays: (UBitArray32) The sets of bits to XOR.

    Returns:
        (UBitArray32) The result of the XOR operation.

    """

    result = reduce(UBitArray32.__xor__, bitarrays)
    return result

def ch(a: UBitArray32, b: UBitArray32, c: UBitArray32) -> UBitArray32:
    """
    Takes the 'choice' of two sets of bits ('b' and 'c') based off of the bits
    in 'a'. 

    Example:
        a: 00010110
        b: 11001010
        c: 01111000
        -> 01101010

    Args:
        a: (UBitArray32) The model set of bits.
        b: (UBitArray32) The bits chosen if the model bit is 1.
        c: (UBitArray32) The bits chosen if the model bit is 0.

    Returns:
        (UBitArray32) The result of the choice operation.

    """

    result = []
    for model, y, z in zip(a, b, c):
        result.append(y if model else z)
    return UBitArray32(result)

def maj(a: UBitArray32, b: UBitArray32, c: UBitArray32) -> UBitArray32:
    """
    Takes the 'majority' of three sets of bits. The bits in each set are
    consecutively iterated over, and the resulting bit is the bit that appears
    most across the current bit. 

    Example:
        a: 00010110
        b: 11001010
        c: 01111000
        -> 01011010

    Args:
        a: (UBitArray32) 
        b: (UBitArray32)
        c: (UBitArray32)

    Returns:
        (UBitArray32) The result of the majority operation.

    """

    result = []
    for bits in zip(a,b,c):
        result.append(max(bits, key=bits.count))
    return UBitArray32(result)

def lsig0(bitarray: UBitArray32) -> UBitArray32:
    """
    (lowercase sigma 0)
    
    Computes the XOR of three sets of bits which result from rotating the input
    set rightwards by 7, then 18, and then right-shifts by 3.

    Args:
        bitarray: (UBitArray32) The set of bits to operate on.

    Returns:
        (UBitArray32) The XOR of the three sets that result from
            rotating/shifting the input set..

    """
    
    a = bitarray.rotr(7)
    b = bitarray.rotr(18)
    c = bitarray.rshift(3)
    return xor(a,b,c)

def lsig1(bitarray: UBitArray32) -> UBitArray32:
    """
    (lowercase sigma 1)
    
    Computes the XOR of three sets of bits which result from rotating the input
    set rightwards by 17, then 19, and then right-shifts by 10.

    Args:
        bitarray: (UBitArray32) The set of bits to operate on.

    Returns:
        (UBitArray32) The XOR of the three sets that result from
            rotating/shifting the input set..

    """
    
    a = bitarray.rotr(17)
    b = bitarray.rotr(19)
    c = bitarray.rshift(10)
    return xor(a,b,c)

def usig0(bitarray: UBitArray32) -> UBitArray32:
    """
    (uppercase sigma 0)
    
    Computes the XOR of three sets of bits which result from rotating the input
    set rightwards by 2, then 13, and then 22.

    Args:
        bitarray: (UBitArray32) The set of bits to operate on.

    Returns:
        (UBitArray32) The XOR of the three sets that result from
            rotating the input set..

    """
    
    a = bitarray.rotr(2)
    b = bitarray.rotr(13)
    c = bitarray.rotr(22)
    return xor(a,b,c)

def usig1(bitarray: UBitArray32) -> UBitArray32:
    """
    (uppercase sigma 1)
    
    Computes the XOR of three sets of bits which result from rotating the input
    set rightwards by 6, then 11, and then 25.

    Args:
        bitarray: (UBitArray32) The set of bits to operate on.

    Returns:
        (UBitArray32) The XOR of the three sets that result from
            rotating the input set..

    """
    
    a = bitarray.rotr(6)
    b = bitarray.rotr(11)
    c = bitarray.rotr(25)
    return xor(a,b,c)
