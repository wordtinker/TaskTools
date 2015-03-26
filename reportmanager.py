from ui.report import *

from PyQt5.QtWidgets import QDialog, QHeaderView
from PyQt5.QtCore import QDate, QAbstractTableModel, Qt, QVariant,\
    QModelIndex

from enums import Projects, Stages
import datetime


class TaskModel(QAbstractTableModel):

    def __init__(self):
        super(TaskModel, self).__init__()

        self.headers = ["Text", "Project", "From", "On", "To", "On", "Valid",
                        "Deadline"]
        self.tasks = []

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.tasks)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.headers)

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()

        elif role != Qt.DisplayRole:
            return QVariant()

        data = self.tasks[index.row()][index.column()]
        return QVariant(data)

    def headerData(self, col, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headers[col])
        return QVariant()

    def setData(self, index, value, role=None):
        if index.isValid():
            self.tasks[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def insertRows(self, position, rows, parent=QModelIndex(), *args, **kwargs):
        self.beginInsertRows(parent, position, position + rows - 1)
        for i in range(rows):
            self.tasks.insert(position, [None] * self.columnCount())
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=QModelIndex(), *args, **kwargs):
        self.beginRemoveRows(parent, position, position + rows - 1)
        for i in range(rows):
            self.tasks.pop(position)
        self.endRemoveRows()
        return True

    def setRowData(self, row, values):
        for i, val in enumerate(values):
            if isinstance(val, (Stages, Projects)):
                val = val.value
            if isinstance(val, datetime.date):
                val = str(val)
            self.setData(self.index(row, i), val)


class Report(Ui_Dialog, QDialog):

    def __init__(self, storage):
        super(Report, self).__init__()

        self.setupUi(self)

        self.storage = storage

        # Connecting signals and slots
        self.reportBtn.clicked.connect(self.report_requested)

        self.taskModel = TaskModel()
        self.taskTable.setModel(self.taskModel)
        self.taskTable.horizontalHeader()\
            .setSectionResizeMode(0, QHeaderView.Stretch)

        today = QDate.currentDate()
        self.fromEdit.setDate(today)
        self.toEdit.setDate(today)

    def report_requested(self):
        start = self.fromEdit.date().toPyDate()
        finish = self.toEdit.date().toPyDate()
        tasks = self.storage.select_tasks_for_report(start, finish)
        self.taskModel.removeRows(0, self.taskModel.rowCount())
        for task in tasks:
            (task, text, project, to_stage, to_date, valid, deadline) = task
            stages = self.storage.select_stages(task, finish, to_stage)
            if len(stages) == 0:
                from_stage = to_stage
                from_date = to_date
            elif len(stages) == 1:
                from_stage = stages[0][0]
                from_date = stages[0][1]
            else:
                before = [i for i in stages if i[1] < start]
                if len(before) > 0:
                    from_stage = before[-1][0]
                    from_date = before[-1][1]
                else:
                    from_stage = stages[0][0]
                    from_date = stages[0][1]

            self.taskModel.insertRows(0, 1)
            self.taskModel.setRowData(0, (text, project, from_stage,
                                          from_date, to_stage, to_date,
                                          valid, deadline))