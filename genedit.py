from ui.generator import *

from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal

from enums import Projects, Stages, Generators
import enums


class GenEdit(Ui_Dialog, QDialog):
    """
    Qt dialog that allows creating and editing of generators.
    """
    genCreated = pyqtSignal(Generators, int, str,
                            Projects, Stages, object, object)
    genEdited = pyqtSignal(int, Generators, int, str,
                           Projects, Stages, object, object)

    def __init__(self, gen_id=None, gen_type=Generators.Daily, shift=1, text='',
                 project=Projects.Money, stage=Stages.Incoming,
                 valid=None, deadline=None):
        super(GenEdit, self).__init__()

        self.setupUi(self)

        for proj in Projects:
            self.projects.addItem(proj.value)

        for _stage in Stages:
            self.stages.addItem(_stage.value)

        for g_type in Generators:
            self.genType.addItem(g_type.value)

        self.validBox.stateChanged.connect(self.valid.setEnabled)
        self.deadlineBox.stateChanged.connect(self.deadline.setEnabled)

        # Init values
        self.gen_id = gen_id
        self.text.setText(text)
        self.genType.setCurrentText(gen_type.value)
        self.dayShift.setValue(shift)
        self.projects.setCurrentText(project.value)
        self.stages.setCurrentText(stage.value)

        self.dayShift.setMinimum(1)
        self.valid.setMinimum(0)
        self.deadline.setMinimum(0)

        if valid is not None:
            self.validBox.setChecked(True)
            self.valid.setEnabled(True)
            self.valid.setValue(valid)
        else:
            self.validBox.setChecked(False)
            self.valid.setEnabled(False)

        if deadline is not None:
            self.deadlineBox.setChecked(True)
            self.deadline.setEnabled(True)
            self.deadline.setValue(deadline)
        else:
            self.deadlineBox.setChecked(False)
            self.deadline.setEnabled(False)

    def accept(self):
        """
        Overrides Qdialog implementation of accept function.
        Gathers data and emits signal.
        :return:
        """
        if self.is_valid():
            text = self.text.toPlainText()
            stage = enums.from_value(Stages, self.stages.currentText())
            project = enums.from_value(Projects, self.projects.currentText())
            gen_type = enums.from_value(Generators, self.genType.currentText())
            gen_shift = self.dayShift.value()
            valid = None
            deadline = None
            if self.validBox.checkState() != 0:
                valid = self.valid.value()
            if self.deadlineBox.checkState() != 0:
                deadline = self.deadline.value()
            if self.gen_id is not None:
                self.genEdited.emit(self.gen_id, gen_type, gen_shift, text,
                                    project, stage, valid, deadline)
            else:
                self.genCreated.emit(gen_type, gen_shift, text, project, stage,
                                     valid, deadline)
            QDialog.accept(self)
            return
        else:
            QMessageBox.information(
                self, "Information",  "Generator is not valid.")
            return

    def is_valid(self):
        # Task text must be not empty
        if len(self.text.toPlainText()) == 0:
            return False

        # Monthly generator cannot generate tasks later then 28th.
        if self.genType.currentText() == "Monthly" and self.dayShift.value() > 28:
            return False

        return True