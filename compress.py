#!/usr/bin/env python3

# ----------------------------------------------------------------------
# compress.py
# Dave Reed
# 05/21/2021

# Keaton Dove
# 12/2/2021
# CS-361

# ----------------------------------------------------------------------

from __future__ import annotations
from typing import Optional, Dict, Tuple, List
from argparse import ArgumentParser

from BinaryFileIO import BinaryFileWriter

# ----------------------------------------------------------------------
class BinaryTree:

    def __init__(self, head: BinaryTreeNode):
        self.head = head

    def getHead(self):
        return self.head

    def getSize(self):
        return self.head.getSize()

class BinaryTreeNode:
    """
    Basic binary tree node class for storing information.
    This class only serves to be a data structure with no additional functionality.
    """

    def __init__(self, data: tuple[str, int], left=None, right=None):
        self.left = left
        self.right = right
        self.data = data

    """  GETTERS  """
    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def getData(self):
        return self.data

    def getSize(self):
        return self.data[1]

    """ SETTERS  """
    def setRight(self, node: BinaryTreeNode):
        self.right = node

    def setLeft(self, node: BinaryTreeNode):
        self.left = node

# ----------------------------------------------------------------------

def _createSubtree(items) -> BinaryTree:

    # Creating BinaryTreeNodes for the frequencies in items
    nodes = []
    total = 0
    for i in items:
        node = BinaryTreeNode(i)
        total += node.getSize()
        nodes.append(node)

    # Creating a root node and a tree with that root
    root = BinaryTreeNode((None, total), nodes[0], nodes[1])
    tree = BinaryTree(root)
    return tree

def _combineSubtrees(lTree: BinaryTree, rTree: BinaryTree) -> BinaryTree:

    # Edge case for the combining the first subtree
    if lTree is None:
        return rTree

    # Creating a new root for the tree and attaching the trees as children of the root
    total = lTree.getSize() + rTree.getSize()
    root = BinaryTreeNode((None, total), lTree.getHead(), rTree.getHead())
    tree = BinaryTree(root)
    return tree

def _generateKeys(node: BinaryTreeNode, bitCode: str = "") -> List[Tuple]:
    # Recursive post order traversal of binary tree
    keys = []

    if node.getLeft():
        # Searching left subtree, add 0 to bitCode
        keys += _generateKeys(node.getLeft(), bitCode + "0")
    if node.getRight():
        # Searching right subtree, add 1 to binary code
        keys += _generateKeys(node.getRight(), bitCode + "1")

    nodeData = node.getData()
    # If the node isn't a filler node, the character node's data is stored in the key
    if nodeData[0] is not None:
        keys.append((nodeData[0], len(bitCode), bitCode))

    return keys

def readData(sourceFile) -> str:

    infile = open(sourceFile, "r")
    fileContents = ""

    # Accumulating all lines in file to a string
    line = infile.readline()
    while line:
        fileContents += line
        line = infile.readline()

    infile.close()

    return fileContents

def readFrequencies(data: str) -> Dict[str, int]:

    frequencies = {}

    for i in range(len(data)):
        char = data[i]

        # Checking dictionary for character
        if char in frequencies:
            # Increment character frequency
            frequencies[char] += 1
        else:
            # Initialize character frequency
            frequencies[char] = 1

    return frequencies

def createTree(priorityQueue) -> BinaryTree:

    # Initializing local variables
    tree = None
    subtrees = []

    # Creating subtrees as long as there are at least 2 items in queue
    while len(priorityQueue) > 1:

        # Creating subtree, appending to subtree array and deleting used frequencies from priorityQueue
        subtree = _createSubtree(priorityQueue[:2])
        subtrees.append(subtree)
        priorityQueue = priorityQueue[2:]

        # If there are two subtrees, combine them
        if len(subtrees) == 2:
            newSubtree = _combineSubtrees(subtrees[0], subtrees[1])

            # If the new tree has a bigger size, it is combined with the whole tree.
            if tree is None or newSubtree.getSize() > tree.getSize():
                tree = _combineSubtrees(tree, newSubtree)
                subtrees = []
            else:
                # Otherwise it stays in the subtrees array
                subtrees = [newSubtree]

    # If there is a leftover single subtree, combine accordingly
    if len(subtrees) == 1:
        if subtrees[0].getSize() < tree.getSize():
            tree = _combineSubtrees(subtrees[0], tree)
        else:
            tree = _combineSubtrees(tree, subtrees[0])

    # If there is a leftover single node, it is appended accordingly
    if len(priorityQueue) == 1:
        lastNodeTree = BinaryTree(BinaryTreeNode(priorityQueue[0]))
        if lastNodeTree.getSize() < tree.getSize():
            tree = _combineSubtrees(lastNodeTree, tree)
        else:
            tree = _combineSubtrees(tree, lastNodeTree)

    return tree

def createKey(tree: BinaryTree) -> List[Tuple]:

    # Creating key from tree and inserting header into keys
    keys = _generateKeys(tree.getHead())
    header = (tree.getSize(), len(keys))
    keys.insert(0, header)

    return keys

def compress(data: str, key: List[Tuple], compressedFile: str):

    bitWriter = BinaryFileWriter(compressedFile)

    # Writing only the header
    bitWriter.writeUInt(key[0][0])
    bitWriter.writeUShort(key[0][1])

    keyDict = {}
    # Writing key data
    for i in range(1, len(key)):

        # (Character, bitCode length, bitCode) for given char
        charData = key[i]

        # Switching list of keys to dictionary mapping chars to binary code for writing input data
        keyDict[charData[0]] = charData[2]

        # Writing character ascii value and amount
        bitWriter.writeUByte(ord(charData[0]))
        bitWriter.writeUShort(charData[1])

        # Writing individual bits for character code
        for num in charData[2]:
            bitWriter.writeBit(int(num))

    # Writing data
    for char in data:
        for num in keyDict[char]:
            bitWriter.writeBit(int(num))

    bitWriter.close()

def main():
    parser = ArgumentParser(description="compress file using Huffman compression algorithm")
    parser.add_argument("file", help="file to compress")
    parser.add_argument("compressedFile", nargs="?", default=None, help="name of compressed file to create; defaults to adding .hc suffix if not supplied")
    args = parser.parse_args()

    fileToCompress = args.file
    compressedFile = args.compressedFile
    if compressedFile is None:
        compressedFile = fileToCompress + ".hc"

    # Reading data from file
    data: str = readData(fileToCompress)

    # If there is no data, cannot perform compression
    if data == "":
        print("Empty file, nothing to compress")
        return 1

    # Determining frequencies of characters in data
    frequencies: Dict[str, int] = readFrequencies(data)

    # Ordering frequencies as a priority queue and creating a sorted binary tree for the characters
    priorityQueue = sorted(frequencies.items(), key=lambda x: x[1])
    tree: BinaryTree = createTree(priorityQueue)

    # Creating a key from the traversal of the binary tree
    key = createKey(tree)
    # Using key to compress file
    compress(data, key, compressedFile)

    return 0
# ----------------------------------------------------------------------

if __name__ == '__main__':
    main()
