## Chaocipher:  Python versions with automatic key generation


### Description

[Chaocipher](http://en.wikipedia.org/wiki/Chaocipher) is a method of
encryption invented by John F. Byrne in 1918 that was never publicly
solved.

The algorithm was published in May 2010. These implementations are
based on a
[paper](http://www.mountainvistasoft.com/chaocipher/ActualChaocipher/Chaocipher-Revealed-Algorithm.pdf)
by Moshe Rubin.

### Usage



The python program `chao.py` reads the plaintext or ciphertext from
standard input and writes the result to stdout.  The `--encrypt` and `--decrypt` and  arguments specify the
mode. The left and right
alphabets are set using the `--left` and `--right` arguments
respectively.

An example of encrypting a file:
    cat myfile.txt | python3 chao.py --autoencrypt

An example of decrypting text entered from the terminal:
    python3 chao.py --decrypt --left HXUCZVAMDSLKPEFJRIGTWOBNYQ --right PTLNBQDEOYSFAVZKGJRIHWXUMC
