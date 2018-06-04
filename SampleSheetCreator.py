#! python
# -*- coding: utf-8 -*-

import sys
import os
from ruamel.yaml import YAML
from collections import OrderedDict
from collections import defaultdict
from collections import Counter

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import *
#from PyQt5.QtWidgets import QApplication

from preferences import Preferences
from verifySave import Generate
from gui.mainWindow import Ui_MainWindow
from gui.validation_error import Ui_Dialog
import data_fields

class ValErrDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super(ValErrDialog, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.on_click)

    def on_click(self):
        self.close()

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.SampleSheetCreator_settings = QSettings('vll', 'SampleSheetCreator')

        yaml = YAML()
        self.yconfig = ""
        self.yindices = ""

        self.yindices_mod = defaultdict(lambda: defaultdict(dict))

        if self.SampleSheetCreator_settings.contains('path_config_file'):
            self.path_config_file = self.SampleSheetCreator_settings.value('path_config_file', type=str)

            if self.path_config_file:
                if os.path.exists(self.path_config_file):
                    self.config_fh = open(self.path_config_file,  encoding="utf-8").read()
                    self.yconfig = yaml.load(self.config_fh)
                    print("loaded yconfig")

            error_list = []

            if self.SampleSheetCreator_settings.contains('path_indices_file'):
                self.path_indices_file = self.SampleSheetCreator_settings.value('path_indices_file', type=str)
                if self.path_config_file:
                    if os.path.exists(self.path_indices_file):
                        self.indices_fh = open(self.path_indices_file,  encoding="utf-8").read()

                        try:
                            self.yindices = yaml.load(self.indices_fh)
                        except yaml.constructor.DuplicateKeyError as e:
                            error_list.append(e)

                        if self.yindices:

                            for k, subdict1 in self.yindices.items():
                                for method, subdict2 in subdict1.items():
                                    for instrument, subdict3 in subdict2.items():
                                        for adapter_type, subdict4 in subdict3.items():
                                            for set, subdict5 in subdict4.items():
                                                if subdict5:
                                                    for index_name, value in subdict5.items():
                                                        try:
                                                            x = self.yindices_mod[method][instrument][index_name]
                                                            error_list.append("duplicate index", method, instrument, index_name)
                                                        except KeyError:
                                                            self.yindices_mod[method][instrument][index_name] = value

                        print("loaded yindices")

            if len(error_list) > 0:
                self.show_valerrordialog(error_list)

        self.sdata_fields_constr = OrderedDict(sorted(data_fields.data_fields.items(), key=lambda x: x[1]['c_p']))
        self.sdata_fields_ss = OrderedDict(sorted(data_fields.data_fields.items(), key=lambda x: x[1]['ss_p']))

        self.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())

        max_fields = 0
        for k in self.sdata_fields_constr:
            if data_fields.data_fields[k]['construct']:
                max_fields = data_fields.data_fields[k]['c_p']

        self.tableWidget_construct.setColumnCount(max_fields+1)

        self.tableWidget_construct.setRowCount(30)
        self.tableWidget_construct.setAcceptDrops(True)

        header_labels = []

        for k in self.sdata_fields_constr:
            if data_fields.data_fields[k]['construct']:
                cnum = data_fields.data_fields[k]['c_p']
                cwidth = data_fields.data_fields[k]['c_w']
                self.tableWidget_construct.setColumnWidth(cnum, cwidth)
                header_labels.append(k)

        self.tableWidget_construct.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_construct.setHorizontalHeaderLabels(header_labels)

        for row in range(30):
#            chkBoxItem = QTableWidgetItem()
#            chkBoxItem.setFlags(Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
#            chkBoxItem.setCheckState(Qt.Unchecked)
#            chkBoxItem.setTextAlignment(QtCore.Qt.AlignCenter)
#            self.tableWidget_construct.setItem(row, data_fields.data_fields['N']['c_p'], chkBoxItem)
            chk_bx = QCheckBox()
            cell_widget = QWidget()
            chk_bx.setCheckState(Qt.Unchecked)
            lay_out = QHBoxLayout(cell_widget)
            lay_out.addWidget(chk_bx)
            lay_out.setAlignment(Qt.AlignCenter)
            lay_out.setContentsMargins(0, 0, 0, 0)
            cell_widget.setLayout(lay_out)
            self.tableWidget_construct.setCellWidget(row, 0, cell_widget)


        self.tableWidget_I5.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_I7.horizontalHeader().setStretchLastSection(True)

        self.setWindowTitle("SampleSheetCreator v.0.3.4")
        self.setWindowIcon(QtGui.QIcon('icons/icon.png'))
        self.actionPreferences.triggered.connect(self.show_preferences)

        self.comboBox_method.activated.connect(self.comboBox_method_activated)
        self.comboBox_panel.activated.connect(self.comboBox_panel_activated)
        self.comboBox_definition.activated.connect(self.comboBox_definition_activated)
        self.comboBox_P7.activated.connect(self.comboBox_P7_activated)
        self.comboBox_P5.activated.connect(self.comboBox_P5_activated)
        self.dateEdit.dateChanged.connect(self.onDateChanged)

        self.pushButton_pasteall.clicked.connect(self.buttonClickedPasteAll)
        self.pushButton_generate.clicked.connect(self.validateTable)
        QApplication.clipboard().dataChanged.connect(self.clipboardChanged)
        self.checkBox.stateChanged.connect(self.toggle_activated)

        if self.yconfig and self.yindices:
            self.populate_all()

        self.clip = QApplication.clipboard()

    def comboBox_method_activated(self, index):
        self.populate_lineEdit_run()
        self.populate_lineEdit_path()
        self.populate_comboBox_P5()
        self.populate_comboBox_P7()
        self.populate_comboBox_panel()
        self.populate_comboBox_definition()
        self.populate_comboBox_analysis()
        return 1

    def comboBox_panel_activated(self, index):
        self.populate_comboBox_definition()
        self.populate_comboBox_analysis()
        return 1

    def comboBox_P5_activated(self, index):
        self.populate_tableWidget_I5()
        return 1

    def comboBox_P7_activated(self, index):
        self.populate_tableWidget_I7()
        return 1

    def comboBox_definition_activated(self, index):
        self.populate_comboBox_analysis()
        return 1

    def onDateChanged(self):
        self.populate_lineEdit_run()
        return 1

    def populate_comboBox_investigator(self):
        investigators_list = self.SampleSheetCreator_settings.value('investigators', type=list)
        self.comboBox_investigator.clear()
        self.comboBox_investigator.addItems(investigators_list)

    def populate_comboBox_instrument(self):
        if self.path_config_file and self.path_indices_file:
            instrument = self.yconfig['Instrument']
            self.comboBox_instrument.clear()
            self.comboBox_instrument.addItems(instrument)

        return 1

    def populate_comboBox_method(self):
        methods = list(self.yconfig['Methods'])
        self.comboBox_method.clear()
        self.comboBox_method.addItems(methods)

        return 1

    def populate_lineEdit_run(self):
        cmethod = self.comboBox_method.currentText()

        tmp_date = self.dateEdit.date()
        date_var = tmp_date.toPyDate()

        run_label = str(date_var) + "_" + str(cmethod)

        self.lineEdit_run.setText(run_label)
        return 1

    def populate_lineEdit_reads(self):
        cmethod = self.comboBox_method.currentText()
        reads = self.yconfig['Methods'][cmethod]['Settings']['Reads']
        self.lineEdit_reads.setText(str(reads))
        return 1

    def populate_lineEdit_manifest(self):
        cmethod = self.comboBox_method.currentText()
        cpanel = self.comboBox_panel.currentText()
        manifests = self.yconfig['Methods'][cmethod]['Panels'][cpanel]['Manifests']

        jmanifests = " ".join(manifests)
        self.lineEdit_manifest.setText(str(jmanifests))
        return 1

    def populate_lineEdit_adapter(self):
        cmethod = self.comboBox_method.currentText()
        adapter = self.yconfig['Methods'][cmethod]['Settings']['Adapter']
        self.lineEdit_adapter.setText(str(adapter))
        return 1

    def populate_lineEdit_path(self):
        cmethod = self.comboBox_method.currentText()
        tmp_date = self.dateEdit.date()
        date_var = tmp_date.toPyDate()
        run_label = str(date_var) + "_" + cmethod
        path_samplesheets_folder = self.SampleSheetCreator_settings.value('path_samplesheets_folder', type=str)
        path = os.path.join(path_samplesheets_folder, run_label)
        self.lineEdit_path.setText(path)
        self.lineEdit_path.setToolTip(path)
        return 1

    def populate_comboBox_P5(self):
        cmethod = self.comboBox_method.currentText()
        cinstrument = self.comboBox_instrument.currentText()

        if self.path_indices_file:

            p5sets = list(self.yindices['Indices'][cmethod][cinstrument]['P5'])
            self.comboBox_P5.clear()
            self.comboBox_P5.addItems(p5sets)

            cP5set = self.comboBox_P5.currentText()

            if self.yindices['Indices'][cmethod][cinstrument]['P5'][cP5set]:
                p5inds = list(self.yindices['Indices'][cmethod][cinstrument]['P5'][cP5set])
                lenp5inds = len(p5inds)

                self.tableWidget_I5.setColumnCount(1)
                self.tableWidget_I5.setRowCount(lenp5inds)

                for index, item in enumerate(p5inds):
                    self.tableWidget_I5.setItem(index, 0, QTableWidgetItem(item.strip()))

                self.populate_tableWidget_I5()
            else:
                self.tableWidget_I5.clear()

        return 1

    def populate_comboBox_P7(self):

        cmethod = self.comboBox_method.currentText()
        cinstrument = self.comboBox_instrument.currentText()

        p7sets = list(self.yindices['Indices'][cmethod][cinstrument]['P7'])
        self.comboBox_P7.clear()
        self.comboBox_P7.addItems(p7sets)

        cP7set = self.comboBox_P7.currentText()

        p7inds = list(self.yindices['Indices'][cmethod][cinstrument]['P7'][cP7set])
        lenp7inds = len(p7inds)

        self.tableWidget_I7.setColumnCount(1)
        self.tableWidget_I7.setRowCount(lenp7inds)

        for index, item in enumerate(p7inds):
            self.tableWidget_I7.setItem(index, 0, QTableWidgetItem(item.strip()))

        self.populate_tableWidget_I7()

        return 1

    def populate_tableWidget_I5(self):

        cmethod = self.comboBox_method.currentText()
        cinstrument = self.comboBox_instrument.currentText()

        if self.path_indices_file:

            cP5set = self.comboBox_P5.currentText()

            if self.yindices['Indices'][cmethod][cinstrument]['P5'][cP5set]:
                p5inds = list(self.yindices['Indices'][cmethod][cinstrument]['P5'][cP5set])
                lenp5inds = len(p5inds)

                self.tableWidget_I5.setColumnCount(1)
                self.tableWidget_I5.setRowCount(lenp5inds)

                for index, item in enumerate(p5inds):
                    self.tableWidget_I5.setItem(index, 0, QTableWidgetItem(item.strip()))
            else:
                self.tableWidget_I5.clear()

        return 1

    def populate_tableWidget_I7(self):

        cmethod = self.comboBox_method.currentText()
        cinstrument = self.comboBox_instrument.currentText()

        if self.path_indices_file:

            cP7set = self.comboBox_P7.currentText()

            p7inds = list(self.yindices['Indices'][cmethod][cinstrument]['P7'][cP7set])
            lenp7inds = len(p7inds)

            self.tableWidget_I7.setColumnCount(1)
            self.tableWidget_I7.setRowCount(lenp7inds)

            for index, item in enumerate(p7inds):
                self.tableWidget_I7.setItem(index, 0, QTableWidgetItem(item.strip()))

        return 1

    def populate_comboBox_definition(self):

        cmethod = self.comboBox_method.currentText()
        cpanel = self.comboBox_panel.currentText()

        print(cmethod, cpanel)

        defpath = self.yconfig['Methods'][cmethod]['Panels'][cpanel]['AnalysisDefPathWin']

        print(defpath)

        files = os.listdir(defpath)
        self.comboBox_definition.clear()
        self.comboBox_definition.addItems(files)
        return 1

    def populate_comboBox_panel(self):
        cmethod = self.comboBox_method.currentText()
        panels = list(self.yconfig['Methods'][cmethod]['Panels'])

        self.comboBox_panel.clear()
        self.comboBox_panel.addItems(panels)

        return 1

    def populate_comboBox_analysis(self):

        def getanalyses(file):
            anals = []
            fh = open(file,  encoding="utf-8")
            for line in fh:
                if line.startswith('>'):
                    l2 = line.strip()
                    anal = l2[1:]
                    anals.append(anal)

            return anals

        cdefinition = self.comboBox_definition.currentText()
        cpanel = self.comboBox_panel.currentText()
        cmethod = self.comboBox_method.currentText()

        defpath = self.yconfig['Methods'][cmethod]['Panels'][cpanel]['AnalysisDefPathWin']

        file = os.path.join(defpath, cdefinition)

        analyses = getanalyses(file)

        self.comboBox_analysis.clear()
        self.comboBox_analysis.addItems(analyses)
        return 1

    def show_preferences(self):
        self.preferences = Preferences(self)
        self.preferences.show()

    def show_valerrordialog(self, incrows):
        d = ValErrDialog()
        for i in incrows:
            print(i)
            d.plainTextEdi_missing_fields.appendPlainText(i)

        d.exec_()

    def cell_contains_text(self, item):
        if item != None:
            item_txt = item.text()
            if any(chr.isalnum() for chr in item_txt):
                return True
            else:
                return False
        else:
            return False

    def show_generate(self):
        self.generate = Generate(self)
        self.generate.setWindowModality(QtCore.Qt.ApplicationModal)
        self.generate.show()

    def validateTable(self):
        rows = self.tableWidget_construct.rowCount()
        columns = self.tableWidget_construct.columnCount()

        required_fields_dict = {}
        nonrequired_fields_dict = {}
        fields_value_constraints = defaultdict(dict)

        nodup_req_fields_dict = defaultdict(dict)
        nodup_nonreq_fields_dict = defaultdict(dict)
        dup_req_fields_dict = defaultdict(dict)
        dup_nonreq_fields_dict = defaultdict(dict)

        populated_required_fields_dict = defaultdict(dict)
        unpopulated_required_fields_dict = defaultdict(dict)

        populated_nonrequired_fields_dict = defaultdict(dict)
        unpopulated_nonrequired_fields_dict = defaultdict(dict)

        populated_false_value_constrained_fields_dict = defaultdict(dict)

        error_log = []

        """ structure fields and columns """
        for cname, subdict in data_fields.data_fields.items():
            if (subdict['c_p'] >= 0 or subdict['combine']) and subdict['required']:
                if subdict['combine']:
                    tmp = subdict['combine'].split(",")
                    required_fields_dict[cname] = str(data_fields.data_fields[tmp[0]]['c_p']) + "," + str(data_fields.data_fields[tmp[1]]['c_p'])
                else:
                    required_fields_dict[cname] = str(data_fields.data_fields[cname]['c_p'])

                if not subdict['duplicates_ok']:
                    if subdict['combine']:
                        tmp = subdict['combine'].split(",")
                        nodup_req_fields_dict[cname] = str(data_fields.data_fields[tmp[0]]['c_p']) + "," + str(
                            data_fields.data_fields[tmp[1]]['c_p'])
                    else:
                        nodup_req_fields_dict[cname] = str(data_fields.data_fields[cname]['c_p'])

                if subdict['value_constraints']:
                    fields_value_constraints[cname]['c_p'] = subdict['c_p']
                    fields_value_constraints[cname]['constraints'] = subdict['value_constraints']

                else:
                    if subdict['combine']:
                        tmp = subdict['combine'].split(",")
                        dup_req_fields_dict[cname] = str(data_fields.data_fields[tmp[0]]['c_p']) + "," + str(
                            data_fields.data_fields[tmp[1]]['c_p'])
                    else:
                        dup_req_fields_dict[cname] = str(data_fields.data_fields[cname]['c_p'])

            elif (subdict['c_p'] >= 0 or subdict['combine']) and not subdict['required']:
                if subdict['combine']:
                    tmp = subdict['combine'].split(",")
                    nonrequired_fields_dict[cname] = str(data_fields.data_fields[tmp[0]]['c_p']) + "," + str(data_fields.data_fields[tmp[1]]['c_p'])
                else:
                    nonrequired_fields_dict[cname] = str(data_fields.data_fields[cname]['c_p'])

                if not subdict['duplicates_ok']:
                    if subdict['combine']:
                        tmp = subdict['combine'].split(",")
                        nodup_nonreq_fields_dict[cname] = str(data_fields.data_fields[tmp[0]]['c_p']) + "," + str(
                            data_fields.data_fields[tmp[1]]['c_p'])
                    else:
                        nodup_nonreq_fields_dict[cname] = str(data_fields.data_fields[cname]['c_p'])

                else:
                    if subdict['combine']:
                        tmp = subdict['combine'].split(",")
                        dup_nonreq_fields_dict[cname] = str(data_fields.data_fields[tmp[0]]['c_p']) + "," + str(
                            data_fields.data_fields[tmp[1]]['c_p'])
                    else:
                        dup_nonreq_fields_dict[cname] = str(data_fields.data_fields[cname]['c_p'])


        """ remove spaces from empty cells """
        for r in range(rows):
            for c in range(columns):
                if c != data_fields.data_fields['N']['c_p']:
                    curr_item = self.tableWidget_construct.item(r, c)
                    if not self.cell_contains_text(curr_item):
                        self.tableWidget_construct.setItem(r, c, QtWidgets.QTableWidgetItem(""))

        """ verify that required fields are populated """
        for r in range(rows):
            for cname in required_fields_dict:
                c = required_fields_dict[cname]
                c_list = c.split(',')
                item_txt_list = []
                for tmp_c in c_list:
                    curr_item = self.tableWidget_construct.item(r, int(tmp_c))
                    if self.cell_contains_text(curr_item):
                        item_txt = curr_item.text()
                        item_txt_list.append(item_txt)

                if(len(item_txt_list)>0):
                    item_txt_join = ','.join(item_txt_list)
                    populated_required_fields_dict[r][cname] = item_txt_join
                else:
                    unpopulated_required_fields_dict[r][cname] = 1

            for cname in nonrequired_fields_dict:
                c = nonrequired_fields_dict[cname]
                c_list = c.split(',')
                item_txt_list = []
                for tmp_c in c_list:
                    curr_item = self.tableWidget_construct.item(r, int(tmp_c))
                    if self.cell_contains_text(curr_item):
                        item_txt = curr_item.text()
                        item_txt_list.append(item_txt)

                if(len(item_txt_list)>0):
                    item_txt_join = ','.join(item_txt_list)
                    populated_nonrequired_fields_dict[r][cname] = item_txt_join
                else:
                    unpopulated_nonrequired_fields_dict[r][cname] = 1

            for cname, subdict in fields_value_constraints.items():
                c = subdict['c_p']
                item_txt_list = []
                curr_item = self.tableWidget_construct.item(r, int(c))
                if self.cell_contains_text(curr_item):
                    item_txt = curr_item.text()
                    item_txt_list.append(item_txt)

                if(len(item_txt_list)>0):
                    item_txt_join = ','.join(item_txt_list)
                    accepted_values = subdict['constraints'].split(",")

                    if item_txt_join not in accepted_values:
                        populated_false_value_constrained_fields_dict[r][cname] = item_txt_join

        for r in range(rows):
            if len(unpopulated_required_fields_dict[r]) > 0 and len(populated_required_fields_dict[r]) > 0:
                unpop_req_list = unpopulated_required_fields_dict[r].keys()
                error_log.append(
                    "Required fields are partially unpopulated in row " + str(r + 1) + ", fields: [" + ", ".join(
                        str(x) for x in unpop_req_list) + "]")

            if len(populated_required_fields_dict[r]) == 0 and len(populated_nonrequired_fields_dict[r]):
                pop_nonreq_list = populated_nonrequired_fields_dict[r].keys()
                error_log.append(
                    "Required fields unpopulated, nonrequired fields populated in row " + str(r + 1) + ", fields: [" + ", ".join(
                        str(x) for x in pop_nonreq_list) + "]")

            for cname in populated_false_value_constrained_fields_dict[r]:
                value = populated_false_value_constrained_fields_dict[r][cname]
                error_log.append(
                    "Incorrect value-constrained field. Field: " + cname + ", row: " + str(r + 1) + ", value: [" +
                        str(value) + "]")

        for cname, positions in nodup_req_fields_dict.items():

            field_values_list = []

            for r in range(rows):
                c = required_fields_dict[cname]
                c_list = c.split(',')
                item_txt_list = []
                for tmp_c in c_list:
                    curr_item = self.tableWidget_construct.item(r, int(tmp_c))
                    if self.cell_contains_text(curr_item):
                        item_txt = curr_item.text()
                        item_txt_list.append(item_txt)

                if (len(item_txt_list) > 0):
                    item_txt_join = ','.join(item_txt_list)
                    field_values_list.append(item_txt_join)

            dups = [item for item, count in Counter(field_values_list).items() if count > 1]

            if len(dups) > 0:
                error_log.append(
                    "Required field, duplicates not allowed contain duplicate values. Field: " + cname + ", values: [" + ", ".join(
                        str(x) for x in dups) + "]")

        for cname, positions in nodup_nonreq_fields_dict.items():

            field_values_list = []

            for r in range(rows):
                c = required_fields_dict[cname]
                c_list = c.split(',')
                item_txt_list = []
                for tmp_c in c_list:
                    curr_item = self.tableWidget_construct.item(r, int(tmp_c))
                    if self.cell_contains_text(curr_item):
                        item_txt = curr_item.text()
                        item_txt_list.append(item_txt)

                if (len(item_txt_list) > 0):
                    item_txt_join = ','.join(item_txt_list)
                    field_values_list.append(item_txt_join)

            dups = [item for item, count in Counter(field_values_list).items() if count > 1]

            if len(dups) > 0:
                error_log.append(
                    "Nonrequired field, duplicates not allowed contain duplicate values. Field: " + cname + ", values: [" + ", ".join(
                        str(x) for x in dups) + "]")

        """ disallow multiple panels in the same batch """

        batch2panel = defaultdict(dict)

        for r in range(rows):
            batch_c = required_fields_dict['Batch']
            panel_c = required_fields_dict['Panel']

            batch_item_list = []
            panel_item_list = []

            batch_item = self.tableWidget_construct.item(r, int(batch_c))
            if self.cell_contains_text(batch_item):
                item_txt = batch_item.text()
                batch_item_list = item_txt.split(",")

            panel_item = self.tableWidget_construct.item(r, int(panel_c))
            if self.cell_contains_text(panel_item):
                item_txt = panel_item.text()
                panel_item_list = item_txt.split(",")

            if len(batch_item_list) > 0 and len(panel_item_list) > 0:
                for b in batch_item_list:
                    for p in panel_item_list:
                        batch2panel[b][p] = 1

        for b in batch2panel:
            if len(batch2panel[b]) > 1:
                panels_list = batch2panel[b].keys()

                error_log.append(
                    "Different panels cannot be analyzed in one batch. Batch " + b + ", panels: " +  "[" + ", ".join(
                        str(x) for x in panels_list) + "]")

        if len(error_log) > 0:
            self.show_valerrordialog(error_log)

        else:
#            print("hej")
            self.show_generate()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Delete:

            indexes = self.tableWidget_construct.selectionModel().selectedIndexes() 
            for index in indexes:
                self.tableWidget_construct.setItem(index.row(),index.column(), QTableWidgetItem(""))

        if e.matches(QtGui.QKeySequence.Paste):

            crow = self.tableWidget_construct.currentRow()
            ccolumn = self.tableWidget_construct.currentColumn()
            if ccolumn > 0:
                cb_rows = QApplication.clipboard().text().split('\n')
                for rnum, rdat in enumerate(cb_rows):
                    cb_columns = rdat.split('\t')
                    for cnum, cdat in enumerate(cb_columns):
                        paste_row = crow + rnum
                        paste_column = ccolumn + cnum
                        self.tableWidget_construct.setItem(paste_row,paste_column, QTableWidgetItem(cdat))

        if e.matches(QtGui.QKeySequence.Copy):
            selected = self.tableWidget_construct.selectedRanges()
            s = ""
            for r in range(selected[0].topRow(), selected[0].bottomRow()+1):
                for c in range(selected[0].leftColumn(), selected[0].rightColumn()+1):
                    try:
                        s += str(self.tableWidget_construct.item(r,c).text()) + "\t"
                    except AttributeError:
                        s += "\t"
                s = s[:-1] + "\n" #eliminate last '\t'

            clip = QApplication.clipboard()
            self.clip.setText(s)

    def clipboardChanged(self):
        text = QApplication.clipboard().text().split('\n')

    def buttonClickedPasteAll(self):
        indexes = self.tableWidget_construct.selectionModel().selectedRows()

        cpanel = self.comboBox_panel.currentText()
        canalysis = self.comboBox_analysis.currentText()
        canalysisdef = self.comboBox_definition.currentText()

        for index in sorted(indexes):
            row = index.row()
            self.tableWidget_construct.setItem(row, data_fields.data_fields['Analysis_Def']['c_p'], QTableWidgetItem(canalysisdef))
            self.tableWidget_construct.setItem(row, data_fields.data_fields['Panel']['c_p'], QTableWidgetItem(cpanel))
            self.tableWidget_construct.setItem(row, data_fields.data_fields['Analysis']['c_p'], QTableWidgetItem(canalysis))

    def populate_all(self):

        self.populate_comboBox_investigator()
        self.populate_comboBox_instrument()
        self.populate_comboBox_method()
        self.populate_comboBox_P5()
        self.populate_comboBox_P7()
        self.populate_comboBox_panel()
        self.populate_comboBox_definition()
        self.populate_comboBox_analysis()
        self.populate_lineEdit_reads()
        self.populate_lineEdit_run()
        self.populate_lineEdit_manifest()
        self.populate_lineEdit_adapter()
        self.populate_lineEdit_path()

        self.comboBox_method.setEnabled(True)
        self.comboBox_instrument.setEnabled(True)
        self.comboBox_instrument.setEnabled(True)
        self.dateEdit.setEnabled(True)
        self.comboBox_investigator.setEnabled(True)
        self.lineEdit_adapter.setEnabled(True)
        self.lineEdit_manifest.setEnabled(True)
        self.lineEdit_run.setEnabled(True)
        self.lineEdit_reads.setEnabled(True)
        self.lineEdit_path.setEnabled(True)
        self.tableWidget_I5.setEnabled(False)
        self.tableWidget_I7.setEnabled(False)
        self.comboBox_P5.setEnabled(False)
        self.comboBox_P7.setEnabled(False)

        self.comboBox_definition.setEnabled(False)
        self.comboBox_panel.setEnabled(False)
        self.comboBox_analysis.setEnabled(False)
        self.pushButton_pasteall.setEnabled(False)
        self.plainTextEdit.setEnabled(False)
        self.tableWidget_construct.setEnabled(False)
        self.pushButton_generate.setEnabled(False)

        return 1

    def toggle_activated(self):
        if self.checkBox.isChecked():
            self.comboBox_method.setEnabled(False)
            self.lineEdit_adapter.setEnabled(False)
            self.lineEdit_manifest.setEnabled(False)
            self.lineEdit_run.setEnabled(False)
            self.lineEdit_reads.setEnabled(False)
            self.lineEdit_path.setEnabled(False)
            self.tableWidget_I5.setEnabled(True)
            self.tableWidget_I7.setEnabled(True)
            self.comboBox_P5.setEnabled(True)
            self.comboBox_P7.setEnabled(True)

            self.comboBox_definition.setEnabled(True)
            self.comboBox_panel.setEnabled(True)
            self.comboBox_analysis.setEnabled(True)
            self.pushButton_pasteall.setEnabled(True)
            self.plainTextEdit.setEnabled(True)
            self.tableWidget_construct.setEnabled(True)
            self.pushButton_generate.setEnabled(True)
        else:
            self.comboBox_method.setEnabled(True)
            self.lineEdit_adapter.setEnabled(True)
            self.lineEdit_manifest.setEnabled(True)
            self.lineEdit_run.setEnabled(True)
            self.lineEdit_reads.setEnabled(True)
            self.lineEdit_path.setEnabled(True)
            self.tableWidget_I5.setEnabled(False)
            self.tableWidget_I7.setEnabled(False)
            self.comboBox_P5.setEnabled(False)
            self.comboBox_P7.setEnabled(False)

            self.comboBox_definition.setEnabled(False)
            self.comboBox_panel.setEnabled(False)
            self.comboBox_analysis.setEnabled(False)
            self.pushButton_pasteall.setEnabled(False)
            self.plainTextEdit.setEnabled(False)
            self.tableWidget_construct.setEnabled(False)
            self.pushButton_generate.setEnabled(False)

            for row in range(30):
#                chkBoxItem = QTableWidgetItem()
#                chkBoxItem.setFlags(Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
#                chkBoxItem.setCheckState(Qt.Unchecked)
#                chkBoxItem.setTextAlignment(QtCore.Qt.AlignCenter)
#                self.tableWidget_construct.setItem(row, 0, chkBoxItem)
                self.tableWidget_construct.setItem(row, data_fields.data_fields['I5_Index_ID']['c_p'], QTableWidgetItem(""))
                self.tableWidget_construct.setItem(row, data_fields.data_fields['I7_Index_ID']['c_p'], QTableWidgetItem(""))
                self.tableWidget_construct.setItem(row, data_fields.data_fields['Analysis_Def']['c_p'], QTableWidgetItem(""))
                self.tableWidget_construct.setItem(row, data_fields.data_fields['Panel']['c_p'], QTableWidgetItem(""))
                self.tableWidget_construct.setItem(row, data_fields.data_fields['Analysis']['c_p'], QTableWidgetItem(""))
                self.tableWidget_construct.setItem(row, data_fields.data_fields['Method']['c_p'], QTableWidgetItem(""))

    def repopulate(self):

        yaml = YAML()
        self.yconfig = ""
        self.yindices = ""

        if self.SampleSheetCreator_settings.contains('path_config_file'):
            self.path_config_file = self.SampleSheetCreator_settings.value('path_config_file', type=str)

            if self.path_config_file:
                if os.path.exists(self.path_config_file):
                    self.config_fh = open(self.path_config_file, encoding="utf-8").read()
                    self.yconfig = yaml.load(self.config_fh)
                    print("reloaded yconfig")

            if self.SampleSheetCreator_settings.contains('path_indices_file'):
                self.path_indices_file = self.SampleSheetCreator_settings.value('path_indices_file', type=str)
                if self.path_indices_file:
                    if os.path.exists(self.path_indices_file):
                        self.indices_fh = open(self.path_indices_file,  encoding="utf-8").read()
                        self.yindices = yaml.load(self.indices_fh)
                        print("reloaded yindices")

                        self.populate_all()


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
