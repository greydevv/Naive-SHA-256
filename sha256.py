from hashlib import sha256
from bitops import BitArray, compress, lsig_0, lsig_1
from const import H, K

def sha256(msg):
    # create padded message block (512 bits)
    # below line is broke, fromstr is deprecated 
    msg_block = BitArray.fromstr(msg).pad()

    # break into 32 bit words for message schedule
    words = [msg_block[i:i+32] for i in range(0, 512, 32)]
    i = 16
    while i < 64:
        a,b,c,d = words[-2], words[-7], words[-15], words[-16]
        new_word = lsig_0(a) + b + lsig_1(c) + d
        words.append(new_word)
        i += 1

    hash_values = compress(words)
    hex_digest = "".join(hv.tohex() for hv in hash_values)
    return hex_digest



if __name__ == "__main__":
    msg = "abc"
    _hash = sha256(msg)
    print(_hash)
