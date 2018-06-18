import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QTableWidget, QApplication, QMainWindow, QTableWidgetItem, \
    QFileDialog, QComboBox, QDialog, QWidget, QListWidgetItem, QSizeGrip
from PyQt5.QtCore import QSettings, QDir, Qt

from gui.pref import Ui_Form
from PyQt5 import QtGui

class Preferences(QWidget, Ui_Form):
    def __init__(self, parent):
        super(Preferences, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Preferences')
        self.btn_ok.clicked.connect(lambda: self.ok(parent))
        self.btn_cancel.clicked.connect(self.cancel)
        self.setWindowIcon(QtGui.QIcon('icons/icon.png'))

        self.toolButton_indices_file.clicked.connect(self.open_indices_file_dialog)
        self.toolButton_samplesheets_folder.clicked.connect(self.open_samplesheets_folder_dialog)
        self.toolButton_config_file.clicked.connect(self.open_config_file_dialog)
        self.pushButton_add_investigator.clicked.connect(self.add_investigator)
        self.pushButton_remove_investigators.clicked.connect(self.remove_investigator)

        SampleSheetCreator_settings = QSettings('vll', 'SampleSheetCreator')

        institute = SampleSheetCreator_settings.value('institute', type=str)
        path_indices_file = SampleSheetCreator_settings.value('path_indices_file', type=str)
        path_config_file = SampleSheetCreator_settings.value('path_config_file', type=str)
        path_samplesheets_folder = SampleSheetCreator_settings.value('path_samplesheets_folder', type=str)
        investigators_list = SampleSheetCreator_settings.value('investigators', type=list)

        if not institute:
            institute = ""
        if not path_indices_file:
            path_indices_file = ""
        if not path_config_file:
            path_config_file = ""            
        if not path_samplesheets_folder:
            path_samplesheets_folder = "";
        if not investigators_list:
            investigators_list = []
		
        self.lineEdit_institute.setText(institute)
        self.lineEdit_indices_file.setText(path_indices_file)
        self.lineEdit_config_file.setText(path_config_file)
        self.lineEdit_samplesheets_folder.setText(path_samplesheets_folder)

        for i in investigators_list:
            item = QListWidgetItem(i)
            self.listWidget_investigators.addItem(item)

        stylesheet = """
                        QTableWidget { 
                            background-color: rgb(80, 80, 80);
                        }

                        QPushButton { 
                            background-color: rgb(90,70,0); 
                        }
                        QTreeWidget::indicator  {
                            width: 10px;
                            height: 10px;
                            margin: 5px;
                            border-radius: 5px;
                            border: 3px solid rgb(120,90,0); 
                        }
                        QTreeWidget::indicator::unchecked  {
                            background-color: transparent rgb(80, 80, 80);
                        }
                        QTreeWidget::indicator::checked {
                            background-color: rgb(150,120,0);
                        }
                        QTreeWidget {
                            background-color: rgb(80, 80, 80);
                        }
                        """

        self.setStyleSheet(stylesheet)
        self.grip1 = QSizeGrip(self)
        self.verticalLayout_3.addWidget(self.grip1, 0, Qt.AlignRight | Qt.AlignBottom)

    def ok(self, parent):
        SampleSheetCreator_settings = QSettings('vll', 'SampleSheetCreator')

        institute = self.lineEdit_institute.text()

        path_indices_file = self.lineEdit_indices_file.text()
        path_config_file = self.lineEdit_config_file.text()
        path_samplesheets_folder = self.lineEdit_samplesheets_folder.text()

        SampleSheetCreator_settings.setValue('institute', institute)
        SampleSheetCreator_settings.setValue('path_indices_file', path_indices_file)
        SampleSheetCreator_settings.setValue('path_config_file', path_config_file)
        SampleSheetCreator_settings.setValue('path_samplesheets_folder', path_samplesheets_folder)

        parent.repopulate()

        self.close()

    def cancel(self):
        self.close()

    def open_indices_file_dialog(self):
        options = QFileDialog.Options()
        path_tmp, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Yaml files (*.yaml *.yml);;All filetypes (*)", options=options)
        path = str(QDir.toNativeSeparators(path_tmp))
        self.lineEdit_indices_file.setText(path)
    
    def open_config_file_dialog(self):
        options = QFileDialog.Options()
        path_tmp, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Yaml files (*.yaml *.yml);;All filetypes (*)", options=options)
        path = str(QDir.toNativeSeparators(path_tmp))
        self.lineEdit_config_file.setText(path)

    def open_samplesheets_folder_dialog(self):
        path_tmp = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        path = str(QDir.toNativeSeparators(path_tmp))
        self.lineEdit_samplesheets_folder.setText(path)

    def add_investigator(self):
        SampleSheetCreator_settings = QSettings('vll', 'SampleSheetCreator')
        investigator = self.lineEdit_add_investigator.text()

        if investigator:
            investigators_list = SampleSheetCreator_settings.value('investigators', type=list)
            investigators_list.append(investigator)
            investigators_list = list(set(investigators_list))
            SampleSheetCreator_settings.setValue('investigators', investigators_list)

            self.listWidget_investigators.clear()
            investigators_list = SampleSheetCreator_settings.value('investigators', type=list)
            for i in investigators_list:
                item = QListWidgetItem(i)
                self.listWidget_investigators.addItem(item)

            self.lineEdit_add_investigator.setText("")

    def remove_investigator(self):
        SampleSheetCreator_settings = QSettings('vll', 'SampleSheetCreator')
        investigator = ""
        try:
            investigator = self.listWidget_investigators.currentItem().text()
        except:
            pass

        if investigator:
            investigators_list = SampleSheetCreator_settings.value('investigators', type=list)
            investigators_list.remove(investigator)
            investigators_list = list(set(investigators_list))
            SampleSheetCreator_settings.setValue('investigators', investigators_list)
            self.listWidget_investigators.clear()
            investigators_list = SampleSheetCreator_settings.value('investigators', type=list)
            for i in investigators_list:
                item = QListWidgetItem(i)
                self.listWidget_investigators.addItem(item)



