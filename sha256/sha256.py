from sha256.core.ubitarray_32 import UBitArray32, lsig0, lsig1, usig0, usig1, choice, majority
from sha256.core.bitops import binary,prepad
from sha256.const import H, K
from sha256.const.tables import ASCII

def schedule(words):
    for i in range(len(words), 64):
        w = lsig1(words[i-2]) + words[i-7] + lsig0(words[i-15]) + words[i-16]
        words.append(w)
    return words

def compress(words, ctx=None):
    # set inital states
    state = ctx or tuple(UBitArray32.fromint(h) for h in H)
    a,b,c,d,e,f,g,h = state

    for i in range(64):
        t1 = usig1(e) + choice(e,f,g) + h + UBitArray32.fromint(K[i]) + words[i]
        t2 = usig0(a) + majority(a,b,c)
        h = g
        g = f
        f = e
        e = d + t1
        d = c
        c = b
        b = a
        a = t1 + t2
        
    a += state[0]
    b += state[1]
    c += state[2]
    d += state[3]
    e += state[4]
    f += state[5]
    g += state[6]
    h += state[7]

    return a,b,c,d,e,f,g,h

def sha256(data):
    msg = []
    for ch in data:
        _ord = ASCII[ch]
        """TODO: possibly deprecate prepad() and build in 8 bits to binary() by default"""
        ch_bits = prepad(binary(_ord), to=8)
        msg.extend(ch_bits)
    
    datalen = binary(len(msg)) # what to do if the length of this is > 64 bits?
    tail = [0]*(64-len(datalen)) + datalen # compose length of data in bits (64 bits)
    padding = [1] + [0]*(511-((len(msg)+len(tail)) % 512))
    msg += padding
    msg += tail
    
    blocks = []
    for i in range(0, len(msg), 512):
        blocks.append(msg[i:i+512])
    
    ctx = None
    for b in blocks:
        # create 32-bit words from 512-bit chunks
        words = [UBitArray32(b[i:i+32]) for i in range(0, 512, 32)]
        words = schedule(words)
        ctx = compress(words, ctx)
    
    return "".join(x.tohex() for x in ctx)

if __name__ == "__main__":
    msg = "abc"*127
    import sys
    result = sha256(msg)
