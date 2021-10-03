import sqlite3


def pat_insert(no, name, adr, city, state, con, gen, file, date, dob):
    """
    Function to insert details in Patient.db
    :param no: Patient Id
    :param name: Name of Patient
    :param adr: Address of Patient
    :param city: City Name
    :param state: State Name
    :param con: Concern
    :param gen: Gender
    :param file: Attachments
    :param date: Date of Registering
    :param dob: Date of Birth
    :return:
    """
    sql = """
        INSERT INTO Patient(no, name, address, gender, city, state, concern, att, date, dob, complete) VALUES('%s','%s', '%s',
        '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s)""" % (no, name, adr, gen, city, state, con, file, date, dob, 0)
    execute_query(sql)


def pat_search(key):
    """
    To search Patient Id
    :param key:
    :return:
    """
    s_key = "%" + key + "%"
    sql1 = """
            SELECT name FROM Patient WHERE no LIKE '%s' ORDER BY date""" % s_key
    sql2 = """
            SELECT date FROM Patient WHERE no LIKE '%s' ORDER BY date""" % s_key
    sql3 = """
            SELECT no FROM Patient WHERE no LIKE '%s' ORDER BY date""" % s_key
    return execute_query(sql1).fetchall(), execute_query(sql2).fetchall(), execute_query(sql3).fetchall()


def pat_search_ac(key, no):
    """
    To search Patient Id for Active and Complete Cases
    :param key:
    :param no:
    :return:
    """
    s_key = "%" + key + "%"
    sql1 = """
            SELECT name FROM Patient WHERE no LIKE '%s' AND complete=%s""" % (s_key, no)
    sql2 = """
            SELECT date FROM Patient WHERE no LIKE '%s' AND complete=%s""" % (s_key, no)
    sql3 = """
            SELECT no FROM Patient WHERE no LIKE '%s' AND complete=%s""" % (s_key, no)
    return execute_query(sql1).fetchall(), execute_query(sql2).fetchall(), execute_query(sql3).fetchall()


def pat_get():
    """
    Get Patient Details by Date Order
    :return:
    """
    sql1 = """
        SELECT no FROM Patient ORDER BY date"""
    sql2 = """
            SELECT name FROM Patient ORDER BY date"""
    sql3 = """
            SELECT date FROM Patient ORDER BY date"""
    no = execute_query(sql1)
    name = execute_query(sql2)
    date = execute_query(sql3)
    return no.fetchall(), name.fetchall(), date.fetchall()


def pat_get_act(no):
    """
    Getting Active Patients using Patient Id
    :param no: Patient Id
    :return:
    """
    sql1 = """
            SELECT no FROM Patient WHERE complete=%s""" % no
    sql2 = """
                SELECT name FROM Patient WHERE complete=%s""" % no
    sql3 = """
                SELECT date FROM Patient WHERE complete=%s""" % no
    no = execute_query(sql1)
    name = execute_query(sql2)
    date = execute_query(sql3)
    return no.fetchall(), name.fetchall(), date.fetchall()


def pat_details(no):
    """
    Getting Patient Details using Patient Id
    :param no:
    :return:
    """
    sql1 = """
            SELECT name FROM Patient WHERE no='%s'""" % no
    sql2 = """
            SELECT gender FROM Patient WHERE no='%s'""" % no
    sql3 = """
            SELECT city FROM Patient WHERE no='%s'""" % no
    sql4 = """
            SELECT concern FROM Patient WHERE no='%s'""" % no
    sql5 = """
            SELECT att FROM Patient WHERE no='%s'""" % no
    sql6 = """
            SELECT date FROM Patient WHERE no='%s'""" % no
    sql7 = """
            SELECT dob FROM Patient WHERE no='%s'""" % no
    sql8 = """
            SELECT complete FROM Patient WHERE no='%s'""" % no
    return execute_query(sql1).fetchall(), execute_query(sql2).fetchall(), execute_query(sql3).fetchall(), \
        execute_query(sql4).fetchall(), execute_query(sql5).fetchall(), execute_query(sql6).fetchall(), \
        execute_query(sql7).fetchall(), execute_query(sql8).fetchall()


def pat_comp(no):
    """
    Marking Patient Case as Complete
    :param no:
    :return:
    """
    sql = """
            UPDATE Patient 
            SET complete = 1
            WHERE no='%s'
            """ % no
    execute_query(sql)


def pat_dashboard(no):
    """
    Getting Details for Patient Dashboard
    :param no:  Patient Id
    :return:
    """
    sql1 = """
            SELECT date FROM Patient WHERE no='%s'""" % no
    sql2 = """
            SELECT att FROM Patient WHERE no='%s'""" % no
    sql3 = """
            SELECT concern FROM Patient WHERE no='%s'""" % no
    return execute_query(sql1).fetchall(), execute_query(sql2).fetchall(), execute_query(sql3).fetchall()


def pat_login(no):
    """
    Getting DOB of Patient
    :param no: Patient Id
    :return:
    """
    sql = """
        SELECT dob FROM Patient WHERE no='%s'""" % no
    return execute_query(sql).fetchall()


def rep_insert(no, file, date):
    """
    Inserting the File Names uploaded by Patient in Database
    :param no: Patient Id
    :param file: File Name
    :param date: Date of Uploading
    :return:
    """
    sql = """
            INSERT INTO Report(no, att, date) VALUES('%s','%s', '%s')""" % (no, file, date)
    execute_query1(sql)


def rep_get(no):
    """
    Getting the File Names of the Patient
    :param no: Patient Id
    :return:
    """
    sql1 = """
            SELECT att FROM Report WHERE no='%s'""" % no
    sql2 = """
            SELECT date FROM Report WHERE no='%s'""" % no
    return execute_query1(sql1).fetchall(), execute_query1(sql2).fetchall()


def case_add():
    """
    Updating the Case Status in Dashboard
    :return:
    """
    sql1 = """
        UPDATE Cases 
        SET active = active + 1
        """
    sql2 = """
        UPDATE Cases 
        SET total = total + 1
        """
    execute_query2(sql1)
    execute_query2(sql2)


def case_comp():
    """
    Marking Case as Complete
    :return:
    """
    sql1 = """
            UPDATE Cases 
            SET active = active - 1
            """
    sql2 = """
            UPDATE Cases 
            SET complete = complete + 1
            """
    execute_query2(sql1)
    execute_query2(sql2)


def case_get():
    """
    Getting the Active and Completed Cases from the Database
    :return:
    """
    sql1 = """
                SELECT active FROM Cases """
    sql2 = """
                SELECT complete FROM Cases """
    sql3 = """
                SELECT total FROM Cases """
    return execute_query2(sql1).fetchall(), execute_query2(sql2).fetchall(), execute_query2(sql3).fetchall()


def execute_query(sql_query):
    """
    To execute the Query of Patient.db
    :param sql_query: Sql Statements
    :return: The Selected Columns and Rows form Database
    """
    with sqlite3.connect("patient.db") as conn:
        cur = conn.cursor()
        result = cur.execute(sql_query)
        conn.commit()
    return result


def execute_query1(sql_query):
    """
    To execute the Query of Report.db
    :param sql_query: Sql Statements
    :return: The Selected Columns and Rows form Database
    """
    with sqlite3.connect("report.db") as conn:
        cur = conn.cursor()
        result = cur.execute(sql_query)
        conn.commit()
    return result


def execute_query2(sql_query):
    """
    To execute the Query of Cases.db
    :param sql_query: Sql Statements
    :return: The Selected Columns and Rows form Database
    """
    with sqlite3.connect("case.db") as conn:
        cur = conn.cursor()
        result = cur.execute(sql_query)
        conn.commit()
    return result
