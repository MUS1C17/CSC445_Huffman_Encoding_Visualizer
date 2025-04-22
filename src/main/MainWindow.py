import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QFont
from TextBox import TextBox
from Button import Button
from HuffmanTableGenerator import *
from LinkedBinaryTree import *
from PyQt5.QtWidgets import QSizePolicy

class MainWindow(QMainWindow):
    '''This is a MainWindow class for front end.
    It will have all interactions with front end'''

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Huffman Encoding Visualizer")
        self.setGeometry(600, 300, 900, 700)
        self.setStyleSheet("background-color: #8FCB9B;")

        # Create a central widget and a layout
        self.centralWidget= QWidget()
        self.mainPanel = QVBoxLayout(self.centralWidget)
        self.topHorizontalPanel = QHBoxLayout()
        self.bottomHorizontalPanel = QHBoxLayout()
        
        # Create a text box and add it to the layout
        self.textBox = TextBox()
        self.textBox.setPlaceholderText("Enter your text here:")
        self.textBox.setFixedSize(500, 200)
        self.topHorizontalPanel.addWidget(self.textBox)

        #Create Button
        self.decodeButton = Button("Decode")
        self.topHorizontalPanel.addWidget(self.decodeButton)
        self.decodeButton.clicked.connect(self.generateHuffmanTableWidget)
        # Set the central widget for the main window

        self.mainPanel.addLayout(self.topHorizontalPanel)
        self.mainPanel.addLayout(self.bottomHorizontalPanel)
        
        self.setCentralWidget(self.centralWidget)

    def generateHuffmanTableWidget(self):
        self.huffmanTableGenerator = HuffmanTableGenerator()

        self.huffmanTableWidget = QTableWidget()

        #Create columns and name them accordingly
        self.huffmanTableWidget.setColumnCount(3)
        self.huffmanTableWidget.setHorizontalHeaderLabels(["Charcter", "Frequency", "Code"])
        self.huffmanTableWidget.setRowCount(len(dict.values(self.huffmanTableGenerator.createDictionary(self.textBox.toPlainText()))))

        #Hide vertical headers
        self.huffmanTableWidget.verticalHeader().hide()

         # 1) shrink columns to fit headers & data
        header = self.huffmanTableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        
        # 2) let the table itself only take as much space as needed
        self.huffmanTableWidget.setSizePolicy(
            QSizePolicy.Minimum,
            QSizePolicy.Preferred
        )

        self.bottomHorizontalPanel.addWidget(self.huffmanTableWidget)
        self.decodeButton.setEnabled(False)

        self.fillHuffmanTableWidgetWithData()
        
        self.bottomHorizontalPanel.addWidget(self.createTreeEncodingWidget())

    def fillHuffmanTableWidgetWithData(self):
        characterData = self.huffmanTableGenerator.getListOfCharacters()
        frequencyData = self.huffmanTableGenerator.getListOfFrequencies()
        for rowNumber in range(len(characterData)):
            self.huffmanTableWidget.setItem(rowNumber, 0, QTableWidgetItem(f"{characterData[rowNumber]}"))
            self.huffmanTableWidget.setItem(rowNumber, 1, QTableWidgetItem(f"{frequencyData[rowNumber]}"))
        
        #root = self.huffmanTableGenerator.updatePriorityQueue(self.huffmanTableGenerator.createPriorityQueue(self.huffmanTableGenerator.getCharacterAndFrequencyDictionary()))
        #tree_widget = create_tree_widget(root, width=400, height=400)
        #self.bottomHorizontalPanel.addWidget(tree_widget)

    def createTreeEncodingWidget(self) -> QWidget:
        priorityQueue = self.huffmanTableGenerator.createPriorityQueue(self.huffmanTableGenerator.getCharacterAndFrequencyDictionary())
        rootNode = self.huffmanTableGenerator.updatePriorityQueue(priorityQueue)
        treeWidget = create_tree_widget(rootNode, width=1000, height=1000)
        treeWidget.setMinimumSize(1000, 1000)
        treeWidget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        return treeWidget

def main():
    mainApp = QApplication(sys.argv)
    mainApp.setFont(QFont("Segoe UI", 12))
    window = MainWindow()
    window.show()
    sys.exit(mainApp.exec_())

if __name__ == "__main__":
    main()