# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'report.ui'
#
# Created: Fri Jan  2 13:04:17 2015
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(467, 369)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.fromEdit = QtWidgets.QDateEdit(Dialog)
        self.fromEdit.setObjectName("fromEdit")
        self.horizontalLayout.addWidget(self.fromEdit)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.toEdit = QtWidgets.QDateEdit(Dialog)
        self.toEdit.setObjectName("toEdit")
        self.horizontalLayout.addWidget(self.toEdit)
        self.reportBtn = QtWidgets.QPushButton(Dialog)
        self.reportBtn.setObjectName("reportBtn")
        self.horizontalLayout.addWidget(self.reportBtn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.taskTable = QtWidgets.QTableView(Dialog)
        self.taskTable.setObjectName("taskTable")
        self.gridLayout.addWidget(self.taskTable, 1, 0, 1, 1)
        self.totalTable = QtWidgets.QTableView(Dialog)
        self.totalTable.setObjectName("totalTable")
        self.gridLayout.addWidget(self.totalTable, 2, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "From"))
        self.label_2.setText(_translate("Dialog", "To"))
        self.reportBtn.setText(_translate("Dialog", "Report"))

