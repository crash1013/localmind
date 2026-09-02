# LlamaBenchmarkData.py

from __future__ import annotations

import os
from pathlib import Path
from logging import Logger
import sqlite3

from localmind.utils.pyodbcext import pyOdbcExt
from localmind.utils.PySqliteExt import SqliteExt

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import json
from typing import Any

from logging import Logger

@dataclass(slots=True)
class LlamaBenchModelInfo:
    model_filename: str
    model_type: str | None
    model_size: int | None
    model_n_params: int | None

    @property
    def model_file_name(self) -> str:
        return Path(self.model_filename).name


@dataclass(slots=True)
class LlamaBenchRunInfo:
    build_commit: str | None
    build_number: int | None
    cpu_info: str | None
    gpu_info: str | None
    backends: str | None


@dataclass(slots=True)
class LlamaBenchResult:
    test_type: str
    test_time: datetime | None
    raw: dict[str, Any]

def parse_llama_bench_json(json_text: str) -> list[dict[str, Any]]:
    """
    Parse llama-bench JSON output.

    llama-bench currently emits a JSON array where each item is one benchmark
    measurement row.
    """
    data = json.loads(json_text)

    if not isinstance(data, list):
        raise ValueError("Expected llama-bench JSON output to be a list.")

    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Expected item {index} to be an object.")

    return data


def derive_test_type(row: dict[str, Any]) -> str:
    n_prompt = int(row.get("n_prompt") or 0)
    n_gen = int(row.get("n_gen") or 0)
    n_depth = int(row.get("n_depth") or 0)

    if n_prompt > 0 and n_gen == 0:
        return "prompt"
    if n_prompt == 0 and n_gen > 0:
        return "generation"
    if n_depth > 0:
        return "depth"

    return "mixed"


def parse_test_time(value: Any) -> datetime | None:
    if not value:
        return None

    if not isinstance(value, str):
        return None

    # llama-bench uses values like: 2026-06-24T08:03:56Z
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None

def extract_model_info(row: dict[str, Any]) -> LlamaBenchModelInfo:
    return LlamaBenchModelInfo(
        model_filename=str(row.get("model_filename") or ""),
        model_type=row.get("model_type"),
        model_size=row.get("model_size"),
        model_n_params=row.get("model_n_params"),
    )


def extract_run_info(row: dict[str, Any]) -> LlamaBenchRunInfo:
    return LlamaBenchRunInfo(
        build_commit=row.get("build_commit"),
        build_number=row.get("build_number"),
        cpu_info=row.get("cpu_info"),
        gpu_info=row.get("gpu_info"),
        backends=row.get("backends"),
    )


def parse_results(json_text: str) -> list[LlamaBenchResult]:
    rows = parse_llama_bench_json(json_text)

    return [
        LlamaBenchResult(
            test_type=derive_test_type(row),
            test_time=parse_test_time(row.get("test_time")),
            raw=row,
        )
        for row in rows
    ]




class LlamaBenchmarkData :

    def __init__(self,
                 use_sqlsvr: bool = True,
                 sqlite_filename: str | None = None,
                 logger: Logger | None = None,
                 ) -> None:
        self.server: str | None = os.environ.get('SQL_SERVER', "127.0.0.1") if use_sqlsvr else None
        self.port: int | None = int(os.environ.get('SQL_PORT', 1433)) if use_sqlsvr else None
        self._database: str | None= "LocalMind" if use_sqlsvr else sqlite_filename
        self.user: str | None  = os.environ.get('SQL_SVR_USER', "crash") if use_sqlsvr else None
        self.password: str | None = os.environ.get('SQL_SVR_PASSWORD', "") if use_sqlsvr else None
        self.driver: str | None = os.environ.get('SQL_SVR_DRIVER', "ODBC Driver 18 for SQL Server") if use_sqlsvr else None
        self.use_sqlsvr: bool = use_sqlsvr
        self.logger = logger
        self.init_tables() # we expect the LocalMind database to exist if SQL Server
        # print(f"Connection string: {self.get_connection_string()}")
        if not use_sqlsvr and self.logger is not None:
            if self._database is not None:
                self.logger.info(f"Initialized LlamaBenchmarkData with SQLite database: {self._database}")
            else:
                self.logger.warn("Initialized LlamaBenchmarkData with no database specified.")

    def get_connection_string(self, database: str | None = None) -> str:
        db = database if database is not None else self._database
        if db is None:
            raise ValueError("Database name must be provided when use_sqlsvr is True.")
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
    
    def init_tables(self) -> None:
        if self.use_sqlsvr:
            db = pyOdbcExt(conn_string=self.get_connection_string("LocalMind"), logger=self.logger)
            db.execute_sql(sql="""
                IF OBJECT_ID(N'dbo.Models', N'U') IS NULL
                BEGIN
                    CREATE TABLE dbo.Models
                    (
                        ModelId              INT IDENTITY(1,1) PRIMARY KEY,

                        -- Human/display fields
                        ModelName            NVARCHAR(255) NOT NULL,
                        ModelFileName        NVARCHAR(255) NOT NULL,
                        ModelType            NVARCHAR(100) NULL,
                        ModelFamily          NVARCHAR(100) NULL,
                        Quantization         NVARCHAR(50) NULL,

                        -- Path/location fields
                        ModelPath            NVARCHAR(1000) NOT NULL,
                        ModelPathHash        CHAR(64) NOT NULL,

                        -- Stable cross-platform model identity
                        ModelIdentityHash    CHAR(64) NOT NULL,

                        -- Model size/detail fields
                        ModelSizeBytes       BIGINT NULL,
                        ModelParameterCount  BIGINT NULL,
                        ModelSha256          CHAR(64) NULL,

                        -- User/application fields
                        Notes                NVARCHAR(MAX) NULL,
                        CreatedAt            DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),

                        CONSTRAINT UQ_Models_ModelIdentityHash UNIQUE (ModelIdentityHash)
                    );                
                END;
                """
            )
            
            db.execute_sql(sql="""
                IF OBJECT_ID(N'dbo.BenchmarkRuns', N'U') is NULL
                BEGIN
                    CREATE TABLE dbo.BenchmarkRuns
                    (
                        BenchmarkRunId     INT IDENTITY(1,1) PRIMARY KEY,
                        ModelId            INT NOT NULL,
                        RunStartedAt       DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
                        RunFinishedAt      DATETIME2 NULL,
                        CommandLine        NVARCHAR(MAX) NULL,
                        LlamaBenchVersion  NVARCHAR(100) NULL,
                        Backend            NVARCHAR(100) NULL,
                        HostName           NVARCHAR(255) NULL,
                        CpuInfo            NVARCHAR(255) NULL,
                        GpuInfo            NVARCHAR(255) NULL,
                        Success            BIT NOT NULL DEFAULT 0,
                        ExitCode           INT NULL,
                        RawJson            NVARCHAR(MAX) NULL,
                        RawOutput          NVARCHAR(MAX) NULL,
                        ErrorOutput        NVARCHAR(MAX) NULL,
                        Notes              NVARCHAR(MAX) NULL,

                        CONSTRAINT FK_BenchmarkRuns_Models
                            FOREIGN KEY (ModelId) REFERENCES dbo.Models(ModelId)
                    );                           
                END; """
                        )
            db.execute_sql(sql="""
                IF OBJECT_ID(N'dbo.BenchmarkSettings', N'U') is NULL
                BEGIN
                    CREATE TABLE dbo.BenchmarkSettings
                    (
                        BenchmarkSettingId INT IDENTITY(1,1) PRIMARY KEY,
                        BenchmarkRunId     INT NOT NULL,
                        SettingName        NVARCHAR(100) NOT NULL,
                        SettingValue       NVARCHAR(500) NULL,

                        CONSTRAINT FK_BenchmarkSettings_BenchmarkRuns
                            FOREIGN KEY (BenchmarkRunId) REFERENCES dbo.BenchmarkRuns(BenchmarkRunId)
                            ON DELETE CASCADE,

                        CONSTRAINT UQ_BenchmarkSettings_RunName
                            UNIQUE (BenchmarkRunId, SettingName)
                    );
                END; """)
            
            db.execute_sql(sql="""
                IF OBJECT_ID(N'dbo.BenchmarkResults', N'U') is NULL
                BEGIN
                    CREATE TABLE dbo.BenchmarkResults
                    (
                        BenchmarkResultId      INT IDENTITY(1,1) PRIMARY KEY,
                        BenchmarkRunId         INT NOT NULL,

                        TestType               NVARCHAR(50) NULL,
                        TestTime               DATETIME2 NULL,
                        NPrompt                INT NULL,
                        NGen                   INT NULL,
                        NDepth                 INT NULL,
                        AvgNs                  BIGINT NULL,
                        StddevNs               BIGINT NULL,



                        AvgTokensPerSecond     FLOAT NULL,
                        StddevTokensPerSecond  FLOAT NULL,

                        SamplesNsJson          NVARCHAR(MAX) NULL,
                        SamplesTokensPerSecondJson          NVARCHAR(MAX) NULL,
                        RawJson                NVARCHAR(MAX) NULL,
                        CreatedAt              DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),

                        CONSTRAINT FK_BenchmarkResults_BenchmarkRuns
                            FOREIGN KEY (BenchmarkRunId)
                            REFERENCES dbo.BenchmarkRuns(BenchmarkRunId)
                            ON DELETE CASCADE
                    );                           
                END; """                
                )
            
            db.execute_sql(sql="""
                IF OBJECT_ID(N'dbo.Hosts', N'U') IS NULL
                BEGIN
                    CREATE TABLE dbo.Hosts
                    (
                        HostId        INT IDENTITY(1,1) PRIMARY KEY,
                        HostName      NVARCHAR(255) NOT NULL,
                        OsName        NVARCHAR(100) NULL,
                        OsVersion     NVARCHAR(255) NULL,
                        CpuInfo       NVARCHAR(1000) NULL,
                        RamBytes      BIGINT NULL,
                        Notes         NVARCHAR(MAX) NULL,
                        CreatedAt     DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),

                        CONSTRAINT UQ_Hosts_HostName UNIQUE (HostName)
                    );
                END;"""
               )
            

        else:
            if self._database is None:
                raise ValueError("SQLite database filename must be provided when use_sqlsvr is False.")
            else:
                if self.logger is not None:
                    self.logger.info(f"Initializing SQLite database at {self._database}")
            conn = SqliteExt(self._database, logger=self.logger)
            try:
                conn.execute_sql(sql="PRAGMA foreign_keys = ON;")

                conn.execute_sql(sql="""
                    CREATE TABLE IF NOT EXISTS Models
                    (
                        ModelId              INTEGER PRIMARY KEY AUTOINCREMENT,

                        -- Human/display fields
                        ModelName            TEXT NOT NULL,
                        ModelFileName        TEXT NOT NULL,
                        ModelType            TEXT NULL,
                        ModelFamily          TEXT NULL,
                        Quantization         TEXT NULL,

                        -- Path/location fields
                        ModelPath            TEXT NOT NULL,
                        ModelPathHash        TEXT NOT NULL,

                        -- Stable cross-platform model identity
                        ModelIdentityHash    TEXT NOT NULL,

                        -- Model size/detail fields
                        ModelSizeBytes       INTEGER NULL,
                        ModelParameterCount  INTEGER NULL,
                        ModelSha256          TEXT NULL,

                        -- User/application fields
                        Notes                TEXT NULL,
                        CreatedAt            TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                        CONSTRAINT UQ_Models_ModelIdentityHash UNIQUE (ModelIdentityHash)
                    );                
                """)

                conn.execute_sql(sql="""
                    CREATE TABLE IF NOT EXISTS BenchmarkRuns
                    (
                        BenchmarkRunId     INTEGER PRIMARY KEY AUTOINCREMENT,
                        ModelId            INTEGER NOT NULL,
                        RunStartedAt       TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        RunFinishedAt      TEXT NULL,
                        CommandLine        TEXT NULL,
                        LlamaBenchVersion  TEXT NULL,
                        Backend            TEXT NULL,
                        HostName           TEXT NULL,
                        CpuInfo            TEXT NULL,
                        GpuInfo            TEXT NULL,
                        Success            INTEGER NOT NULL DEFAULT 0,
                        ExitCode           INTEGER NULL,
                        RawJson            TEXT NULL,
                        RawOutput          TEXT NULL,
                        ErrorOutput        TEXT NULL,
                        Notes              TEXT NULL,

                        CONSTRAINT FK_BenchmarkRuns_Models
                            FOREIGN KEY (ModelId)
                            REFERENCES Models(ModelId)
                    );
                """)

                conn.execute_sql(sql="""
                    CREATE TABLE IF NOT EXISTS BenchmarkSettings
                    (
                        BenchmarkSettingId INTEGER PRIMARY KEY AUTOINCREMENT,
                        BenchmarkRunId     INTEGER NOT NULL,
                        SettingName        TEXT NOT NULL,
                        SettingValue       TEXT NULL,

                        CONSTRAINT FK_BenchmarkSettings_BenchmarkRuns
                            FOREIGN KEY (BenchmarkRunId)
                            REFERENCES BenchmarkRuns(BenchmarkRunId)
                            ON DELETE CASCADE,

                        CONSTRAINT UQ_BenchmarkSettings_RunName
                            UNIQUE (BenchmarkRunId, SettingName)
                    );
                """)

                conn.execute_sql("""
                    CREATE TABLE IF NOT EXISTS BenchmarkResults
                    (
                        BenchmarkResultId      INTEGER PRIMARY KEY AUTOINCREMENT,
                        BenchmarkRunId         INTEGER NOT NULL,

                        TestType               TEXT NULL,
                        TestTime               TEXT NULL,
                        NPrompt                INTEGER NULL,
                        NGen                   INTEGER NULL,
                        NDepth                 INTEGER NULL,
                        AvgNs                  INTEGER NULL,
                        StddevNs               INTEGER NULL,
                        AvgTokensPerSecond     REAL NULL,
                        StddevTokensPerSecond  REAL NULL,
                        SamplesNsJson          TEXT NULL,
                        SamplesTokensPerSecondJson          TEXT NULL,
                        RawJson                TEXT NULL,
                        CreatedAt              TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,


                        CONSTRAINT FK_BenchmarkResults_BenchmarkRuns
                            FOREIGN KEY (BenchmarkRunId)
                            REFERENCES BenchmarkRuns(BenchmarkRunId)
                            ON DELETE CASCADE
                    );
                """)
                conn.execute_sql("""
                    CREATE TABLE IF NOT EXISTS Hosts
                    (
                        HostId        INTEGER PRIMARY KEY AUTOINCREMENT,
                        HostName      TEXT NOT NULL,
                        OsName        TEXT NULL,
                        OsVersion     TEXT NULL,
                        CpuInfo       TEXT NULL,
                        RamBytes      INTEGER NULL,
                        Notes         TEXT NULL,
                        CreatedAt     TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                        CONSTRAINT UQ_Hosts_HostName UNIQUE (HostName)
                    );                
                """)    

            except sqlite3.Error as exc:
                #conn.rollback()
                if self.logger is not None:
                    self.logger.exception(f"Error creating SQLite benchmark tables: {exc}")

            finally:
                pass


