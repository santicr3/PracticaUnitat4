from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtSql import *
from PySide6.QtCore import *

class Add_Task(QDialog):
    def __init__(self, module_list):
        super().__init__()

        self.setWindowTitle("New Task")
        
        self.name = QLineEdit()
        self.module = QComboBox()
        self.module.addItems(module_list)
        self.finsihed = QRadioButton("Finished")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.check)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        
        self.layout.addWidget(QLabel("Task name:"))
        self.layout.addWidget(self.name)
        self.layout.addWidget(QLabel("Select the module:"))
        self.layout.addWidget(self.module)
        self.layout.addWidget(self.finsihed)
        
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def check(self):
        if self.name.text() == "":
                QMessageBox.critical(
                    self,
                    "Error!",
                    "The module name can´t be empty",
                    buttons=QMessageBox.Ok
                )
        else:
            self.close()