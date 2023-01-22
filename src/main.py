# from PySide6.QtCore import()
import os
import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtSql import *
from PySide6.QtCore import *
from add_task_dialog import Add_Task

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tasks organizer")
        self.resize(720, 480)

        #Module model
        self.module_model = QSqlTableModel(self)
        self.module_model.setTable("modules")
    
        self.module_model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.module_model.setHeaderData(0, Qt.Horizontal, "Name")
        self.module_model.select()

        #Module view
        self.module_view = QListView()
        self.module_view.setModel(self.module_model)
        self.module_view.setCurrentIndex(QModelIndex())
        self.item = ""
        
        self.module_view.selectionModel().selectionChanged.connect(
            self.get_item
        )
        

        #Task model
        self.task_model = QSqlTableModel(self)
        self.task_model.setTable("tasks")
        
        self.task_model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.task_model.setHeaderData(0, Qt.Horizontal, "Name")
        self.task_model.setHeaderData(1, Qt.Horizontal, "Module")
        self.task_model.setHeaderData(2, Qt.Horizontal, "Finished")
        self.task_model.setFilter("Module like " + "\"" + self.item + "\"")
        self.task_model.select()
        self.db = self.task_model.database()
        
        #Task view
        self.task_view = QTreeView()
        self.task_view.setModel(self.task_model)
        path = os.path.join(os.path.dirname(__file__))
        path = path.removesuffix("src")

        self.layout = QHBoxLayout()
        main_component = QWidget()
        main_component.setLayout(self.layout)
        self.setCentralWidget(main_component)

        self.v_modules = QVBoxLayout()
        self.v_tasks = QVBoxLayout()

        self.modules_buttons_layout = QHBoxLayout()
        self.tasks_buttons_layout = QHBoxLayout()

        #Buttons
        #Module
        self.new_module_button = QPushButton()
        self.new_module_button.setIcon(QIcon(path+"/res/img/plus.png"))
        self.new_module_button.clicked.connect(self.new_module)

        self.remove_module_button = QPushButton()
        self.remove_module_button.setIcon(QIcon(path+"/res/img/cancel.png"))
        self.remove_module_button.clicked.connect(self.remove_module)

        self.modules_buttons_layout.addWidget(self.new_module_button)
        self.modules_buttons_layout.addWidget(self.remove_module_button)

        #Task
        self.new_task_button = QPushButton()
        self.new_task_button.setIcon(QIcon(path+"/res/img/plus.png"))
        self.new_task_button.clicked.connect(self.new_task)

        self.remove_task_button = QPushButton()
        self.remove_task_button.setIcon(QIcon(path+"/res/img/cancel.png"))
        self.remove_task_button.clicked.connect(self.del_task)

        self.tasks_buttons_layout.addWidget(self.new_task_button)
        self.tasks_buttons_layout.addWidget(self.remove_task_button)
        
        self.v_modules.addWidget(QLabel("Modules:"))
        self.v_modules.addWidget(self.module_view)
        self.v_modules.addLayout(self.modules_buttons_layout)

        self.v_tasks.addWidget(QLabel("Tasks:"))
        self.v_tasks.addWidget(self.task_view)
        self.v_tasks.addLayout(self.tasks_buttons_layout)
        
        #Main Layout
        self.layout.addLayout(self.v_modules)
        self.layout.insertSpacing(1, 20)
        self.layout.addLayout(self.v_tasks)
        
    def get_item(self):
        self.item = self.module_view.currentIndex().data()
        self.task_model.setFilter("Module like " + "\"" + self.item + "\"")
        self.task_model.select()

    def new_module(self):
        
        while True:
            modules = self.modules_list()
            dialog = QInputDialog.getText(self, 'New Module', 'Module Name')
            
            if dialog[0] == "" and dialog[1]:
                QMessageBox.critical(
                    self,
                    "Error!",
                    "The module name can´t be empty",
                    buttons=QMessageBox.Ok
                )
            elif dialog[0] in modules:
                QMessageBox.critical(
                    self,
                    "Error!",
                    "The module name alredy exists",
                    buttons=QMessageBox.Ok
                    )
            elif dialog[0] != "":
                r = self.module_model.record()
                r.setValue("name", dialog[0])
                self.module_model.insertRecord(-1, r)
                break
            else:
                break

    def remove_module(self):
        buttons = QMessageBox.warning(
            self,
            "Warning!",
            "This action can't be undo",
            buttons=QMessageBox.Ok | QMessageBox.Cancel,
            defaultButton=QMessageBox.Cancel
        )
        if buttons == QMessageBox.Ok:
            self.item = self.module_view.currentIndex().row()
            self.module_model.removeRow(self.item)
            self.module_model.select()
            for i in range(self.task_model.rowCount()):
                self.task_model.removeRow(i)
                self.task_model.select()
            
    def new_task(self):
        dialog = Add_Task(self.modules_list())
        dialog.exec()
        task_name = dialog.name.text()
        task_module = dialog.module.currentText()
        task_finished = dialog.finsihed.isChecked()
        
        if dialog.name.text() != "":
            r = self.task_model.record()
            r.setValue("name", task_name)
            r.setValue("module", task_module)
            if task_finished:
                r.setValue("finished", 1)
            else:
                r.setValue("finished", 0)
                
            self.task_model.insertRecord(-1, r)
        
    def del_task(self):
        buttons = QMessageBox.warning(
            self,
            "Warning!",
            "This action can't be undo",
            buttons=QMessageBox.Ok | QMessageBox.Cancel,
            defaultButton=QMessageBox.Cancel
        )
        if buttons == QMessageBox.Ok:
            item = self.task_view.currentIndex().row()
            self.task_model.removeRow(item)
            self.task_model.select()
            
    def modules_list(self):
        modules = []
        for i in range(self.module_model.rowCount()):
                module = self.module_model.primaryValues(i).value(0)
                modules.append(module)
        return modules


def createConnection():
    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setDatabaseName(os.path.join(os.path.dirname(__file__),"modulos.sqlite"))
    
    if not con.open():
        QMessageBox.critical(
            "Error!",
            "QTableView Example - Error!",
            "Database Error: %s" % con.lastError().databaseText(),
        )
        return False
    return True
    

app = QApplication(sys.argv)
if not createConnection():
    sys.exit(1)
win = MainWindow()
win.show()
sys.exit(app.exec())