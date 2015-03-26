from ui.task import *

from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, QDate

from enums import Projects, Stages
import enums


class TaskEdit(Ui_Dialog, QDialog):
    """
    Qdialog that creates or edits the task.
    """

    taskCreated = pyqtSignal(str, Projects, Stages, object, object)
    taskEdited = pyqtSignal(int, str, Projects, Stages, object, object)

    def __init__(self, task_id=None, text='', project=Projects.Money,
                 stage=Stages.Incoming, valid=None, deadline=None):
        super(TaskEdit, self).__init__()

        self.setupUi(self)

        for proj in Projects:
            self.projects.addItem(proj.value)

        for _stage in Stages:
            self.stages.addItem(_stage.value)

        self.validCheckBox.stateChanged.connect(self.valid.setEnabled)
        self.deadLineCheckbox.stateChanged.connect(self.deadline.setEnabled)

        # Init values
        self.task_id = task_id
        self.taskText.setText(text)
        self.projects.setCurrentText(project.value)
        self.stages.setCurrentText(stage.value)

        today = QDate.currentDate()
        if valid is not None:
            self.validCheckBox.setChecked(True)
            self.valid.setDate(valid)
        else:
            self.valid.setDate(today)

        if deadline is not None:
            self.deadLineCheckbox.setChecked(True)
            self.deadline.setDate(deadline)
        else:
            self.deadline.setDate(today)

    def accept(self):
        """
        Gathers parameters of the task and emits the signal.
        :return:
        """
        if self.is_valid():
            text = self.taskText.toPlainText()
            stage = enums.from_value(Stages, self.stages.currentText())
            project = enums.from_value(Projects, self.projects.currentText())
            valid = None
            deadline = None
            if self.validCheckBox.checkState() != 0:
                valid = self.valid.date().toPyDate()
            if self.deadLineCheckbox.checkState() != 0:
                deadline = self.deadline.date().toPyDate()
            if self.task_id is not None:
                self.taskEdited.emit(self.task_id, text, project, stage,
                                     valid, deadline)
            else:
                self.taskCreated.emit(text, project, stage, valid, deadline)
            QDialog.accept(self)
            return
        else:
            QMessageBox.information(
                self, "Information",  "Task is not valid.")
            return

    def is_valid(self):
        if len(self.taskText.toPlainText()) == 0:
            return False

        result = True
        if self.validCheckBox.checkState() != 0:
            result = self.valid.date().isValid() and result

        if self.deadLineCheckbox.checkState() != 0:
            result = self.deadline.date().isValid() and result

        return result