# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Tue Dec 30 23:02:05 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(529, 333)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tasks = QtWidgets.QGridLayout()
        self.tasks.setObjectName("tasks")
        self.verticalLayout.addLayout(self.tasks)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 529, 25))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuTask = QtWidgets.QMenu(self.menuBar)
        self.menuTask.setObjectName("menuTask")
        self.menuPattern = QtWidgets.QMenu(self.menuBar)
        self.menuPattern.setObjectName("menuPattern")
        self.menuReports = QtWidgets.QMenu(self.menuBar)
        self.menuReports.setObjectName("menuReports")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionManage = QtWidgets.QAction(MainWindow)
        self.actionManage.setObjectName("actionManage")
        self.actionReport = QtWidgets.QAction(MainWindow)
        self.actionReport.setObjectName("actionReport")
        self.menuFile.addAction(self.actionExit)
        self.menuTask.addAction(self.actionNew)
        self.menuPattern.addAction(self.actionManage)
        self.menuReports.addAction(self.actionReport)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuTask.menuAction())
        self.menuBar.addAction(self.menuPattern.menuAction())
        self.menuBar.addAction(self.menuReports.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuTask.setTitle(_translate("MainWindow", "Task"))
        self.menuPattern.setTitle(_translate("MainWindow", "Pattern"))
        self.menuReports.setTitle(_translate("MainWindow", "Reports"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionNew.setText(_translate("MainWindow", "Add"))
        self.actionManage.setText(_translate("MainWindow", "Manage"))
        self.actionReport.setText(_translate("MainWindow", "Report"))

