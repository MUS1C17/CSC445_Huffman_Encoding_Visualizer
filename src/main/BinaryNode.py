
class BinaryNode:
    '''
    This is BinaryNode class that represents each node in a tree
    '''
    def __init__(self, value, frequency=0):
        '''Constructor that takes in a value that will be stored in the node. 
        Right and left nodes will be none by default so setter methods can be called'''
        self.value = value
        self.frequency = frequency
        self.leftNode = None
        self.rightNode = None

        self.x = 0
        self.y = 0
        self.mod = 0


    def __lt__(self, comparedValue):
        '''This method is used to get rid of the TypeError'''
        return self.value < comparedValue.value
    
    @property
    def children(self):
        # return non-null children in order
        return [c for c in (self.leftNode, self.rightNode) if c]
        
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
    

    # Layout functions following the layout(tree)->addmods(setup(tree)) pattern
def compute_leaves(tree):
    '''Annotate each node with the count of leaves in its subtree.'''
    if not tree.children:
        tree._leaf_count = 1
    else:
        tree._leaf_count = sum(compute_leaves(c) for c in tree.children)
    return tree._leaf_count


def assign_positions(tree, depth=0, next_x=0):
    '''Two-pass position assignment:
       - Leaves get successive x-coordinates (unit spacing).
       - Internal nodes get x = midpoint of first & last child.
       - All nodes get y = depth.
       Returns the next available x index after this subtree.'''
    tree.y = depth
    if not tree.children:
        tree.x = next_x
        return next_x + 1

    current = next_x
    for c in tree.children:
        current = assign_positions(c, depth + 1, current)
    first = tree.children[0].x
    last = tree.children[-1].x
    tree.x = (first + last) / 2
    return current


def layout(tree):
    '''Compute leaf counts, assign x/y positions.'''    
    compute_leaves(tree)
    assign_positions(tree)
    return tree
    