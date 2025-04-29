from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QPixmap, QPainter, QCursor, QColor,QPen
from PyQt5.QtCore import Qt, QEvent, QTimer
class TextBox(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("""
                QTextEdit { 
                           border: 2px solid;
                           border-color: #12130F;
                            border-radius: 15px;
                            background: #7A9CC6; 
                            padding: 0px;             
                            margin: 0px;
                           }
                QTextEdit::viewport {
                           border-radius: 15px;
                            background-color: white;
                            margin: 0px;
                           }
            """)
        self.default_cursor = self.cursor()
        self.custom_mouse_cursor = self.create_custom_text_ibeam_cursor()
        self.viewport().installEventFilter(self)
        self.custom_cursor_color = QColor("#12130F")
        self.setCursorWidth(0)
        self.cursor_visible = True
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.blink_cursor)
        self.blink_timer.start(500)

    def create_custom_text_ibeam_cursor(self):
        size = 16 
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor("#12130F"), 2)
        painter.setPen(pen)
        painter.drawLine(size // 2, 0, size // 2, size)
        painter.end()
        return QCursor(pixmap, size // 2, 0)
    
    def eventFilter(self, obj, event):
        if obj is self.viewport():
            if event.type() == QEvent.Enter:
                self.viewport().setCursor(self.custom_mouse_cursor)
            elif event.type() == QEvent.Leave:
                self.viewport().setCursor(self.default_cursor)
        return super().eventFilter(obj, event)
    
    def blink_cursor(self):
        self.cursor_visible = not self.cursor_visible
        self.viewport().update()
    
    def paintEvent(self, event):
        super().paintEvent(event)
        if self.hasFocus() and self.cursor_visible:
            painter = QPainter(self.viewport())
            painter.setPen(self.custom_cursor_color)
            rect = self.cursorRect()
            painter.drawLine(rect.x(), rect.top(), rect.x(), rect.bottom())