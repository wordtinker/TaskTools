from ui.report import *

from PyQt5.QtWidgets import QDialog, QHeaderView
from PyQt5.QtCore import QDate, QSortFilterProxyModel

from baseTableModel import BaseTaBleModel
from enums import Projects, Stages
import datetime


class TaskModel(BaseTaBleModel):
    headers = ["Text", "Project", "From", "On", "To", "On", "Valid", "Deadline"]

    def __init__(self):
        super(TaskModel, self).__init__(self.headers)

    def setRowData(self, row, values):
        for i, val in enumerate(values):
            if isinstance(val, (Stages, Projects)):
                val = val.value
            if isinstance(val, datetime.date):
                val = str(val)
            self.setData(self.index(row, i), val)


class ReportModel(BaseTaBleModel):
    headers = ["Project", "Undone", "Lost", "Done"]

    def __init__(self):
        super(ReportModel, self).__init__(self.headers)

        for project in Projects:
            self.insertRows(0, 1)
            self.setData(self.index(0, 0), project.value)

    def init(self):
        for row in range(self.rowCount()):
            self.setData(self.index(row, 1), 0)
            self.setData(self.index(row, 2), 0)
            self.setData(self.index(row, 3), 0)

    def add(self, project, pos):
        for row in range(self.rowCount()):
            if self.index(row, 0).data() == project.value:
                old_val = self.index(row, pos).data()
                self.setData(self.index(row, pos), old_val + 1)
                break


class Report(Ui_Dialog, QDialog):

    def __init__(self, storage):
        super(Report, self).__init__()

        self.setupUi(self)

        self.storage = storage

        # Connecting signals and slots
        self.reportBtn.clicked.connect(self.report_requested)

        self.taskModel = TaskModel()
        self.proxyModel = QSortFilterProxyModel()
        self.proxyModel.setSourceModel(self.taskModel)
        self.taskTable.setModel(self.proxyModel)

        self.reportModel = ReportModel()
        self.totalTable.setModel(self.reportModel)

        self.taskTable.setSortingEnabled(True)
        self.taskTable.horizontalHeader()\
            .setSectionResizeMode(0, QHeaderView.Stretch)
        self.totalTable.horizontalHeader()\
            .setSectionResizeMode(0, QHeaderView.Stretch)

        today = QDate.currentDate()
        self.fromEdit.setDate(today)
        self.toEdit.setDate(today)

    def report_requested(self):
        start = self.fromEdit.date().toPyDate()
        finish = self.toEdit.date().toPyDate()
        tasks = self.storage.select_tasks_for_report(start, finish)

        self.taskModel.removeRows(0, self.taskModel.rowCount())
        self.reportModel.init()

        for task in tasks:
            (task, text, project, to_stage, to_date, valid, deadline) = task
            stages = self.storage.select_stages(task, finish, to_stage)
            # There is only one stage for the task
            if len(stages) == 0:
                from_stage = to_stage
                from_date = to_date
            # There are only two stages for the task
            elif len(stages) == 1:
                from_stage = stages[0][0]
                from_date = stages[0][1]
            else:
                # If the stage came before start date use that stage
                before = [i for i in stages if i[1] < start]
                if len(before) > 0:
                    from_stage = before[-1][0]
                    from_date = before[-1][1]
                # Use the first stage of the task
                else:
                    from_stage = stages[0][0]
                    from_date = stages[0][1]

            self.taskModel.insertRows(0, 1)
            self.taskModel.setRowData(0, (text, project, from_stage,
                                          from_date, to_stage, to_date,
                                          valid, deadline))
            self.reportModel.add(project, 1)
            if to_stage == Stages.Done:
                self.reportModel.add(project, 3)
            elif valid is not None and valid <= to_date:
                self.reportModel.add(project, 2)