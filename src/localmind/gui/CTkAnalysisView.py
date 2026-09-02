# CTkAnalysisView.py

import customtkinter as ctk # type: ignore
import sys
import os
import shutil
import subprocess
from pathlib import Path
import tkinter as tk
import pandas as pd
import seaborn as sns
from datetime import date, datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from localmind.widgets.CTkDialog import CTkDialog
from localmind.widgets.CTkSelectReportType import CTkSelectReportType
from localmind.widgets.CTkBoolListbox import CTkBoolListbox
from localmind.widgets.CTkRadioListbox import CTkRadioListbox
from localmind.widgets.ctkDateRangePicker import CTkDateRangePicker
from localmind.widgets.CTkMarkdownView import CTkMarkdownView
from localmind.gui.CTkAppData import CTkAppData
from localmind.gui.CTkAppView import CTkAppView, FontSpec
from localmind.gui.LocalMindSettings import LocalMindSettings

import json
from enum import Enum

from typing import List, Optional, Any, Literal, cast
from localmind.utils.pyodbcext import pyOdbcExt
from localmind.utils.PySqliteExt import SqliteExt

class ChartType(Enum):
    HORIZONTAL_BAR = "Horizontal Bar"
    VERTICAL_BAR = "Vertical Bar"
    LINE = "Line"
    SCATTER = "Scatter"

class CategoryType(Enum):
    MODEL = "Model"
    BACKEND = "Backend"
    GPU = "GPU"
    HOST = "Host"
    LLAMA_BENCH_VERSION = "LlamaBench Version"
    TEST_TYPE = "Test Type"

class BackendType(Enum):
    VULKAN = "Vulkan"
    SYCL = "SYCL"

class MetricType(Enum):
    AVG_TOKENS_PER_SECOND = "Average Tokens per Second"
    MODEL_SIZE_BYTES = "Model Size (Bytes)"
    MODEL_PARAMETER_COUNT = "Model Parameter Count"


class EditFiltersDialog(ctk.CTkToplevel):
    """
    A dialog for editing filters. This dialog allows the user to select a filter type (Model, Backend, GPU, Host, or Time Range) 
    and then select specific items for that filter type. 
    The selected filters are stored in a dictionary and can be retrieved after the dialog is closed.
    """
    def __init__(self, 
                 parent: ctk.CTk | ctk.CTkFrame, 
                 title: str='Filters', 
                 message='Select Filters', 
                 font: Optional[FontSpec]=None,
                 hosts: Optional[List[str]]=None,
                 gpus: Optional[List[str]]=None,
                 models: Optional[List[str]]=None,
                 backends: Optional[List[str]]=None,
                 llama_bench_versions: Optional[List[str]]=None,
                 llama_bench_test_types: Optional[List[str]]=None,
                 initial_group_by: Optional[str]=None,
                 initial_filters: Optional[dict[str, list[str] | tuple[str, str]]]=None,
                 ):
        
        super().__init__(parent)
        self.title(title)
        self.parent = parent
        self.hosts: list[str] = hosts if hosts is not None else []
        self.gpus: list[str] = gpus if gpus is not None else []
        self.models: list[str] = models if models is not None else []
        self.backends: list[str] = backends if backends is not None else []
        self.llama_bench_versions: list[str] = llama_bench_versions if llama_bench_versions is not None else []
        self.llama_bench_test_types: list[str] = llama_bench_test_types if llama_bench_test_types is not None else []
        self.font = font
        self.result: dict[str, list[str] | tuple[str, str]] | None = None # Store the result here (the edited filter text)
        self._result: dict[str, list[str] | tuple[str, str]] = initial_filters if initial_filters is not None else {}
        self.group_by: str | None = initial_group_by
        self.transient(cast(ctk.CTk, parent))
        self.geometry("900x800")
        self.start_date: date | None = None
        self.end_date: date | None = None
        # self.group_by: str | None = initial_group_by
        self.selected_models: list[str] = []
        self.selected_backends: list[str] = []
        self.selected_gpus: list[str] = []
        self.selected_hosts: list[str] = []
        self.selected_test_types: list[str] = []
        self.selected_versions: list[str] = []

        if self._result is not None:
            if "Model" in self._result and isinstance(self._result["Model"], list):
                self.selected_models = self._result["Model"]
            if "Backend" in self._result and isinstance(self._result["Backend"], list):
                self.selected_backends = self._result["Backend"]
            if "GPU" in self._result and isinstance(self._result["GPU"], list):
                self.selected_gpus = self._result["GPU"]
            if "Host" in self._result and isinstance(self._result["Host"], list):
                self.selected_hosts = self._result["Host"]
            if "Test Type" in self._result and isinstance(self._result["Test Type"], list):
                self.selected_test_types = self._result["Test Type"]
            if "LlamaBench Version" in self._result and isinstance(self._result["LlamaBench Version"], list):
                self.selected_versions = self._result["LlamaBench Version"]

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure([2], weight=1)

        #self.grid_columnconfigure(1, weight=1)
        #self.grid_rowconfigure(1, weight=1)

        message_label = ctk.CTkLabel(self, text=message, font=font)
        message_label.grid(row=0, column=0, padx=10, pady=(10,10), sticky='ew')

        self.radio_frame = ctk.CTkFrame(self, bg_color='transparent')
        self.radio_frame.grid(row=1, column=0, padx=10, pady=(10, 10), sticky="ew")
        self.radio_frame.grid_columnconfigure([0, 1, 2], weight=1)

        self.radio_var = ctk.StringVar(value="Model")
        self.model_radio = ctk.CTkRadioButton(self.radio_frame, text="Model", variable=self.radio_var, value="Model", font=font)
        self.model_radio.grid(row=0, column=0, padx=10, pady=(10,10), sticky='ew')
        self.backend_radio = ctk.CTkRadioButton(self.radio_frame, text="Backend", variable=self.radio_var, value="Backend", font=font)
        self.backend_radio.grid(row=1, column=0, padx=10, pady=(10,10), sticky='ew')
        self.gpu_radio = ctk.CTkRadioButton(self.radio_frame, text="GPU", variable=self.radio_var, value="GPU", font=font)
        self.gpu_radio.grid(row=2, column=0, padx=10, pady=(10,10), sticky='ew')
        self.host_radio = ctk.CTkRadioButton(self.radio_frame, text="Host", variable=self.radio_var, value="Host", font=font)
        self.host_radio.grid(row=0, column=1, padx=10, pady=(10,10), sticky='ew')
        self.test_type_radio = ctk.CTkRadioButton(self.radio_frame, text="Test Type", variable=self.radio_var, value="Test Type", font=font)
        self.test_type_radio.grid(row=1, column=1, padx=10, pady=(10,10), sticky='ew')
        self.time_range_radio = ctk.CTkRadioButton(self.radio_frame, text="Time Range", variable=self.radio_var, value="Time Range", font=font)
        self.time_range_radio.grid(row=2, column=1, padx=10, pady=(10,10), sticky='ew')
        self.llama_version_radio = ctk.CTkRadioButton(self.radio_frame, text="LlamaBench Version", variable=self.radio_var, value="LlamaBench Version", font=font)
        self.llama_version_radio.grid(row=0, column=2, padx=10, pady=(10,10), sticky='ew')

        # filter window frame
        self.filter_frame = ctk.CTkFrame(self, bg_color='transparent')
        self.filter_frame.grid(row=2, column=0, padx=10, pady=(10, 10), sticky="nsew")
        self.filter_frame.grid_columnconfigure(0, weight=1)
        self.filter_frame.grid_rowconfigure(0, weight=1)
        self.filter_box = ctk.CTkTextbox(self.filter_frame, font=font, state="disabled") # width=400, height=200,
        self.filter_box.grid(row=0, column=0, padx=10, pady=(10,10), sticky='nsew') 
        

        # Buttons frame
        button_frame = ctk.CTkFrame(self, bg_color='transparent')
        button_frame.grid(row=3, column=0, padx=10, pady=(10, 10), sticky="ew")

        # button_frame.grid_rowconfigure(2, weight=1)
        button_frame.grid_columnconfigure([0,1,2,3], weight=1)

        #button_frame.pack(pady=10)
        self.select_button = ctk.CTkButton(button_frame, text="Select", command=self.select_clicked, font=font)
        self.select_button.grid(row=0, column=0, padx=10, pady=(10,10), sticky='ew')
        self.group_by_button = ctk.CTkButton(button_frame, text="Group By", command=self.group_by_clicked, font=font)
        self.group_by_button.grid(row=0, column=3, padx=10, pady=(10,10), sticky='ew')
        self.done_button = ctk.CTkButton(button_frame, text="Done", command=self.yes_clicked, font=font)
        self.done_button.grid(row=0, column=1, padx=10, pady=(10,10), sticky='ew')
        self.cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=self.no_clicked, font=font)
        self.cancel_button.grid(row=0, column=2, padx=10, pady=(10,10), sticky='ew')
        # Center the dialog over parent
        self.center_on_parent(parent)
        
        self.protocol("WM_DELETE_WINDOW", self.no_clicked)  # Treat window close as 'No'
        self.wait_visibility()
        self.lift(self.parent)
        self.grab_set()
        self.update_filter_box(self.format_filters(self._result))        
        self.wait_window(self)

    def group_by_clicked(self):
        dlg = CTkRadioListbox(self.parent, 
                              title="Select Group By", 
                              items=["None", "Backend", "Test Type", "Host", "GPU", "Model", "LlamaBench Version"], selected_item=self.group_by, font=self.font)
        self.group_by = dlg.result
        self.update_filter_box(self.format_filters(self._result))

    def update_filter_box(self, filter_text: str) -> None:
        self.filter_box.configure(state="normal")
        self.filter_box.delete("1.0", "end")
        self.filter_box.insert("1.0", filter_text)
        self.filter_box.configure(state="disabled")

    def format_filters(self, filters: dict[str, list[str] | tuple[str, str]]) -> str:
        lines: list[str] = []

        for name, value in filters.items():
            lines.append(name)

            if isinstance(value, tuple):
                lines.append(f"    {value[0]} → {value[1]}")
            else:
                for item in value:
                    lines.append(f"    • {item}")

            lines.append("")

        if self.group_by:
            lines.append("Group By")
            lines.append(f"    • {self.group_by}")

        return "\n".join(lines)

    def select_clicked(self):
        filter_item = self.radio_var.get()
        match filter_item:
            case "Time Range":
                start_date = datetime.now().date()
                dr = CTkDateRangePicker(cast(ctk.CTk, self.parent), font=self.font if self.font is not None else None)
                self.start_date = dr.begin_date
                self.end_date = dr.end_date
                if self.start_date and self.end_date:
                    self._result['Time Range'] = (self.start_date.isoformat(), self.end_date.isoformat()) 
                # self._result = f""
            case "Model":
                dlg = CTkBoolListbox(cast(ctk.CTk, self.parent), title="Select Models", items=self.models, selected_items=self.selected_models, font=self.font)
                self.selected_models = dlg.get_selected_items()
                if isinstance(self.selected_models, list): # and len(self.selected_models) > 0: # we can clear all models
                    self._result['Model'] = self.selected_models
            case "Backend":
                dlg = CTkBoolListbox(cast(ctk.CTk, self.parent), title="Select Backends", items=self.backends, selected_items=self.selected_backends, font=self.font)
                self.selected_backends = dlg.get_selected_items()
                if isinstance(self.selected_backends, list): # and len(self.selected_backends) > 0:
                    self._result['Backend'] = self.selected_backends
            case "GPU":
                dlg = CTkBoolListbox(cast(ctk.CTk, self.parent), title="Select GPUs", items=self.gpus, selected_items=self.selected_gpus, font=self.font)
                self.selected_gpus = dlg.get_selected_items()
                if isinstance(self.selected_gpus, list): # and len(self.selected_gpus) > 0:
                    self._result['GPU'] = self.selected_gpus
            case "Host":
                dlg = CTkBoolListbox(cast(ctk.CTk, self.parent), title="Select Hosts", items=self.hosts, selected_items=self.selected_hosts, font=self.font)
                self.selected_hosts = dlg.get_selected_items()
                if isinstance(self.selected_hosts, list): # and len(self.selected_hosts) > 0:
                    self._result['Host'] = self.selected_hosts
            case "Test Type":
                dlg = CTkBoolListbox(cast(ctk.CTk, self.parent), title="Select Test Types", items=self.llama_bench_test_types, selected_items=self.selected_test_types, font=self.font)
                self.selected_test_types = dlg.get_selected_items()
                if isinstance(self.selected_test_types, list): # and len(self.selected_test_types) > 0:
                    self._result['Test Type'] = self.selected_test_types
            case "LlamaBench Version":
                dlg = CTkBoolListbox(cast(ctk.CTk, self.parent), title="Select LlamaBench Versions", items=self.llama_bench_versions, selected_items=self.selected_versions, font=self.font)
                self.selected_versions = dlg.get_selected_items()
                if isinstance(self.selected_versions, list): # and len(self.selected_versions) > 0:
                    self._result['LlamaBench Version'] = self.  selected_versions
        
        self.update_filter_box(self.format_filters(self._result))

    def center_on_parent(self, parent):
        # Update the geometry to get accurate dimensions
        self.update_idletasks()
        parent.update_idletasks()
        # Calculate position to center the dialog over the main application window
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        dialog_width = self.winfo_reqwidth()
        dialog_height = self.winfo_reqheight()

        position_x = parent_x + (parent_width / 2) - (dialog_width / 2)
        position_y = parent_y + (parent_height / 2) - (dialog_height / 2)

        # Set position
        self.geometry("+%d+%d" % (position_x, position_y))


    def yes_clicked(self):
        self.result = self._result
        self.destroy()

    def no_clicked(self):
        self.result = {}
        self.destroy()

GraphType = Literal[
    "Horizontal Bar",
    "Vertical Bar",
    "Line",
    "Scatter",
]


class CTkGraph(ctk.CTkFrame):
    DEFAULT_PLOT_THEMES: dict[str, str] = {
        "dark": "dark_background",
        "light": "seaborn-v0_8-whitegrid",
    }

    def __init__(
        self,
        parent: Any,
        dataframe: pd.DataFrame,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        # CTkFrame arguments must remain in kwargs. Remove graph-specific
        # arguments before calling CTkFrame.__init__().

        self.show_quant: bool = kwargs.pop(
            "show_quant",
            True,
        )
        self.font: ctk.CTkFont = kwargs.pop(
            "font",
            ctk.CTkFont(size=14),
        )

        self.title_font: ctk.CTkFont = kwargs.pop(
            "title_font",
            self.font,
        )
        self.xylabel_font: ctk.CTkFont = kwargs.pop(
            "xylabel_font",
            self.font,
        )
        self.xytick_font: ctk.CTkFont = kwargs.pop(
            "xytick_font",
            self.font,
        )

        self.graph_type: GraphType = kwargs.pop(
            "graph_type",
            "Vertical Bar",
        )

        self.title: str = kwargs.pop(
            "title",
            "Default Title",
        )
        self.xlabel: str = kwargs.pop(
            "xlabel",
            "X-axis",
        )
        self.ylabel: str = kwargs.pop(
            "ylabel",
            "Y-axis",
        )

        self.category: str = kwargs.pop(
            "category",
            "ModelName",
        )
        self.metric: str = kwargs.pop(
            "metric",
            "AvgTokensPerSecond",
        )
        self.hue: str | None = kwargs.pop(
            "hue",
            None,
        )

        self.plot_style: str = kwargs.pop(
            "plot_style",
            "auto",
        )

        self.estimator: str = kwargs.pop(
            "estimator",
            "mean",
        )

        self.show_legend: bool = kwargs.pop(
            "show_legend",
            True,
        )

        self.rotate_x_labels: float = kwargs.pop(
            "rotate_x_labels",
            45.0,
        )

        self.show_values: bool = kwargs.pop(
            "show_values",
            True,
        )

        self.dataframe = dataframe.copy()

        super().__init__(parent, *args, **kwargs)

        self.app_mode = ctk.get_appearance_mode()
        self.resolved_plot_style = self._resolve_plot_style(
            self.plot_style
        )

        self.figure: Figure
        self.axes: Any
        self._mpl_canvas: FigureCanvasTkAgg
        self.canvas_widget: tk.Canvas

        self._create_figure()
        self._create_canvas()
        self.draw()
        self.figure.savefig( Path.home() / ".LocalMind" / "performance_graph.png", dpi=200, bbox_inches='tight', facecolor=self.figure.get_facecolor())

    # ------------------------------------------------------------------
    # Figure and canvas creation
    # ------------------------------------------------------------------

    def colors(self)-> dict[str, str]:
        """Return a dictionary of colors used in the current Matplotlib style."""
        with plt.style.context(self.resolved_plot_style):
            return  {
            "background": CTkAppView.theme_color("CTkTextbox", "fg_color"),
            "text": CTkAppView.theme_color("CTkLabel", "text_color"),
            "grid": CTkAppView.theme_color("CTkFrame", "border_color"),
            "border": CTkAppView.theme_color("CTkFrame", "border_color"),
            "accent": CTkAppView.theme_color("CTkButton", "fg_color"),
        }

    def _create_figure(self) -> None:
        """Create the Matplotlib figure and axes once."""

        with plt.style.context(self.resolved_plot_style):
            self.figure = Figure(
                figsize=(10, 6),
                dpi=100,
                constrained_layout=True,
            )
            self.axes = self.figure.add_subplot(111)
            
            c = self.colors()

            self.figure.patch.set_facecolor(c["background"])
            self.axes.set_facecolor(c["background"])
            self.axes.tick_params(colors=c["text"])
            self.axes.xaxis.label.set_color(c["text"])
            self.axes.yaxis.label.set_color(c["text"])
            self.axes.title.set_color(c["text"])

            for spine in self.axes.spines.values():
                spine.set_color(c["border"])

            self.axes.grid(color=c["grid"], alpha=0.4)

    def _create_canvas(self) -> None:
        """Embed the Matplotlib figure in the CTkFrame."""

        self._mpl_canvas = FigureCanvasTkAgg(
            self.figure,
            master=self,
        )

        self.canvas_widget = cast(tk.Canvas, self._mpl_canvas.get_tk_widget())
        c = self.colors()
        self.canvas_widget.configure(
            background=c["background"],
            highlightthickness=0,
        )
        self.canvas_widget.pack(
            fill=tk.BOTH,
            expand=True,
            #padx=10,
            #pady=10,
        )

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def draw(self) -> None:
        """Clear the axes and redraw the selected graph."""

        self.app_mode = ctk.get_appearance_mode()
        self.resolved_plot_style = self._resolve_plot_style(
            self.plot_style
        )

        with plt.style.context(self.resolved_plot_style):
            self.axes.clear()
            self._apply_figure_theme()

            if self.dataframe.empty:
                self._draw_message("No data available")
            elif not self._required_columns_exist():
                self._draw_missing_column_message()
            else:
                self._draw_graph()
                self._configure_axes()

        self._mpl_canvas.draw_idle()

    def set_dataframe(
        self,
        dataframe: pd.DataFrame,
        *,
        redraw: bool = True,
    ) -> None:
        """Replace the graph's DataFrame."""

        self.dataframe = dataframe.copy()

        if redraw:
            self.draw()

    def configure_graph(
        self,
        *,
        graph_type: GraphType | None = None,
        category: str | None = None,
        metric: str | None = None,
        hue: str | None = None,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        plot_style: str | None = None,
        redraw: bool = True,
    ) -> None:
        """
        Change graph settings without recreating the CTkGraph widget.

        Pass hue="" to remove the current hue selection.
        """

        if graph_type is not None:
            self.graph_type = graph_type

        if category is not None:
            self.category = category

        if metric is not None:
            self.metric = metric

        if hue is not None:
            self.hue = hue or None

        if title is not None:
            self.title = title

        if xlabel is not None:
            self.xlabel = xlabel

        if ylabel is not None:
            self.ylabel = ylabel

        if plot_style is not None:
            self.plot_style = plot_style

        if redraw:
            self.draw()

    def clear(self, message: str | None = None) -> None:
        """Clear the graph and optionally display a message."""

        with plt.style.context(self.resolved_plot_style):
            self.axes.clear()
            self._apply_figure_theme()

            if message:
                self._draw_message(message)

        self._mpl_canvas.draw_idle()

    # ------------------------------------------------------------------
    # Plotting
    # ------------------------------------------------------------------

    def _draw_graph(self) -> None:
        """Dispatch to the selected graph type."""
        if self.category == "LlamaBenchVersion":
            # self.dataframe["LlamaBenchVersion"] = self.dataframe["LlamaBenchVersion"].astype(int)
            self.dataframe["_sort_key"] = pd.to_numeric(self.dataframe["LlamaBenchVersion"], errors='coerce')
            self.dataframe = self.dataframe.sort_values("_sort_key", kind="stable").drop(columns="_sort_key")
        else:
            self.dataframe = self.dataframe.sort_values(by=self.category, ascending=True, kind="stable")

        def display_model_name(model_name: str) -> str:
            name = model_name.removesuffix(".gguf")
            if not self.show_quant:
                if "-" in name:
                    name = name.rsplit("-", 1)[0]
            return name
        
        self.plot_df = self.dataframe.copy()
        self.plot_df['ModelName'] = self.plot_df['ModelName'].apply(display_model_name)
        match self.graph_type:
            case "Horizontal Bar":
                self._draw_horizontal_barplot()

            case "Vertical Bar":
                self._draw_vertical_barplot()

            case "Line":
                self._draw_lineplot()

            case "Scatter":
                self._draw_scatterplot()

            case _:
                raise ValueError(
                    f"Unsupported graph type: {self.graph_type}"
                )

    def _add_horizontal_bar_labels(self) -> None:
        xmin, xmax = self.axes.get_xlim()
        axis_span = xmax - xmin

        for container in self.axes.containers:
            for bar in container:
                value = bar.get_width()
                y = bar.get_y() + bar.get_height() / 2

                # Long enough to hold the text comfortably
                if value >= axis_span * 0.08:
                    x = bar.get_x() + value / 2
                    ha = "center"
                    color = "black"
                else:
                    # Tiny bar: place label just to the right
                    x = bar.get_x() + value + axis_span * 0.01
                    ha = "left"
                    color = self.axes.xaxis.label.get_color()

                self.axes.text(
                    x,
                    y,
                    f"{value:.1f}",
                    ha=ha,
                    va="center",
                    fontsize=10,
                    color=color,
                )

    def _add_bar_labels(self) -> None:
        if not self.show_values:
            return

        for container in self.axes.containers:
            self.axes.bar_label(
                container,
                fmt="%.1f",
                label_type="center",
                # padding=-4,
                fontsize=12,
            )

    def _draw_horizontal_barplot(self) -> None:
        sns.barplot(
            data=self.plot_df,
            y=self.category,
            x=self.metric,
            hue=self.hue,
            estimator=self.estimator,
            errorbar=None,
            ax=self.axes,
        )
        self._add_horizontal_bar_labels()

    def _draw_vertical_barplot(self) -> None:
        sns.barplot(
            data=self.plot_df,
            x=self.category,
            y=self.metric,
            hue=self.hue,
            estimator=self.estimator,
            errorbar=None,
            ax=self.axes,
        )
        self._add_horizontal_bar_labels()

    def _draw_lineplot(self) -> None:
        sns.lineplot(
            data=self.plot_df,
            x=self.category,
            y=self.metric,
            hue=self.hue,
            estimator=self.estimator,
            errorbar=None,
            marker="o",
            ax=self.axes,
        )

    def _draw_scatterplot(self) -> None:
        sns.scatterplot(
            data=self.plot_df,
            x=self.category,
            y=self.metric,
            hue=self.hue,
            ax=self.axes,
        )

    # ------------------------------------------------------------------
    # Formatting
    # ------------------------------------------------------------------

    def _configure_axes(self) -> None:
        """Apply titles, labels, fonts, tick rotation, and legend."""

        title_family, title_size = self._get_font_properties(
            self.title_font
        )
        label_family, label_size = self._get_font_properties(
            self.xylabel_font
        )
        tick_family, tick_size = self._get_font_properties(
            self.xytick_font
        )

        self.axes.set_title(
            self.title,
            fontfamily=title_family,
            fontsize=title_size,
        )

        self.axes.set_xlabel(
            self.xlabel,
            fontfamily=label_family,
            fontsize=label_size,
        )

        self.axes.set_ylabel(
            self.ylabel,
            fontfamily=label_family,
            fontsize=label_size,
        )

        for label in self.axes.get_xticklabels():
            label.set_fontfamily(tick_family)
            label.set_fontsize(tick_size)

        for label in self.axes.get_yticklabels():
            label.set_fontfamily(tick_family)
            label.set_fontsize(tick_size)

        # Horizontal graph category labels should normally remain horizontal.
        # Vertical graphs often need rotated category labels.
        if self.graph_type != "Horizontal Bar":
            for label in self.axes.get_xticklabels():
                label.set_rotation(self.rotate_x_labels)
                label.set_horizontalalignment("right")

        self.axes.tick_params(
            axis="both",
            labelsize=tick_size,
        )

        legend = self.axes.get_legend()

        if legend is not None:
            if self.hue is None or not self.show_legend:
                legend.remove()
            else:
                legend_frame = legend.get_frame()
                legend_frame.set_facecolor(CTkAppView.theme_color("CTkTextbox", "fg_color"))
                legend_frame.set_edgecolor(CTkAppView.theme_color("CTkTextbox", "border_color"))
                text_color = CTkAppView.theme_color("CTkLabel", "text_color")
                legend.set_title(self.hue)

                for text in legend.get_texts():
                    text.set_color(text_color)
                    text.set_fontfamily(tick_family)
                    text.set_fontsize(tick_size)

                legend_title = legend.get_title()
                legend_title.set_fontfamily(label_family)
                legend_title.set_fontsize(label_size)

    def _apply_figure_theme(self) -> None:
        """
        Reapply style-dependent colors after axes.clear().

        Axes.clear() reads the current rcParams, so this method is called
        while the appropriate style context is active.
        """

        c = self.colors()

        self.figure.set_facecolor(c["background"])
        self.axes.set_facecolor(c["background"])

        try:
            self.canvas_widget.configure(
                background=c["background"],
                highlightthickness=0,
            )
        except tk.TclError:
            # Some Matplotlib color specifications may not be accepted
            # directly by Tk. This does not prevent the plot from drawing.
            pass

    # ------------------------------------------------------------------
    # Validation and messages
    # ------------------------------------------------------------------

    def _required_columns_exist(self) -> bool:
        required_columns = {
            self.category,
            self.metric,
        }

        if self.hue:
            required_columns.add(self.hue)

        return required_columns.issubset(
            self.dataframe.columns
        )

    def _draw_missing_column_message(self) -> None:
        required_columns = {
            self.category,
            self.metric,
        }

        if self.hue:
            required_columns.add(self.hue)

        missing_columns = sorted(
            required_columns.difference(
                self.dataframe.columns
            )
        )

        message = (
            "Missing DataFrame column"
            if len(missing_columns) == 1
            else "Missing DataFrame columns"
        )

        self._draw_message(
            f"{message}:\n{', '.join(missing_columns)}"
        )

    def _draw_message(self, message: str) -> None:
        """Display a centered message within the graph area."""

        family, size = self._get_font_properties(self.font)

        self.axes.set_axis_off()
        self.axes.text(
            0.5,
            0.5,
            message,
            ha="center",
            va="center",
            transform=self.axes.transAxes,
            fontfamily=family,
            fontsize=size,
        )

    # ------------------------------------------------------------------
    # Utility methods
    # ------------------------------------------------------------------

    def _resolve_plot_style(
        self,
        requested_style: str,
    ) -> str:
        """Resolve auto, named, and fallback Matplotlib styles."""

        if requested_style.casefold() == "auto":
            mode = self.app_mode.casefold()

            return (
                self.DEFAULT_PLOT_THEMES["dark"]
                if mode == "dark"
                else self.DEFAULT_PLOT_THEMES["light"]
            )

        if requested_style == "default":
            return "default"

        if requested_style in plt.style.available:
            return requested_style

        return "classic"

    @staticmethod
    def _get_font_properties(
        font: ctk.CTkFont,
    ) -> tuple[str, int]:
        family = str(font.cget("family"))
        size = abs(int(font.cget("size")))

        return family, size

    def destroy(self) -> None:
        """
        Release the Matplotlib figure before destroying the Tk widget.
        """

        plt.close(self.figure)
        super().destroy()

class CTkAnalysisView(CTkAppView):

    def __init__(self, parent: ctk.CTk, frame: ctk.CTkFrame, font: FontSpec, data: CTkAppData) -> None:
        super().__init__(parent, frame, font, data)
        self.dpi = parent.winfo_fpixels('1i')  # Get the DPI of the screen
        self.data.logger.debug(f"****> Screen DPI <*****: {self.dpi}")

        use_sqlsvr = self.data.use_sqlsvr
        if use_sqlsvr:
            sqlite_filename = None
            self.server: str | None = os.environ.get('SQL_SERVER', "127.0.0.1")
            self.port: int | None = int(os.environ.get('SQL_PORT', 1433))
            self._database: str | None = "LocalMind"
            self.user: str | None  = os.environ.get('SQL_SVR_USER', "crash")
            self.password: str | None = os.environ.get('SQL_SVR_PASSWORD', "")
            self.driver: str | None = os.environ.get('SQL_SVR_DRIVER', "ODBC Driver 18 for SQL Server")
        else:
            sqlite_filename = "LocalMind.db"
            self.server = None
            self.port = None
            self._database = self.data.database_path if self.data.database_path else None
            self.user = None
            self.password = None
            self.driver = None
        self.initialize_widgets()
        self._settings: LocalMindSettings = LocalMindSettings(app_name=self.data._app_name if self.data._app_name is not None else "LocalMind", logger=self.data.logger)
        self._filters: dict[str, list[str] | tuple[str, str]] = {}
        self._df: pd.DataFrame | None = None
        self.graph: CTkGraph | None = None
        self.group_by_column: str | None = None
        self.filter_str: str | None = None

    def format_filters(
        self, filters: dict[str, list[str] | tuple[str, str]], group_by: str | None = None
    ) -> str:
        lines: list[str] = []

        for name, value in filters.items():
            lines.append(name)

            if isinstance(value, tuple):
                lines.append(f"    {value[0]} → {value[1]}")
            else:
                for item in value:
                    lines.append(f"    • {item}")

            lines.append("")
        if group_by is not None:
            lines.append(f"Group By")
            lines.append(f"    • {group_by}")
            lines.append("")

        return "\n".join(lines)

    def get_group_by_column(self, group_by_name: str) -> str | None:
        group_by_column: str | None = None
        match group_by_name:
            case "Backend":
                group_by_column = "Backend"
            case "Test Type":
                group_by_column = "TestType"
            case "Host":
                group_by_column = "HostName"
            case "GPU":
                group_by_column = "GpuInfo"
            case "Model":
                group_by_column = "ModelName"
            case "LlamaBench Version":
                group_by_column = "LlamaBenchVersion"
            case _:
                group_by_column = None
        return group_by_column

    def get_group_by_name(self, group_by_column: str | None) -> str | None:
        group_by_name: str | None = None
        match group_by_column:
            case "Backend":
                group_by_name = "Backend"
            case "TestType":
                group_by_name = "Test Type"
            case "HostName":
                group_by_name = "Host"
            case "GpuInfo":
                group_by_name = "GPU"
            case "ModelName":
                group_by_name = "Model"
            case "LlamaBenchVersion":
                group_by_name = "LlamaBench Version"
            case _:
                group_by_name = None
        return group_by_name

    def get_category_column(self, category_name: str) -> str | None:
        category_column: str | None = None
        match category_name:
            case "Backend":
                category_column = "Backend"
            case "Test Type":
                category_column = "TestType"
            case "Host":
                category_column = "HostName"
            case "GPU":
                category_column = "GpuInfo"
            case "Model":
                category_column = "ModelName"
            case "LlamaBench Version":
                category_column = "LlamaBenchVersion"
            case _:
                category_column = None
        return category_column

    def get_metric_column(self, metric_name: str) -> str | None:
        metric_column: str | None = None
        match metric_name:
            case "Average Tokens per Second":
                metric_column = "AvgTokensPerSecond"
            case "Model Size (Bytes)":
                metric_column = "ModelSizeBytes"
            case "Model Parameter Count":
                metric_column = "ModelParameterCount"
            case _:
                metric_column = None
        return metric_column

    def apply_analysis_filters(
        self,
        df: pd.DataFrame,
        filters: dict[str, list[Any] | tuple[str, str]],
    ) -> pd.DataFrame:
    
        filtered_df = df.copy()

        column_map = {
            "Model": "ModelName",
            "Backend": "Backend",
            "GPU": "GpuInfo",
            "Host": "HostName",
            "Test Type": "TestType",
            "LlamaBench Version": "LlamaBenchVersion",
        }

        self.data.logger.debug(f"Current DataFrame before filtering: {filtered_df.head()}")

        for filter_name, selected_values in filters.items():
            if not selected_values:
                continue

            self.data.logger.debug(f"Applying filter: {filter_name} with values: {selected_values}")

            if filter_name == "Time Range":
                if len(selected_values) != 2:
                    raise ValueError(
                        "Time Range must contain a begin date and an end date."
                    )

                begin_date = pd.to_datetime(selected_values[0])
                end_date = pd.to_datetime(selected_values[1])

                run_dates = pd.to_datetime(
                    filtered_df["RunStartedAt"],
                    errors="coerce",
                )

                filtered_df = filtered_df.loc[
                    run_dates.between(begin_date, end_date, inclusive="both")
                ]

                continue

            column_name = column_map.get(filter_name)

            if column_name is None:
                raise ValueError(f"Unknown filter type: {filter_name!r}")

            if column_name not in filtered_df.columns:
                raise KeyError(
                    f"Dataframe does not contain column {column_name!r}"
                )

            filtered_df = filtered_df.loc[
                filtered_df[column_name].isin(selected_values)
            ]
        self.data.logger.debug(f"Current DataFrame after filtering: {filtered_df.head()}")

        return filtered_df    


    def get_connection_string(self, database: Optional[str] = None) -> str:
        db = database if database is not None else self._database
        if db is not None:
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
        else:
            conn_str = ""
        return conn_str
    
    def get_models(self) -> list[str]:

        df = self.get_bench_data() if self._df is None else self._df
        self._df = df

        if df is None or df.empty:
            self.data.logger.warning("No benchmark data available to find GGUF models.")
            return []

        models: list[str] = []
        models = df['ModelName'].unique().tolist()
        return models

    def get_backends(self) -> list[str]:

        df = self.get_bench_data() if self._df is None else self._df
        self._df = df
        if df is None or df.empty:
            self.data.logger.warning("No benchmark data available to find backends.")
            return []

        backends: list[str] = []
        backends = df['Backend'].unique().tolist()
        return backends
    
    def get_gpus(self) -> list[str]:
        
        df = self.get_bench_data() if self._df is None else self._df
        self._df = df
        if df is None or df.empty:
            self.data.logger.warning("No benchmark data available to find GPUs.")
            return []

        gpus: list[str] = []
        gpus = df['GpuInfo'].unique().tolist()
        for i, gpu in enumerate(gpus):
            gpu_name = gpu.strip().split(",")[0] if gpu else "Unknown GPU"
            gpus[i] = gpu_name
        return gpus
    
    def get_hosts(self) -> list[str]:
        df = self.get_bench_data() if self._df is None else self._df
        self._df = df
        if df is None or df.empty:
            self.data.logger.warning("No benchmark data available to find hosts.")
            return []

        hosts: list[str] = []
        hosts = df['HostName'].unique().tolist()
        return hosts
    
    def get_raw_json(self) -> list[dict[str, Any]]:
        df = self.get_bench_data() if self._df is None else self._df
        self._df = df
        if df is None or df.empty:
            self.data.logger.warning("No benchmark data available to find raw JSON.")
            return []

        raw_json: list[str] = df['RawJson'].to_list()
    
        json_data: list[dict[str, Any]] = [json.loads(item) for item in raw_json] if raw_json else []

        return json_data
    
    def get_llama_bench_versions(self) -> list[str]:
        df = self.get_bench_data() if self._df is None else self._df
        self._df = df
        if df is None or df.empty:
            self.data.logger.warning("No benchmark data available to find LlamaBench versions.")
            return []

        versions: list[str] = []
        versions = df['LlamaBenchVersion'].unique().tolist()
        versions = [v.split('-')[0] for v in versions if v]  # Filter out empty versions
        # version SELECT shouod be 'version LIKE <version_string>%' to match any version starting with the given string
        versions = sorted(set(versions))  # Remove duplicates and sort
        return versions
    
    def get_llama_test_types(self) -> list[str]:
        df = self.get_bench_data() if self._df is None else self._df
        self._df = df
        if df is None or df.empty:
            self.data.logger.warning("No benchmark data available to find LlamaBench test types.")
            return []

        test_types: list[str] = []
        test_types = df['TestType'].unique().tolist()
        return test_types
    
    def get_bench_data(self) -> pd.DataFrame | None:


        if not self.data.use_sqlsvr:
            db: SqliteExt | pyOdbcExt = SqliteExt(self.data.database_path, logger=self.data.logger)
            table_id_models: str = "Models"
            table_id_runs: str = "BenchmarkRuns"
            table_id_results: str = "BenchmarkResults"
        else:
            db = pyOdbcExt(self.get_connection_string(), logger=self.data.logger)
            table_id_models = "dbo.Models"
            table_id_runs = "dbo.BenchmarkRuns"
            table_id_results = "dbo.BenchmarkResults"

        sql = f"""
        SELECT
            br.RunStartedAt, 
            br.RunFinishedAt, 
            br.LlamaBenchVersion,
            br.Backend,
            br.HostName,
            br.GpuInfo,
            m.ModelName,
            m.ModelSizeBytes,
            m.ModelParameterCount,
            res.TestType,
            res.NPrompt,
            res.NGen,
            res.AvgTokensPerSecond,
            res.RawJson
        FROM {table_id_runs} br
        INNER JOIN {table_id_models} m 
            ON br.ModelId = m.ModelId
        INNER JOIN {table_id_results} res
            ON br.BenchmarkRunId = res.BenchmarkRunId;
        """
        

        # db = pyOdbcExt(conn_string=self.get_connection_string())
        df = db.query_to_dataframe(sql)
        if df is not None:
           self.data.logger.debug(f"Retrieved {len(df)} rows of benchmark data from the database.")
           self.data.logger.debug(f"Benchmark data columns: {df.columns.tolist()}")
           df['LlamaBenchVersion'] = df['LlamaBenchVersion'].apply(lambda x: x.split('-')[0] if isinstance(x, str) else x)
        return df

    def sb_button_list(self) -> List[str]:
        """ Enable the sidebar button functions for this view return default list here 
            Override in your derived classes
        """

        return ['first', 'edit', 'new', 'export' ]  # first=start, last=stop, edit=edit the settings for the current filter, new=clear the graph

    def on_visible(self) -> None:
        """ Called when the view becomes visible. Override in derived classes for custom behavior. """

        self.data.logger.debug(f"{self.__class__}.on_visible() called")
        self.set_button_names(
            {
                "first": "Show Graph",
                "edit": "Filters",
                "new": "Clear Graph",
                "export": "Export"
            }
        )
        button = self.data.get_button("first")
        if button:
            button.configure(state='normal')

        button = self.data.get_button("edit")
        if button: 
            button.configure(state='normal')

        button = self.data.get_button("new")
        if button:
            button.configure(state='normal')

        button = self.data.get_button("export")
        if button:
            button.configure(state='normal')
        

    
    def on_sidebar_edit(self) -> None:
        models: list[str] = self.get_models()
        self.data.logger.debug(f"Found GGUF models: {models}")
        json_data: list[dict[str, Any]] = self.get_raw_json()
        self.data.logger.debug(f"Found {len(json_data)} raw JSON entries.")
        self.data.logger.debug(f"The first raw JSON entry: {json.dumps(json_data[0], indent=2)}") if json_data else self.data.logger.debug("No raw JSON entries found.")

        dlg = EditFiltersDialog(self.parent,
                                title="Edit Filters", 
                                message="Select a Filter Type", 
                                font=self.font,
                                hosts=self.get_hosts(),
                                gpus=self.get_gpus(),
                                models=self.get_models(),
                                backends=self.get_backends(),
                                llama_bench_versions=self.get_llama_bench_versions(),
                                llama_bench_test_types=self.get_llama_test_types(),
                                initial_filters=self._filters,
                                initial_group_by=self.get_group_by_name(self.group_by_column))
        if dlg.result:  
            self.data.logger.debug(f"User selected filter type: {dlg.result}")
            self._filters = dlg.result
            if dlg.group_by:
                self.group_by_column = self.get_group_by_column(dlg.group_by)
            else:
                self.group_by_column = None
            # self.update_filters(self.format_filters(self._filters, group_by=self.group_by_column))
            self.filter_str = self.format_filters(self._filters, group_by=self.group_by_column)

    def on_sidebar_new(self) -> None:
        if self.graph is not None:
            self.graph.destroy()
            self.graph = None

    
    def build_metric_interpretation(
        self,
        *,
        dataframe: pd.DataFrame,
        metric: str,
        category: str,
        group_by: str | None,
        filters: dict[str, list[str] | tuple[str, str]],
    ) -> str:

        def join_words(values: list[str]) -> str:
            if not values:
                return ""

            if len(values) == 1:
                return values[0]

            if len(values) == 2:
                return f"{values[0]} and {values[1]}"

            return f"{', '.join(values[:-1])}, and {values[-1]}"
        
        displayed = {category}
        if group_by:
            displayed.add(group_by)

        sentences = [
            (
                f"Each displayed value is the arithmetic mean of {metric} "
                "for all matching benchmark result rows."
            )
        ]

        test_type_column = "TestType"

        if (
            "Test Type" not in displayed
            and "Test Type" not in filters
            and test_type_column in dataframe.columns
        ):
            test_types = sorted(
                dataframe[test_type_column]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            if len(test_types) > 1:
                sentences.append(
                    "Because Test Type is neither filtered nor displayed, "
                    f"{join_words(test_types)} results are included "
                    "in the same average."
                )

        return " ".join(sentences)
    
    def build_scope_table_data(
        self,
        *,
        dataframe: pd.DataFrame,
        category: str,
        metric: str,
        group_by: str | None,
        filters: dict[str, list[str] | tuple[str, str]],
        body_style: ParagraphStyle,
    ) -> list[list[object]]:

        def display_model_name(model_name: str) -> str:
            name = model_name.removesuffix(".gguf")
            if "-" in name:
                name = name.rsplit("-", 1)[0]
            return name
        
        rows: list[list[object]] = [
            ["Property", "Selection", "Interpretation"],
            [
                "Metric",
                metric,
                Paragraph(
                    self.build_metric_interpretation(
                        dataframe=dataframe,
                        metric=metric,
                        category=category,
                        group_by=group_by,
                        filters=filters,
                    ),
                    body_style,
                ),
            ],
            [
                "Category",
                category,
                Paragraph(
                    f"Each axis category represents a distinct {category} value.",
                    body_style,
                ),
            ],
            [
                "Group By",
                group_by or "None",
                Paragraph(
                    (
                        f"Results within each {category} are separated by "
                        f"{group_by}."
                        if group_by
                        else (
                            f"Results are not subdivided within each {category}; "
                            "all remaining dimensions may contribute to the aggregate."
                        )
                    ),
                    body_style,
                ),
            ],
        ]

        for dimension in CategoryType:
            selected = filters.get(dimension.value)
            if isinstance(selected, list) and dimension.value == "Model":
                selected = [display_model_name(model) for model in selected]
            if selected:
                # selection_text = self.format_filters(self._filters, group_by=self.group_by_column) # self.format_filter_value(selected)
                selection_text = "<br/>".join(list(selected))
                interpretation = (
                    f"Only the selected {dimension.value.lower()} values are included."
                )
            elif dimension == category:
                selection_text = "Category"
                interpretation = (
                    f"Values are displayed separately because {dimension.value} "
                    "is the graph category."
                )
            elif dimension == group_by:
                selection_text = "Grouped"
                interpretation = (
                    f"Values are displayed separately because {dimension.value} "
                    "is the grouping dimension."
                )
            else:
                selection_text = "All"
                interpretation = (
                    f"All {dimension.value.lower()} values are included and may be "
                    "combined within each displayed aggregate."
                )

            rows.append(
                [
                    dimension.value,
                    Paragraph(selection_text, body_style),
                    Paragraph(interpretation, body_style),
                ]
            )

        return rows


    def export_analysis_pdf(
        self,
        dataframe: pd.DataFrame,
        output_path: Path,
        graph_path: Path,
        *,
        graph_type: str,
        category: str,
        metric: str,
        group_by: str | None,
        filters: dict[str, list[str] | tuple[str, str]],
        comments: str = "",
    ) -> None:
        if not graph_path.is_file():
            CTkDialog(self.parent, 
                      title="Graph image not found", 
                      message=f"The graph image file '{graph_path}' does not exist.\nPlease regenerate the graph before exporting the PDF report.", 
                      font=self.font)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        document = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=0.5 * inch,
            leftMargin=0.5 * inch,
            topMargin=0.5 * inch,
            bottomMargin=0.5 * inch,
            title="LocalMind Analysis Report",
            author="LocalMind",
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Title"],
            alignment=TA_CENTER,
            spaceAfter=12,
        )

        body_style = cast(ParagraphStyle, styles["BodyText"])
        body_style.leading = 14

        story: list[Any] = []

        story.append(
            Paragraph("LocalMind Analysis Report", title_style)
        )

        configuration_data = [
            ["Graph Type", graph_type],
            ["Category", category],
            ["Metric", metric],
            ["Group By", group_by or "None"],
        ]

        configuration_table = Table(
            configuration_data,
            colWidths=[1.25 * inch, 5.75 * inch],
            hAlign="LEFT",
        )

        configuration_table.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )

        story.append(configuration_table)
        story.append(Spacer(1, 12))

        graph = Image(str(graph_path))
        max_width = 7.0 * inch
        max_height = 4.75 * inch
        scale = min(max_width / graph.imageWidth, max_height / graph.imageHeight, 1.0)
        graph.drawWidth = graph.imageWidth * scale
        graph.drawHeight = graph.imageHeight * scale
        # graph._restrictSize(7.0 * inch, 4.75 * inch)
        story.append(graph)
        story.append(Spacer(1, 16))

        story.append(Paragraph("Analysis Scope", styles["Heading2"]))

        scope_data = self.build_scope_table_data(
            dataframe=dataframe,
            category=category,
            metric=metric,
            group_by=group_by if group_by is not None else "",
            filters=filters,
            body_style=body_style,
        )


        scope_table = Table(
            scope_data,
            colWidths=[1.25 * inch, 1.75 * inch, 4.0 * inch],
            repeatRows=1,
            hAlign="LEFT",
        )

        scope_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )

        story.append(scope_table)

        if comments.strip():
            story.append(Spacer(1, 16))
            story.append(Paragraph("Comments", styles["Heading2"]))
            story.append(Paragraph(comments, body_style))

        document.build(story)

    def open_pdf(self, pdf_path: str | Path) -> None:
        path = Path(pdf_path).expanduser().resolve()

        if not path.is_file():
            raise FileNotFoundError(f"PDF report not found: {path}")

        if sys.platform == "win32":
            os.startfile(path)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.run(["open", str(path)], check=True)
        else:
            subprocess.run(["xdg-open", str(path)], check=True)

    def build_markdown_scope_table_data(
        self,
        *,
        dataframe: pd.DataFrame,
        category: str,
        metric: str,
        group_by: str | None,
        filters: dict[str, list[str] | tuple[str, str]],
    ) -> list[list[str]]:

        def display_model_name(model_name: str) -> str:
            name = model_name.removesuffix(".gguf")
            if "-" in name:
                name = name.rsplit("-", 1)[0]
            return name
        
        rows: list[list[str]] = [
            ["Property", "Selection", "Interpretation"],
            [
                "Metric",
                metric,
                self.build_metric_interpretation(
                    dataframe=dataframe,
                    metric=metric,
                    category=category,
                    group_by=group_by,
                    filters=filters,
                )
            ],
            [
                "Category",
                category,
                f"Each axis category represents a distinct {category} value.",
            ],
            [
                "Group By",
                group_by or "None",
                (
                    f"Results within each {category} are separated by "
                    f"{group_by}."
                    if group_by
                    else (
                        f"Results are not subdivided within each {category}; "
                        "all remaining dimensions may contribute to the aggregate."
                    )
                ),
            ],
        ]

        for dimension in CategoryType:
            selected = filters.get(dimension.value)
            if isinstance(selected, list) and dimension.value == "Model":
                selected = [display_model_name(model) for model in selected]
            if selected:
                # selection_text = self.format_filters(self._filters, group_by=self.group_by_column) # self.format_filter_value(selected)
                selection_text = "<br>".join(list(selected))
                interpretation = (
                    f"Only the selected {dimension.value.lower()} values are included."
                )
            elif dimension == category:
                selection_text = "Category"
                interpretation = (
                    f"Values are displayed separately because {dimension.value} "
                    "is the graph category."
                )
            elif dimension == group_by:
                selection_text = "Grouped"
                interpretation = (
                    f"Values are displayed separately because {dimension.value} "
                    "is the grouping dimension."
                )
            else:
                selection_text = "All"
                interpretation = (
                    f"All {dimension.value.lower()} values are included and may be "
                    "combined within each displayed aggregate."
                )

            rows.append(
                [
                    dimension.value,
                    selection_text,
                    interpretation,
                ]
            )

        return rows

    def export_analysis_markdown(
        self,
        dataframe: pd.DataFrame,
        output_path: Path,
        graph_path: Path,
        *,
        graph_type: str,
        category: str,
        metric: str,
        group_by: str | None,
        filters: dict[str, list[str] | tuple[str, str]],
        comments: str = "",
    ) -> None:
        if not graph_path.is_file():
            CTkDialog(self.parent, 
                      title="Graph image not found", 
                      message=f"The graph image file '{graph_path}' does not exist.\nPlease regenerate the graph before exporting the PDF report.", 
                      font=self.font)
            return
        new_graph_path = output_path.with_suffix(".png")
        if new_graph_path.exists():
            new_graph_path.unlink()  # Remove the existing file if it exists
        Path.rename(graph_path, new_graph_path)
        try:
            shutil.copy(new_graph_path, output_path.parent / new_graph_path.name)
        except Exception as e:
            self.data.logger.error(f"Failed to copy graph image: {e}")

        rows: list[list[str]] = self.build_markdown_scope_table_data(dataframe=dataframe, category=category, metric=metric, group_by=group_by, filters=filters)
        markdown = f"""
# LocalMind Analysis Report
****
**Graph Type**: {graph_type} 
**Category**  : {category}
**Metric**    : {metric}
**Group By**  : {group_by or "None"}

****

![Performance Graph]({new_graph_path.name})

****

"""

        markdown += "| " + " | ".join(rows[0]) + " |\n"
        markdown += "| " + " | ".join([":---"] * len(rows[0])) + " |\n"
        for row in rows[1:]:
            markdown += "| " + " | ".join(str(cell) for cell in row) + " |\n"

        if comments.strip():
            markdown += "\n****\n"
            markdown += "## Comments\n"
            markdown += f"{comments}\n"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown)

        curdir = Path.cwd()
        os.chdir(output_path.parent)
        if isinstance(self.font, ctk.CTkFont):
           markdown_font = (self.font.cget('family'), self.font.cget('size'))
        else:
            markdown_font = (self.font[0], self.font[1])
        preview = CTkMarkdownView(self.parent, title="Markdown Report Preview", message="Markdown Report Preview", font=markdown_font, markdown=markdown)
        os.chdir(curdir)       

    def on_sidebar_export(self) -> None:
        users_home = Path.home() / ".LocalMind"
        performance_graph_path = users_home/ "performance_graph.png"
        select_report_type = CTkSelectReportType(self.parent, title="Select Report Type", message="Select a Report Type", font=self.font)
        if select_report_type.result:
            report_type = select_report_type.result
            filters_text = self.filter_str
            if report_type == 'pdf':
                report_path = users_home / "performance_report.pdf"
                report_path = Path(ctk.filedialog.asksaveasfilename(
                    initialdir=users_home,
                    initialfile="performance_report.pdf",
                    title="Save PDF Report",
                    filetypes=[("PDF files", "*.pdf")],
                ))

                self.data.logger.debug(f"Generating PDF report at: {report_path}")
                self.export_analysis_pdf(
                    dataframe=self._df if self._df is not None else pd.DataFrame(),
                    output_path=report_path,
                    graph_path=performance_graph_path,
                    graph_type=self.graph_type_var.get(),
                    category=self.category_var.get(),
                    metric=self.metric_var.get(),
                    group_by=self.get_group_by_name(self.group_by_column),
                    filters=self._filters                        
                )
                if select_report_type.open_pdf:
                    self.data.logger.debug(f"Opening PDF report: {report_path}")
                    self.open_pdf(report_path)
            elif report_type == 'markdown':
                report_path = users_home / "performance_report.md"
                report_path = Path(ctk.filedialog.asksaveasfilename(
                    initialdir=users_home,
                    initialfile="performance_report.md",
                    title="Save Markdown Report",
                    filetypes=[("Markdown files", "*.md")],
                ))

                self.data.logger.debug(f"Generating Markdown report at: {report_path}")

                self.export_analysis_markdown(
                    dataframe=self._df if self._df is not None else pd.DataFrame(),
                    output_path=report_path,
                    graph_path=performance_graph_path,
                    graph_type=self.graph_type_var.get(),
                    category=self.category_var.get(),
                    metric=self.metric_var.get(),
                    group_by=self.get_group_by_name(self.group_by_column),
                    filters=self._filters,
                    comments=""
                )   
        else:
            self.data.logger.debug("User cancelled report type selection.")

    def on_sidebar_first(self) -> None:
        """ we will render the graph when the user clicks the first button in the sidebar. Override in derived classes for custom behavior. """
        if self.graph is not None:
            self.graph.destroy()
            self.graph = None
        self._df = self.get_bench_data()        
        filtered_df = self.apply_analysis_filters(self._df, self._filters) if self._df is not None else None
        if filtered_df is not None and not filtered_df.empty:
            self.data.logger.debug(f"Filtered data contains {len(filtered_df)} rows after applying filters: {self._filters}")
            match self.graph_type_var.get():
                case ChartType.HORIZONTAL_BAR.value:
                    self.data.logger.debug("Rendering Horizontal Bar Chart")
                    self.graph = CTkGraph(self.graph_frame,
                                      title="Performance Analysis",
                                      xlabel=self.metric_var.get(),
                                      ylabel=self.category_var.get(),
                                      dataframe=filtered_df,
                                      category=self.get_category_column(self.category_var.get()),
                                      metric=self.get_metric_column(self.metric_var.get()),
                                      graph_type=ChartType.HORIZONTAL_BAR.value,
                                      hue=self.group_by_column)
                    self.graph.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                case ChartType.VERTICAL_BAR.value:
                    self.data.logger.debug("Rendering Vertical Bar Chart")
                    self.graph = CTkGraph(self.graph_frame,
                                      title="Performance Analysis",
                                      xlabel=self.category_var.get(),
                                      ylabel=self.metric_var.get(),
                                      dataframe=filtered_df,
                                      category=self.get_category_column(self.category_var.get()),
                                      metric=self.get_metric_column(self.metric_var.get()),
                                      graph_type=ChartType.VERTICAL_BAR.value,
                                      hue=self.group_by_column)
                    self.graph.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)    
                case ChartType.LINE.value:
                    self.data.logger.debug("Rendering Line Chart")
                    self.graph = CTkGraph(self.graph_frame,
                                      title="Performance Analysis",
                                      xlabel=self.category_var.get(),
                                      ylabel=self.metric_var.get(),
                                      dataframe=filtered_df,
                                      category=self.get_category_column(self.category_var.get()),
                                      metric=self.get_metric_column(self.metric_var.get()),
                                      graph_type=ChartType.LINE.value,
                                      hue=self.group_by_column)
                    self.graph.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                case ChartType.SCATTER.value:
                    self.data.logger.debug("Rendering Scatter Chart")
                    self.graph = CTkGraph(self.graph_frame,
                                      title="Performance Analysis",
                                      xlabel=self.category_var.get(),
                                      ylabel=self.metric_var.get(),
                                      dataframe=filtered_df,
                                      category=self.get_category_column(self.category_var.get()),
                                      metric=self.get_metric_column(self.metric_var.get()),
                                      graph_type=ChartType.SCATTER.value,
                                      hue=self.group_by_column)
                    self.graph.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            

    def on_sidebar_last(self) -> None:
        self.data.logger.debug(f"{self.__class__.__name__}: on_sidebar_last not implemented.")
    
    def on_close_tab(self) -> None:
        """ Called when the tab is closed. Override in derived classes for custom behavior. """
        self.data.logger.debug(f"{self.__class__}.on_tab_closed() called")

    def initialize_widgets(self) -> None:
        self.frame.grid_columnconfigure(0, weight=1)
        self.control_frame = self.labeled_frame(self.frame, "Controls", 0, 0, 3, 1, [1,1,1])
        self.graph_frame = self.labeled_frame(self.frame, "Graph", 1, 0, 1, 1, [1], make_scrollable=False)

        self.graph_type_frame = self.labeled_frame(self.control_frame, "Graph Type", 0, 0, 1, 1, [1])
        self.graph_type_var = ctk.StringVar(value=ChartType.HORIZONTAL_BAR.value)
        self.graph_type_var.trace_add("write", self.graph_type_changed)

        self.graph_type_opt_list = ctk.CTkOptionMenu(self.graph_type_frame, 
                                                     dropdown_font=self.font, 
                                                     variable=self.graph_type_var, 
                                                     values=[ChartType.HORIZONTAL_BAR.value, 
                                                             ChartType.VERTICAL_BAR.value, 
                                                             ChartType.LINE.value, 
                                                             ChartType.SCATTER.value], 
                                                     font=self.font)
        self.graph_type_opt_list.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        
        self.category_frame = self.labeled_frame(self.control_frame, "Category", 0, 1, 1, 1, [1])
        self.category_var = ctk.StringVar(value=CategoryType.MODEL.value)
        self.category_var.trace_add("write", self.category_changed)
        self.category_opt_list = ctk.CTkOptionMenu(self.category_frame, 
                                                   dropdown_font=self.font, 
                                                   variable=self.category_var, 
                                                   values=[CategoryType.MODEL.value, 
                                                           CategoryType.BACKEND.value, 
                                                           CategoryType.GPU.value, 
                                                           CategoryType.HOST.value,
                                                           CategoryType.TEST_TYPE.value,
                                                           CategoryType.LLAMA_BENCH_VERSION.value], 
                                                   font=self.font)
        self.category_opt_list.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # self.filters_frame = self.labeled_frame(self.control_frame, "Filters", 1, 0, 1, 1, [])

        # self.filter_text = ctk.CTkTextbox(self.filters_frame, font=self.font, width=400, height=200)
        # self.filter_text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        # self.filter_text.configure(state="disabled")


        self.metric_frame = self.labeled_frame(self.control_frame, "Metric", 0, 2, 1, 1, [1])
        self.metric_var = ctk.StringVar(value=MetricType.AVG_TOKENS_PER_SECOND.value)
        self.metric_var.trace_add("write", self.metric_changed)
        self.metric_opt_list = ctk.CTkOptionMenu(self.metric_frame, 
                                                 dropdown_font=self.font, 
                                                 variable=self.metric_var, 
                                                 values=[MetricType.AVG_TOKENS_PER_SECOND.value, 
                                                         MetricType.MODEL_SIZE_BYTES.value, 
                                                         MetricType.MODEL_PARAMETER_COUNT.value], 
                                                 font=self.font)
        self.metric_opt_list.grid(row=0, column=0, padx=5, pady=5, sticky="new")


    def graph_type_changed(self, *args) -> None:
        """ Called when the graph type is changed. Override in derived classes for custom behavior. """
        chart_type: ChartType  = ChartType(self.graph_type_var.get())
        match chart_type:
            case ChartType.HORIZONTAL_BAR:
                self.data.logger.debug("Graph type changed to Horizontal Bar")
            case ChartType.VERTICAL_BAR:
                self.data.logger.debug("Graph type changed to Vertical Bar")
            case ChartType.LINE:
                self.data.logger.debug("Graph type changed to Line")
            case ChartType.SCATTER:
                self.data.logger.debug("Graph type changed to Scatter")

    def metric_changed(self, *args) -> None:
        """ Called when the metric is changed. Override in derived classes for custom behavior. """
        metric_type: MetricType = MetricType(self.metric_var.get())
        match metric_type:
            case MetricType.AVG_TOKENS_PER_SECOND:
                self.data.logger.debug("Metric changed to Avg Tokens Per Second")
            case MetricType.MODEL_SIZE_BYTES:
                self.data.logger.debug("Metric changed to Model Size Bytes")
            case MetricType.MODEL_PARAMETER_COUNT:
                self.data.logger.debug("Metric changed to Model Parameter Count")

    def category_changed(self, *args) -> None:
        """ Called when the category is changed. Override in derived classes for custom behavior. """
        category_type: CategoryType = CategoryType(self.category_var.get())
        match category_type:
            case CategoryType.MODEL:
                self.data.logger.debug("Category changed to Model")
            case CategoryType.BACKEND:
                self.data.logger.debug("Category changed to Backend")
            case CategoryType.GPU:
                self.data.logger.debug("Category changed to GPU")
            case CategoryType.HOST:
                self.data.logger.debug("Category changed to Host")
