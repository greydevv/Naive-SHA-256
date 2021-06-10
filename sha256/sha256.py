from sha256.core.ubitarray_32 import UBitArray32, lsig0, lsig1, usig0, usig1, choice, majority
from sha256.core.bitops import binary, prepad
from sha256.const import H, K
from sha256.const.tables import ASCII

def schedule(wds):
    for i in range(len(wds), 64):
        w = lsig1(wds[i-2]) + wds[i-7] + lsig0(wds[i-15]) + wds[i-16]
        wds.append(w)

    return wds

def compress(wds, ctx=None):
    # set initial state registers
    # if ctx is not supplied, use defined constants
    state = ctx or tuple(UBitArray32.fromint(h) for h in H)
    a,b,c,d,e,f,g,h = state

    for i in range(64):
        t1 = usig1(e) + choice(e,f,g) + h + UBitArray32.fromint(K[i]) + wds[i]
        t2 = usig0(a) + majority(a,b,c)
        # assign registers to previous (b=a, c=b, etc.)
        h = g
        g = f
        f = e
        e = d + t1
        d = c
        c = b
        b = a
        a = t1 + t2

    # add new state to original state
    a += state[0]
    b += state[1]
    c += state[2]
    d += state[3]
    e += state[4]
    f += state[5]
    g += state[6]
    h += state[7]

    return a,b,c,d,e,f,g,h

def SHA256(data):
    msg = []
    for e in data:
        # convert chars to binary in 8-bit 
        chbin = prepad(binary(ASCII[e]), to=8)
        msg.extend(chbin)
    
    # get length (in bits) of input
    datalen = binary(len(msg))
    if len(datalen) > 64:
        raise ValueError("input is too large")

    # pad out message to factor of 512 (512-bit blocks)
    tail = [0]*(64-len(datalen)) + datalen
    padding = [1] + [0]*(511-((len(msg)+len(tail)) % 512))
    msg += (padding + tail)
    
    ctx = None
    for i in range(0, len(msg), 512):
        block = msg[i:i+512] 
        wds = [UBitArray32(block[i:i+32]) for i in range(0, 512, 32)]
        wds = schedule(wds)
        # set context for next block
        ctx = compress(wds, ctx)

    return "".join(x.tohex() for x in ctx)
