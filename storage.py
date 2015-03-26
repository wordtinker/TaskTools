import sqlite3
import datetime

import enums


class Storage:
    def __init__(self, db_path):
        self.db_path = db_path
        # Adding support for custom types in DB.
        self.db_conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        sqlite3.register_adapter(enums.Projects, enums.adapt_enum)
        sqlite3.register_converter(
            "PROJECT", enums.convert_enum(enums.Projects))
        sqlite3.register_adapter(enums.Stages, enums.adapt_enum)
        sqlite3.register_converter(
            "STAGE", enums.convert_enum(enums.Stages))
        sqlite3.register_adapter(enums.Generators, enums.adapt_enum)
        sqlite3.register_converter(
            "GENERATOR", enums.convert_enum(enums.Generators))

        # Initialize tables
        self.db_cursor = self.db_conn.cursor()
        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS Tasks(
        taskid INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        project PROJECT,
        valid DATE,
        deadline DATE,
        generated_by INTEGER)""")
        self.db_conn.commit()

        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS TimeLog(
        stage STAGE,
        date DATE,
        task INTEGER,
        FOREIGN KEY(task) REFERENCES Tasks(taskid) ON DELETE CASCADE)""")
        self.db_conn.commit()

        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS Generators(
        genid INTEGER PRIMARY KEY AUTOINCREMENT,
        type GENERATOR,
        day INTEGER,
        text TEXT,
        project PROJECT,
        stage STAGE,
        valid INTEGER,
        deadline INTEGER
        )""")
        self.db_conn.commit()

        # Enabling foreign key support
        self.db_cursor.execute("""
        PRAGMA foreign_keys = ON
        """)
        self.db_conn.commit()

    def add_task(self, text, project, stage, valid, deadline,
                 gen_id=None, date=None):
        db_cursor = self.db_conn.cursor()

        db_cursor.execute("""INSERT INTO Tasks(text, project, valid,
        deadline, generated_by)
        VALUES(?,?,?,?,?)
        """, (text, project, valid, deadline, gen_id))
        self.db_conn.commit()
        rowid = db_cursor.lastrowid

        self.set_new_stage(rowid, stage, date)

        return rowid

    def add_generator(self, gen_type, shift, text, project, stage,
                      valid, dealine):

        db_cursor = self.db_conn.cursor()

        db_cursor.execute("""INSERT INTO Generators(type, day, text, project,
        stage, valid, deadline)
        VALUES(?,?,?,?,?,?,?)
        """, (gen_type, shift, text, project, stage, valid, dealine))
        self.db_conn.commit()
        gen_id = db_cursor.lastrowid

        return gen_id

    def select_tasks_for_today(self):
        """
        Returns tasks that fit for today.
        1) valid for today
        2) not completed before today
        3) returned stage is the latest stage for the task
        """
        today = datetime.date.today()
        db_cursor = self.db_conn.cursor()
        db_cursor.execute("""SELECT
        m1.task, t.project, m1.stage, t.text, t.valid, t.deadline
        FROM Timelog m1
        LEFT JOIN TimeLog m2 ON (m1.task = m2.task AND m1.rowid < m2.rowid)
        INNER JOIN Tasks t ON m1.task=t.taskid
        WHERE m2.rowid IS NULL
        AND (t.valid >= ? OR t.valid is NULL)
        AND NOT (m1.stage = ? AND m1.date < ?)""",
                          (today, enums.Stages.Done, today))
        return db_cursor.fetchall()

    def select_tasks_for_report(self, start, finish):
        """
        1) valid in between start and finish date
        2) not completed before the start date
        3) not later than finished date
        4) returned stage is the latest stage for the task
        """
        db_cursor = self.db_conn.cursor()
        db_cursor.execute("""SELECT
        m1.task, t.text, t.project, m1.stage, m1.date, t.valid, t.deadline
        FROM ( SELECT * FROM TimeLog
               WHERE date <=:finish
               GROUP BY task) m1
        INNER JOIN Tasks t ON m1.task=t.taskid
        AND (t.valid >=:start OR t.valid is NULL)
        AND NOT (m1.stage =:done AND m1.date <:start)
        """, {"start": start, "finish": finish, "done": enums.Stages.Done})
        return db_cursor.fetchall()

    def select_stages(self, task, finish, stage):
        """
        Returns stages for a given task excluding the given stage
        and before the finish date.
        """
        db_cursor = self.db_conn.cursor()
        db_cursor.execute("""SELECT
        stage, date FROM TimeLog
        WHERE task=:task
        AND date <=:finish
        AND stage <>:stage
        """, {"task": task, "finish": finish, "stage": stage})
        return db_cursor.fetchall()

    def select_generators(self):
        db_cursor = self.db_conn.cursor()
        db_cursor.execute("""SELECT *
        FROM Generators
        """, ())
        return db_cursor.fetchall()

    def get_last_generated_date(self, gen_id):
        """
        Finds the list of dates where tasks has been generated,
        return the last such date.
        :param gen_id:
        :return:
        """
        db_cursor = self.db_conn.cursor()
        db_cursor.execute("""SELECT
        MAX(m1.date)
        FROM Timelog m1
        LEFT JOIN TimeLog m2 ON (m1.task = m2.task AND m1.rowid > m2.rowid)
        INNER JOIN Tasks t ON m1.task=t.taskid
        WHERE m2.rowid IS NULL
        AND t.generated_by=?
        """, (gen_id, ))
        # Converting to datetime type because MAX() breaks the custom adapter.
        last_date = db_cursor.fetchone()[0]
        if last_date:
            last_date = last_date.split('-')
            last_date = [int(x) for x in last_date]
            last_date = datetime.date(*last_date)
        return last_date

    def update_generator(self, gen_id, gen_type, shift, text, project, stage,
                      valid, dealine):
        db_cursor = self.db_conn.cursor()
        db_cursor.execute("""UPDATE Generators
        SET type=?, day=?, text=?, project=?, stage=?, valid=?, deadline=?
        WHERE genid=?
        """, (gen_type, shift, text, project, stage, valid, dealine, gen_id))
        self.db_conn.commit()

    def set_new_stage(self, rowid, stage, date=None):
        if not date:
            date = datetime.date.today()
        db_cursor = self.db_conn.cursor()
        db_cursor.execute("""INSERT INTO Timelog
        VALUES(?,?,?)
        """, (stage, date, rowid))
        self.db_conn.commit()

    def set_new_project(self, rowid, project):
        db_cursor = self.db_conn.cursor()
        db_cursor.execute("""UPDATE Tasks
        SET project=?
        WHERE taskid=?
        """, (project, rowid))
        self.db_conn.commit()

    def set_new_stats(self, rowid, text, project, valid, deadline):
        db_cursor = self.db_conn.cursor()
        db_cursor.execute("""UPDATE Tasks
        SET project=?, text=?, valid=?, deadline=?
        WHERE taskid=?
        """, (project, text, valid, deadline, rowid))
        self.db_conn.commit()

    def delete_task(self, rowid):
        db_cursor = self.db_conn.cursor()
        db_cursor.execute("""DELETE FROM Tasks
        WHERE taskid=?
        """, (rowid, ))
        self.db_conn.commit()

    def delete_generator(self, gen_id):
        db_cursor = self.db_conn.cursor()
        db_cursor.execute("""DELETE FROM Generators
        WHERE genid=?
        """, (gen_id, ))
        self.db_conn.commit()