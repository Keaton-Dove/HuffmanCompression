#!/usr/bin/env python3

# ----------------------------------------------------------------------
# compress.py
# Dave Reed
# 05/21/2021
# ----------------------------------------------------------------------

from __future__ import annotations
from typing import Optional, Dict, Tuple
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
    root = BinaryTreeNode((None, total), lTree, rTree)
    tree = BinaryTree(root)
    return tree

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

def createTree(priorityQueue) -> BinaryTree:

    # Initializing local variables
    tree = None
    subtrees = []

    # Creating subtrees as long as there are at least 2 items in queue
    while len(priorityQueue) > 1:

        # Creating subtree, appending to subtree array and deleting frequencies from priorityQueue
        subtree = _createSubtree(priorityQueue[:2])
        subtrees.append(subtree)
        priorityQueue = priorityQueue[2:]

        # If there are two subtrees, combine them
        if len(subtrees) == 2:
            newSubtree = _combineSubtrees(subtrees[0], subtrees[1])
            # If the new tree is bigger, it is combined with the whole tree.
            if tree is None or newSubtree.getSize() > tree.getSize():
                tree = _combineSubtrees(tree, newSubtree)
                subtrees = []
            else:
                subtrees = [newSubtree]

    # If there is a leftover single subtree, it is appended respectively
    if len(subtrees) == 1:
        if subtrees[0].getSize() < tree.getSize():
            tree = _combineSubtrees(subtrees[0], tree)
        else:
            tree = _combineSubtrees(tree, subtrees[0])

    # If there is a leftover single node, combine accordingly
    if len(priorityQueue) == 1:
        lastNodeTree = BinaryTree(BinaryTreeNode(priorityQueue[0]))
        if lastNodeTree.getSize() < tree.getSize():
            tree = _combineSubtrees(lastNodeTree, tree)
        else:
            tree = _combineSubtrees(tree, lastNodeTree)

    return tree

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

    # Reading frequencies from file
    data: str = readData(fileToCompress)
    frequencies: Dict[str, int] = readFrequencies(data)

    # Ordering frequencies as a priority queue and creating a BinaryTree from frequencies
    priorityQueue = sorted(frequencies.items(), key=lambda x: x[1])
    tree = createTree(priorityQueue)

# ----------------------------------------------------------------------

if __name__ == '__main__':
    main()
