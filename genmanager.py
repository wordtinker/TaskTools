from ui.generators import *

from PyQt5.QtWidgets import QDialog, QAbstractItemView, QHeaderView
from PyQt5.QtCore import pyqtSignal, QDate, QAbstractTableModel, Qt, QVariant,\
    QModelIndex

from enums import Projects, Stages, Generators
import enums
from genedit import GenEdit

class GeneratorModel(QAbstractTableModel):

    def __init__(self):
        super(GeneratorModel, self).__init__()

        self.headers = ["Id", "Type", "Shift", "Text", "Project", "Stage", "Valid",
                        "Deadline"]
        self.generators = []

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.generators)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.headers)

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()

        elif role != Qt.DisplayRole:
            return QVariant()

        data = self.generators[index.row()][index.column()]
        return QVariant(data)

    def headerData(self, col, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headers[col])
        return QVariant()

    def setData(self, index, value, role=None):
        if index.isValid():
            self.generators[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def insertRows(self, position, rows, parent=QModelIndex(), *args, **kwargs):
        self.beginInsertRows(parent, position, position + rows - 1)
        for i in range(rows):
            self.generators.insert(position, [None] * self.columnCount())
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=QModelIndex(), *args, **kwargs):
        self.beginRemoveRows(parent, position, position + rows - 1)
        for i in range(rows):
            self.generators.pop(position)
        self.endRemoveRows()
        return True

    def setRowData(self, row, values):
        for i, val in enumerate(values):
            if isinstance(val, (Stages, Projects, Generators)):
                val = val.value
            self.setData(self.index(row, i), val)


class GenManager(Ui_Dialog, QDialog):

    generatorChanged = pyqtSignal()

    def __init__(self, storage):
        super(GenManager, self).__init__()

        self.setupUi(self)

        self.__storage = storage

        # Connecting signals and slots
        self.addGenerator.clicked.connect(self.add_generator_clicked)
        self.editGenerator.clicked.connect(self.edit_generator_clicked)
        self.deleteGenerator.clicked.connect(self.delete_generator_clicked)

        self.gen_model = GeneratorModel()
        self.generatorsTable.setModel(self.gen_model)
        self.generatorsTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.generatorsTable.horizontalHeader()\
            .setSectionResizeMode(3, QHeaderView.Stretch)

        self.load_initial_values()

    def load_initial_values(self):
        generators = self.__storage.select_generators()
        for gen in generators:
            self.gen_model.insertRows(0, 1)
            self.gen_model.setRowData(0, gen)

    def add_generator_clicked(self):
        # Fire up widget
        manager = GenEdit()
        manager.genCreated.connect(self.add_generator)
        manager.exec_()

    def edit_generator_clicked(self):
        index = self.generatorsTable.selectedIndexes()
        if index:
            idx = index[0].row()
            gen_id = self.gen_model.index(idx, 0).data()
            gen_type = self.gen_model.index(idx, 1).data()
            gen_type = enums.from_value(Generators, gen_type)
            shift = self.gen_model.index(idx, 2).data()
            text = self.gen_model.index(idx, 3).data()
            project = self.gen_model.index(idx, 4).data()
            project = enums.from_value(Projects, project)
            stage = self.gen_model.index(idx, 5).data()
            stage = enums.from_value(Stages, stage)
            valid = self.gen_model.index(idx, 6).data()
            deadline = self.gen_model.index(idx, 7).data()
            manager = GenEdit(gen_id, gen_type, shift, text, project, stage,
                              valid, deadline)
            manager.genEdited.connect(self.edit_generator)
            manager.exec_()

    def delete_generator_clicked(self):
        index = self.generatorsTable.selectedIndexes()
        if index:
            idx = index[0].row()
            gen_id = self.gen_model.index(idx, 0).data()
            self.__storage.delete_generator(gen_id)
            self.gen_model.removeRow(idx)

    def add_generator(self, *args):
        gen_id = self.__storage.add_generator(*args)
        self.gen_model.insertRows(0, 1)
        self.gen_model.setRowData(0, (gen_id, ) + args)
        self.generatorChanged.emit()

    def edit_generator(self, *args):
        self.__storage.update_generator(*args)
        gen_id = args[0]
        for row in range(self.gen_model.rowCount()):
            if self.gen_model.index(row, 0).data() == gen_id:
                self.gen_model.setRowData(row, args)
                self.generatorChanged.emit()
                break