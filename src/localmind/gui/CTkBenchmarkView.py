# CTkBenchmarkView.py

import customtkinter as ctk # type: ignore
import tkinter as tk
import copy
from datetime import datetime
import socket

from localmind.widgets.CTkYesNo import CTkYesNo
from localmind.widgets.LlamaBenchSettingsDialog import LlamaBenchSettingsDialog

from localmind.gui.CTkAppData import CTkAppData

from localmind.gui.CTkAppView import CTkAppView, FontSpec

from localmind.utils.LlamaBenchmarkData import LlamaBenchmarkData, parse_results, LlamaBenchModelInfo, LlamaBenchRunInfo, LlamaBenchResult
from localmind.utils.kill_llama_servers import kill_llama_servers, get_llama_server_procs

import hashlib
import json
from pathlib import Path
import os
from enum import IntEnum

from typing import List, Optional, Any
from localmind.gui.LocalMindSettings import LocalMindSettings, resolve_llama_executable
from localmind.utils.llama_bench_help_spec import HELP_SPEC
from localmind.utils.pyodbcext import pyOdbcExt
from localmind.utils.PySqliteExt import SqliteExt

from logging import Logger

import subprocess
import threading

def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def json_dumps(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, default=str)


def stable_model_identity(raw: dict[str, Any]) -> str:
    model_filename = str(raw.get("model_filename") or "")
    model_file_name = Path(model_filename).name

    return "|".join(
        [
            model_file_name,
            str(raw.get("model_size") or ""),
            str(raw.get("model_n_params") or ""),
            str(raw.get("model_type") or ""),
        ]
    )

class CTkBenchmarkView(CTkAppView):
    class status(IntEnum):
        STOP = 0
        RUN = 1
        ERROR = 2

    def __init__(self, parent: ctk.CTk, frame: ctk.CTkFrame, font: FontSpec, data: CTkAppData) -> None:
        super().__init__(parent, frame, font, data)
        self._settings: dict[str, Any] = copy.deepcopy(HELP_SPEC)
        self.lm_server_settings: LocalMindSettings = LocalMindSettings(app_name=self.data._app_name if self.data._app_name is not None else "LocalMind",
                                                              logger=self.data.logger)
        self.benchmark_options = self.data.benchmark_settings
        self.benchmark_process: subprocess.Popen[str] | None = None
        self.benchmark_running: bool = False
        self.benchmark_output: str = ""
        self.benchmark_data = LlamaBenchmarkData(use_sqlsvr=self.data.use_sqlsvr, sqlite_filename=self.data.database_path, logger=self.data.logger)
        self.llama_bench_results: list[LlamaBenchResult]
        self.llama_bench_model_info: list[LlamaBenchModelInfo]
        self.llama_bench_run_info: list[LlamaBenchRunInfo]
        self.server = os.environ.get('SQL_SERVER', "127.0.0.1")
        self.port = int(os.environ.get('SQL_PORT', 1433))
        self._database: str = self.data.database_path
        self.user = os.environ.get('SQL_SVR_USER', "crash")
        self.password = os.environ.get('SQL_SVR_PASSWORD', "")
        self.driver = os.environ.get('SQL_SVR_DRIVER', "ODBC Driver 18 for SQL Server")

        self.start_time: datetime | None = None
        self.end_time: datetime | None = None
        self.last_benchmark_command: list[str] | None = None

        self.initialize_widgets()

    def get_connection_string(self, database: Optional[str] = None) -> str:
        db = database if database is not None else self._database
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
        return conn_str
    

    def sb_button_list(self) -> List[str]: # no buttones yet
        return  [
                'first', # start
                'last',  # stop
                'edit',  # edit the settings for the current filter, GPU/MODEL/BACKEND
                'new'    # clear the graph
                ]


    def on_visible(self) -> None:
        """ Called when the view becomes visible. Override in derived classes for custom behavior.
            In this case, we want to change the text of the buttons we use to reflect the current view.
        """

        self.data.logger.debug(f"{self.__class__}.on_visible() called")
        self.set_button_names({
            "first": "Start",
            "last": "Stop",
            "edit": "Parameters",
            "new": "Clear"
        })
        if self.run_button is not None and self.stop_button is not None:
            if self.benchmark_running:
                self.run_button.configure(state="disabled")
                self.stop_button.configure(state="normal")
            else:
                self.run_button.configure(state="normal")
                self.stop_button.configure(state="disabled")
    

    def initialize_widgets(self) -> None:
        # set the start and stop buttons
        self.run_button: ctk.CTkButton | None = self.data.get_button('first')
        self.stop_button: ctk.CTkButton | None = self.data.get_button('last')
        self.clear_button: ctk.CTkButton | None = self.data.get_button('new')
        self.edit_button: ctk.CTkButton | None = self.data.get_button('edit')

        # relabel the sidebar buttons to Start and Stop and enable them
        if self.run_button is not None:
            self.run_button.configure(state="normal")
        if self.stop_button is not None:
            self.stop_button.configure(state="disabled")    
        if self.run_button is not None:
            self.run_button.configure(text='Start')
        if self.stop_button is not None:
            self.stop_button.configure(text='Stop')
        if self.clear_button is not None:
            self.clear_button.configure(text='Clear')
        if self.edit_button is not None:
            self.edit_button.configure(text='Parameters')

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(3, weight=1)
        self.frame.grid_rowconfigure([0,1,2], weight=0)
        self.command_line_label_frame = ctk.CTkFrame(self.frame, bg_color='transparent')
        self.command_line_label_frame.grid(row=0,column=0, sticky='new', padx=5, pady=5)
        self.command_line_label_frame.grid_columnconfigure(0, weight=1)
        self.command_line_label = ctk.CTkLabel(self.command_line_label_frame, text="llama-bench command line", font=self.font)
        self.command_line_label.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

        self.settings_textbox_frame = ctk.CTkFrame(self.frame, bg_color='transparent')
        self.settings_textbox_frame.grid(row=1,column=0, sticky='new', padx=5, pady=5)
        self.settings_textbox_frame.grid_columnconfigure(0, weight=1)

        self.settings_textbox = ctk.CTkTextbox(self.settings_textbox_frame,
                                               wrap="word",
                                               # text=" ".join(self.build_benchmark_command(llama_bench_path='llama-bench', options=self.benchmark_options))
                                               font=self.font)
        self.settings_textbox.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.console_label_frame = ctk.CTkFrame(self.frame, bg_color='transparent')
        self.console_label_frame.grid(row=2,column=0, sticky='nsew', padx=5, pady=5)
        self.console_label_frame.grid_columnconfigure(0, weight=1)

        self.console_label = ctk.CTkLabel(self.console_label_frame, text="llama-bench Output", font=self.font)
        self.console_label.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        self.console_frame = ctk.CTkFrame(self.frame, bg_color='transparent')
        self.console_frame.grid(row=3,column=0, sticky='nsew', padx=5, pady=5)
        self.console_frame.grid_columnconfigure(0, weight=1)
        self.console_frame.grid_rowconfigure(0, weight=1)
        self.console = ctk.CTkTextbox(self.console_frame, wrap="word", font=self.font)
        self.console.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')


        """
        self.console_frame = self.labeled_frame(self.frame, 
                                                label="llama-bench Output", 
                                                parent_row=0,
                                                parent_column=0,
                                                columns=1,
                                                column_weight=[1])
        self.console = ctk.CTkTextbox(self.console_frame, wrap="word", font=self.font)
        self.console.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.arguement_frame = self.labeled_frame(self.frame,
                                                    label='llama-bench command line',
                                                    parent_row=1,
                                                    parent_column=0,
                                                    columns=1,
                                                    column_weight=[1])
        self.settings_textbox = ctk.CTkTextbox(self.arguement_frame,
                                               wrap="word",
                                               # text=" ".join(self.build_benchmark_command(llama_bench_path='llama-bench', options=self.benchmark_options))
                                               font=self.font)
        self.settings_textbox.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        """
        self.update_benchmark_summary()

    def append_console(self, text: str) -> None:
        self.console.insert("end", text)
        self.console.see("end")

    def set_server_running(self, running: bool) -> None:
        if self.run_button is not None and self.stop_button is not None:
            self.run_button.configure(state="disabled" if running else "normal")
            self.stop_button.configure(state="normal" if running else "disabled")

    def run_benchmark(self) -> None:
        if self.benchmark_running:
            return
        running_servers = get_llama_server_procs()
        if running_servers:
            yes_no = CTkYesNo(self.parent, 
                              title="Terminate Running Servers", 
                              message=f"Found {len(running_servers)} running llama-server processes. Do you want to terminate them?", 
                              font=self.font)
            if yes_no.result is False:
                self.append_console("User chose not to terminate running llama-server processes. Aborting benchmark start.\n")
                return 
            self.append_console(f"Found {len(running_servers)} running llama-server processes. Attempting to terminate them...\n")
            pids = kill_llama_servers(logger=self.data.logger)
            if pids:
                self.append_console(f"Terminated llama-server processes: {pids}\n")
            else:
                self.append_console("No running llama-server processes found.\n")
        
        self.lm_server_settings = LocalMindSettings(app_name=self.data._app_name if self.data._app_name is not None else "LocalMind",
                                                              logger=self.data.logger)

        self.start_time = datetime.now()
        if self.benchmark_options is not None:
            cmd = self.build_benchmark_command(
                llama_bench_path=str(resolve_llama_executable(self.lm_server_settings.settings, 'llama-bench')), # self.data.llama_bench_path,
                options=self.benchmark_options,
            )
        else:
            cmd = self.build_benchmark_command(
                llama_bench_path=str(resolve_llama_executable(self.lm_server_settings.settings, 'llama-bench')), # self.data.llama_bench_path,
                options={},
            )


        self.benchmark_running = True
        self.set_benchmark_buttons_running(True)
        self.append_benchmark_output("$ " + " ".join(cmd) + "\n\n")

        thread = threading.Thread(
            target=self._benchmark_worker,
            args=(cmd,),
            daemon=True,
        )
        thread.start()

    def append_benchmark_output(self, text: str) -> None:
        self.console.configure(state="normal")
        self.console.insert(tk.END, text)
        self.console.see(tk.END)
        self.console.configure(state="disabled")

    def _benchmark_worker(self, cmd: list[str]) -> None:
        try:
            self.benchmark_output = ""

            self.benchmark_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                env=os.environ.copy(),
            )

            assert self.benchmark_process.stdout is not None

            for line in self.benchmark_process.stdout:
                self.parent.after(0, self.append_benchmark_output, line)
                self.benchmark_output += line

            return_code = self.benchmark_process.wait()

            self.parent.after(
                0,
                self._benchmark_finished,
                return_code,
            )

        except Exception as exc:
            self.parent.after(0, self.append_benchmark_output, f"\n[ERROR] {exc}\n")
            self.parent.after(0, self._benchmark_finished, -1)

    def _benchmark_finished(self, return_code: int) -> None:
        self.end_time = datetime.now()
        self.benchmark_running = False
        self.benchmark_process = None
        self.set_benchmark_buttons_running(False)

        def extract_json_from_llama_output(output: str) -> str:
            """
            Extract JSON from llama-bench output that may contain backend log headers
            before the actual JSON.

            Supports JSON arrays or objects.
            """

            text = output.strip()

            array_start = text.find("[")

            json_start = output.find("[")

            if json_start == -1:
                raise ValueError("No JSON array found in llama-bench output.")

            json_text = output[json_start:].strip()

            # Validate that the extracted text is actually valid JSON.
            json.loads(json_text)

            return json_text
        if return_code == 0:
            self.append_benchmark_output("\n[Benchmark completed successfully]\n")
            raw = extract_json_from_llama_output(self.benchmark_output)
            self.llama_bench_results = parse_results(raw)
            self.data.logger.debug(f"results: {self.llama_bench_results}")

            if self.llama_bench_results:
                self.save_llama_bench_results(self.llama_bench_results)
        else:
            self.append_benchmark_output(f"\n[Benchmark exited with code {return_code}]\n")

    def save_llama_bench_results(self, results: list[LlamaBenchResult] | None) -> None:
        if not results:
            return

        first_raw = results[0].raw

        model_id = self.upsert_model(first_raw)
        run_id = self.insert_benchmark_run(first_raw, model_id)

        for result in results:
            self.insert_benchmark_result(
                run_id=run_id,
                result=result,
            )

        self.data.logger.debug(
            "Saved llama-bench results: model_id=%s, run_id=%s, result_count=%s",
            model_id,
            run_id,
            len(results),
        )

    def upsert_model(self, raw: dict[str, Any]) -> int:
        model_filename = str(raw.get("model_filename") or "")
        model_file_name = Path(model_filename).name

        model_type = raw.get("model_type")
        model_size = raw.get("model_size")
        model_n_params = raw.get("model_n_params")

        model_identity_hash = sha256_text(stable_model_identity(raw))
        model_path_hash = sha256_text(model_filename.lower())

        if not self.data.use_sqlsvr:
            conn: SqliteExt | pyOdbcExt = SqliteExt(self.data.database_path, logger=self.data.logger)
            table_id: str = "Models"
        else:
            conn = pyOdbcExt(self.get_connection_string(), logger=self.data.logger)
            table_id = "dbo.Models"

        result = conn.execute_sql(
            sql=
            f"""
            SELECT ModelId
            FROM {table_id}
            WHERE ModelIdentityHash = ?
            """,
            parameters=(model_identity_hash,),
            fetch_results=True,
            return_dict=True
        )

        if result and isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict) and "ModelId" in result[0]:
            return int(result[0]["ModelId"])

        if self.data.use_sqlsvr:
            conn.execute_sql( # ModelFamily, Quantitization, ModelSha256, Notes
                f"""
                INSERT INTO {table_id}
                (
                    ModelName, 
                    ModelPath, 
                    ModelPathHash, 
                    ModelIdentityHash,
                    ModelFileName,
                    ModelSizeBytes,
                    ModelParameterCount,
                    ModelType,
                    CreatedAt
                )
                OUTPUT INSERTED.ModelId
                VALUES
                (
                    ?, ?, ?, ?, ?, ?, ?, ?, SYSUTCDATETIME()
                )
                """,
                parameters=(
                    model_file_name,
                    model_filename,
                    model_path_hash,
                    model_identity_hash,
                    model_file_name,
                    model_size,
                    model_n_params,
                    model_type,
                ),
            )
        else:
            conn.execute_sql(
                f"""
                INSERT INTO {table_id}
                (
                    ModelName, 
                    ModelPath, 
                    ModelPathHash, 
                    ModelIdentityHash,
                    ModelFileName,
                    ModelSizeBytes,
                    ModelParameterCount,
                    ModelType,
                    CreatedAt
                )
                VALUES
                (
                    ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP
                )
                """,
                parameters=(
                    model_file_name,
                    model_filename,
                    model_path_hash,
                    model_identity_hash,
                    model_file_name,
                    model_size,
                    model_n_params,
                    model_type,
                ),
            )

        result = conn.execute_sql(
            sql=
            f"""
            SELECT ModelId
            FROM {table_id}
            WHERE ModelIdentityHash = ?
            """,
            parameters=(model_identity_hash,),
            fetch_results=True,
            return_dict=True
        )

        if result and isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict) and "ModelId" in result[0]:
            return int(result[0]["ModelId"])
        else:
            raise ValueError("Failed to upsert model and retrieve ModelId.")
    
    def insert_benchmark_run(self, raw: dict[str, Any], model_id: int) -> int:
        # conn = pyOdbcExt(self.get_connection_string(), logger=self.data.logger)
        if not self.data.use_sqlsvr:
            conn: SqliteExt | pyOdbcExt = SqliteExt(self.data.database_path, logger=self.data.logger)
            table_id: str = "BenchmarkRuns"
        else:
            conn = pyOdbcExt(self.get_connection_string(), logger=self.data.logger)
            table_id = "dbo.BenchmarkRuns"


        llama_bench_version = (
            f"{raw.get('build_number')}-{raw.get('build_commit')}"
            if raw.get('build_number') is not None and raw.get('build_commit')
            else str(raw.get('build_number') or raw.get('build_commit') or "")
        )
        def get_host_name() -> str:
            """Return the local machine hostname in a cross-platform way."""
            host_name = socket.gethostname().strip()

            if not host_name:
                return "unknown-host"

            return host_name

        if self.data.use_sqlsvr:
            result = conn.execute_sql(
                sql=
                    f"""
                    INSERT INTO {table_id}
                    (
                        ModelId,
                        RunStartedAt,
                        RunFinishedAt,
                        CommandLine,
                        llamaBenchVersion,
                        Backend,
                        HostName,
                        CpuInfo,
                        GpuInfo,
                        Success,
                        ExitCode,
                        RawJson,
                        RawOutput,
                        ErrorOutput,
                        Notes
                    )
                    OUTPUT INSERTED.BenchmarkRunId
                    VALUES
                    (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                    """,
                parameters=(
                    model_id,
                    self.start_time,
                    self.end_time,
                    " ".join(self.last_benchmark_command) if self.last_benchmark_command else "",
                    llama_bench_version,
                    raw.get("backends"),
                    get_host_name(),
                    raw.get("cpu_info"),
                    raw.get("gpu_info"),
                    1,
                    0,
                    json.dumps(raw),
                    "",
                    "",
                    ""
                )
            )
        else:
            result = conn.execute_sql(
                sql=
                    f"""
                    INSERT INTO {table_id}
                    (
                        ModelId,
                        RunStartedAt,
                        RunFinishedAt,
                        CommandLine,
                        llamaBenchVersion,
                        Backend,
                        HostName,
                        CpuInfo,
                        GpuInfo,
                        Success,
                        ExitCode,
                        RawJson,
                        RawOutput,
                        ErrorOutput,
                        Notes
                    )
                    VALUES
                    (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                    """,
                parameters=(
                    model_id,
                    self.start_time,
                    self.end_time,
                    " ".join(self.last_benchmark_command) if self.last_benchmark_command else "",
                    llama_bench_version,
                    raw.get("backends"),
                    get_host_name(),
                    raw.get("cpu_info"),
                    raw.get("gpu_info"),
                    1,
                    0,
                    json.dumps(raw),
                    "",
                    "",
                    ""
                )
            )

        result = conn.execute_sql(
                    sql =
                        f"""
                        SELECT BenchmarkRunId from {table_id}
                        WHERE ModelId = ? AND RunStartedAt = ? AND RunFinishedAt = ?
                        """,
                    parameters=(
                        model_id,
                        self.start_time,
                        self.end_time
                    ),
                    fetch_results=True,
                    return_dict=True
            )   

        if result and isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict) and "BenchmarkRunId" in result[0]:
            return int(result[0]["BenchmarkRunId"])
        else:
            raise ValueError("Failed to upsert model and retrieve benchmarkRunId.")


        return int(result[0]["BenchmarkRunId"])

    def insert_benchmark_result(
        self,
        run_id: int,
        result: LlamaBenchResult,
    ) -> int:
        raw = result.raw

        if not self.data.use_sqlsvr:
            conn: SqliteExt | pyOdbcExt = SqliteExt(self.data.database_path, logger=self.data.logger)
            table_id: str = "BenchmarkResults"
            conn.execute_sql(
                sql =
                    f"""
                        INSERT INTO {table_id}
                        (
                            BenchmarkRunId,
                            TestType,
                            TestTime,
                            NPrompt,
                            NGen,
                            NDepth,
                            AvgNs,
                            StddevNs,
                            AvgTokensPerSecond,
                            StddevTokensPerSecond,
                            SamplesNsJson,
                            SamplesTokensPerSecondJson,
                            RawJson,
                            CreatedAt
                        )
                        VALUES
                        (
                            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP
                        )
                    """,
                parameters=(    
                    run_id,
                    result.test_type,
                    result.test_time,
                    raw.get("n_prompt"),
                    raw.get("n_gen"),
                    raw.get("n_depth"),
                    raw.get("avg_ns"),
                    raw.get("stddev_ns"),
                    json_dumps(raw.get("avg_ts")),
                    json_dumps(raw.get("stddev_ts")),
                    json_dumps(raw.get("samples_ns")),
                    json_dumps(raw.get("samples_ts")),
                    json_dumps(raw),
                )
            )

        else:
            conn = pyOdbcExt(self.get_connection_string(), logger=self.data.logger)
            table_id = "dbo.BenchmarkResults"

            # conn = pyOdbcExt(self.get_connection_string(), logger=self.data.logger)

            conn.execute_sql(
                sql =
                    f"""
                        INSERT INTO {table_id}
                        (
                            BenchmarkRunId,
                            TestType,
                            TestTime,
                            NPrompt,
                            NGen,
                            NDepth,
                            AvgNs,
                            StddevNs,
                            AvgTokensPerSecond,
                            StddevTokensPerSecond,
                            SamplesNsJson,
                            SamplesTokensPerSecondJson,
                            RawJson,
                            CreatedAt
                        )
                        OUTPUT INSERTED.BenchmarkResultId
                        VALUES
                        (
                            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, SYSUTCDATETIME()
                        )
                    """,
                parameters=(    
                    run_id,
                    result.test_type,
                    result.test_time,
                    raw.get("n_prompt"),
                    raw.get("n_gen"),
                    raw.get("n_depth"),
                    raw.get("avg_ns"),
                    raw.get("stddev_ns"),
                    json_dumps(raw.get("avg_ts")),
                    json_dumps(raw.get("stddev_ts")),
                    json_dumps(raw.get("samples_ns")),
                    json_dumps(raw.get("samples_ts")),
                    json_dumps(raw),

                )
            )
                    
        #row = cursor.fetchone()
        #conn.commit()

        res = conn.execute_sql(
            sql=
                f"""
                SELECT BenchmarkResultId
                FROM {table_id}
                WHERE BenchmarkRunId = ? AND TestType = ? AND TestTime= ?
                """,
            parameters=(
                run_id,
                result.test_type,
                result.test_time,
            ),
            fetch_results=True,
            return_dict=True
        ) 

        if res is None or not isinstance(res, list) or len(res) == 0 or not isinstance(res[0], dict) or "BenchmarkResultId" not in res[0]:
            raise RuntimeError("Failed to insert benchmark result.")

        return int(res[0]["BenchmarkResultId"])

    def stop_benchmark(self) -> None:
        if self.benchmark_process is not None:
            self.benchmark_process.terminate()
            self.append_benchmark_output("\n[Stopping benchmark...]\n")

    def update_benchmark_summary(self) -> None:
        self.settings_textbox.configure(state="normal")
        self.settings_textbox.delete("1.0", tk.END)

        if not self.benchmark_options:
            self.settings_textbox.insert(tk.END, "Using llama-bench defaults.\n")
        else:
            for key, value in sorted(self.benchmark_options.items()):
                if isinstance(value, bool):
                    self.settings_textbox.insert(tk.END, f"{key}\n")
                else:
                    self.settings_textbox.insert(tk.END, f"{key} {value}\n")

        self.settings_textbox.configure(state="disabled")

    def set_benchmark_buttons_running(self, running: bool) -> None:
        if self.run_button is not None and self.stop_button is not None and self.edit_button is not None:
            self.run_button.configure(state="disabled" if running else "normal")
            self.stop_button.configure(state="normal" if running else "disabled")
            self.edit_button.configure(state="disabled" if running else "normal")       

    def on_sidebar_edit(self) -> None:
        if self.data.benchmark_settings is None or "--output" not in self.data.benchmark_settings or self.data.benchmark_settings["--output"] != "json":
            if self.data.benchmark_settings is None:
                self.data.benchmark_settings = {}
            self.data.benchmark_settings["--output"] = "json"
            self.settings_textbox.insert(tk.END, "Forcing json output.\n")
        bsdlg = LlamaBenchSettingsDialog(self.parent, 
                                              self._settings, 
                                              font=self.font, 
                                              title="Benchmark Settings", 
                                              current_options=self.data.benchmark_settings )
        self.benchmark_options = bsdlg.result

        if self.benchmark_options is None:
            return
        self.data.benchmark_settings = self.benchmark_options
        self.update_benchmark_summary()

    def clear_benchmark_output(self) -> None:
        self.console.configure(state="normal")
        self.console.delete("1.0", tk.END)
        self.console.configure(state="disabled")


    def on_sidebar_new(self) -> None:
        """This sidebar buttons provides the clear function """
        self.clear_benchmark_output()

    def build_benchmark_command(
        self,
        llama_bench_path: str,
        options: dict[str, Any]
    ) -> list[str]:
        if options is None:
            return [llama_bench_path]
        cmd = [llama_bench_path]

        for option, value in options.items():
            if isinstance(value, bool):
                if value:
                    cmd.append(option)
            else:
                cmd.extend([option, str(value)])
        self.last_benchmark_command = cmd
        return cmd

    def on_sidebar_first(self) -> None:
        """Start the benchmark """
        self.run_benchmark()

        return None

    def on_sidebar_last(self) -> None:
        "Stop the server"
        self.stop_benchmark()
        return None
