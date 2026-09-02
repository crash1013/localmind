
import sqlite3
from pathlib import Path
import re
import pandas as pd
# moduleses used for testing
from datetime import datetime
from datetime import date
import datetime as dt
from logging import Logger

from typing import Any, Union, Optional

class SqliteExt:
    """"
        pyODBCExt is an ODBC extension of pyodbc.
        This module simplifies many simple tasks associated with database management

    """
    def __init__(self, database_name: Optional[str]=None, logger: Optional[Logger]=None):
        """
            All we need is the connection string and the logger if any
        """
        self.database_name = database_name
        self.logger=logger
        self.lastrowid = 0
        self.rowcount = 0

    def log_info(self, message):
        """ standard logging function for non-critical information,
            if logger is not installed we just print the message """
        
        if self.logger is None:
            print(f"SqliteExt Info: {message}")
            return
        try:
            self.logger.info(message)
        except Exception as e:
            print(f"Logger Exception: {e}")

    def log_debug(self, message):
        """ standard logging function for debugging messages,
            if logger is not installed we just print the message """
        if self.logger is None:
            print(f"SqliteExt Debug: {message}")
            return
        try:
            self.logger.debug(message)
        except Exception as e:
            print(f"Logger Exception: {e}")

    def log_error(self, message):
        """ standard logging function for non-critical information,
            if logger is not installed we just print the message """
        if self.logger is None:
            print(f"SqliteExt Error: {message}")
            return
        try:
            self.logger.info(message)
        except Exception as e:
            print(f"Logger Exception: {e}")

    def result_to_dict(self, cursor: sqlite3.Cursor, rows: list[Any]) -> list[dict]:
        """ result_to_dict:
            returns a list of dictionaries extracted from the cursor and rows data. The cursor
            and rows are the result of an SQL query.
            The keys which are the column names are read from the result description.
            String values are stripped to remove unwanted leading and trailing spaces """
        nrows = len(rows)
        ncols = 0
        result = None
        result = []
        if nrows > 0:
            ncols = len(cursor.description)
            
            if ncols > 0:
                for r in rows:
                    d = {}
                    for index in range(ncols):
                        if isinstance(r[index], str): # if it is a string strip white space that pads the string
                            d[cursor.description[index][0]] = r[index].strip()
                        else:
                            d[cursor.description[index][0]] = r[index]
                    result.append(d)
        return result
    
    def execute_sql(self, 
                    sql: str,  
                    database_name: Optional[str]=None, 
                    parameters: Optional[Union[list,tuple]]=None, 
                    fetch_results: bool=False,
                    return_dict: bool=False) -> Union[int, list]: 
        """
        Execute a given SQL command or query.

        :param database_name: name of an sqlite3 database file.
        :param sql: SQL command or query string.
        :param parameters: A tuple or list of values to be used in a parameterized query.
        :param fetch_results: Whether to fetch results after executing a query.
        
        :return: Results if fetch_results=True and it's a query, otherwise the number of affected rows.
                 if fetch_results returns None then an empty list is returned
        """
        results: Optional[list] = None
        self.rowcount = 0
        conn = None
        if database_name == None:
            database_name = self.database_name
        try:
            if database_name is None:
                raise ValueError("'database_name' never initialized")
            with sqlite3.connect(database_name) as conn:
                cursor: sqlite3.Cursor = conn.cursor()
                
                if parameters:
                    cursor.execute(sql, parameters)
                else:
                    cursor.execute(sql)
                    
                if fetch_results:
                    results = cursor.fetchall()
                    if return_dict:
                        results = self.result_to_dict(cursor, results)
                else:
                    conn.commit()
                    if cursor is not None and cursor.rowcount is not None:
                        self.lastrowid = cursor.lastrowid if isinstance(cursor.lastrowid, int) else 0
                        self.rowcount = cursor.rowcount if isinstance(cursor.rowcount, int) else 0
        except ValueError:
            raise
        except Exception as e:
            self.log_error(f"Error executing sql: {str(e)}")
        finally:
            # the context manager does not close the connection
            # it only takes care of commit on writes and rollback on errors
            if conn != None:
                conn.close()

        # Note: For SELECT queries, it returns results.
        # For commands like INSERT, UPDATE, DELETE, it returns the number of affected rows.
        if fetch_results and results is not None:
            return results
        elif fetch_results and results is None:
            return []
        return self.rowcount
    
    def keys_from_dict(self, d: dict) -> str:
        """ keys_from_dict: 
            returns a string that contains all the dictionary keys separated by commas 
        """
        return  f"{','.join(d.keys())}"
    
    def items_from_dict(self, d) -> tuple:
        """ items_from_dict:
            returns a tuple that contains the values from the referenced dictionary.
        """
        return tuple(d.values())
        # return tuple([ self.format_value(v) for v in d.values() ])
        
    def insert_from_dict(self, table_name: str, data_dict: dict) -> int:
        """ insert_from_dict:
            Inserts the record defined in the data_dict. 
            Returns the number of records inserted.
        """
        if not isinstance(table_name, str) or not isinstance(data_dict, dict):
            raise TypeError("Invalid parameter type")
        parameters = self.items_from_dict(data_dict)
        sql = f"INSERT INTO {table_name} ({self.keys_from_dict(data_dict)}) VALUES ({','.join(['?'] * len(parameters))})"
        result = self.execute_sql(sql, parameters=parameters)
        return result if isinstance(result, int) else 0
        
    def update_from_dict(self, table_name: str, data_dict: dict, condition: Optional[str]=None) -> int:
        """ update_from_dict:
            Updates the record accessed using the specified condition. 
            Returns the number of rows affected.
        """
        if not isinstance(condition, str):
            raise ValueError("SQL update requires a conditional string")
        if not isinstance(table_name, str) or not isinstance(data_dict, dict):
            raise TypeError("Invalid parameter type")
        parameters = self.items_from_dict(data_dict)
        sql = f"""UPDATE {table_name} SET {','.join([f'{k} = ?' for k in data_dict.keys()])} WHERE {condition} """
        result = self.execute_sql(sql, parameters=parameters)
        return result if isinstance(result, int) else 0
        #return self.execute_sql(sql, parameters=parameters)
    
    def create_from_dict(self, table_name: str, cdict: dict):
        """ Create a database table using a dictionary to define the fields.
            The table creates the table if it does not exist.
            Each key, value pair in the dictionary define a key and type pair in the database table.
            The value field may contain multiple strings. There are no limitations.


            table_name: The name of the table to be created
            cdict: The dictionary that defines the table
        """
        create_str = f"""CREATE TABLE IF NOT EXISTS {table_name} (\n """ 
        create_str += ',\n'.join([f"{k}    {v}" for k, v in cdict.items()]) + ")"
        return self.execute_sql(create_str)
    
    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists in an SQLite database.

        Args:
            database_name (str): The name of the SQLite database file.
            table_name (str): The name of the table to check for.

        Returns:
            bool: True if the table exists, False otherwise.
        """
        try:
            result = None
            # Connect to the SQLite database
            if isinstance(self.database_name, str) and len(self.database_name) > 0:
                conn = sqlite3.connect(self.database_name)
                cursor = conn.cursor()

                # Check if the table exists in the sqlite_master table
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
                result = cursor.fetchone()

            # Close the cursor and connection
                cursor.close()
                conn.close()
            else:
                raise ValueError("Database name is not defined")
            # If result is not None, the table exists
            return result is not None

        except sqlite3.Error as e:
            self.log_error(f"SQLite error: {e}")
            return False
    
    def drop_table(self, table_name: str) -> None:
        """ drop_table:
            removes the specifed table from the database. 
            WARNING: This has the potential to be very dangerous.
        """
        if not isinstance(table_name, str):
            raise TypeError("Table name must be a string")
        self.execute_sql(f"DROP TABLE {table_name}")

    def get_columns_and_types_old(self, table_name: str) -> list[tuple]:
        """
            Get the columns and their data types for a table in an SQLite database.

            Args:
                database_name (str): The name of the SQLite database file.
                table_name (str): The name of the table to retrieve columns from.

            Returns:
                list of tuples: A list of tuples where each tuple contains (column_name, data_type).
        """
        try:
            # Connect to the SQLite database
            columns_and_types = []
            if isinstance(self.database_name, str) and len(self.database_name) > 0 and self.database_name is not None:
                conn = sqlite3.connect(self.database_name)
                cursor = conn.cursor()

                # Query the table's columns and types from sqlite_master
                cursor.execute(f"PRAGMA table_info('{table_name}');")
                columns_info = cursor.fetchall()

                # Extract column names and data types
                columns_and_types = [(col_info[1], col_info[2]) for col_info in columns_info]

                # Close the cursor and connection
                cursor.close()
                conn.close()

            return columns_and_types

        except sqlite3.Error as e:
            self.log_error(f"SQLite error: {e}")
            return []
        

    def parse_sqlite_type(self, declared_type: str | None) -> tuple[str, int | None]:
        """
        Parse SQLite declared types like:
            nvarchar(128)
            varchar(255)
            text
            integer

        Returns:
            (base_type, max_length)
        """
        if not declared_type:
            return "", None

        declared_type = declared_type.strip()

        match = re.match(r"^([a-zA-Z0-9_ ]+)\s*\(\s*(\d+)\s*\)", declared_type)

        if match:
            base_type = match.group(1).strip()
            max_length = int(match.group(2))
            return base_type, max_length

        return declared_type, None   
    
    def get_columns_and_types(self, table_name: str) -> list[tuple]:
        """
        Get the columns, data types, and max character lengths for a table
        in an SQLite database.

        Returns:
            list[tuple]:
                A list of tuples where each tuple contains:
                (column_name, data_type, character_maximum_length)
        """
        columns_and_types = []

        try:
            if (
                self.database_name is not None
                and isinstance(self.database_name, str)
                and len(self.database_name) > 0
            ):
                conn = sqlite3.connect(self.database_name)
                cursor = conn.cursor()

                # PRAGMA cannot use a parameter placeholder for the table name.
                # Double quotes are safer than single quotes for identifiers.
                safe_table_name = table_name.replace('"', '""')
                cursor.execute(f'PRAGMA table_info("{safe_table_name}");')

                columns_info = cursor.fetchall()

                for col_info in columns_info:
                    column_name = col_info[1]
                    declared_type = col_info[2]

                    data_type, max_length = self.parse_sqlite_type(declared_type)

                    columns_and_types.append(
                        (
                            column_name,
                            data_type,
                            max_length,
                        )
                    )

                cursor.close()
                conn.close()

        except sqlite3.Error as e:
            if self.logger is not None:
                self.logger.error(f"SQLite error reading columns for table '{table_name}': {e}")

        return columns_and_types
    
    def format_value(self, v):
        """Format the value based on its type."""
        if isinstance(v, str):
            return f"'{v}'"
        elif isinstance(v, datetime):
            return f"'{v.isoformat()}'"
        elif isinstance(v, date):
            return f"'{v}'"
        else:
            return str(v)

    def build_query_from_dict(self, tab, d):
        """ used to create a query string that performs an exact match of the dictionary
            tab: The name of the table
            d:   The dictionary 
        """

        assert(isinstance(tab, str) and isinstance(d, dict))
        query = f"SELECT * FROM {tab} WHERE {' AND '.join([ f'{k} = {self.format_value(v)}' for k, v in d.items()])}"
        return query
    
    def insert_if_not_present(self, table_name: str, data_dict: dict) -> int:
        """ insert_if_not_present:
            Inserts the data contained in the data_dict unles another record exists with the same
            contents. 
            Returns the number of rows inserted, 0 if already present, 1 if successfully inserted.
            for an SQLite3 database. This ensures insertion only if a record with the same values does not exist.

            Args:
                table_name (str): The name of the table to insert data into.
                data (dict): A dictionary where keys are column names and values are the data to be inserted.

            Returns:
               
        """
        if not isinstance(data_dict, dict):
            raise TypeError("insert if not present requires a dictionary")
        if not data_dict:
            raise ValueError("Data dictionary is empty")

        result = self.execute_sql(self.build_query_from_dict(tab=table_name, d=data_dict), fetch_results=True, return_dict=True)
        if isinstance(result, list) and len(result) > 0:
            return 0
        return self.insert_from_dict(table_name=table_name, data_dict=data_dict)        
    
    def query_to_dataframe(self, sql, parameters=None) -> pd.DataFrame:
        """ query_to_dataframe:
            runs the specified sql query with the associated parameters and returns the 
            result as a pandas DataFrame.
        """
        l = self.execute_sql(sql, parameters, fetch_results=True, return_dict=True)
        if isinstance(l, list) and len(l) > 0:
            return pd.DataFrame(l)
        return pd.DataFrame()
    
    
if __name__=="__main__":
    pass