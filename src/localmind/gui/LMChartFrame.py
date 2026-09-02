
import customtkinter as ctk # type: ignore
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import seaborn as sns


class LMChartFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.figure = Figure(figsize=(10, 8), dpi=120)
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=1)

    def clear(self):
        self.axes.clear()

    def draw_barplot(self, df, x, y, hue=None):
        self.clear()

        sns.barplot(
            data=df,
            x=x,
            y=y,
            hue=hue,
            ax=self.axes,
        )

        self.figure.tight_layout()
        self.canvas.draw_idle()

    def draw_lineplot(self, df, x, y, hue=None):
        self.clear()

        sns.lineplot(
            data=df,
            x=x,
            y=y,
            hue=hue,
            ax=self.axes,
        )

        self.figure.tight_layout()
        self.canvas.draw_idle()

    def draw_scatter(self, df, x, y, hue=None):
        self.clear()

        sns.scatterplot(
            data=df,
            x=x,
            y=y,
            hue=hue,
            ax=self.axes,
        )

        self.figure.tight_layout()
        self.canvas.draw_idle()