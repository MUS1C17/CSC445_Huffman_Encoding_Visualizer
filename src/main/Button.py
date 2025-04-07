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

        '''TODO: For some reason it is very difficult to make a button round
        so this is a note to finish it later here:'''
        self.setStyleSheet("""
                QPushButton{
                           border: 2px solid;
                           border-color: #12130F;
                           border-radius 25px;
                           background: #5B9279;
                           }
                            """)
        self.clicked.connect(self.animateButton)

    '''def animateButton(self):
         # Save the button's current geometry (if not already saved).
        if self.original_geom is None:
            self.original_geom = self.geometry()

        original_geom = self.geometry()
        shrink_factor = 0.9
        new_width = int(original_geom.width() * shrink_factor)
        new_height = int(original_geom.height() * shrink_factor)
        delta_w = (original_geom.width() - new_width) // 2
        delta_h = (original_geom.height() - new_height) // 2
        
        # Create a smaller geometry centered on the original.
        smaller_geom = QRect(
            original_geom.x() + delta_w,
            original_geom.y() + delta_h,
            new_width,
            new_height
        )
        
        # Animate geometry from original to smaller and back.
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(150)  # duration in milliseconds
        self.anim.setStartValue(original_geom)
        self.anim.setKeyValueAt(0.5, smaller_geom)
        self.anim.setEndValue(original_geom)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.anim.start()'''
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.setGraphicsEffect(self.shadow)
        self.tm = QtCore.QBasicTimer()
        self.shadow.setOffset(0, 0)
        self.shadow.setBlurRadius(20)
        self.shadow.setColor(QtGui.QColor("#3F3F3F"))
        self.mouse = ''
        
        self.changeColor(color="lightgrey")

        #button shadow grading.
        self.expand = 0
        self.maxExpand = 4 # expanding size - #optional
        self.init_s_color = "#3F3F3F" #optional
        self.end_s_color = "#FFFF33"  #optional
        self.garding_s_seq = self.gradeColor(c1=self.init_s_color, 
									        c2=self.end_s_color, 
									        steps=self.maxExpand)
        #button color grading.
        self.grade = 0
        self.maxGrade=15 # gradding size - #optional
        self.init_bg_color = "lightgrey"   #optional
        self.end_bg_color = "darkgrey"     #optional
        self.gradding_bg_seq = self.gradeColor( c1=self.init_bg_color, 
									        	c2=self.end_bg_color, 
									        	steps=self.maxGrade)

    def changeColor(self, color=(255,255,255)):
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor(color))
        self.setPalette(palette)

    def gradeColor(self, c1, c2, steps):
        return list([str(i) for i in Color(c1).range_to(Color(c2), steps)])

    def enterEvent(self, e) -> None:
        self.mouse = 'on'
        #self.setGraphicsEffect(self.shadow)
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
