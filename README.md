# SHA-256

A purely Python, dependency-free implementation of the *256-bit Secure Hash Algorithm*, more commonly known as **SHA-256**. 

This implementation of **SHA-256** is *not* meant for use in cryptographically secure programs. It is simply the most basic implementation of **SHA-256** written purely in python. For use of this code, please refer to the [LICENSE (MIT)](https://github.com/greysonDEV/SHA-256/blob/main/LICENSE) under this repository.


### Goal

Not only was this project meant for research on hashing algorithms, but also for research and practice in manipulating bits in binary sequences. There are no uses of builtins such as `bin`, `ord`, `hex`, or any others that may assist in converting between strings, integers, and binary representations. Instead, they are implemented from scratch and can be found in the [`sha256/core`](https://github.com/greysonDEV/SHA-256/blob/main/LICENSE)


### Documentation

Aside from the implementation of **SHA-256**, this repository also contains many methods that deal with the various computations that are necessary for an implementation of **SHA-256**. The repository directory is as follows:
```python
├── sha256
    ├── __init__.py
    ├── const
    │   ├── __init__.py
    │   └── tables.py
    ├── core
    │   ├── __init__.py
    │   ├── bitops.py
    │   └── ubitarray_32.py
    └── sha256.py
```
In [`sha256/core/ubitarray_32.py`](https://github.com/greysonDEV/SHA-256/blob/main/sha256/core/ubitarray_32.py), `UBitArray32` is defined. This class is the heart of the binary computations that are used by **SHA-256**. Although it may not be obvious by looking at the `SHA256` method's source code, this class is relied upon heavily.\
Similarly, in [`sha256/core/bitops.py`](https://github.com/greysonDEV/SHA-256/blob/main/sha256/core/bitops.py), many methods, such as `binary` are defined. These methods are useful in both the `SHA256` method and `UBitArray32`. Tables such as `HEX` and `ASCII` are defined in [`sha256/const/tables.py`](https://github.com/greysonDEV/SHA-256/blob/main/sha256/const/tables.py), and are important in converting strings into their binary representation and integers into their hexadecimal representation.
