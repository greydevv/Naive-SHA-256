from bitops import UBitArray
import pytest

def test___init___with_insignificant_leading_zeros():
    result = UBitArray([0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1])
    expected = [1,1,1,1,1,1,1,1]
    assert result.bits == expected
    
    result = UBitArray([0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,])
    expected = [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1]
    assert result.bits == expected

    result = UBitArray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,])
    expected = [0,0,0,0,0,0,0,0]
    assert result.bits == expected

def test___init___with_bit_length_not_divisible_by_eight():
    result = UBitArray([1,1,1,1])
    expected = [0,0,0,0,1,1,1,1]
    assert result.bits == expected

    result = UBitArray([0])
    expected = [0,0,0,0,0,0,0,0]
    assert result.bits == expected

def test_from_int_with_positive_ints():
    result = UBitArray.fromint(10)
    expected = [0,0,0,0,1,0,1,0]
    assert result.bits == expected

    result = UBitArray.fromint(97)
    expected = [0,1,1,0,0,0,0,1]
    assert result.bits == expected

    result = UBitArray.fromint(247)
    expected = [1,1,1,1,0,1,1,1]
    assert result.bits == expected

    result = UBitArray.fromint(3984982)
    expected = [0,0,1,1,1,1,0,0,1,1,0,0,1,1,1,0,0,1,0,1,0,1,1,0]
    assert result.bits == expected

def test_toint():
    result = UBitArray([0,0,0,0,1,0,1,0]).toint()
    expected = 10
    assert result == expected

    result = UBitArray([0,1,1,0,0,0,1,1,1,0,0,0,1,1,1,1]).toint()
    expected = 25487
    assert result == expected

def test_tohex():
    result = UBitArray([0,0,1,0,0,1,0,1]).tohex()
    expected = "25"
    assert result == expected

    result = UBitArray([1,0,1,0,1,1,1,0,0,0,0,1,1,1,1,1]).tohex()
    expected = "ae1f"
    assert result == expected

def test_rshift():
    # test with n inside bounds
    result = UBitArray([0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,1]).rshift(3)
    expected = [0,1,1,1,1,1,1,0]
    assert result.bits == expected
    
    # test with n outside of bounds
    result = UBitArray([1,0,1,0,1,1,1,1]).rshift(20)
    expected = [0,0,0,0,0,0,0,0]
    assert result.bits == expected

def test_rotr():
    # test with n inside bounds
    result = UBitArray([1,0,1,0,1,0,1,0,1,0,1,0,0,0,1,1]).rotr(3)
    expected = [0,1,1,1,0,1,0,1,0,1,0,1,0,1,0,0]
    assert result.bits == expected

    # test with n out of bounds
    result = UBitArray([0,0,0,1,1,1,1,1,1,1,0,0,1,1,0,0]).rotr(20)
    expected = [1,1,0,0,0,0,0,1,1,1,1,1,1,1,0,0] 
    assert result.bits == expected

def test___xor___with_even_bit_lengths():
    result = UBitArray([1,0,0,0,1,1,0,1]) ^ UBitArray([0,0,0,1,1,1,0,0])
    expected = [1,0,0,1,0,0,0,1]
    assert result.bits == expected

    result = UBitArray([1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0]) ^ UBitArray([1,0,1,1,0,0,1,1,0,0,1,1,0,0,1,0])
    expected = [0,1,0,1,0,1,1,1,0,0,1,1,0,0,1,0]
    assert result.bits == expected

def test___xor___with_uneven_bit_lengths():
    result = UBitArray([0,0,0,0,1,1,1,1]) ^ UBitArray([0,0,0,1,1,1,0,1,1,0,1,1,0,0,0,1])
    expected =[0,0,0,1,1,1,0,1,1,0,1,1,1,1,1,0]
    assert result.bits == expected

def test___add___with_even_bit_lengths():
    result = UBitArray.fromint(8) + UBitArray.fromint(27)
    expected = UBitArray([0,0,1,0,0,0,1,1])
    assert result == expected
    
    result = UBitArray.fromint(152) + UBitArray.fromint(83)
    expected = UBitArray([1,1,1,0,1,0,1,1])
    assert result == expected

def test___add___with_uneven_bit_lengths():
    result = UBitArray.fromint(359) + UBitArray.fromint(1092)
    expected = UBitArray([0,0,0,0,0,1,0,1,1,0,1,0,1,0,1,1])
    assert result == expected

    result = UBitArray.fromint(4329105) + UBitArray.fromint(8773429)
    expected = UBitArray([1,1,0,0,0,1,1,1,1,1,1,0,1,1,0,1,1,1,0,0,0,1,1,0])
    assert result == expected

def test___eq___with_equal():
    result = UBitArray.fromint(10) == UBitArray.fromint(10)
    expected = True
    assert result == expected

def test___eq___with_not_equal():
    result = UBitArray.fromint(10) == UBitArray.fromint(9)
    expected = False
    assert result == expected

def test___getitem___with_int_index():
    a = UBitArray.fromint(10)
    result = isinstance(a[0], int)
    expected = True
    assert result == expected

def test___getitem___with_slice_index():
    a = UBitArray.fromint(10)
    result = isinstance(a[0:5], UBitArray)
    expected = True
    assert result == expected

def test___getitem___with_invalid_slice_index():
    with pytest.raises(ValueError, match="slice results in an empty UBitArray"):
        UBitArray.fromint(10)[:0]

def test___len__():
    result = len(UBitArray.fromint(10))
    expected = 8
    assert result == expected

def test___str__():
    result = str(UBitArray.fromint(10)) 
    expected = "00001010"
    assert result == expected

def test___repr__():
    result = repr(UBitArray.fromint(10))
    expected = "UBitArray[0 0 0 0 1 0 1 0]"
    assert result == expected
