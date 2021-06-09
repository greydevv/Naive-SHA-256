from sha256.core.bitops import binary, prepad, add, twos

def test_binary():
    result = binary(0)
    expected = [0]
    assert result == expected
    
    result = binary(10)
    expected = [1,0,1,0]
    assert result == expected

    result = binary(528193)
    expected = [1,0,0,0,0,0,0,0,1,1,1,1,0,1,0,0,0,0,0,1]
    assert result == expected

def test_prepad():
    result = prepad([0,0,1,1], to=0)
    expected = [0,0,1,1]
    assert result == expected

    result = prepad([1,1,1,1], to=8)
    expected = [0,0,0,0,1,1,1,1]
    assert result == expected

    result = prepad([0,0,0,0,1,1,1,1], to=32)
    expected = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1]
    assert result == expected

def test_add():
    result = add([1,0,1,0,1,0,1,0], [1,1,0,0,1,1,0,0])
    expected = [1,0,1,1,1,0,1,1,0]
    assert result == expected
