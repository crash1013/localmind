# pyodbcext.py
"""
This module extends pyodbc to include some high level functionality.
It is designed to to be compliant with python version 3.7 or greater
It is designed to strictly work with Microsoft SQL Server

"""

import pyodbc # type: ignore
import pandas as pd
from logging import Logger, DEBUG
from localmind.utils.initLogger import init_logger

from typing import Union, Optional

class pyOdbcExt:
    """"
        pyODBCExt is an ODBC extension of pyodbc.
        This module simplifies many simple tasks associated with database management
    """
    def __init__(self, conn_string: str="DSN=CTkApp", logger: Optional[Logger]=None) -> None:
        """
            All we need is the connection string and the logger if any
        """
        self.conn_string = conn_string
        self.rowcount: int = 0
        if logger is None:
            self.logger: Logger = init_logger('odbc_ext',level=DEBUG, log_dir='./')
        else:
            self.logger = logger

    def log_info(self, message):
        """ standard logging function for non-critical information,
            if logger is not installed we just print the message """
        
        if self.logger is None:
            print(f"ODBC Info: {message}")
            return
        try:
            self.logger.info(message)
        except Exception as e:
            print(f"Logger Exception: {e}")

    def log_debug(self, message):
        """ standard logging function for debugging messages,
            if logger is not installed we just print the message """
        if self.logger is None:
            print(f"ODBC Debug: {message}")
            return
        try:
            self.logger.debug(message)
        except Exception as e:
            print(f"Logger Exception: {e}")

    def log_error(self, message):
        """ standard logging function for non-critical information,
            if logger is not installed we just print the message """
        if self.logger is None:
            print(f"ODBC Error: {message}")
            return
        try:
            self.logger.info(message)
        except Exception as e:
            print(f"Logger Exception: {e}")

    def result_to_dict(self, cursor: pyodbc.Cursor, rows: list[pyodbc.Row]) -> list[dict]: #***
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
                    sql,  
                    connection_string=None, 
                    parameters=None, 
                    fetch_results=False,
                    return_dict=False) -> Union[int, list]: 
        """
        Execute a given SQL command or query.

        :param connection_string: ODBC connection string.
        :param sql: SQL command or query string.
        :param parameters: A tuple or list of values to be used in a parameterized query.
        :param fetch_results: Whether to fetch results after executing a query.
        
        :return: Results if fetch_results=True and it's a query, otherwise the number of affected rows.
        """
        results = []
        self.rowcount = 0
        self.lastrowid = None
        conn = None
        if connection_string == None:
            connection_string = self.conn_string
        try:
            with pyodbc.connect(connection_string) as conn:
                cursor: pyodbc.Cursor = conn.cursor()
                
                if parameters:
                    cursor.execute(sql, parameters)
                else:
                    cursor.execute(sql)
                    
                if fetch_results:
                    results = cursor.fetchall()
                    if return_dict:
                        results = self.result_to_dict(cursor, results)
                else:
                    self.rowcount = cursor.rowcount
                    #self.lastrowid = cursor.lastrowid
        except Exception as e:
            self.log_error(f"Error executing sql: {str(e)}")
        finally:
            # the context manager does not close the connection
            # it only takes care of commit on writes and rollback on errors
            if isinstance(conn, pyodbc.Connection):
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
        
    def insert_from_dict(self, table_name: str, data_dict: dict) -> Union[int, list]:
        """ insert_from_dict:
            Inserts the record defined in the data_dict. 
            Returns the number of records inserted.
        """
        if not isinstance(table_name, str) or not isinstance(data_dict, dict):
            raise TypeError("Invalid parameter type")
        parameters = self.items_from_dict(data_dict)
        sql = f"INSERT INTO {table_name} ({self.keys_from_dict(data_dict)}) VALUES ({','.join(['?'] * len(parameters))})"
        return self.execute_sql(sql, parameters=parameters)
        
    def update_from_dict(self, table_name: str, data_dict: dict = dict(), condition: str="")  -> Union[int, list]:
        """ update_from_dict:
            Updates the record accessed using the specified condition. 
            Returns the number of rows affected.
        """

        if not isinstance(condition, str) or len(condition) == 0:
            raise ValueError("SQL update requires a conditional string")
        if not isinstance(table_name, str) or not isinstance(data_dict, dict):
            raise TypeError("Invalid parameter type")
        parameters = self.items_from_dict(data_dict)
        sql = f"""UPDATE {table_name} SET {','.join([f'{k} = ?' for k in data_dict.keys()])} WHERE {condition} """
        return self.execute_sql(sql, parameters=parameters)
    
    def create_from_dict(self, table_name: str, cdict: dict) -> Union[int, list]:
        """ Create a database table using a dictionary to define the fields.
            The table creates the table if it does not exist.
            Each key, value pair in the dictionary define a key and type pair in the database table.
            The value field may contain multiple strings. There are no limitations.


            table_name: The name of the table to be created
            cdict: The dictionary that defines the table
        """
        create_str = f"""IF NOT EXISTS (SELECT * FROM sys.objects WHERE name='{table_name}' AND type='U')
                         CREATE TABLE {table_name} (\n """ 
        create_str += ',\n'.join([f"{k}    {v}" for k, v in cdict.items()]) + ")"
        return self.execute_sql(create_str)
    
    def table_exists(self, table_name: str) -> bool:
        """ table_exists:
            checks for the existence of the specified table in the database and returns
            True if found, False otherwise.
        """
        if not isinstance(table_name, str):
            raise TypeError("Table name must be a string")
        query = "SELECT * FROM information_schema.tables WHERE table_name = ?"
        result = self.execute_sql(sql=query, parameters=(table_name,), fetch_results=True)
        if isinstance(result, list):
            return len(result) > 0
        return False
    
    def drop_table(self, table_name: str) -> None:
        """ drop_table:
            removes the specifed table from the database. 
            WARNING: This has the potential to be very dangerous.
        """
        if not isinstance(table_name, str):
            raise TypeError("Table name must be a string")
        self.execute_sql(f"DROP TABLE {table_name}")

    def get_columns_and_types(self, table_name: str) -> Union[int, list]:
        """ get_columns_and_types:
            returns a list of dictionary describing the columns of the specified table
        """
        query = """
        SELECT  COLUMN_NAME, 
                DATA_TYPE,
                CHARACTER_MAXIMUM_LENGTH
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = ?
        """
        
        return self.execute_sql(query, parameters=(table_name,), fetch_results=True, return_dict=True)
    
    def insert_if_not_present(self, table_name: str, data_dict: dict) -> int:
        """ insert_if_not_present:
            Inserts the data contained in the data_dict unles another record exists with the same
            contents. 
            Returns the number of rows inserted, 0 if already present, 1 if successfully inserted.
        """
        if not isinstance(table_name, str) or not isinstance(data_dict, dict):
            raise TypeError("Invalid parameter type")
        columns = ', '.join(data_dict.keys())
        placeholders = ', '.join(['?'] * len(data_dict))
        conditions = ' AND '.join([f"Target.{col} = Source.{col}" for col in data_dict.keys()])
        
        sql = f"""
        MERGE INTO {table_name} AS Target
        USING (VALUES ({placeholders})) AS Source ({columns})
        ON {conditions}
        WHEN NOT MATCHED THEN 
            INSERT ({columns}) VALUES ({placeholders});
        """
        result = self.execute_sql(sql=sql, parameters=tuple(data_dict.values()) * 2)
        if isinstance(result, int):
            return result
        else:
            return 0
        
    def query_to_dataframe(self, sql: str, parameters: Optional[list[str]]=None) -> Optional[pd.DataFrame]:
        """ query_to_dataframe:
            runs the specified sql query with the associated parameters and returns the 
            result as a pandas DataFrame.
        """
        result = self.execute_sql(sql, parameters, fetch_results=True, return_dict=True)
        if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict):
            return pd.DataFrame(result)
        else:
            return None
    
if __name__=="__main__":
    pass