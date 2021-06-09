from sha256.const.tables import HEX, ASCII
import string

def test_HEX():
    result = HEX
    expected = {n:hex(n)[2:] for n in range(16)}
    assert result == expected

def test_ASCII():
    result = ASCII
    expected = {ch:ord(ch) for ch in sorted(list(string.printable), key=lambda ch: ord(ch))}
    assert result == expected
