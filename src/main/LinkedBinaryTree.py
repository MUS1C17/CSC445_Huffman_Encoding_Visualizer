from BinaryNode import *
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import Qt
import sys
from HuffmanTableGenerator import *
import math

class TreeWidget(QWidget):
    '''Draws a binary tree using the leaf-based tidy layout.'''
    H_SPACING = 80   # horizontal pixels per unit x
    V_SPACING = 100  # vertical pixels per unit y
    RADIUS = 20      # node circle radius

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
        # compute center of this node
        px = node.x * self.H_SPACING + self.RADIUS
        py = node.y * self.V_SPACING + self.RADIUS

        # draw edges to children
        for c in node.children:
            cx = c.x * self.H_SPACING + self.RADIUS
            cy = c.y * self.V_SPACING + self.RADIUS

            dx = cx - px
            dy = cy - py
            dist = math.hypot(dx, dy)
            if dist == 0:
                ux, uy = 0, 0
            else:
                ux, uy = dx / dist, dy / dist

            # offset start/end by circle radius
            start_x = px + ux * self.RADIUS
            start_y = py + uy * self.RADIUS
            end_x   = cx - ux * self.RADIUS
            end_y   = cy - uy * self.RADIUS

            painter.drawLine(
                int(start_x), int(start_y),
                int(end_x),   int(end_y)
            )

            # draw 0/1 label centered on the line
            label = '0' if c is node.leftNode else '1'
            mx, my = (start_x + end_x) / 2, (start_y + end_y) / 2
            # perpendicular unit vector
            perp_x, perp_y = -uy, ux
            # offset away from line
            ox = perp_x * (self.RADIUS / 2)
            oy = perp_y * (self.RADIUS / 2)
            tx = mx + ox
            ty = my + oy
            # measure text size
            fm = painter.fontMetrics()
            w = fm.horizontalAdvance(label)
            h = fm.height()
            # draw centered
            painter.drawText(
                int(tx - w/2),
                int(ty + h/4),
                label
            )

            # recurse
            self._draw(c, painter)

        painter.setBrush(QBrush(QColor("#7A9CC6")))

        # (optionally) ensure your outline stays a contrasting color:
        painter.setPen(QColor("#000000"))

        # draw node circle
        painter.drawEllipse(
            int(px - self.RADIUS), int(py - self.RADIUS),
            2 * self.RADIUS, 2 * self.RADIUS
        )

        painter.setBrush(Qt.NoBrush)

        # draw node value centered
        val = str(node.value)
        fm = painter.fontMetrics()
        w = fm.horizontalAdvance(val)
        h = fm.height()
        painter.drawText(
            int(px - w/2),
            int(py + h/4),
            val
        )


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
