import sys
from PyQt5.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, 
    QVBoxLayout, 
    QPushButton, 
    QLineEdit, 
    QFileDialog, 
    QLabel
)
import requests  # only if you actually need to POST the file

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 File “Upload” Demo")

        # central widget + layout
        container = QWidget()
        layout = QVBoxLayout()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # a line edit to show the chosen file path
        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)
        layout.addWidget(QLabel("Selected file:"))
        layout.addWidget(self.path_edit)

        # button to open file dialog
        btn_pick = QPushButton("Choose File…")
        btn_pick.clicked.connect(self.choose_file)
        layout.addWidget(btn_pick)

        # button to “upload” (i.e. send) the file
        btn_upload = QPushButton("Upload File")
        btn_upload.clicked.connect(self.upload_file)
        layout.addWidget(btn_upload)

    def choose_file(self):
        # only allow selecting one file; filter by common filetypes
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a file to upload",
            "",                       # start dir
            "All Files (*);;Text (*.txt)"
        )
        if file_path:
            self.path_edit.setText(file_path)

    def upload_file(self):
        path = self.path_edit.text()
        if not path:
            return  # no file chosen
        # ---- OPTION A: using Python requests ----
        url = "https://example.com/upload"  # your endpoint
        with open(path, 'rb') as f:
            files = {'file': (path.split('/')[-1], f)}
            r = requests.post(url, files=files)
        if r.status_code == 200:
            print("Upload succeeded!")
        else:
            print("Upload failed:", r.status_code, r.text)

        # ---- OPTION B: using QNetworkAccessManager (pure Qt) ----
        # from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QHttpMultiPart, QHttpPart
        # nam = QNetworkAccessManager(self)
        # request = QNetworkRequest(QUrl(url))
        # multipart = QHttpMultiPart(QHttpMultiPart.FormDataType)
        # file_part = QHttpPart()
        # file_part.setHeader(QNetworkRequest.ContentDispositionHeader, 
        #     'form-data; name="file"; filename="{}"'.format(path.split('/')[-1]))
        # file_part.setBodyDevice(open(path, 'rb'))  # careful with ownership
        # multipart.append(file_part)
        # nam.post(request, multipart)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
