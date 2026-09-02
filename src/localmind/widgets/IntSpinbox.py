# IntSpinbox.py
import customtkinter # type: ignore
from typing import Union, Callable, Optional

class IntSpinbox(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: int = 1,
                 min: int = 0,
                 max: int = 99,
                 current: int = 0,
                 command: Optional[Callable] = None,
                 font: Optional[Union[tuple, customtkinter.CTkFont]]=None,
                 **kwargs) -> None:
        font = kwargs.pop('font', ('Ariel', 18, ))
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size: int = step_size
        self.min: int = min
        self.max: int = max
        self.command: Optional[Callable] = command

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = customtkinter.CTkButton(self, text="-", width=height-6, height=height-6,
                                                       command=self.subtract_button_callback, font=font)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = customtkinter.CTkEntry(self, width=width-(2*height), height=height-6, border_width=0, font=font)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = customtkinter.CTkButton(self, text="+", width=height-6, height=height-6,
                                                  command=self.add_button_callback, font=font)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
        self.entry.insert(0, str(self.min if current == 0 else current))

    def add_button_callback(self):
        try:
            value = int(self.entry.get()) + self.step_size
            if value <= self.max:
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
            if self.command is not None:
                self.command(value)
        except ValueError:
            return

    def subtract_button_callback(self) -> None:
        try:
            value = int(self.entry.get()) - self.step_size
            if value >= self.min:
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
            if self.command is not None:
                self.command(value)
        except ValueError:
            return

    def get(self) -> Union[int, None]:
        try:
            return int(self.entry.get())
        except ValueError:
            return None

    def set(self, value: int) -> None:
        if value in range(self.min, self.max+1):
            self.entry.delete(0, "end")
            self.entry.insert(0, str(int(value)))
