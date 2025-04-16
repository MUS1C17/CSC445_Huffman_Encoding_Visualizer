
class LinkedBinaryTree:
    def __init__(self, root):
        '''Constructor that takes root of the tree (BinaryNode).
        Size variable shows number of nodes in the tree.
        Size is being set to 1 originally because tree will always have a root'''
        self.root = root
        self.size = 1

    def getRoot(self):
        '''Method to get the root of the tree'''
        return self.root
    
    def getSize(self):
        '''Method to get size of the tree'''
        return self.size
    
    def isEmpty(self):
        '''Method to check if tree is emtpy'''
        return self.size == 0    

    def drawTree(self):
        