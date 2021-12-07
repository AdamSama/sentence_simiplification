from typing import Tuple
import nltk
from nltk.corpus import treebank
from nltk.parse import CoreNLPParser
from nltk.tree import Tree, ParentedTree
import re
import copy
parser = CoreNLPParser(url='http://localhost:9000')
FILE_PATH = '../data/data1/PWKP_108016'

'''
This page provides utility functions that breaks down a complex sentences into multiple simpler ones.
'''

def action(original: str) -> str:
    if original[-1] == '.':
        original = original[:-1]
    tree = next(parser.parse(parser.tokenize(original)))
    tree = ParentedTree.convert(tree)
    res2 = list()
    res = list()
    for child in tree[0]:
        if child.label() == ',':
            del tree[child.treeposition()]
    treelist = removecomplex(tree)
    for index, node in enumerate(treelist):
        # node.draw()
        lis = removeconjunction(node)
        for each in lis:
            # each.draw()
            res.append(each)
    for i in res:
        string = " ".join(i.leaves())
        if string[-1] != '.':
            string += '.'
        if string[0].islower():
            string = string[0].upper() + string[1:]
        print(string)
        res2.append(res2)
    return res2

def removecomplex(tree: Tree) -> list:
    subtrees = list()
    for subtree in reversed(list(tree.subtrees())):
        hasNP = False
        if subtree.label() == 'SBAR':
            subtree.draw()
            for index, children in enumerate(subtree):
                i = index
                if subtree.label() == 'SBAR' and children.label() == 'S':
                    for grandchildren in children:
                        if grandchildren.label() == 'NP':
                            ## this means that the subtree contains the 'NP'
                            hasNP = True
            ## Meaning that we don't have to take subject from other part of the sentence.
            if hasNP:
                # if subtree[i][0].label() == ',':
                #     subtree[i].draw()
                #     del subtree[i][subtree[i][0].treeposition]
                subtrees.append(subtree[i])

                del tree[subtree.treeposition()]
            else:
                for index, node in enumerate(subtree.parent()):
                    if node.label() == 'NP':
                        tree1 = node
                    elif node.label() == 'VP':
                        for subindex, subnode in enumerate(node):
                            if subnode.label()[:2] == 'VB':
                                tree2 = subnode
                treetemp1 = copy.deepcopy(tree2)
                treetemp2 = copy.deepcopy(tree1)
                del tree[subtree[0].treeposition()]
                subtree.insert(0, treetemp1)
                subtree.insert(0, treetemp2)
                subtrees.append(subtree)
                del tree[subtree.treeposition()]

    # if tree[0].label() == ',':
    #     del tree[tree[0].treeposition]
    subtrees.append(tree)
    for subtree in subtrees:
        subtree.draw()
    return subtrees

def removeconjunction(tree: Tree) -> Tree:
    
    lis = helper(tree)
    return lis

# If we see a conjunction or , remove them by connecting all its sliblings to their grandparents.
def helper(tree: Tree) -> list:
    changed = False
    subtreelist = list()
    result = list()
    # tree.draw()
    for subtree in list(list(tree.subtrees())):
        if subtree.label() == 'CC' or subtree.label() == ',':
            # print(subtree.label())
            parent = subtree.parent()
            grandparent = parent.parent()
            grandposition = grandparent.treeposition()
            # print(grandparent.label())
            for children in parent:
                newnode = copy.deepcopy(tree)
                if children.label() != 'CC' and children.label() != ',':
                    newnode[grandposition].insert(len(grandparent), copy.deepcopy(children))
                    # print(children.label())
                    del newnode[children.treeposition()]
                    del newnode[parent.treeposition()]
                    subtreelist.append(newnode)
                    # newnode.draw()
            changed = True
            break
    if changed:
        tree.draw()
        for each in subtreelist:
            newlist = helper(each)
            if len(newlist) != 0:
                for node in newlist:
                    result.append(node)
        return result
    else:
        return [tree]

def run(sen: str) -> None:
    # file = File(FILE_PATH, True)
    sentences = action(sen)
    return sentences