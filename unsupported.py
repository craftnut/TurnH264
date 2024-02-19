import sys

from PySide6 import QtCore
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QFileDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QComboBox,
    QWidget,
)
        
def unsupported_dialog(platform):
    
    if __name__ == "unsupported":
        app = QApplication(sys.argv)
        popup = Unsupported(platform)
        popup.resize(300, 100)
        popup.show()
        sys.exit(app.exec())
    
def exit_app():
    print("Apologies for the lack of support.")
    exit()
    
class Unsupported(QWidget):
    def __init__(self, platform: str):
        super().__init__()
        
        self.setWindowTitle("Unsupported Platform")
        unsupported_notice = QLabel(
            f"Unfortunately, {platform} is not currently supported.\n You can add support and submit a merge request if you'd like.",
            alignment=QtCore.Qt.AlignCenter
        )
        acknowledge = QPushButton("Ok")
        acknowledge.clicked.connect(exit_app)
        
        layout = QGridLayout(self)
        layout.addWidget(unsupported_notice, 0, 0, 1, 3)
        layout.addWidget(acknowledge, 1, 2, 1, 1)