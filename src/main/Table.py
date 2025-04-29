from PyQt5.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView, QSizePolicy

class Table(QTableWidget):
    def __init__(self, rows, columns, parent=None):
        super().__init__(rows, columns, parent)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSizePolicy(
        QSizePolicy.Expanding,
        QSizePolicy.Minimum
    )
        self.verticalHeader().hide()
        self.setStyleSheet("""
                    QHeaderView::section {
                           background-color: #7A9CC6;
                        }
                    QTableWidget {
                            border: 2px solid #aaa;
                            border-radius: 10px;
                           }
                            """)
        
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setHighlightSections(False)  # so clicking a header doesn't "select" it