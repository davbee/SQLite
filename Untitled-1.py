# a = ['c{:} INTEGER'.format() for i in range(23)]

for i in range(3):
    print('c'+str(i))

col = tuple(['C'+str(i) + ' INTEGER' for i in range(23)])
col2 = ','.join(col)
c2 = '''(%s)''' % col2
print(c2)
# print(type(col))
# Create a table called OT (Optical Test)
tableName = 'OT'
createTable = 'CREATE TABLE IF NOT EXISTS %s (' % tableName + col2 + ')'
# createTable = createTable + col2 +')'
print(createTable)

c = '''(
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
'''


# print(type(c))

# print(c)

# d = 'stre'
# print(type(d))
# print("\U0001F600")
# print("\U0001F601")

# print("\U0001F605")
# print("\U0001F923")
# print("\U0001F602")
# print("\U0001F642")
# print("\U0001F607")
# print("\U0001F60D")
# print("\U0001F612")
