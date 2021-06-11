# ============================================================================ #
# Author: Greyson Murray (greyson.murray@gmail.com)
#
# Description: This file contains various methods responsible for binary/bit
#                  conversions/computations.
#
# LICENSE: MIT
# ============================================================================ #

from sha256.const.tables import ASCII
from sha256.const import H, K

def binary(n):
    """
    Converts an integer into its unsigned binary representation. If a negative
    number is input, the binary representation of its positive counterpart
    will be returned.

    Args:
        n: (int) The integer to be converted.

    Returns:
        (List[int]) The binary representation of the input integer.
        
    """
    
    if n == 0:
        return [0]
    elif n < 0:
        n *= -1

    bits = []
    while n != 0:
        bits.append(n % 2)
        n = n // 2
    
    return bits[::-1]

def prepad(bits, to=32):
    """
    Pads a list of bits to a certain length factor.

    Args:
        bits: (List[int]) The bits to pad.
        to: (int) The length factor to pad the bits with. If a 43-bit list is
            input and this parameter is left at default (32), the list will be
            padded out to the next factor of 32, which will be 64 in this case.

    Returns:
        (List[int]) The padded bits.

    """

    if to == 0: return bits

    rem = len(bits) % to
    if rem > 0:
        bits = [0]*(to-rem) + bits
    
    return bits

def add(a,b):
    """
    Adds two lists of bits together. When summing bits, they are added from
    left to right. For that reason, a reverse range is used to iterate through
    the bits backwards. The resulting bits are then reversed after addition to
    rectify the result.
    
    Args:
        a: (List[int]) The first addend.
        b: (List[int]) The second addend.

    Returns:
       (List[int]) The sum of the two addends. 

    """

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
    """
    Converts a list of bits into its Two's Complement representation. The bits
    are negated (flipped) and the list of bits is then added with 1.

    Agrs:
        bits: (List[int]) The bits to take Two's Complement of.

    Returns:
        (List[int]) The Two's Complement representation.

    """

    # 1-bit flips the bit (1-0=1, 1-1=0)
    bits = [1-bit for bit in bits]
    other = [0]*(len(bits)-1) + [1]  

    return add(bits, other)
