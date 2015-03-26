# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'task.ui'
#
# Created: Mon Dec 22 17:09:54 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(399, 400)
        Dialog.setMaximumSize(QtCore.QSize(399, 400))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.stages = QtWidgets.QComboBox(Dialog)
        self.stages.setObjectName("stages")
        self.verticalLayout.addWidget(self.stages)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.projects = QtWidgets.QComboBox(Dialog)
        self.projects.setObjectName("projects")
        self.verticalLayout.addWidget(self.projects)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.taskText = QtWidgets.QTextEdit(Dialog)
        self.taskText.setObjectName("taskText")
        self.horizontalLayout.addWidget(self.taskText)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.validCheckBox = QtWidgets.QCheckBox(Dialog)
        self.validCheckBox.setEnabled(True)
        self.validCheckBox.setText("")
        self.validCheckBox.setObjectName("validCheckBox")
        self.horizontalLayout_3.addWidget(self.validCheckBox)
        self.valid = QtWidgets.QDateEdit(Dialog)
        self.valid.setEnabled(False)
        self.valid.setObjectName("valid")
        self.horizontalLayout_3.addWidget(self.valid)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.deadLineCheckbox = QtWidgets.QCheckBox(Dialog)
        self.deadLineCheckbox.setEnabled(True)
        self.deadLineCheckbox.setText("")
        self.deadLineCheckbox.setObjectName("deadLineCheckbox")
        self.horizontalLayout_3.addWidget(self.deadLineCheckbox)
        self.deadline = QtWidgets.QDateEdit(Dialog)
        self.deadline.setEnabled(False)
        self.deadline.setObjectName("deadline")
        self.horizontalLayout_3.addWidget(self.deadline)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "Stage"))
        self.label_3.setText(_translate("Dialog", "Project"))
        self.label_5.setText(_translate("Dialog", "Valid till"))
        self.label_4.setText(_translate("Dialog", "Deadline"))

