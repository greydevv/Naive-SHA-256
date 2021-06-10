from sha256.sha256 import sha256

def test_with_0_bits():
    result = sha256("")
    expected = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert result == expected

def test_with_24_bits():
    result = sha256("abc")
    expected = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    assert result == expected

def test_with_488_bits():
    result = sha256("abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq")
    expected ="248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"
    assert result == expected

def test_with_896_bits():
    result = sha256("abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu")
    expected = "cf5b16a778af8380036ce59e7b0492370b249b11e8f07a51afac45037afee9d1"
    assert result == expected

