from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtCore import Qt

from BinaryNode import *
from LinkedBinaryTree import *

class ScrollableTreeWidget(QScrollArea):
    '''A scrollable container for TreeWidget.'''
    def __init__(self, root: BinaryNode, parent=None):
        super().__init__(parent)
        tree = TreeWidget(root)
        self.setWidget(tree)
        self.setWidgetResizable(False)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

def create_scrollable_tree(root: BinaryNode) -> ScrollableTreeWidget:
    '''Return a scrollable tree widget for embedding.'''
    return ScrollableTreeWidget(root)