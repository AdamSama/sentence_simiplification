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

def action(sent: str) -> str:
    if sent[-1] == '.':
        sent = sent[:-1]
    tree = next(parser.parse(parser.tokenize(sent)))
    tree = ParentedTree.convert(tree)
    res2 = set()
    res = []
    # tree.draw()
    for child in tree[0]:
        if child.label() == ',':
            del tree[child.treeposition()]
    # tree.draw()
    treelist = removecomplex(tree)
    # # for treee in treelist:
    # #     print(treee)
    
    for index, node in enumerate(treelist):
        # node.draw()
        lis = removeconjunction(node)
        for each in lis:
            # print(" ".join(each.leaves()))
            res.append(each)
    for i in res :
        string = " ".join(i.leaves())
        if string[-1] != '.':
            string += '.'
        if string[0].islower():
            string = string[0].upper() + string[1:]
        # print(string)
        res2.add(string)
    return res2

def removecomplex(tree: Tree) -> list:
    subtrees = list()
    for subtree in reversed(list(tree.subtrees())):
        hasNP = False
        if subtree.label() == 'SBAR':
            # subtree.draw()
            for index, children in enumerate(subtree):
                i = index
                if subtree.label() == 'SBAR' and children.label() == 'S':
                    for grandchildren in children:
                        if grandchildren.label() == 'NP':
                            ## this means that the subtree contains the 'NP'
                            hasNP = True
            ## Meaning that we don't have to take subject from other part of the sentence.
            if hasNP:
                subtrees.append(subtree[i])
                # print(' '.join(subtree[i].leaves()))
                del tree[subtree.treeposition()]
            else:
                # print('No NP')
                # print(" ".join(tree.leaves()))
                # print(" ".join(subtree.leaves()))
                # subtree.draw()
                if subtree.leaves()[0] in ['that', 'which']:
                    prevs = list()
                    for prev in list(tree.subtrees()):
                        if prev == subtree:
                            break
                        else:
                            if prev.label() == 'NP':
                                prevs.append(prev)
                    np = copy.deepcopy(prevs[-1])
                    newnode = copy.deepcopy(subtree)
                    newnode.insert(0, np)
                    subtrees.append(newnode)
                    del tree[subtree.treeposition()]
                else:
                    # tree.draw()
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
    # print(' '.join(tree.leaves()))
    subtrees.append(tree)
    # for subtree in subtrees:
    #     subtree.draw()
    return subtrees

def removeconjunction(tree: Tree) -> Tree:
    
    lis = helper(tree)
    return lis

# If we see a conjunction or , remove them by connecting all its sliblings to their grandparents.
def helper(temp: Tree) -> list:
    changed = False
    subtreelist = list()
    result = list()
    # tree.draw()
    tree = copy.deepcopy(temp)
    for subtree in list(list(tree.subtrees())):
        if subtree.label() == 'CC' or subtree.label() == ',':
            parent = subtree.parent()
            for children in parent:
                newnode = copy.deepcopy(tree)
                for subtree2 in list(list(newnode.subtrees())):
                    if subtree2 == subtree:
                        temp2 = subtree2
                        # temp2.parent().draw()
                        parent3 = temp2.parent()
                if children.label() != 'CC' and children.label() != ',':
                    toDelete = True
                    while toDelete:
                        for otherchildren in parent3:
                            # parent3.draw()
                            if children != otherchildren:
                                del newnode[otherchildren.treeposition()]
                                # newnode.draw()
                                break
                        # parent3.draw()
                        if len(parent3) == 1:
                            toDelete = False
                    subtreelist.append(newnode)
                    # newnode.draw()
            changed = True
            break
    if changed:
        # tree.draw()
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
    # print(sentences)
    return sentences
# run("When I'm on the courts or on the court playing, I'm a competitor and I want to beat every single person whether they're in the locker room or across the net.")
