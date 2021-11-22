#!/usr/bin/env python3

# ----------------------------------------------------------------------
# decompress.py
# Dave Reed
# 05/21/2021
# ----------------------------------------------------------------------

from typing import Optional
from argparse import ArgumentParser

from BinaryFileIO import *

# ----------------------------------------------------------------------

def main():
    parser = ArgumentParser(description="decompress file using Huffman compression algorithm")
    parser.add_argument("file", help="file to decompress")
    parser.add_argument("decompressedFile", nargs="?", default=None,
                        help="name of decompressed file to create; defaults to removing .hc suffix if not supplied or using .dc if no .huc suffix at end")
    args = parser.parse_args()

    fileToDecompress = args.file
    decompressedFile = args.decompressedFile
    if decompressedFile is None:
        if fileToDecompress[-3:] == ".hc":
            decompressedFile = fileToDecompress[:-3]
        else:
            decompressedFile = fileToDecompress + ".huc"

# ----------------------------------------------------------------------

if __name__ == '__main__':
    main()
