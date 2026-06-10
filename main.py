import sqlite3, pathlib, sys
import db_objects, db_operations

from queries import query_info_pilots
from queries import query_mvt_airports
from queries import query_info_planes

# Helpers
def check_valid_name(string):
    if not string.isidentifier():
        print("Invalid Input")
        raise ValueError("The column name characters are alphanumerical and '_'")
    
def select_base_class(string):
    __choice = int(input(f"> {string}:\n"
                        "[1. people] [2. plane_models] [3. destinations] [4. flights] [5. pilots]\n"
                        "[6. planes] [7. crew] [8. certifications] [9. manifests] [10. crew_manifests]\n"
                        "[11. passenger_manifests] [12. legs]? "
                        "Number: "))
    print()
    __choice -= 1
    if __choice < 0:
        raise ValueError("list index out of range")
    cls = [db_objects.people, db_objects.plane_models, db_objects.destinations, db_objects.flights, db_objects.pilots, db_objects.planes, 
           db_objects.crew, db_objects.certifications, db_objects.manifests, db_objects.crew_manifests, db_objects.passenger_manifests,
           db_objects.legs][__choice]
    
    return cls

def select_view_class():
    __choice = int(input("> Which table do you want to see or search: "
                         "[1. pilots] [2. manifests] [3. destinations] [4. planes] [5. flights]? "
                         "Number: "))
    print()
    __choice -= 1
    if __choice < 0:
        raise ValueError("list index out of range")
    cls = [db_objects.Pilot, db_objects.Manifest, db_objects.Destination, db_objects.Plane, db_objects.Flight][__choice]

    return cls

# Functions for the menu

def create_table(db, db_path):
    if input("> Do you also want to seed the table with test data? [Yy]es or enter: ").lower().startswith("y"):
        db = db_operations.DBOperations(db_path, script="schema.sql", seed_data="seed_data.sql")
    else:
        db = db_operations.DBOperations(db_path, script="schema.sql")

def insert_views(db):
    cls = select_view_class()
    # hack because Manifest is too troublesome in db_objects
    if cls == db_objects.Manifest:
        cls = db_objects.manifests
    elif cls == db_objects.Pilot:
        print("! A new pilot can be entered without certification if that is left blank")
        print("! To add a new certification, leave all fields blank except pil_id and model")
    object = db_objects.make_object(cls)
    db.insert_data(object)

def insert_data(db):
    cls = select_base_class("In which table do you want to insert data?")
    object = db_objects.make_object(cls)
    db.insert_data(object)

# Select all data from the views defined in the database
def select_all_data(db):
    cls = select_view_class()
    objects = db.select_all(cls)
    db_objects.pprint_db_objects(objects)

def search_views(db):
    cls = select_view_class()
    db_objects.list_headers(cls)

    col_name = input("> Type in the column name of the search criteria: ")
    check_valid_name(col_name)
    search_value = input("> Type in the search value: ")
    print()

    objects = db.search_column(cls, col_name, search_value)
    db_objects.pprint_db_objects(objects)

def update_data(db):
    cls = select_base_class("In which table do you want to update data?")
    db_objects.list_headers(cls)

    where_col_name = input("> Type in the column name of the search criteria: ")
    check_valid_name(where_col_name)
    where_value = input("> Type in the search value: ")
    set_col_name = input("> Type in the column in which the value will change: ")
    check_valid_name(set_col_name)
    set_value = input("> Type in the new value: ")
    print()
    
    db.update_data(cls, set_col_name, where_col_name, set_value, where_value)

def delete_data(db):
    cls = select_base_class("In which table do you want to delete data?")
    db_objects.list_headers(cls)

    col_name = input("> Type in the column name of the search criteria for deletion: ")
    check_valid_name(col_name)
    search_value = input("> Type in the search value for deletion: ")
    print()
    
    db.delete_data(cls, col_name, search_value)

def enter_arrival_time(db):
    cls = db_objects.legs
    where_col_name = "fli_num"
    where_value = input("> Type in the flight number: ")
    set_col_name = "ATA"
    set_value = input("> Type in the actual time of arrival: ")
    print()
    
    db.update_data(cls, set_col_name, where_col_name, set_value, where_value)

# Ready-made queries are directly imported into this file
def extra_queries_submenu(db):

    print("\n *******************")
    print(" ** Extra Queries **")
    print(" *******************")
    print(" 01. Detailed information on the pilots")
    print(" 02. Movement report by airport")
    print(" 03. Flight time for each plane")
    print()

    __choose_submenu = int(input("> Enter your choice. Number: "))
    match __choose_submenu:
        case 1:
            db.run_command(query_info_pilots)
        case 2:
            db.run_command(query_mvt_airports)
        case 3:
            db.run_command(query_info_planes)
        case _:
            print("Invalid Choice")
            return 1

# Ready-made queries are directly imported into this file
def shortcuts_submenu(db):

    print("\n *************************************")
    print(" ** Most frequently used operations **")
    print(" *************************************")
    print(" 01. Enter arrival time for a flight")
    print()

    __choose_submenu = int(input("> Enter your choice. Number: "))
    match __choose_submenu:
        case 1:
            enter_arrival_time(db)
        case _:
            print("Invalid Choice")
            return 1

# TODO: drop table, alter table
def admin_submenu(db):

    print("\n ****************")
    print(" ** Admin Menu **")
    print(" ****************")
    print(" 01. Drop a table or a view")
    print(" 02. Run a one-liner SQL query")
    print(" 03. Turn off foreign key constraints")
    print(" 04. Turn on foreign key constraints (default)")
    print()

    __choose_submenu = int(input("> Enter your choice. Number: "))
    match __choose_submenu:
        case 1:
            cls = select_base_class("Which table do you want to drop?")
            db.drop_table(cls)
        case 2:
            command = input("Run a SQL command: ")
            print()
            db.run_command(command)
        case 3:
            db.pragma = False
        case 4:
            db.pragma = True
        case _:
            print("Invalid Choice")
            return 1

def main():

    db_path = "airline.sqlite3"
    if not pathlib.Path(db_path).is_file():
        print("Database not found, do you want to create it? "
              "If yes, enter a name, to use default leave blank.")
        name = input("> Enter a name: ")
        if name:
            db_path = name
            
    db = db_operations.DBOperations(db_path)

    while True:
        print("\n *********************")
        print(" ** FlightInfo Menu **")
        print(" *********************")
        print(" 01. Create database FlightInfo")
        print(" 02. Insert data into a View")
        print(" 03. Display all data in a View")
        print(" 04. Search for data in a View")
        print(" 05. Insert data in a base table")
        print(" 06. Update data in a base table")
        print(" 07. Delete data in a base table")
        print(" 08. Extra specific queries (submenu)")
        print(" 09. Most frequently used operations (submenu)")
        print(" *** Admin area ***")
        print(" 99. Admin commands (submenu)")
        print(" 00. Exit\n")

        try:
            __choose_menu = int(input("> Enter your choice. Number: "))
            match __choose_menu:
                case 1:
                    create_table(db, db_path)
                case 2:
                    insert_views(db)
                case 3:
                    select_all_data(db)
                case 4:
                    search_views(db)
                case 5:
                    insert_data(db)
                case 6:
                    update_data(db)
                case 7:
                    delete_data(db)
                case 8:
                    extra_queries_submenu(db)
                case 9:
                    shortcuts_submenu(db) 
                case 99:
                    admin_submenu(db)
                case 0:
                    print("Leaving the program... Bye!")
                    break
                case _:
                    print("Invalid Choice")
        except Exception as e:
            print("ERROR:", e)
            continue

    # Cleaning up since db = db_operations.DBOperations(db_path) creates a file even it no data has been entered
    file = pathlib.Path(db_path)
    if file.exists() and file.stat().st_size == 0:
        file.unlink()

if __name__ == "__main__":
    sys.exit(main())
