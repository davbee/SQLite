# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 16:14:20 2022

@author: DB

Create SQLite3 databases; then insert database2 after database1
"""

# Import module
import sqlite3

import numpy as np
import pandas as pd


# import os
# import re
# -----------------------------------------------------------------------------
# Generate data
# -----------------------------------------------------------------------------
def randb() -> None:
    # generate seeded random data matrix1
    r = 10
    c = 23
    np.random.seed(seed=np.random.randint(100))
    matrix1 = np.random.randint(100, size=(r, c))

    # generate seeded random data matrix2
    np.random.seed(seed=np.random.randint(100))
    matrix2 = np.random.randint(100, size=(r, c))

    # convert numpy 2D array to Pandas dataframe
    df1 = pd.DataFrame(matrix1)
    df2 = pd.DataFrame(matrix2)

    print("Random Dataset #1:")
    print(df1)
    print("\nRandom Dataset #2:")
    print(df2)

    # convert Pandas dataframe to list of tuple for inserting into database
    record1 = [tuple(i) for i in df1.values.tolist()]
    record2 = [tuple(i) for i in df2.values.tolist()]
    # -----------------------------------------------------------------------------

    # -----------------------------------------------------------------------------
    # Create SQLite3 database
    # -----------------------------------------------------------------------------
    # Connecte to sqlite
    conn = sqlite3.connect("Random.db")  # create a database file
    # conn = sqlite3.connect(':memory:')  # create a database in memory

    # Create a cursor object using the cursor() method
    cursor = conn.cursor()

    # Create a table called randMat (Random Matrix)
    tablename = "randMat"

    # createtable = '''
    # CREATE TABLE IF NOT EXISTS %s (
    #           C00             INTEGER key,
    #           C01           INTEGER,
    #           C02            INTEGER,
    #           C03              INTEGER,
    #           C04              INTEGER,
    #           C05          INTEGER,
    #           C06             INTEGER,
    #           C07             INTEGER,
    #           C08              INTEGER,
    #           C09               INTEGER,
    #           C10             INTEGER,
    #           C11               INTEGER,
    #           C12        INTEGER,
    #           C13 INTEGER,
    #           C14         INTEGER,
    #           C15         INTEGER,
    #           C16              INTEGER,
    #           C17              INTEGER,
    #           C18         INTEGER,
    #           C19              INTEGER,
    #           C20             INTEGER,
    #           C21            INTEGER,
    #           C22              INTEGER
    #           )
    #           ''' % tablename

    # programmatically create column names
    col1 = tuple(["C" + str(i) + " INTEGER" for i in range(c)])
    col2 = ",".join(col1)
    # col = "(%s)" % col2
    col = f"({col2})"

    # assemble SQL command for creating Table Name
    # createtable = "CREATE TABLE IF NOT EXISTS %s " % tablename + col
    createtable = f"CREATE TABLE IF NOT EXISTS {tablename + col} "

    # execute SQL command for creating Table Name
    cursor.execute(createtable)

    # -----------------------------------------------------------------------------
    # Create as many '?,' as there are fields in the table
    # -----------------------------------------------------------------------------
    def fieldnum(a, w) -> str:
        return a.join([a + "?," for i in range(w)])[:-1]

    a = fieldnum("", c)

    # -----------------------------------------------------------------------------
    # Insert OT data into the table with one-shot
    # -----------------------------------------------------------------------------
    # cursor.executemany('INSERT INTO '+tablename+' VALUES(?,?,?,?,?,?,?,?,?,?,
    # ?,?,?,?,?,?,?,?,?,?,?,?,?);',record1);
    cursor.executemany("INSERT INTO " + tablename + " VALUES(" + a + ");",
                       record1)
    cursor.executemany("INSERT INTO " + tablename + " VALUES(" + a + ");",
                       record2)

    # Commit changes in the database
    conn.commit()

    # Print information about how many records inserted into the table
    print("\nWe have inserted", cursor.rowcount * 2, "records to the table.")

    # Display data in the database table
    print("\nData Inserted in the table:")
    # data = cursor.execute("""SELECT * FROM %s""" % tablename)
    data = cursor.execute(f"SELECT * FROM {tablename}")
    k = 0
    for row in data:
        print(row)
        k += 1

    print(str(k) + " rows.")
    # cursor.execute("SELECT * from %s" % tablename)
    # myresult = cursor.fetchall()
    # print(myresult)

    # Closing the database connection
    conn.close()
    # -----------------------------------------------------------------------------


if __name__ == "__main__":
    randb()
