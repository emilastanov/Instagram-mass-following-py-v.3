import sqlite3

class Database:
    def __init__(self, db_name):
        self.db = sqlite3.connect(db_name)

    def create_table(self, table, **cols_data):  # example: create_table('Users', id='INTEGER NOT NULL PRIMARY KEY
        # AUTOINCREMENT', login='VARCHAR(100)')
        cols = ""
        for col_name in cols_data.keys():
            if col_name != list(cols_data.keys())[-1]:
                cols += "{col_name} {type}".format(col_name=col_name, type=cols_data[col_name]) + ', '
            else:
                cols += "{col_name} {type}".format(col_name=col_name, type=cols_data[col_name])
        self.db.execute("CREATE TABLE IF NOT EXISTS {table} ({cols});".format(table=table, cols=cols))
        return 'SUCCESS'

    def drop_table(self, table):  # example: drop_table('Users')
        self.db.execute("DROP TABLE {table};".format(table=table))
        return 'SUCCESS'

    def select(self, table, *values,
               where=None):  # example: select('Users', 'id', 'first_name', 'last_name', where='id=1')
        vals = ''
        ifs = ''

        if values:
            for val in values:
                if val != values[-1]:
                    vals += val + ', '
                else:
                    vals += val
        else:
            vals += '*'

        if where:
            ifs += 'WHERE {}'.format(where)

        data = self.db.execute("SELECT {vals} FROM {table} {ifs};".format(vals=vals, table=table, ifs=ifs))
        return data.fetchall()

    def insert(self, table, **values):  # example: insert('Users', first_name='blabla', last_name='blablabla')
        cols = ""
        vals = ""
        for col in values.keys():
            if col != list(values.keys())[-1]:
                cols += "{col}".format(col=col) + ', '
                vals += "'{val}'".format(val=values[col]) + ','
            else:
                cols += "{col}".format(col=col)
                vals += "'{val}'".format(val=values[col])
        self.db.execute("INSERT INTO {table}({cols}) VALUES ({vals});".format(table=table, cols=cols, vals=vals))
        self.db.commit()
        return 'SUCCESS'

    def delete(self, table, where=None):  # example: delet('Users', where='id=1')
        self.db.execute("DELETE FROM {table} WHERE {ifs}".format(table=table, ifs=where))
        self.db.commit()
        return 'SUCCESS'

    def add_col(self, table, **colum):  # add_col('Users',phone='VARCHAR(12)')
        if len(colum) == 1:
            col = "{col} {type}".format(col=list(colum.keys())[0], type=colum[list(colum.keys())[0]])
            self.db.execute("ALTER TABLE {table} ADD COLUMN {col};".format(table=table, col=col))
            return 'SUCCESS'
        else:
            return 'ERROR: You can add only one col in times!'

    def execute_script(self, script):  # example: execute('ALTER TABLE Users ADD COLUMN description VARCHAR(10);')
        data = self.db.executescript(script)
        self.db.commit()
        return data.fetchall()

    def table_info(self, table):  # example: table_info('Users')
        return self.db.execute('PRAGMA table_info({});'.format(table)).fetchall()

    def update(self, table, where=None, **values):
        vals = ""
        for col in values.keys():
            if col != list(values.keys())[-1]:
                vals += "{col} = '{val}'".format(col=col, val=values[col]) + ', '
            else:
                vals += "{col} = '{val}'".format(col=col, val=values[col])

        self.db.execute("UPDATE {table} SET {vals} WHERE {ifs};".format(table=table,vals=vals, ifs=where))
        self.db.commit()
        return 'SUCCESS'