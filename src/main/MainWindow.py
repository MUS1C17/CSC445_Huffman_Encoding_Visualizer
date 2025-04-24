import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QFileDialog, QMessageBox, QAbstractItemView
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtCore import Qt
from TextBox import TextBox
from Button import Button
from HuffmanTableGenerator import *
from LinkedBinaryTree import *
from PyQt5.QtWidgets import QSizePolicy
from ScrollableTreeWidget import *

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
        self.middleHorizontalPanel = QHBoxLayout()
        self.bottomHorizontalPanel = QHBoxLayout()
        
        # Create a text box and add it to the layout
        self.textBox = TextBox()
        self.textBox.setPlaceholderText("Enter your text here:")
        self.textBox.setFixedSize(700, 300)
        self.topHorizontalPanel.addWidget(self.textBox)

        #Create Button
        self.decodeButton = Button("Decode")
        self.topHorizontalPanel.addWidget(self.decodeButton)
        self.decodeButton.clicked.connect(lambda: self.generateHuffmanTableWidget(self.textBox.toPlainText()))
        # Set the central widget for the main window

        #Create File upload
        self.filePathLine = QLineEdit()
        self.filePathLine.setReadOnly(True)
        self.middleHorizontalPanel.addWidget(self.filePathLine)

        #Create Upload File button
        self.fileUploadButton = Button("Upload File And Decode")
        self.fileUploadButton.clicked.connect(self.uploadFile)
        self.middleHorizontalPanel.addWidget(self.fileUploadButton)


        self.mainPanel.addLayout(self.topHorizontalPanel)
        self.mainPanel.addLayout(self.middleHorizontalPanel)
        self.mainPanel.addLayout(self.bottomHorizontalPanel)
        
        self.setCentralWidget(self.centralWidget)

    def generateHuffmanTableWidget(self, text):
        self.clearBottomPanel()
        self.huffmanTableGenerator = HuffmanTableGenerator()

        freq_dict = self.huffmanTableGenerator.createDictionary(text)

        # Prepare data lists
        characters = list(freq_dict.keys())
        frequencies = list(freq_dict.values())
        rowCount = len(characters)

        self.huffmanTableWidget = QTableWidget(rowCount, 3)
        self.huffmanTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        #Create columns and name them accordingly
        self.huffmanTableWidget.setColumnCount(3)
        self.huffmanTableWidget.setHorizontalHeaderLabels(["Charcter", "Frequency", "Code"])
    
        #Hide vertical headers
        self.huffmanTableWidget.verticalHeader().hide()

         # Column sizing: char/freq auto, code fixed for 8 chars
        header = self.huffmanTableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        avg_char_w = self.huffmanTableWidget.fontMetrics().averageCharWidth()
        code_width = avg_char_w * 8 + 20
        header.resizeSection(2, int(code_width))

        # Size policy to hug contents
        self.huffmanTableWidget.setSizePolicy(
            QSizePolicy.Minimum, QSizePolicy.Preferred
        )

        self.bottomHorizontalPanel.addWidget(self.huffmanTableWidget)
        # Build tree and codes
        pq = self.huffmanTableGenerator.createPriorityQueue(freq_dict)
        root = self.huffmanTableGenerator.updatePriorityQueue(pq)
        codes = self.huffmanTableGenerator.generateCodeForCharacters(root)

        # Fill table rows
        for row, ch in enumerate(characters):
            self.huffmanTableWidget.setItem(
                row, 0, QTableWidgetItem(ch)
            )
            self.huffmanTableWidget.setItem(
                row, 1, QTableWidgetItem(str(frequencies[row]))
            )
            code = codes.get(ch, "")
            self.huffmanTableWidget.setItem(
                row, 2, QTableWidgetItem(code)
            )

        # Create and add tree widget
        scroll_tree = create_scrollable_tree(root)
        self.bottomHorizontalPanel.addWidget(scroll_tree)


    def fillHuffmanTableWidgetWithData(self):
        characterData = self.huffmanTableGenerator.getListOfCharacters()
        frequencyData = self.huffmanTableGenerator.getListOfFrequencies()
        for rowNumber in range(len(characterData)):
            self.huffmanTableWidget.setItem(rowNumber, 0, QTableWidgetItem(f"{characterData[rowNumber]}"))
            self.huffmanTableWidget.setItem(rowNumber, 1, QTableWidgetItem(f"{frequencyData[rowNumber]}"))

    def createTreeEncodingWidget(self) -> QWidget:
        priorityQueue = self.huffmanTableGenerator.createPriorityQueue(self.huffmanTableGenerator.getCharacterAndFrequencyDictionary())
        rootNode = self.huffmanTableGenerator.updatePriorityQueue(priorityQueue)
        codes = self.huffmanTableGenerator.generateCodeForCharacters(rootNode)
        treeWidget = create_tree_widget(rootNode, width=1000, height=1000)
        treeWidget.setMinimumSize(1000, 1000)
        treeWidget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        return treeWidget
    
    def uploadFile(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self,
            "Select a file to upload",
            "",
            "Text(*.txt)"
        )
        if filePath:
            self.filePathLine.setText(filePath)

            try:
                with open(filePath, 'r', encoding='utf-8') as f:
                    inputText = f.read()
            except Exception as e:
                # show an error, or fall back
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText(f"Error occured: {e}")
                msg.setWindowTitle("Error")  
                msg.exec_()       
            self.generateHuffmanTableWidget(inputText)
        else: 
            pass

    def clearBottomPanel(self):
        """Remove all widgets from the bottom panel."""
        # Take each item out of the layout and delete its widget
        layout = self.bottomHorizontalPanel
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                # this removes it from the GUI and schedules it for deletion
                widget.setParent(None)

def main():
    mainApp = QApplication(sys.argv)
    mainApp.setFont(QFont("Segoe UI", 12))
    window = MainWindow()
    window.show()
    sys.exit(mainApp.exec_())

if __name__ == "__main__":
    main()