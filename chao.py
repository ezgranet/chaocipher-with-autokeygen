#!/usr/bin/python3

'''
Python Chaocipher implementation.
Copyright 2010 Joel Martin
Additions copyright 2024 Elijah Granet

Licensed under LGPLv3 (see LICENSE.txt)
'''

import sys, optparse, re
import string_utils

class Chaocipher:
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.";

    def __init__(self, left, right,autoleft,autoright):
        self.orig_left = left
        self.orig_right = right
        self.orig_autoleft = autoleft
        self.orig_autoright = autoright

        self.reset()
        self.check()

    def reset(self):
        self.left = list(self.orig_left.upper())
        self.right = list(self.orig_right.upper())
        self.autoleft = list(self.orig_autoleft.upper())
        self.autoright = list(self.orig_autoright.upper())

    def check(self):
        left = self.left
        right = self.right
        autoleft = self.autoleft
        autoright = self.autoright

        if len(left) != 38:
            raise Exception("Left side must contain 38 characters")
        if len(right) != 38:
            raise Exception("Right side must contain 38 characters")

        for i in range(38):
            char = self.alphabet[i]
            if left.count(char) != 1:
                raise Exception("Left side missing '%s'" % char)
            if right.count(char) != 1:
                raise Exception("Right side missing '%s'" % char)

    def permute(self, idx):
        # Permute the left

        # Step 1: Rotate idx to zenith
        for cnt2 in range(idx):
            self.left.append(self.left.pop(0))
        # Step 2 and 3: extract zenith +1
        char = self.left.pop(1)
        # Step 4: Insert at nadir
        self.left.insert(19, char)

        # Permute the right

        # Step 1 and 2: rotate idx to zenith-1
        for cnt2 in range(idx+1):
            self.right.append(self.right.pop(0))
        # Step 3 and 4: remove zenith + 2
        char = self.right.pop(2)
        # Step 5: insert at nadir
        self.right.insert(19, char)
        # Permute the autoleft

        # Step 1: Rotate idx to zenith
        for cnt2 in range(idx):
            self.autoleft.append(self.autoleft.pop(0))
        # Step 2 and 3: extract zenith +1
        char = self.autoleft.pop(1)
        # Step 4: Insert at nadir
        self.autoleft.insert(19, char)

        # Permute the autoright

        # Step 1 and 2: rotate idx to zenith-1
        for cnt2 in range(idx+1):
            self.autoright.append(self.autoright.pop(0))
        # Step 3 and 4: remove zenith + 2
        char = self.autoright.pop(2)
        # Step 5: insert at nadir
        self.autoright.insert(19, char)

    def crypt(self, text, mode):
        src = list(text)
        dest = []

        for cnt in range(len(src)):
            char = src[cnt]
            if self.alphabet.find(char) < 0:
                #print("Ignoring character '%s'" % char)
                continue

            if mode == "decrypt":
                idx = self.right.index(char)
                dest.append(self.left[idx])
            elif mode == "autoencrypt":
                idx = self.autoleft.index(char)
                dest.append(self.autoright[idx])
            else:
                idx = self.left.index(char)
                dest.append(self.right[idx])

            if cnt + 1 == len(src):
                break

            self.permute(idx)

        return ''.join(dest)


if __name__ == '__main__':
    usage = "%prog [--left LEFT] [--right RIGHT] [--encrypt|--autoencrypt|--decrypt]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("--left", help="left alphabet",
                      default="0123456789_HXUCZVAMDSLKPEFJRIGTWOBNYQ.")
    parser.add_option("--right", help="right alphabet",
                      default="PTLNBQDEO0123456789_YSFAVZKGJRI.HWXUMC")
    parser.add_option("--autoleft", help="automatic  left alphabet",
                      default=string_utils.shuffle("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._"))
    parser.add_option("--autoright", help="automatic right alphabet",
                      default=string_utils.shuffle("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._"))
    parser.add_option("--encrypt", help="perform encryption",
                      action="store_const", const="encrypt", dest="mode",
                      default="encrypt")
    parser.add_option("--autoencrypt", help="perform automatic encryption",
                      action="store_const", const="autoencrypt", dest="mode",
                      default="encrypt")
    parser.add_option("--decrypt", help="perform decryption",
                      action="store_const", const="decrypt", dest="mode")
    (options, args) = parser.parse_args()

    C = Chaocipher(options.left, options.right, options.autoleft, options.autoright)

    if sys.stdin.isatty():
        if options.mode == "encrypt":
            print("Using  left: %s" % options.left)
            print("Using right: %s" % options.right)
            print("Enter plaintext (Ctrl-D to finish):")
        elif options.mode == "autoencrypt": 
            print("Using  autoleft: %s" % options.autoleft)
            print("Using autoright: %s" % options.autoright)
            print("Enter plaintext (Ctrl-D to finish):")
        else:
            print("Enter ciphertext (Ctrl-D to finish):")

    text = sys.stdin.read()

    result = C.crypt(text, options.mode)
    if sys.stdin.isatty():
        print("%sed result:\n%s" % (options.mode, result))
    elif options.mode == "autoencrypt":
        print("Using autoleft: %s" % options.autoleft)
        print("Using autoright: %s" % options.autoright)
        print(result)
    else:
        print(result)
