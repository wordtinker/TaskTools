# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'generators.ui'
#
# Created: Fri Dec 26 01:44:38 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(456, 356)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.generatorsTable = QtWidgets.QTableView(Dialog)
        self.generatorsTable.setObjectName("generatorsTable")
        self.gridLayout.addWidget(self.generatorsTable, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addGenerator = QtWidgets.QPushButton(Dialog)
        self.addGenerator.setObjectName("addGenerator")
        self.horizontalLayout.addWidget(self.addGenerator)
        self.editGenerator = QtWidgets.QPushButton(Dialog)
        self.editGenerator.setObjectName("editGenerator")
        self.horizontalLayout.addWidget(self.editGenerator)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.deleteGenerator = QtWidgets.QPushButton(Dialog)
        self.deleteGenerator.setObjectName("deleteGenerator")
        self.horizontalLayout.addWidget(self.deleteGenerator)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Generators"))
        self.addGenerator.setText(_translate("Dialog", "Add"))
        self.editGenerator.setText(_translate("Dialog", "Edit"))
        self.deleteGenerator.setText(_translate("Dialog", "Delete"))

