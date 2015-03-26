from ui.generators import *

from PyQt5.QtWidgets import QDialog, QAbstractItemView, QHeaderView
from PyQt5.QtCore import pyqtSignal

from baseTableModel import BaseTaBleModel
from enums import Projects, Stages, Generators
import enums
from genedit import GenEdit


class GeneratorModel(BaseTaBleModel):
    """
    Simple model that holds current generators information.
    """
    headers = ["Id", "Type", "Shift", "Text", "Project", "Stage", "Valid",
                        "Deadline"]

    def __init__(self):
        super(GeneratorModel, self).__init__(self.headers)

    def setRowData(self, row, values):
        for i, val in enumerate(values):
            if isinstance(val, (Stages, Projects, Generators)):
                val = val.value
            self.setData(self.index(row, i), val)


class GenManager(Ui_Dialog, QDialog):
    """
    QDialog that shows list of generators and some GUI to add and edit them.
    """

    generatorChanged = pyqtSignal()

    def __init__(self, storage):
        super(GenManager, self).__init__()

        self.setupUi(self)

        self.__storage = storage

        # Connecting signals and slots
        self.addGenerator.clicked.connect(self.add_generator_clicked)
        self.editGenerator.clicked.connect(self.edit_generator_clicked)
        self.deleteGenerator.clicked.connect(self.delete_generator_clicked)

        # Connect model and view
        self.gen_model = GeneratorModel()
        self.generatorsTable.setModel(self.gen_model)
        self.generatorsTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.generatorsTable.horizontalHeader()\
            .setSectionResizeMode(3, QHeaderView.Stretch)

        self.load_initial_values()

    def load_initial_values(self):
        """
        On start shows the generators that are in the DB.
        """
        generators = self.__storage.select_generators()
        for gen in generators:
            self.gen_model.insertRows(0, 1)
            self.gen_model.setRowData(0, gen)

    def add_generator_clicked(self):
        """
        Shows the widget for adding new generator.
        """
        manager = GenEdit()
        manager.genCreated.connect(self.add_generator)
        manager.exec_()

    def edit_generator_clicked(self):
        """
        Shows the widget for editing existent generator.
        :return:
        """
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
        """
        Deletes the generator from the DB and from the list of generators.
        """
        index = self.generatorsTable.selectedIndexes()
        if index:
            idx = index[0].row()
            gen_id = self.gen_model.index(idx, 0).data()
            self.__storage.delete_generator(gen_id)
            self.gen_model.removeRow(idx)

    def add_generator(self, *args):
        """
        Catches the signal that generator has been added.
        Adds generator to DB and to the current list of generators.
        """
        gen_id = self.__storage.add_generator(*args)
        self.gen_model.insertRows(0, 1)
        self.gen_model.setRowData(0, (gen_id, ) + args)
        self.generatorChanged.emit()

    def edit_generator(self, *args):
        """
        Catches the signal that generator has been edited.
        Unpdates generator ine the  DB and in the current list of generators.
        """
        self.__storage.update_generator(*args)
        gen_id = args[0]
        for row in range(self.gen_model.rowCount()):
            if self.gen_model.index(row, 0).data() == gen_id:
                self.gen_model.setRowData(row, args)
                self.generatorChanged.emit()
                break