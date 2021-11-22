#!/usr/bin/env python3

# ----------------------------------------------------------------------
# compress.py
# Dave Reed
# 05/21/2021
# ----------------------------------------------------------------------

from __future__ import annotations
from typing import Optional
from argparse import ArgumentParser

from BinaryFileIO import BinaryFileWriter

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------

def main():
    parser = ArgumentParser(description="compress file using Huffman compression algorithm")
    parser.add_argument("file", help="file to compress")
    parser.add_argument("compressedFile", nargs="?", default=None, help="name of compressed file to create; defaults to adding .hc suffix if not supplied")
    args = parser.parse_args()

    fileToCompress = args.file
    compressedFile = args.compressedFile
    if compressedFile is None:
        compressedFile = fileToCompress + ".hc"


# ----------------------------------------------------------------------

if __name__ == '__main__':
    main()
