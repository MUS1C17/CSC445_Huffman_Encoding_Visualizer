import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit, QVBoxLayout, QWidget, QPushButton

class MainWindow(QMainWindow):
    '''This is a MainWindow class for front end.
    It will have all interactions with front end'''

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Huffman Encoding Visualizer")
        self.setGeometry(600, 300, 900, 700)

        # Create a central widget and a layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # Create a text box and add it to the layout
        textBox = QTextEdit()
        textBox.setPlaceholderText("Enter your text here:")
        textBox.setFixedSize(300, 100)
        layout.addWidget(textBox)

        #Create Button
        decodeButton = QPushButton("Decode")
        decodeButton.setFixedSize(50, 20)
        layout.addWidget(decodeButton)
        # Set the central widget for the main window
        self.setCentralWidget(central_widget)

def main():
    mainApp = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(mainApp.exec_())


if __name__ == "__main__":
    main()