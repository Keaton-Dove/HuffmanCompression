#!/usr/bin/env python3

# ----------------------------------------------------------------------
# decompress.py
# Dave Reed
# 05/21/2021

# Keaton Dove
# 12/2/2021
# CS-361

# ----------------------------------------------------------------------

from typing import Optional, Dict
from argparse import ArgumentParser

from BinaryFileIO import *

# ----------------------------------------------------------------------

def _readKey(binaryReader: BinaryFileReader, amntUniqueChar: int) -> Dict[str, str]:

    keyDict = {}

    # While dictionary has less keys than amount of unique characters...
    while (len(keyDict) < amntUniqueChar):

        # Getting the character and amount of bits in its code
        char = chr(binaryReader.readUByte())
        amntBits = binaryReader.readUShort()

        bitCode = ""

        # Accumulating the bitCode
        for i in range(amntBits):
            bitCode += str(binaryReader.readBit())

        # Creating entry from that bitCode to the respective character
        keyDict[bitCode] = char

    return keyDict

def _readData(binaryReader: BinaryFileReader, keyDict: Dict[str, str], totalBytes: int) -> str:

    data = ""

    # Only reading data while they are more characters
    while len(data) < totalBytes:

        currentBitCode = ""

        # Checking if binary code matches character in dictionary
        while currentBitCode not in keyDict:
            # If not, adding another bit to the code
            currentBitCode += str(binaryReader.readBit())

        # If so, accumulating to data string
        data += keyDict[currentBitCode]

    return data

def _writeData(data: str, destinationFile) -> None:

    outfile = open(destinationFile, "w")
    outfile.write(data)
    outfile.close()

def decompress(sourceFile, destinationFile) -> str:

    # Initializing binary reader
    binaryReader = BinaryFileReader(sourceFile)

    # Getting header info from file: total amount of characters and amount of unique characters
    try:
        totalBytes = binaryReader.readUInt()
        amntUniqueChar = binaryReader.readUShort()
    # If no header information
    except ValueError:
        print("Empty file, nothing to decompress")
        return 1

    # Reading key data and creating key that maps binary code to character
    keyDict = _readKey(binaryReader, amntUniqueChar)

    # Reading data using the key and writing data to output file
    data = _readData(binaryReader, keyDict, totalBytes)
    _writeData(data, destinationFile)

    return ""

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

    # Decompress file to output file
    decompress(fileToDecompress, decompressedFile)

    return 0

# ----------------------------------------------------------------------

if __name__ == '__main__':
    main()
