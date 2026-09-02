import customtkinter as ctk # type: ignore
import tkinter as tk
from tkinter import filedialog

from localmind.widgets.CTkDialog import CTkDialog
from localmind.widgets.CTkYesNo import CTkYesNo
from localmind.widgets.CTkGetText import CTkGetText

from localmind.gui.CTkAppData import CTkAppData

from localmind.gui.CTkAppView import CTkAppView, FontSpec   
from localmind.widgets.CTkNewDatabaseObject import CTkNewDatabaseObject

from localmind.utils.PySqliteExt import SqliteExt
from localmind.utils.pyodbcext import pyOdbcExt
import sqlite3

from localmind.utils.validate_mssql_type import is_valid_mssql_type
from localmind.utils.validate_sqlite_type import is_valid_sqlite_type

import os
from pathlib import Path

from typing import Tuple, List, Optional


class CTkDatabaseManager(CTkAppView):
    USE_NONE = 0
    USE_SQLITE = 1
    USE_SQL_SVR = 2

    def __init__(self, parent: ctk.CTk, frame: ctk.CTkFrame, font: FontSpec, data: CTkAppData):
        super().__init__(parent, frame, font, data)
    
        self.server = os.environ.get('SQL_SERVER', "127.0.0.1")
        self.port = int(os.environ.get('SQL_PORT', 1433))
        self._database: str = self.data.database_path
        self.user = os.environ.get('SQL_SVR_USER', "crash")
        self.password = os.environ.get('SQL_SVR_PASSWORD', "")
        self.driver = os.environ.get('SQL_SVR_DRIVER', "ODBC Driver 18 for SQL Server")
        # self.data.use_sqlsvr = True
        self.initialize_widgets()
        #s = self.get_connection_string()
        #print(s)

    @property
    def database(self) -> str:
        if self._database is not None:
            if not self.data.use_sqlsvr and os.path.exists(self._database):
                return self._database
            self._database = Path(self._database).stem
        return self._database
        
    def get_connection_string(self, database: Optional[str] = None) -> str:
        db = database if database is not None else self.database
        database = Path(db).stem
        conn_str = (
            f"DRIVER={self.driver};"
            f"SERVER={self.server},{self.port};"
            f"DATABASE={database};"
            f"UID={self.user};"
            f"PWD={self.password};"
            "Encrypt=yes;"
            "TrustServerCertificate=yes;"
        )
        #return f'DRIVER={self.driver};SERVER={self.server}:{self.port};DATABASE={db};UID={self.user};PWD={self.password}'
        return conn_str
         
    def get_databases(self) -> List[str]:
        if self.data.use_sqlsvr and self.selected_db_var.get() != self.USE_NONE:
            db = pyOdbcExt(self.get_connection_string(), logger = self.data.logger)
            databases = db.execute_sql(sql="SELECT name FROM sys.databases", fetch_results=True, return_dict=True)
            if isinstance(databases, list) and len(databases) and isinstance(databases[0], dict):
                result = [ d['name'] for d in databases]
                if all([isinstance(s, str) for s in result]):
                    return result
                else:
                    return []
            else: 
                return []
        elif not self.data.use_sqlsvr and self.selected_db_var.get() != self.USE_NONE:
            return [self.database]
        else:
            return []
        
    def get_tables(self, database: str) -> List[str]:
        if self.data.use_sqlsvr and self.selected_db_var.get() != self.USE_NONE:
            db = pyOdbcExt(self.get_connection_string(database=database), logger = self.data.logger)
            list_tables_sql = 'SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = \'BASE TABLE\''
            tables = db.execute_sql(sql=list_tables_sql, fetch_results=True, return_dict=True)
            if isinstance(tables, list) and len(tables) and isinstance(tables[0], dict):
                result = [ f"{d['TABLE_SCHEMA']}.{d['TABLE_NAME']}" for d in tables ]
                if all([isinstance(s, str) for s in result]):
                    return result
                else:
                    return []
            else: 
                return []
        elif not self.data.use_sqlsvr and self.selected_db_var.get() != self.USE_NONE:
            db_sqlite = SqliteExt(self.database)
            sql = "SELECT name FROM sqlite_master WHERE type='table'" 
            tables = db_sqlite.execute_sql(sql=sql, fetch_results=True, return_dict=True)
            if isinstance(tables, list) and len(tables) and isinstance(tables[0], dict):
                result = [ d['name'] for d in tables ]
                if all([isinstance(s, str) for s in result]):
                    return result
                else:
                    return []
            else: 
                return []
        else: 
            return []
     
    def get_columns_and_types(self, database: str, table: str) -> List[Tuple[str, str, str | None]]:
        column_info = []
        if self.data.use_sqlsvr and self.selected_db_var.get() != self.USE_NONE:
            db = pyOdbcExt(self.get_connection_string(database=database), logger = self.data.logger)
            result = db.get_columns_and_types(table)
            if isinstance(result, list) and len(result) and isinstance(result[0], dict):
                column_info = [(d['COLUMN_NAME'], d['DATA_TYPE'], d['CHARACTER_MAXIMUM_LENGTH']) for d in result ]
        elif not self.data.use_sqlsvr and self.selected_db_var.get() != self.USE_NONE:
            db_sqlite = SqliteExt(self.database)
            column_info = db_sqlite.get_columns_and_types(table)

        return column_info


    def initialize_widgets(self) -> None:
        self.frame.grid_columnconfigure(0, weight=1)
        
        self.database_select_frame = self.labeled_frame(self.frame, "Select the database type to use", 0, 0, 2)
        self.selected_db_var = ctk.IntVar(value=0)
        self.db_select_sqlite_radio = ctk.CTkRadioButton(self.database_select_frame, text="SQLite3", variable=self.selected_db_var, value=self.USE_SQLITE, font=self.font, command=self.db_select_event) 
        self.db_select_sqlite_radio.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.db_select_mssql_radio = ctk.CTkRadioButton(self.database_select_frame, text="MS SQL Server", variable=self.selected_db_var, value=self.USE_SQL_SVR, font=self.font, command=self.db_select_event) 
        self.db_select_mssql_radio.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        self.db_browser_frame    = self.labeled_frame(self.frame,            "Database Browser", 1, 0, 6)
        self.db_database_frame   = self.labeled_frame(self.db_browser_frame, "Databases", 0, 0, 1, 2)
        self.db_table_frame      = self.labeled_frame(self.db_browser_frame, "Tables",    0, 2, 1, 2)
        self.db_table_info_frame = self.labeled_frame(self.db_browser_frame, "Content",   0, 4, 1, 2)

        listbox_font = self.get_tk_font()
        # database pick list and scroll bar
        self.database_pick_list =  tk.Listbox(self.db_database_frame, font=listbox_font)
        self.database_pick_list.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.database_pick_list.bind('<ButtonRelease-1>', self.database_changed)
        self.selected_database: Optional[str] = None

        self.dbpl_vsb = ctk.CTkScrollbar(self.db_database_frame)
        self.dbpl_vsb.grid(row=0, column=1, padx=2, pady=2, sticky='wns')
        
        self.database_pick_list.configure(yscrollcommand=self.dbpl_vsb.set)
        self.dbpl_vsb.configure(command=self.database_pick_list.yview)
        self.insert_databases()

        # table pick list and scroll bar
        self.table_pick_list = tk.Listbox(self.db_table_frame, font=listbox_font)
        self.table_pick_list.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.table_pick_list.bind('<ButtonRelease-1>', self.table_changed)
        self.selected_table: Optional[str] = None

        self.tpl_vsb = ctk.CTkScrollbar(self.db_table_frame)
        self.tpl_vsb.grid(row=0, column=1, padx=2, pady=2, sticky='wns')
        
        self.table_pick_list.configure(yscrollcommand=self.tpl_vsb.set)
        self.tpl_vsb.configure(command=self.table_pick_list.yview)

        # content pick list and scroll bar
        self.content_pick_list = tk.Listbox(self.db_table_info_frame, font=listbox_font)
        self.content_pick_list.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.content_pick_list.bind('<ButtonRelease-1>', self.content_changed)
        self.selected_column: Optional[str] = None

        self.cpl_vsb = ctk.CTkScrollbar(self.db_table_info_frame)
        self.cpl_vsb.grid(row=0, column=1, padx=2, pady=2, sticky='wns')
        
        self.table_pick_list.configure(yscrollcommand=self.cpl_vsb.set)
        self.cpl_vsb.configure(command=self.content_pick_list.yview)


    def insert_databases(self) -> None:
        self.database_pick_list.delete(0, tk.END)
        databases = self.get_databases()
        for s in databases:
            self.database_pick_list.insert('end', s)

    def database_changed(self, ev) -> None:
        selection = self.database_pick_list.curselection()
        if selection:
            self.selected_database = self.database_pick_list.get(selection[0])
        else:
            self.data.logger.debug("No database selected in database_changed handler")
            self.selected_database = None
        self.selected_table = None
        self.selected_column = None
        self.table_pick_list.delete(0, tk.END)
        self.content_pick_list.delete(0, tk.END)
        if self.selected_database is not None:
            self.insert_tables()

    def insert_tables(self) -> None:
        self.table_pick_list.delete(0, tk.END)
        if self.selected_database is not None:
            tables =self.get_tables(self.selected_database)
            for s in tables:
                self.table_pick_list.insert('end', s)

    def table_changed(self, ev) -> None:
        selection = self.table_pick_list.curselection()
        if selection:
            self.selected_table = self.table_pick_list.get(selection[0])
        else:
            self.data.logger.debug("No table selected in table_changed handler")
            self.selected_table = None
        self.selected_column = None
        self.insert_content()

    def split_schema_table(self, selected_table: str) -> tuple[str, str]:
        """
        Convert 'schema.table' into ('schema', 'table').

        SQL Server table names from the database browser are expected to be
        displayed as schema.table.
        """
        if "." not in selected_table:
            return "dbo", selected_table

        schema_name, table_name = selected_table.split(".", 1)
        return schema_name.strip(), table_name.strip()
    
    def insert_content(self) -> None:
        self.content_pick_list.delete(0, tk.END)
        if self.selected_database is not None and self.selected_table is not None:
            if '.' in self.selected_table:
                schema_name, table_name = self.split_schema_table(self.selected_table)
                table = table_name
            else:
                table = self.selected_table
            content = self.get_columns_and_types(self.selected_database, table)
            for t in content:
                s = t[0]
                s += ': '
                s += t[1]
                if len(s) > 2 and t[2] is not None:
                   s += f"({t[2]})"
                self.content_pick_list.insert('end', s)

    def get_column_info(self) -> Tuple[str, str]:
        if self.selected_column is not None:
            l = self.selected_column.split(':')
            if len(l) == 2:
                return (l[0], l[1])
        return ('', '')

    def content_changed(self, ev) -> None:
        selection = self.content_pick_list.curselection()
        if selection:
            self.selected_column = self.content_pick_list.get(selection[0])
        else:
            self.data.logger.debug("No column selected in content_changed handler")
            self.selected_column = None

    def db_select_event(self):
        new_db_type = self.selected_db_var.get()
        if self.data.use_sqlsvr and new_db_type == self.USE_SQLITE:
            self.data.logger.info("Switching from MS SQL Server to SQLite3")
            CTkDialog(self.parent, title="Database Type Change", message="Switching from MS SQL Server to SQLite3. Please restart the application to ensure that you have the correct database file selected.", font=self.font)
        self.data.use_sqlsvr = new_db_type == self.USE_SQL_SVR
        self.data.logger.info(f"Selected Database is {'MS SQL Server' if self.data.use_sqlsvr else 'SQLite3'}")
        self.table_pick_list.delete(0, tk.END)
        self.content_pick_list.delete(0, tk.END)
        self.insert_databases()

    def create_database(self, db_name: str) -> None:
        if self.data.use_sqlsvr:
            db = pyOdbcExt(conn_string=self.get_connection_string(database='master'), logger = self.data.logger)
            db.execute_sql(sql=f'CREATE DATABASE {db_name}')
        else:
            db_ext = os.path.splitext(db_name)[1]
            if len(db_ext) == 0:
                db_name = os.path.join(db_name, '.sqlite')
                #db_name += '.sqlite'
            conn = sqlite3.connect(db_name)
            conn.close()
        self._database = db_name

    def create_table(self, table_name: str, columns: List[Tuple[str, str]]) -> None:
        if self.selected_database is None:
            return
        if self.data.use_sqlsvr:
            db = pyOdbcExt(self.get_connection_string(database=self.selected_database), logger = self.data.logger)
            column_defs = ', '.join([f'{col[0]} {col[1]}' for col in columns])
            create_table_sql = f'CREATE TABLE {table_name} ({column_defs})'
            db.execute_sql(sql=create_table_sql)
        else:
            db_sqlite = SqliteExt(self.database)
            column_defs = ', '.join([f'{col[0]} {col[1]}' for col in columns])
            create_table_sql = f'CREATE TABLE {table_name} ({column_defs})'
            db_sqlite.execute_sql(sql=create_table_sql)

    def sb_button_list(self) -> List[str]:
        """ return the list of supported button names """
        return ['new', 'add', 'remove']  # 'update'

    def on_visible(self) -> None:
        """ change the text of the buttons we use to reflect the current view"""
        self.set_button_names({
            "new": "New",
            "add": "Add",
            "remove": "Remove",
            # "update": "Update"
        })

    def on_sidebar_new(self):
        """ 
            Activate the on_sidebar_new function in the active view
        """
        new_db_obj = CTkNewDatabaseObject(self.parent, font=self.font, db_type='mssql' if self.data.use_sqlsvr else 'sqlite')
        result = new_db_obj.result
        if result == 0:
            return
        if result == 1: # database or database file
            if not self.data.use_sqlsvr:
                file_path = filedialog.asksaveasfilename(
                    title = 'Select a SQLite database file',
                    filetypes=(('SQLite Files', '*.sqlite'), ('Database Files', '*.db'))
                )
                self.create_database(file_path)
            else:
                text = CTkGetText(self.parent, title='Database Name', message='Enter the name of the database', font=self.font)
                if isinstance(text.result, str) and len(text.result) > 0:
                    db_name = text.result
                    if os.path.exists(db_name): 
                        result =CTkDialog(self.parent, title="Warning", message="The database file will not be created it already exists", font=self.font)
                    if len(db_name) :
                        self.create_database(db_name)
                    self.database_changed(None)
                else:
                    CTkDialog(self.parent, title="Error", message="No database or database file created", font=self.font)

        elif result == 2: # new table in the current selected database
            dbn = self.selected_database
            if dbn: # create a new table with types
                # for simplicity create a table with an ID column only
                # we need the name of the table
                text = CTkGetText(self.parent, title='Table Name', message='Enter the name of the new table', font=self.font)
                if isinstance(text.result, str) and len(text.result) > 0:
                    table_name = text.result
                    if self.data.use_sqlsvr:
                        self.create_table(table_name=table_name, columns=[('id', 'INT IDENTITY(1, 1) PRIMARY KEY')])
                    else:
                        self.create_table(table_name=table_name, columns=[('id', 'INTEGER PRIMARY KEY AUTOINCREMENT')])
                    self.table_changed(None)
                else:
                    CTkDialog(self.parent, title="Error", message="No table created", font=self.font)

    def on_sidebar_remove(self):
        """ 
            Activate the on_sidebar_remove function in the active view
            remove the selected database, table or column
        """
        if self.selected_column is not None:
            col_name, col_type = self.get_column_info()
            if self.selected_database is None or self.selected_table is None:
                CTkDialog(self.parent, title="Error", message="No database or table selected", font=self.font)
                return
            confirm = CTkYesNo(self.parent, title="Confirm Delete", message=f"You want to delete column? '{col_name}' from table '{self.selected_table}'?", font=self.font)
            if confirm.result:
                if self.data.use_sqlsvr:
                    db = pyOdbcExt(self.get_connection_string(database=self.selected_database), logger = self.data.logger)
                    alter_table_sql = f'ALTER TABLE {self.selected_table} DROP COLUMN {col_name}'
                    db.execute_sql(sql=alter_table_sql)
                else:
                    CTkDialog(self.parent, title="Error", message="SQLite can't drop columns directly", font=self.font)
                self.insert_content()
        elif self.selected_table is not None:
            if self.selected_database is None:
                CTkDialog(self.parent, title="Error", message="No database selected", font=self.font)
                return
            confirm = CTkYesNo(self.parent, title="Confirm Delete", message=f"You want to delete table? '{self.selected_table}'?", font=self.font)
            if confirm.result:
                if self.data.use_sqlsvr:
                    db = pyOdbcExt(self.get_connection_string(database=self.selected_database), logger = self.data.logger)
                    drop_table_sql = f'DROP TABLE {self.selected_table}'
                    db.execute_sql(sql=drop_table_sql)
                else:
                    db_sqlite = SqliteExt(self.database)
                    drop_table_sql = f'DROP TABLE {self.selected_table}'
                    db_sqlite.execute_sql(sql=drop_table_sql)
                self.selected_table = None
                self.selected_column = None
                self.insert_tables()
                self.content_pick_list.delete(0, tk.END)
                self.table_changed(None)
        elif self.selected_database is not None:
            confirm = CTkYesNo(self.parent, title="Confirm Delete", message=f"You want to delete database? '{self.selected_database}'?", font=self.font)
            if confirm.result:
                if self.data.use_sqlsvr:
                    db = pyOdbcExt(self.get_connection_string(database='master'), logger = self.data.logger)
                    drop_db_sql = f'DROP DATABASE {self.selected_database}'
                    db.execute_sql(sql=drop_db_sql)
                else:
                    try:
                        os.remove(self.selected_database)
                    except Exception as e:
                        CTkDialog(self.parent, title="Error", message=f"Failed to delete database file: {e}", font=self.font)
                self.selected_database = None
                self.selected_table = None
                self.selected_column = None
                self.insert_databases()
                self.table_pick_list.delete(0, tk.END)
                self.content_pick_list.delete(0, tk.END)
                self.database_changed(None)

    def on_sidebar_add(self):
        """ 
            Activate the on_sidebar_add function in the active view
            add a new column to the selected table
        """
        if self.selected_database is None or self.selected_table is None:
            CTkDialog(self.parent, title="Error", message="No database or table selected for adding a column", font=self.font)
            return
        text = CTkGetText(self.parent, title='Column Definition', message='Enter the column definition as "column_name data_type"', font=self.font)
        if isinstance(text.result, str) and len(text.result) > 0:
            col_def = text.result.strip().split(' ')
            if len(col_def) != 2:
                CTkDialog(self.parent, title="Error", message="Invalid column definition format", font=self.font)
                return
            column_name = col_def[0]
            data_type = col_def[1]
            if self.data.use_sqlsvr:
                if not is_valid_mssql_type(data_type):
                    CTkDialog(self.parent, title="Error", message=f"Invalid MS SQL Server data type: {data_type}", font=self.font)
                    return
                db = pyOdbcExt(self.get_connection_string(database=self.selected_database), logger = self.data.logger)
                alter_table_sql = f'ALTER TABLE {self.selected_table} ADD {column_name} {data_type}'
                db.execute_sql(sql=alter_table_sql)
            else:
                if not is_valid_sqlite_type(data_type):
                    CTkDialog(self.parent, title="Error", message=f"Invalid SQLite data type: {data_type}", font=self.font)
                    return
                db_sqlite = SqliteExt(self.database)
                alter_table_sql = f'ALTER TABLE {self.selected_table} ADD COLUMN {column_name} {data_type}'
                db_sqlite.execute_sql(sql=alter_table_sql)
            self.insert_content
        else:
            CTkDialog(self.parent, title="Error", message="No column definition provided", font=self.font)

    def on_sidebar_update(self):
        """ 
            Activate the on_sidebar_update function in the active view
            Refresh the database, table and content lists
        """
        pass
