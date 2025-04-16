
class BinaryNode:
    '''
    This is BinaryNode class that represents each node in a tree
    '''
    def __init__(self, value):
        '''Constructor that takes in a value that will be stored in the node. 
        Right and left nodes will be none by default so setter methods can be called'''
        self.value = value
        self.leftNode = None
        self.rightNode = None

    def __lt__(self, comparedValue):
        '''This method is used to get rid of the TypeError'''
        return self.value < comparedValue.value
        
    def __str__(self):
        return f"Value: {self.getValue()}\n Right Node: {self.getRight()}\n Left Node: {self.getRight()}"
        
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

    def setRight(self, rightNode):
        '''Setter for the right node'''
        self.rightNode = rightNode
    

    