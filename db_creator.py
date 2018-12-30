"""

db_creator module

Eric Riddoch
Nov 22, 2018

"""

import sqlite3 as sql
import csv

class db_creator:
    """
    Object that builds a database from one or multiple csv files.
    """

    def __init__(self, db_file):
        # call create_db
        # later functions will be called to add tables and their columns
        self.db_file = db_file
        self.create_db(self.db_file)

        # dictionary {table_name : columns_dict}
        self.tables = dict()

    def create_db(self, read_file):
        """
        Parameters:
            read_file (str): name of file to convert to database
        """

        # estalblish a connection in order to ensure database exists
        try:
            with sql.connect(self.db_file) as conn:
                pass
        finally:
            conn.close()

    def print_table(self, table_name, num_rows=-1):
        """Print contents of table. 
        Print the first num_rows of them is specified"""
        try:
            with sql.connect(self.db_file) as conn:
                cur = conn.cursor()
                rows = list()

                if num_rows != -1:
                    rows = cur.execute(f"""SELECT * FROM {table_name}""").fetchmany(num_rows)
                else:
                    rows = cur.execute(f"""SELECT * FROM {table_name}""").fetchall()

                for row in rows:
                    print(row)
        finally:
            conn.close()

    def get_table_format(self, columns):
        """get column format for table"""
        table_format = ""
        col_names = list(columns.keys())
        for i in range(len(col_names)):
            col_name = col_names[i]
            col_type = columns[col_name]
            table_format += f"{col_name} {col_type}"
            if i != len(col_names) - 1:
                table_format += ", "
        return "(" + table_format + ")"

    def get_values_tuple(self, columns):
        """Get VALUES(?,?,...,?) tuple for creating a new table"""
        col_names = list(columns.keys())
        return "(" + ("?," * len(col_names))[:-1] + ")"

    def add_table(self, input_file, table_name, columns, file_type="csv"):
        """Read in input_file and add it to the database as a new table.

        ! Assume that the csv does not contain it's own header row !
        
        Parameters:
            input_file (str): path to csv file
            table_name (str): name of table
            columns    (dict): {column name : column type} 
            file_type  (str): csv or tsv
                
                if column type not of INTEGER, REAL, TEXT, NULL,
                raise ValueError
            """
        
        # check types
        valid_types = set(['INTEGER', 'REAL', 'TEXT', 'NULL'])
        if set(columns.values()) | valid_types != valid_types:
            raise ValueError("Invalid sqlite column type!")
        
        # add table to self.tables
        self.tables[table_name] = columns

        # connect to database
        try:
            with sql.connect(self.db_file) as conn:
                cur = conn.cursor()
                
                # drop table if it exists
                cur.execute(f"DROP TABLE IF EXISTS {table_name}")
                
                table_format = self.get_table_format(columns)
                
                # create the table
                cur.execute(f"""CREATE TABLE {table_name}
                {table_format}""")

                # 'rows' will be a list of lists
                rows = None

                # get rows
                if file_type == 'csv':
                    # populate table from csv
                    with open(input_file, 'r') as infile:
                        # get studentinfo data as list of tuples
                        rows = list(csv.reader(infile))
                        # rows = list(map(tuple, rows))

                elif file_type == 'tsv':
                    with open(input_file, 'r') as infile:
                        rows = infile.readlines()
                        for i, row in enumerate(rows):
                            rows[i] = row.strip('\n').split('\t')

                # insert rows into table
                values = self.get_values_tuple(columns)
                cur.executemany("""INSERT INTO {} 
                    VALUES{}""".format(table_name, values), rows)

        finally:
            conn.close()
        
    def to_null(self, value_to_null, table_name):
        """
        Set a certain value in the given table to NULL
        """

        if type(value_to_null) == str:
            value_to_null = "\"" + value_to_null + "\""

        try:
            with sql.connect(self.db_file) as conn:
                cur = conn.cursor()
                columns = self.tables[table_name]
                # print(columns.keys())
                for col in columns.keys():
                    # print(col)
                    cur.execute(f"""UPDATE {table_name} SET {col}=NULL 
                    WHERE {col}=={value_to_null}""")
        finally:
            conn.close()