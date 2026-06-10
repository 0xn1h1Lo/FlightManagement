# Queries Library

def gen_select_all(table):
    sql_select_all = f"""
        SELECT *
        FROM {table}
    """
    return sql_select_all

def gen_insert_data(table, col_number):
    slots = ", ".join("?" * col_number)
    sql_insert_data = f"""
        INSERT INTO {table}
        VALUES ({slots})
    """
    return sql_insert_data

def gen_search_column(table, col_name):
    sql_search_person = f"""
        SELECT *
        FROM {table}
        WHERE {col_name} = ?
    """
    return sql_search_person

def gen_update_data(table, set_col_name, where_col_name):
    sql_update_data = f"""
        UPDATE {table}
        SET {set_col_name} = ?
        WHERE {where_col_name} = ?
    """
    return sql_update_data

def gen_delete_data(table, col_name):
    sql_delete_data = f"""
        DELETE FROM {table}
        WHERE {col_name} = ?
    """
    return sql_delete_data

def gen_drop_table(table):
    sql_drop_table = f"""
        DROP TABLE {table};
    """
    return sql_drop_table

# Specific queries

query_info_pilots = f"""
SELECT 
    pil_id,
    first_name,
    last_name,
    DOB,
    email,
    phone_num,
    flight_total,
    flying_time_min / 60 AS flight_time_hrs
FROM people 
    JOIN (
        SELECT pil_id, count(*) AS flight_total
        FROM legs
            NATURAL JOIN manifests 
            GROUP BY pil_id
    ) ON pil_id = person_id
    NATURAL JOIN pilots
"""

query_mvt_airports = f"""
SELECT
    airport,
    takeoffs,
    landings,
    takeoffs + landings AS movements
FROM (
    SELECT orig AS airport, count(*) AS takeoffs
    FROM legs
    GROUP BY orig
) 
    NATURAL JOIN (
        SELECT dest AS airport, count(*) AS landings
        FROM legs
        GROUP BY dest
    );
"""

query_info_planes = f"""
SELECT * 
FROM planes
    NATURAL JOIN plane_models
    NATURAL JOIN (
        SELECT reg, round(sum((julianday(ATA) - julianday(STD)) * 24 * 60)) AS flying_time_min
        FROM legs 
        GROUP BY reg
    );
"""