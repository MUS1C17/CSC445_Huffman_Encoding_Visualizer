from PyQt5.QtWidgets import QPushButton
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QRegion
from PyQt5.QtCore import QPropertyAnimation, QPoint, QEasingCurve, QRect
from colour import Color 

class Button(QPushButton):
    '''Button class to have custom buttons with our own settings. 
    This class inherits from QPushButton'''
    def __init__(self, parent=None):
        super().__init__(parent)

        self.original_geom = None
        self.shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.setGraphicsEffect(self.shadow)
        self.tm = QtCore.QBasicTimer()
        self.shadow.setOffset(0, 0)
        self.shadow.setBlurRadius(20)
        self.shadow.setColor(QtGui.QColor("#3F3F3F"))
        self.mouse = ''
        
        self.changeColor(color="lightgrey")

        self.expand = 0
        self.maxExpand = 4 
        self.init_s_color = "#3F3F3F" 
        self.end_s_color = "#FFFF33"
        self.garding_s_seq = self.gradeColor(c1=self.init_s_color, 
									        c2=self.end_s_color, 
									        steps=self.maxExpand)

        self.grade = 0
        self.maxGrade=15 
        self.init_bg_color = "lightgrey"   
        self.end_bg_color = "darkgrey"    
        self.gradding_bg_seq = self.gradeColor( c1=self.init_bg_color, 
									        	c2=self.end_bg_color, 
									        	steps=self.maxGrade)
        self.setStyleSheet("""
            QPushButton {
                border: 2px solid #12130F;
                border-radius: 15px;
                background-color: #7A9CC6;
                color: black;
                padding: 8px 4px;
            }
            QPushButton:hover {
                background-color: #3A79C0;
            }
            QPushButton:pressed {
                background-color: #1E4F83;
            }
        """)

    def changeColor(self, color=(255,255,255)):
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor(color))
        self.setPalette(palette)

    def gradeColor(self, c1, c2, steps):
        return list([str(i) for i in Color(c1).range_to(Color(c2), steps)])

    def enterEvent(self, e) -> None:
        self.mouse = 'on'
        self.tm.start(15, self)

    def leaveEvent(self, e) -> None:
        self.mouse = 'off'

    def timerEvent(self, e) -> None:
        
        if self.mouse == 'on' and self.grade < self.maxGrade:
            self.grade += 1
            self.changeColor(color=self.gradding_bg_seq[self.grade-1])
        
        elif self.mouse == 'off' and self.grade > 0:
            self.changeColor(color=self.gradding_bg_seq[self.grade-1])
            self.grade -= 1

        if self.mouse == 'on' and self.expand < self.maxExpand:
            self.expand += 1
            self.shadow.setColor(QtGui.QColor(self.garding_s_seq[self.expand-1]))
            self.setGeometry(self.x()-1, int(self.y()-1), self.width()+2, self.height()+2)
        
        elif self.mouse == 'off' and  self.expand > 0:
            self.expand -= 1
            self.setGeometry(self.x()+1, int(self.y()+1), self.width()-2, self.height()-2)
        
        elif self.mouse == 'off' and self.expand in [0, self.maxExpand] and self.grade in [0, self.maxGrade]:
            self.shadow.setColor(QtGui.QColor(self.init_s_color))
            self.tm.stop()
