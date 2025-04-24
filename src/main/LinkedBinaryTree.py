from BinaryNode import *
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter
import sys
from HuffmanTableGenerator import *
import math

class TreeWidget(QWidget):
    '''Draws a binary tree using the leaf-based tidy layout.'''
    H_SPACING = 80   # horizontal pixels per unit x
    V_SPACING = 100  # vertical pixels per unit y
    RADIUS = 15      # node circle radius

    def __init__(self, root: BinaryNode):
        super().__init__()
        self.root = layout(root)
        max_x = self._max_x(self.root)
        max_y = self._max_y(self.root)
        self.setMinimumSize(int(max_x * self.H_SPACING + 2*self.RADIUS),
                            int(max_y * self.V_SPACING + 2*self.RADIUS))

    def _max_x(self, node):
        xs = [node.x]
        for c in node.children:
            xs.append(self._max_x(c))
        return max(xs)

    def _max_y(self, node):
        ys = [node.y]
        for c in node.children:
            ys.append(self._max_y(c))
        return max(ys)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self._draw(self.root, painter)

    def _draw(self, node, painter):
        px = int(node.x * self.H_SPACING + self.RADIUS)
        py = int(node.y * self.V_SPACING + self.RADIUS)
        for c in node.children:
            cx = int(c.x * self.H_SPACING + self.RADIUS)
            cy = int(c.y * self.V_SPACING + self.RADIUS)
            painter.drawLine(px, py, cx, cy)
            # label 0/1 offset off the line
            label = '0' if c is node.leftNode else '1'
            mx, my = (px+cx)/2, (py+cy)/2
            dx, dy = cx-px, cy-py
            length = math.hypot(dx, dy)
            if length == 0:
                ux, uy = 0, -1
            else:
                ux, uy = -dy/length, dx/length
            offset = self.RADIUS
            lx = mx + ux * offset
            ly = my + uy * offset
            painter.drawText(int(lx), int(ly), label)
            self._draw(c, painter)
        painter.drawEllipse(px - self.RADIUS, py - self.RADIUS,
                            2 * self.RADIUS, 2 * self.RADIUS)
        painter.drawText(px - self.RADIUS//2, py + self.RADIUS//2,
                         str(node.value))


def create_tree_widget(root: BinaryNode, width: int = 800, height: int = 600) -> TreeWidget:
    '''Return a configured TreeWidget for embedding in other layouts.'''
    widget = TreeWidget(root)
    widget.resize(width, height)
    return widget


def show_tree(root: BinaryNode, width: int = 800, height: int = 600):
    '''Standalone display: opens a window and draws the tree.'''
    app = QApplication(sys.argv)
    widget = create_tree_widget(root, width, height)
    widget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    # Example usage
    nodes = [BinaryNode(str(i)) for i in range(1, 51)]
    for i, n in enumerate(nodes):
        l, r = 2*i + 1, 2*i + 2
        if l < len(nodes): n.setLeft(nodes[l])
        if r < len(nodes): n.setRight(nodes[r])
    show_tree(nodes[0], width=1600, height=1000)
