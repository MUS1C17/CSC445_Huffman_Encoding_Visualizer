'''
 This is BinaryNode class that represents each node in a tree
'''
class BinaryNode:

    def __init__(self, value):
        '''Constructor that takes in a value that will be stored in the node. 
        Right and left nodes will be none by default so setter methods can be called'''
        self.value = value
        self.leftNode = None
        self.rightNode = None
        
    def getValue(self):
        '''Returns current value that is stored in the Node'''
        return self.value
    
    def getLeft(self):
        '''Returns left node'''
        return self.leftNode
    
    def getRight(self):
        '''Returns right node'''
        return self.rightNode
    
    def setLeft(self, leftNode):
        '''Setter for a left Node'''
        self.leftNode = leftNode

    def setLeft(self, rightNode):
        '''Setter for the right node'''
        self.rightNode = rightNode
    

    