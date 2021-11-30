#!/usr/bin/env python3

# ----------------------------------------------------------------------
# compress.py
# Dave Reed
# 05/21/2021
# ----------------------------------------------------------------------

from __future__ import annotations
from typing import Optional, Dict
from argparse import ArgumentParser

from BinaryFileIO import BinaryFileWriter

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------

def readData(filename) -> str:

    infile = open(filename, "r")
    fileContents = ""

    line = infile.readline()
    while line:
        fileContents += line
        line = infile.readline()

    return fileContents

def readFrequencies(data: str) -> Dict[str, int]:

    frequencies = {}
    for i in range(len(data)):
        char = data[i]
        if char in frequencies:
            frequencies[char] = frequencies[char] + 1
        else:
            frequencies[char] = 1

    return frequencies

def createHeap():
    pass

def compress():
    # writer = BinaryFileWriter()
    pass

def main():
    parser = ArgumentParser(description="compress file using Huffman compression algorithm")
    parser.add_argument("file", help="file to compress")
    parser.add_argument("compressedFile", nargs="?", default=None, help="name of compressed file to create; defaults to adding .hc suffix if not supplied")
    args = parser.parse_args()

    fileToCompress = args.file
    compressedFile = args.compressedFile
    if compressedFile is None:
        compressedFile = fileToCompress + ".hc"

    data: str = readData(fileToCompress)
    frequencies: Dict[str, int] = readFrequencies(data)

    print(frequencies)

# ----------------------------------------------------------------------

if __name__ == '__main__':
    main()
