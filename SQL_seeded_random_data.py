# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 16:14:20 2022

@author: DB
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
# generate seeded random data Matrix1
np.random.seed(seed=11)
Matrix1 = np.random.randint(100, size=(10, 23))

# generate seeded random data Matrix2
np.random.seed(seed=13)
Matrix2 = np.random.randint(100, size=(10, 23))

# convert numpy 2D array to Pandas dataframe
df1 = pd.DataFrame(Matrix1)
df2 = pd.DataFrame(Matrix2)

# convert Pandas dataframe to list of tuple for inserting into database
record1 = [tuple(i) for i in df1.values.tolist()]
record2 = [tuple(i) for i in df2.values.tolist()]
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Create SQLite3 database
# -----------------------------------------------------------------------------
# Connecte to sqlite
# conn = sqlite3.connect('OT.db') # create a database file
conn = sqlite3.connect(':memory:')  # create a database in memory

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create a table called OT (Optical Test)
tableName = 'OT'

createTable = '''
CREATE TABLE IF NOT EXISTS %s (
          C00             INTEGER key,
          C01           INTEGER,
          C02            INTEGER,
          C03              INTEGER,
          C04              INTEGER,
          C05          INTEGER,
          C06             INTEGER,
          C07             INTEGER,
          C08              INTEGER,
          C09               INTEGER,
          C10             INTEGER,
          C11               INTEGER,
          C12        INTEGER,
          C13 INTEGER,
          C14         INTEGER,
          C15         INTEGER,
          C16              INTEGER,
          C17              INTEGER,
          C18         INTEGER,
          C19              INTEGER,
          C20             INTEGER,
          C21            INTEGER,
          C22              INTEGER
          )
          ''' % tableName

cursor.execute(createTable)

# -----------------------------------------------------------------------------
# Create as many '?,' as there are fields in the table
# -----------------------------------------------------------------------------


def fieldNum(a, w):
    return a.join([a+'?,' for i in range(w)])[:-1]


a = fieldNum('', 23)

# -----------------------------------------------------------------------------
# Insert OT data into the table with one-shot
# -----------------------------------------------------------------------------
# cursor.executemany('INSERT INTO '+tableName+' VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);',record1);
cursor.executemany('INSERT INTO '+tableName+' VALUES('+a+');', record1)
cursor.executemany('INSERT INTO '+tableName+' VALUES('+a+');', record2)

# Commit changes in the database
conn.commit()

# Print information about how many records inserted into the table
print('We have inserted', cursor.rowcount*2, 'records to the table.')

# Display data in the database table
print("Data Inserted in the table:")
data = cursor.execute('''SELECT * FROM %s''' % tableName)
for row in data:
    print(row)

# Closing the database connection
conn.close()
# -----------------------------------------------------------------------------