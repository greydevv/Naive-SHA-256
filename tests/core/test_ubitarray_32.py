from sha256.core.ubitarray_32 import UBitArray32, xor, ch, maj, lsig0, lsig1, usig0, usig1
import pytest

def test___init___with_greater_than_32_bits():
    # UBitArray32.__init__  should remove leadings bits if length of input
    # bits exceeds 32
    result = UBitArray32([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0])
    expected = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0]
    assert result.bits == expected
    
    result = UBitArray32([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0])
    expected = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0]
    assert result.bits == expected

def test___init___with_less_than_32_bits():
    result = UBitArray32([1,1,1,1])
    expected = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1]
    assert result.bits == expected

    result = UBitArray32([1])
    expected = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
    assert result.bits == expected

def test___init___with_no_bits():
    with pytest.raises(ValueError, match="cannot create empty UBitArray32"):
        UBitArray32([])

def test_from_int_with_positive_int():
    result = UBitArray32.fromint(10)
    expected = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0]
    assert result.bits == expected

    result = UBitArray32.fromint(97)
    expected = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1]
    assert result.bits == expected

    result = UBitArray32.fromint(247)
    expected = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,1,1]
    assert result.bits == expected

    result = UBitArray32.fromint(3984982)
    expected = [0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,1,1,0,0,1,1,1,0,0,1,0,1,0,1,1,0]
    assert result.bits == expected

def test_from_int_with_negative_int():
    # -24 (signed) -> 4292967272 (unsigned)
    result = UBitArray32.fromint(-24)
    expected = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,0,0]
    assert result.bits == expected

def test_from_int_exceeding_max_value():
    with pytest.raises(ValueError, match="maximum value of \\(2\\*\\*32\\)-1, or 4294967295, exceeded"):
        UBitArray32.fromint(4294967296)

def test_toint():
    result = UBitArray32([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0]).toint()
    expected = 10
    assert result == expected

    result = UBitArray32([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,0,0,0,1,1,1,1]).toint()
    expected = 25487
    assert result == expected

def test_tohex():
    result = UBitArray32([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,1,1,0,0,0,0,1,1,1,1,1]).tohex()
    expected = "0000ae1f"
    assert result == expected

    result = UBitArray32([1,0,0,1,1,1,0,0,1,0,1,0,0,1,1,0,1,0,1,0,0,1,0,0,0,0,0,1,0,0,0,1]).tohex()
    expected = "9ca6a411"
    assert result == expected

def test_rshift():
    # test with n inside bounds
    result = UBitArray32([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,1]).rshift(3)
    expected = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0]
    assert result.bits == expected
    
    # test with n outside of bounds
    result = UBitArray32([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,1,1,1]).rshift(46)
    expected = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    assert result.bits == expected

def test_rotr():
    # test with n inside bounds
    result = UBitArray32([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0,1,1]).rotr(3)
    expected = [0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,0]
    assert result.bits == expected

    # test with n out of bounds
    result = UBitArray32([1,1,1,0,0,0,0,0,1,1,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,1,0,0,1,1,0,0]).rotr(40)
    expected = [1,1,0,0,1,1,0,0,1,1,1,0,0,0,0,0,1,1,0,0,1,1,1,1,0,0,0,1,1,1,1,1] 
    assert result.bits == expected

def test___xor___with_even_bit_lengths():
    a = UBitArray32([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,0,1])
    b = UBitArray32([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0])
    result =  a ^ b
    expected = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1]
    assert result.bits == expected

    a = UBitArray32([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0])
    b = UBitArray32([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,0,0,1,1,0,0,1,1,0,0,1,0])
    result = a ^ b 
    expected = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,1,1,0,0,1,1,0,0,1,0]
    assert result.bits == expected

def test___add__():
    result = UBitArray32.fromint(8) + UBitArray32.fromint(27)
    expected = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1]
    assert result.bits == expected
    
    result = UBitArray32.fromint(152) + UBitArray32.fromint(83)
    expected = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,0,1,1]
    assert result.bits == expected

def test___eq___with_equal():
    result = UBitArray32.fromint(10) == UBitArray32.fromint(10)
    expected = True
    assert result == expected

def test___eq___with_not_equal():
    result = UBitArray32.fromint(10) == UBitArray32.fromint(9)
    expected = False
    assert result == expected

def test___getitem___with_integer_index():
    # integer index returns an int, either 1 or 0 (bit)
    a = UBitArray32.fromint(10)
    result = isinstance(a[0], int)
    expected = True
    assert result == expected

def test___getitem___with_slice_index():
    # slice returns an instance of UBitArray32
    a = UBitArray32.fromint(10)
    result = isinstance(a[0:5], UBitArray32)
    expected = True
    assert result == expected

def test___getitem___with_invalid_slice_index():
    with pytest.raises(ValueError, match="slice results in empty UBitArray32"):
        UBitArray32.fromint(10)[:0]

def test___len__():
    result = len(UBitArray32.fromint(10))
    expected = 32
    assert result == expected

def test___str__():
    result = str(UBitArray32.fromint(10)) 
    expected = "00000000000000000000000000001010"
    assert result == expected

def test___repr__():
    result = repr(UBitArray32.fromint(10))
    expected = "UBitArray32[0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 1 0]"
    assert result == expected

def test_xor():
    a = UBitArray32([0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,1,1,1,1,1,0,1,0,0,1,1,0,0,1,0,1])
    b = UBitArray32([0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,1,1,0,0,1,0,1,0,1,0,1,1,0,1,0,0,1])
    c = UBitArray32([0,0,0,0,1,0,1,0,0,1,1,0,0,1,1,1,1,0,0,0,0,0,0,1,0,1,1,0,1,0,0,1])
    result = xor(a,b,c)
    expected = [0,0,0,1,0,0,1,0,0,0,0,0,0,0,1,0,1,1,1,0,1,1,1,0,0,1,1,0,0,1,0,1]
    assert result.bits == expected

def test_ch():
    a = UBitArray32([0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,1,1,1,1,1,0,1,0,0,1,1,0,0,1,0,1])
    b = UBitArray32([0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,1,1,0,0,1,0,1,0,1,0,1,1,0,1,0,0,1])
    c = UBitArray32([0,0,0,0,1,0,1,0,0,1,1,0,0,1,1,1,1,0,0,0,0,0,0,1,0,1,1,0,1,0,0,1])
    result = ch(a,b,c)
    expected = [0,0,0,0,1,0,1,0,1,0,0,0,0,0,1,1,1,0,0,1,0,0,0,1,0,1,1,0,1,0,0,1]
    assert result.bits == expected

def test_maj():
    a = UBitArray32([0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,1,1,1,1,1,0,1,0,0,1,1,0,0,1,0,1])
    b = UBitArray32([0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,1,1,0,0,1,0,1,0,1,0,1,1,0,1,0,0,1])
    c = UBitArray32([0,0,0,0,1,0,1,0,0,1,1,0,0,1,1,1,1,0,0,0,0,0,0,1,0,1,1,0,1,0,0,1])
    result = maj(a,b,c)
    expected = [0,0,0,0,1,0,0,0,1,1,1,0,0,1,0,1,1,0,0,1,0,0,0,1,0,1,1,0,1,0,0,1]
    assert result.bits == expected

def test_lsig0():
    a = UBitArray32([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
    result = lsig0(a)
    expected = [1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,0,0,0]
    assert result.bits == expected

def test_lsig1():
    a = UBitArray32([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
    result = lsig1(a)
    expected = [0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1]
    assert result.bits == expected

def test_usig0():
    a = UBitArray32([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
    result = usig0(a)
    expected = [0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,0]
    assert result.bits == expected

def test_usig1():
    a = UBitArray32([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
    result = usig1(a)
    expected = [0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,0,0,0]
    assert result.bits == expected
