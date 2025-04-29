from PyQt5.QtWidgets import QLineEdit

class LineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaximumWidth(700)
        self.setStyleSheet("""
            QLineEdit {
                border: 2px solid #12130F;    
                border-radius: 10px;      
                background-color: #7A9CC6;   
                padding: 5px;     
            }
            QLineEdit:focus {
                border: 2px solid #4A90E2;
            }
        """)