# ============================================================================ #
# Author: Greyson Murray (greyson.murray@gmail.com)
#
# Description: This file defines SHA256 and other auxiliary methods that deal
#                   with the computation of hexadecimal digests of data.
#
# LICENSE: MIT
# ============================================================================ #

from sha256.core.ubitarray_32 import UBitArray32, lsig0, lsig1, usig0, usig1, ch, maj
from sha256.core.bitops import binary, prepad
from sha256.const import H, K
from sha256.const.tables import ASCII

def schedule(wds):
    """
    Expands 16 words (each 32-bit) into a 64-word message schedule for
    compression. Making use of both 'σ0' and 'σ1' (lowercase sigma rotational 
    functions), new words are composed using the bits of previous words.

    Args:
        wds: (List[UBitArray32]) The original 16 words.

    Returns:
        (List[UBitArray32]) The final 64 words (message schedule).

    """

    for i in range(len(wds), 64):
        w = lsig1(wds[i-2]) + wds[i-7] + lsig0(wds[i-15]) + wds[i-16]
        wds.append(w)

    return wds

def compress(wds, ctx=None):
    """
    Compresses each word into eight state registers (a, b, c, d, e, f, g, h).
    New state is computed using '∑0' and '∑1' (uppercase sigma rotational
    methods) as well as the 'ch' (choice) and 'maj' (majority) methods.

    Args:
        wds: (List[UBitArray32]) The 64 words of the incoming message schedule.

    Returns:
        (Tuple[UBitArray32]) The resulting context of the
            state registers.

    """

    # set initial state registers
    # if ctx is not supplied, use defined constants
    state = ctx or tuple(UBitArray32.fromint(h) for h in H)
    a,b,c,d,e,f,g,h = state

    for i in range(64):
        t1 = usig1(e) + ch(e,f,g) + h + UBitArray32.fromint(K[i]) + wds[i]
        t2 = usig0(a) + maj(a,b,c)
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
    """
    '256-bit Secure Hash Algorithm' (SHA-256)

    Computes the hash of a piece of data. SHA-256 receives data to hash and
    creates 512-bit message blocks from the input. From the message blocks,
    a message schedule is created which contains 64 words (each 32-bit). This
    message schedule is sent to the compression function where each word in the
    schedule is then compressed into eight state registers. The context
    returned from a previous compression is then used for the next round of
    compression.

    Args:
        data: (str) The input data.

    Returns:
        (str) The hexadecimal digest of the hashed data.

    """

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

    hexdigest = "".join(x.tohex() for x in ctx)
    return hexdigest 
