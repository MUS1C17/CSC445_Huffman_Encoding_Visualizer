import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QFileDialog, QMessageBox, QAbstractItemView,  QPlainTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtCore import Qt
from TextBox import TextBox
from Button import Button
from HuffmanTableGenerator import *
from LinkedBinaryTree import *
from PyQt5.QtWidgets import QSizePolicy
from ScrollableTreeWidget import *
from Table import *
from PlainTextEdit import *
from LineEdit import *

class MainWindow(QMainWindow):
    '''This is a MainWindow class for front end.
    It will have all interactions with front end'''

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Huffman Encoding Visualizer")
        self.setGeometry(600, 300, 900, 700)
        self.setStyleSheet("background-color: #9FBBCC;")

        # Create a central widget and a layout
        self.centralWidget= QWidget()
        self.mainPanel = QVBoxLayout(self.centralWidget)
        self.topHorizontalPanel = QHBoxLayout()
        self.middleHorizontalPanel = QHBoxLayout()
        self.encodedPanel = QHBoxLayout()
        self.bottomHorizontalPanel = QHBoxLayout()
        
        # Create a text box and add it to the layout
        self.textBox = TextBox()
        self.textBox.setPlaceholderText("Enter your text here:")
        self.textBox.setMinimumHeight(300)
        self.textBox.setMaximumWidth(1500)
        self.topHorizontalPanel.addWidget(self.textBox)

        #Create Button
        self.decodeButton = Button("Decode")
        self.topHorizontalPanel.addWidget(self.decodeButton)
        self.decodeButton.clicked.connect(lambda: self.generateHuffmanTableWidget(self.textBox.toPlainText()))

        #Create File upload
        self.filePathLine = LineEdit()
        self.filePathLine.setReadOnly(True)
        self.middleHorizontalPanel.addWidget(self.filePathLine)

        #Create Upload File button
        self.fileUploadButton = Button("Upload File And Decode")
        self.fileUploadButton.clicked.connect(self.uploadFile)
        self.middleHorizontalPanel.addWidget(self.fileUploadButton)

        #Create QPlainTextEdit
        self.encodedTextBox = PlainTextEdit()
        self.encodedTextBox.setReadOnly(True)
        self.encodedTextBox.setPlaceholderText("Encoded bits will appear here…")
        self.encodedTextBox.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.encodedTextBox.setMinimumHeight(50)
        self.encodedTextBox.setMaximumWidth(1500)
        self.encodedPanel.addWidget(self.encodedTextBox)
    
        #Create Encode button
        self.showOriginalButton = Button("Encode")
        self.showOriginalButton.clicked.connect(self.onShowOriginal)
        self.encodedPanel.addWidget(self.showOriginalButton)

        self.mainPanel.addLayout(self.topHorizontalPanel)
        self.mainPanel.addLayout(self.middleHorizontalPanel)
        self.mainPanel.addLayout(self.encodedPanel)
        self.mainPanel.addLayout(self.bottomHorizontalPanel)

        self.setCentralWidget(self.centralWidget)
        self.currentInputText = ""

    def generateHuffmanTableWidget(self, text):
        self.clearBottomPanel()
        self.currentInputText = text

        if len(text) != 0:
            self.huffmanTableGenerator = HuffmanTableGenerator()

            freq_dict = self.huffmanTableGenerator.createDictionary(text)

            # Prepare data lists
            characters = list(freq_dict.keys())
            frequencies = list(freq_dict.values())
            rowCount = len(characters)

            self.huffmanTableWidget = Table(rowCount, 3)
            self.huffmanTableWidget.setHorizontalHeaderLabels(["Charcter", "Frequency", "Code"])


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
            
            header = self.huffmanTableWidget.horizontalHeader()
            col_count = self.huffmanTableWidget.columnCount()
            total_col_w = sum(header.sectionSize(i) for i in range(col_count))
            vert_header_w = self.huffmanTableWidget.verticalHeader().width()
            frame_w = self.huffmanTableWidget.frameWidth() * 2

            max_table_w = total_col_w + vert_header_w + frame_w
            self.huffmanTableWidget.setMaximumWidth(max_table_w)

            # Create and add tree widget
            scroll_tree = create_scrollable_tree(root)
            self.bottomHorizontalPanel.addWidget(scroll_tree)

            encoded_bits = "".join(codes.get(ch, "") for ch in text)
            self.encodedTextBox.setPlainText(encoded_bits)


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
        """Remove all widgets from the bottom panel"""
        layout = self.bottomHorizontalPanel
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

    def onShowOriginal(self):
        """Replace the bit-string with the original text"""
        self.encodedTextBox.setPlainText(self.currentInputText)

def main():
    mainApp = QApplication(sys.argv)
    mainApp.setFont(QFont("Segoe UI", 12))
    window = MainWindow()
    window.show()
    sys.exit(mainApp.exec_())

if __name__ == "__main__":
    main()