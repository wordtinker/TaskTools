from PyQt5.QtCore import Qt, QAbstractListModel, QModelIndex, pyqtSignal,\
    QSize, QMimeData, QVariant, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow,\
    QListView, QLabel, QAbstractItemView

from ui.mainWindow import Ui_MainWindow
from taskedit import TaskEdit
from genmanager import GenManager
from reportmanager import Report

import sys
import os
import logging
import datetime
from dateutil.relativedelta import relativedelta

import storage
import config
from enums import Stages, Projects, Generators

app_data_path = None
if "APPDATA" in os.environ:  # We are on Windows
    app_data_path = os.path.join(os.environ["APPDATA"], config.appname)
elif "HOME" in os.environ:  # We are on Linux
    app_data_path = os.path.join(os.environ["HOME"], "." + config.appname)
else:  # Fallback to our working dir
    app_data_path = os.getcwd()

if not os.path.exists(app_data_path):
    os.makedirs(app_data_path)


class Task():

    def __init__(self, task_id, project, stage, text, valid, deadline):
        self.id = task_id
        self.project = project
        self.stage = stage
        self.text = text
        self.valid = valid
        self.deadline = deadline


class TaskPool(QObject):
    """
    The lower level of task pool model.
    """

    taskAdded = pyqtSignal(int, Stages, Projects)
    taskDropped = pyqtSignal(int, Stages, Projects)

    def __init__(self, storage):
        super(TaskPool, self).__init__()
        self.__pool = {}
        self.__storage = storage

    def __insert_task(self, task_id, project, stage, text, valid, deadline):
        new_task = Task(task_id, project, stage, text, valid, deadline)
        self.__pool[new_task.id] = new_task

        self.taskAdded.emit(new_task.id, stage, project)

    def add_task(self, text, project, stage, valid, deadline,
                 gen_id=None, date=None):
        task_id = self.__storage.add_task(text, project, stage,
                                          valid, deadline,
                                          gen_id=gen_id, date=date)
        self.__insert_task(task_id, project, stage, text, valid, deadline)

    def edit_task(self, task_id, text, project, stage, valid, deadline):
        task = self.__pool[task_id]
        old_stage = task.stage
        old_project = task.project
        if old_stage != stage:
            self.__storage.set_new_stage(task_id, stage)
            task.stage = stage

        if task.text != text or old_project != project or task.valid != valid \
                or task.deadline != deadline:
            self.__storage.set_new_stats(task_id, text, project, valid, deadline)
            task.text = text
            task.project = project
            task.valid = valid
            task.deadline = deadline

        if old_stage != stage or old_project != project:
            self.taskDropped.emit(task_id, old_stage, old_project)
            self.taskAdded.emit(task_id, task.stage, task.project)

    def drop_task(self, task_id):
        stage = self.__pool[task_id].stage
        project = self.__pool[task_id].project
        self.__storage.delete_task(task_id)
        del self.__pool[task_id]
        self.taskDropped.emit(task_id, stage, project)

    def get_task_name_by_id(self, task_id):
        if task_id in self.__pool:
            return self.__pool[task_id].text
        else:
            return ""

    def get_task_stats_by_id(self, task_id):
        if task_id in self.__pool:
            task = self.__pool[task_id]
            return task.text, task.project, task.stage, task.valid, task.deadline
        else:
            return ""

    def onTaskMoved(self, task_id, new_stage, new_project):
        if task_id not in self.__pool:
            return False

        task = self.__pool[task_id]
        if task.stage != new_stage:
            self.__storage.set_new_stage(task_id, new_stage)
            task.stage = new_stage

        if task.project != new_project:
            self.__storage.set_new_project(task_id, new_project)
            task.project = new_project

    def load(self):
        records = self.__storage.select_tasks_for_today()
        for record in records:
            self.__insert_task(*record)

    def generate_new_tasks(self):
        generators = self.__storage.select_generators()
        today = datetime.date.today()
        for generator in generators:
            logging.info("Going to use generator: {}".format(generator))
            gen_id = generator[0]
            last_date = self.__storage.get_last_generated_date(gen_id)

            gen_type = generator[1]
            rate = generator[2]
            if gen_type == Generators.Daily:
                logging.info("The generator is: {}".format(gen_type))
                if not last_date:
                    logging.info("The generator is new!")
                    self.generate_single_task(today, gen_id, *generator[3:])
                else:
                    logging.info("The generator is old!")
                    for i in range(abs((last_date - today).days)):
                        if (i + 1) % rate == 0:
                            delta = datetime.timedelta(days=i+1)
                            task_date = last_date + delta
                            self.generate_single_task(
                                task_date, gen_id, *generator[3:])
            elif gen_type == Generators.Monthly:
                logging.info("The generator is: {}".format(gen_type))
                if not last_date:
                    logging.info("The generator is new!")
                    task_date = datetime.date(today.year, today.month, rate)
                    if task_date <= today:
                        self.generate_single_task(
                            task_date, gen_id, *generator[3:])
                else:
                    logging.info("The generator is old!")
                    logging.info("last date {}:".format(last_date))
                    months = relativedelta(today, last_date).months
                    logging.info("Difference: {}".format(months))
                    for i in range(abs(months)):
                        task_date = datetime.date(
                            last_date.year, last_date.month, rate)
                        delta = relativedelta(months=i+1)
                        task_date = task_date + delta
                        logging.info("New task date is {}:".format(task_date))
                        if task_date <= today:
                            logging.info("Generating task for  {}:"
                                         .format(task_date))
                            self.generate_single_task(
                                task_date, gen_id, *generator[3:])
        logging.info("Done generating!\n")

    def generate_single_task(self, baseline_date, gen_id,
                             text, project, stage, valid_days, deadline_days):
        valid = None
        deadline = None
        today = datetime.date.today()
        if valid_days != '' and valid_days is not None:
            valid = baseline_date + datetime.timedelta(days=valid_days)
        if deadline_days != '' and deadline_days is not None:
            deadline = baseline_date + datetime.timedelta(days=deadline_days)
        task_id = self.__storage.add_task(text, project, stage, valid, deadline,
                                          gen_id, baseline_date)
        if (valid is None or valid >= today) \
                and not (stage == Stages.Done and baseline_date < today):
            self.__insert_task(task_id, project, stage, text, valid, deadline)


class TaskListModel(QAbstractListModel):
    """
    The upper level of task pool model.
    """

    taskMoved = pyqtSignal(int, Stages, Projects)

    def __init__(self, stage, project, pool):
        super(TaskListModel, self).__init__()
        self.tasks = []
        self.stage = stage
        self.project = project
        self.pool = pool
        self.pool.taskAdded.connect(self.onItemAdded)
        self.pool.taskDropped.connect(self.onItemDropped)
        self.taskMoved.connect(self.pool.onTaskMoved)

    def onItemAdded(self, task_id, stage, project):
        if self.stage == stage and self.project == project:
            self.insertRows(0, 1)
            self.setData(self.index(0), task_id)

    def onItemDropped(self, task_id, stage, project):
        if self.stage == stage and self.project == project:
            # self.tasks.remove(task_id)
            index = self.tasks.index(task_id)
            self.removeRows(index, 1)

    def get_id(self, row):
        return self.tasks[row]

    # Basic methods

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.tasks)

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()

        if role == Qt.ToolTipRole:
            task_id = self.tasks[index.row()]
            text, *rest, valid, deadline = self.pool.get_task_stats_by_id(task_id)
            today = datetime.date.today()
            if deadline:
                text = " ".join((text, "D:", str(deadline)))
            if valid:
                text = " ".join((text, "V:", str(valid)))
            return QVariant(text)

        elif role != Qt.DisplayRole:
            return QVariant()

        task_id = self.tasks[index.row()]
        text = self.pool.get_task_name_by_id(task_id)
        if len(text) > 23:
            text = text[:20] + " ..."
        return QVariant(text)

    # Editable model methods

    def setData(self, index, value, role=None):
        if index.isValid():
            self.tasks[index.row()] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def insertRows(self, position, rows, parent=QModelIndex(), *args, **kwargs):
        self.beginInsertRows(parent, position, position + rows - 1)
        for i in range(rows):
            self.tasks.insert(position, 0)
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=QModelIndex(), *args, **kwargs):
        self.beginRemoveRows(parent, position, position + rows - 1)
        for i in range(rows):
            self.tasks.pop(position)
        self.endRemoveRows()
        return True

    # Drag and Drop methods

    def supportedDropActions(self):
        return Qt.MoveAction

    def supportedDragActions(self):
        return Qt.MoveAction

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled | Qt.ItemIsDropEnabled
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | \
               Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled

    def mimeTypes(self):
        return ["text/plain"]

    def mimeData(self, indices):
        index = indices[0]
        mimedata = QMimeData()
        task_id = self.get_id(index.row())
        mimedata.setText(str(task_id))
        return mimedata

    def dropMimeData(self, mime, action, row, column, index):
        if action == Qt.IgnoreAction:
            return True

        task_id = int(mime.text())
        row = index.row()
        if row == -1:
            row = 0
        self.insertRows(row, 1)
        self.setData(self.index(row), task_id)
        self.taskMoved.emit(task_id, self.stage, self.project)
        return True


class TaskListView(QListView):
    dropTaskSignal = pyqtSignal(int)

    def __init__(self):
        super(TaskListView, self).__init__()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            if self.currentIndex() != -1:
                row = self.currentIndex().row()
                model = self.model()
                task_id = model.get_id(row)
                self.dropTaskSignal.emit(task_id)


class MainWindow(Ui_MainWindow, QMainWindow):

    def __init__(self, storage):
        super(MainWindow, self).__init__()

        #
        self.storage = storage
        self.taskpool = TaskPool(storage)

        # Set up the user interface
        self.setupUi(self)

        self.setObjectName(config.appname)
        self.resize(800, 600)
        self.setMinimumSize(QSize(800, 600))

        # Connect signals and slots
        self.actionNew.triggered.connect(self.add_new_task)
        self.actionManage.triggered.connect(self.manage_patterns)
        self.actionReport.triggered.connect(self.report)

        # Set headers for Stages
        for i, stage in enumerate(Stages):
            name = QLabel()
            name.setText(stage.value)
            self.tasks.addWidget(name, 0, i + 1)
        # Set headers for Projects
        for j, project in enumerate(Projects):
            name = QLabel()
            name.setText(project.value)
            self.tasks.addWidget(name, j + 1, 0)
        # Create models for tasks and show their views
        for i, stage in enumerate(Stages):
            for j, project in enumerate(Projects):
                model = TaskListModel(stage, project, self.taskpool)

                listview = TaskListView()
                listview.setModel(model)
                # Enable drag and drop
                listview.setSelectionMode(QAbstractItemView.SingleSelection)
                listview.setDragEnabled(True)
                listview.setAcceptDrops(True)
                listview.setDropIndicatorShown(True)

                self.tasks.addWidget(listview, j + 1, i + 1)

                listview.doubleClicked.connect(self.edit_task)
                listview.dropTaskSignal.connect(self.taskpool.drop_task)

        self.load_initial_values()

    def load_initial_values(self):
        self.taskpool.load()
        self.taskpool.generate_new_tasks()

    def add_new_task(self):
        # Fire up widget
        task_manager = TaskEdit()
        task_manager.taskCreated.connect(self.taskpool.add_task)
        self.menuBar.setEnabled(False)

        task_manager.exec_()

        self.menuBar.setEnabled(True)

    def edit_task(self, model_index):
        model = model_index.model()
        row = model_index.row()
        task_id = model.get_id(row)

        # Fire up widget
        task_manager =\
            TaskEdit(task_id, *self.taskpool.get_task_stats_by_id(task_id))
        task_manager.taskEdited.connect(self.taskpool.edit_task)
        self.menuBar.setEnabled(False)

        task_manager.exec_()

        self.menuBar.setEnabled(True)

    def manage_patterns(self):
        generator_manager = GenManager(self.storage)
        generator_manager.generatorChanged.connect(
            self.taskpool.generate_new_tasks)
        self.menuBar.setEnabled(False)

        generator_manager.exec_()

        self.menuBar.setEnabled(True)

    def report(self):
        report = Report(self.storage)

        self.menuBar.setEnabled(False)

        report.exec_()

        self.menuBar.setEnabled(True)


if __name__ == "__main__":
    log_name = os.path.join(app_data_path, config.log)

    logging.basicConfig(
        filename=log_name,
        format='%(asctime)s %(message)s',
        level=logging.ERROR)
        # level=logging.INFO)
    logging.info("app_data_path:" + app_data_path)

    try:
        app = QApplication(sys.argv)

        storage = storage.Storage(os.path.join(app_data_path, config.dbname))
        form = MainWindow(storage)

        form.showMaximized()

        sys.exit(app.exec_())

    except Exception as e:
        logging.exception(e)