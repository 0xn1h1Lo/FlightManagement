import sqlite3

# Define DBOperation class to manage all data into the database.
# Give a name of your choice to the database

import db_objects, queries

class DBOperations:

    @staticmethod
    def pprint(results="", headers=""):
        if headers:
            print(" | ".join(str(col[0]) for col in headers))
        if results:
            for row in results:
                print(" | ".join(str(cell) for cell in row))

    # helper methods
    def sql_run_script(self, script, table_firsttime=False):
        with open(script, "r") as file:
            self.conn.executescript(file.read())

    def get_connection(self):
        self.conn = sqlite3.connect(self.database)
        if self.pragma:
            self.conn.execute("PRAGMA foreign_keys = ON")  # This seems to be if in schema.sql
        self.cursor = self.conn.cursor()

    # creates the database object with custom path and SQL script
    def __init__(self, database, script="", seed_data=""):
        try:
            self.database = database
            self.pragma = True
            self.get_connection()
            if script:
                self.sql_run_script(script)
            if seed_data:
                self.sql_run_script(seed_data)
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    # Decorator to reuse try, except, finally pattern, not using @functools.wraps
    def db_operation(function):
        def wrapper(self, *args, **kwargs):
            try:
                self.get_connection()
                res = function(self, *args, **kwargs)
                return res
            except Exception as e:
                print(e)
            finally:
                self.conn.close()
        return wrapper

    @db_operation
    def select_all(self, db_object):
        # TODO: validate tables in a predefined list of views if user input later
        self.cursor.execute(queries.gen_select_all(db_object.table))
        results = self.cursor.fetchall()
        # if view changes, check the columns in the view definition matches the fields in db_objects
        res = [db_object(*result) for result in results]
        return res
    
    # data is a tuple of values, one for each attribute of the object
    @db_operation
    def insert_data(self, db_object):
        data = db_object.sql_ready()  # key is the table and value is the tuple of user data
        for key in data:
            # generate an INSERT statement with as many '?' as elements in the tuple and insert
            self.cursor.execute(queries.gen_insert_data(key, len(data[key])), data[key])
        self.conn.commit()
        print("Inserted data successfully")

    @db_operation
    def search_column(self, db_object, col_name, search_value):
        self.cursor.execute(queries.gen_search_column(db_object.table, col_name), (search_value,))
        results = self.cursor.fetchall()
        res = [db_object(*result) for result in results]
        return res
    
    @db_operation
    def update_data(self, db_object, set_col_name, where_col_name, set_value, where_value):
        self.cursor.execute(queries.gen_update_data(db_object.table, set_col_name, where_col_name), (set_value, where_value))
        if (num := self.cursor.rowcount) != 0:
            print(str(num) + " row(s) updated.")
        else:
            print("Cannot find this record in the database")
        self.conn.commit()

    @db_operation
    def delete_data(self, db_object, col_name, search_value):
        self.cursor.execute(queries.gen_delete_data(db_object.table, col_name), (search_value,))
        if (num := self.cursor.rowcount) != 0:
            print(str(num) + " row(s) deleted.")
        else:
            print("Cannot find this record in the database")
        self.conn.commit()

    @db_operation
    def drop_table(self, db_object):
        self.cursor.execute(queries.gen_drop_table(db_object.table))
        print("Table dropped")

    @db_operation
    def run_command(self, command):
        self.cursor.execute(command)
        if self.cursor.description is not None:
            headers = [element[0] for element in self.cursor.description]
            results = self.cursor.fetchall()
            db_objects.pprint_table(results, headers)
        else:
            self.conn.commit()
            print("Success!")