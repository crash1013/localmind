
# CTkAppView.py

import customtkinter as ctk # type: ignore
import tkinter as tk
import tkinter.font as tkfont
from abc import ABC, abstractmethod


from localmind.gui.CTkAppData import CTkAppData
# from CTkApp import CTkApp

from typing import Union, List, Tuple, Optional

FontSpec = Union[
    ctk.CTkFont,  # type: ignore
    Tuple[str, int],
    Tuple[str, int, str],
    Tuple[str, int, str, str],
]

button_name_map = {
    "first": "First",
    "last": "Last",
    "next": "Next",
    "prior": "Prior",
    "new": "New",
    "edit": "Edit",
    "add": "Add",
    "update": "Update",
    "remove": "Remove",
    "search": "Search",
    "import": "Import",
    "export": "Export",
    "help": "Help"
}

class CTkAppView(ABC):
    """ Base class for all tab views in the CTkApp. Provides common functionality and structure for derived views. """
    def __init__(self, parent, frame: ctk.CTkFrame, font: FontSpec, data: CTkAppData) -> None:
        """ provides the base functionality for all tabs in the CTktabview """
        self._data = data
        self.parent = parent
        self.frame = frame
        self.font = font

    def get_tk_font(self, f: Optional[ctk.CTkFont] = None) -> tkfont.Font:
        """ Convert a CTkFont or font specification to a tkinter Font object. 
            If no font is provided, use the view's default font. 
            Only the family and size are used; other attributes are ignored."""
        if f is None:
            if isinstance(self.font, ctk.CTkFont):
                family=self.font.cget('family')
                size=self.font.cget('size')
            elif isinstance(self.font, tuple):
                family = self.font[0]
                size = self.font[1]
            else:
                self.data.logger.warning("Invalid font passed to CTkAppView using default Helvetica")
                family="Helvetica"
                size=14
        else:
            family=f.cget('family')
            size=f.cget('size')

        return tkfont.Font(family=family, size=size)

    def _set_button_names(self, name_map: dict[str, str]) -> None:
        """ Set the button name mapping for this view. """
        for key, value in name_map.items():
            if key in button_name_map:
                button: ctk.CTkButton | None = self._data.get_button(key)
                if button is not None:
                    button.configure(text=value)
            else:
                self._data.logger.warning(f"Invalid button name '{key}' passed to set_button_names. Ignored.")

    def set_button_names(self, names: dict[str, str]) -> None:
        """Set sidebar button labels for this view."""

        # Restore defaults
        for key, default_text in button_name_map.items():
            button = self.data.get_button(key)
            if button is not None:
                button.configure(text=default_text)

        # Apply view-specific overrides
        for key, text in names.items():
            if key not in button_name_map:
                self.data.logger.warning(
                    f"Invalid button name '{key}' passed to set_button_names. Ignored."
                )
                continue

            button = self.data.get_button(key)
            if button is not None:
                button.configure(text=text)

    @staticmethod
    def theme_color(widget: str, option: str) -> str:
        """ Return the color value for a given widget and option from the current theme. 
            Raises ValueError if the widget or option is not found. """
        if widget not in ctk.ThemeManager.theme:
            raise ValueError(f"Widget '{widget}' not found in theme.")
        if option not in ctk.ThemeManager.theme[widget]:
            raise ValueError(f"Option '{option}' not found for widget '{widget}' in theme.")
        value = ctk.ThemeManager.theme[widget][option]

        if isinstance(value, list):
            return value[0] if ctk.get_appearance_mode() == "Light" else value[1]

        return value
    
    def do_update(self) -> None:

        pass

    def sb_button_list(self) -> List[str]:
        """ Enable the sidebar button functions for this view return default list here 
            Override in your derived classes
        """

        return ['new', 'edit', 'add']
    
    def on_visible(self) -> None:
        """ Called when the view becomes visible. Override in derived classes for custom behavior. """

        self.data.logger.debug(f"{self.__class__}.on_visible() called")

    def on_close_tab(self) -> None:
        """ Called when the tab is closed. Override in derived classes for custom behavior. """
        self.data.logger.debug(f"{self.__class__}.on_tab_closed() called")

    
    @property
    def data(self) -> CTkAppData:
        """ Return the data object for this view """
        return self._data
    
    @data.setter  
    def data(self, value: CTkAppData) -> None:
        if not isinstance(value, CTkAppData):
            raise TypeError("Data type error, expecting CTkAppData")
        self._data = value
    
    @abstractmethod
    def initialize_widgets(self) -> None:
        """Initialize visual elements. Must be implemented by subclasses."""
        """ 
            Activate the on_sidebar_start function in the active view
        """
        pass

    def labeled_frame(
        self,
        parent: ctk.CTkBaseClass,
        label: str,
        parent_row: int,
        parent_column: int,
        columns: int,
        columnspan: int = 1,
        column_weight: List[int] = [],
        row0_weight: int = 1,
        make_scrollable: bool = False,
    ) -> ctk.CTkFrame:
        """
        Create a labeled CTk frame consisting of an outer frame (label + inner frame)
        and return the inner frame. The returned inner frame is configured so row 0
        and all specified columns can expand to fill available space.

        The outer frame is placed into `parent` at (parent_row, parent_column)
        with the given columnspan and sticky='nsew' so it can expand.
        """
        if len(column_weight) == 0:
            column_weight = [1] * columns

        # OUTER container
        if not make_scrollable:
            frame_outer = ctk.CTkFrame(parent)
        else:
            frame_outer = ctk.CTkScrollableFrame(parent)
            
        frame_outer.grid(row=parent_row, 
                         column=parent_column,
                         columnspan=columnspan, 
                         padx=10, 
                         pady=10, 
                         sticky="nsew")

        # Let the outer frame expand inside its parent cell
        # (the parent must also give this grid cell weight; see caller below)
        frame_outer.grid_columnconfigure(0, weight=1)
        frame_outer.grid_rowconfigure(0, weight=0)  # label row
        frame_outer.grid_rowconfigure(1, weight=1)  # inner frame row expands

        ctk_label = ctk.CTkLabel(frame_outer, text=label, font=self.font)
        ctk_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # INNER container (we return this)
        frame_inner = ctk.CTkFrame(frame_outer)
        frame_inner.grid(row=1, column=0, columnspan=columnspan, padx=5, pady=5, sticky="nsew")

        # Make inner frame's row 0 expand (where your widgets usually go)
        frame_inner.grid_rowconfigure(0, weight=row0_weight)

        # Make requested columns expand
        cl = len(column_weight)
        for c in range(columns):
            frame_inner.grid_columnconfigure(c, weight=column_weight[c])

        return frame_inner

    def on_sidebar_first(self) -> None:
        self.data.logger.debug(f"{self.__class__.__name__}: on_sidebar_first not implemented.")

    def on_sidebar_last(self) -> None:
        self.data.logger.debug(f"{self.__class__.__name__}: on_sidebar_last not implemented.")

    def on_sidebar_next(self) -> None:
        self.data.logger.debug(f"{self.__class__.__name__}: on_sidebar_next not implemented.")
    
    def on_sidebar_prior(self) -> None:
        self.data.logger.debug(f"{self.__class__.__name__}: on_sidebar_prior not implemented.")
    
    def on_sidebar_new(self) -> None:
        """Activate the on_sidebar_new function in the active view"""
        self.data.logger.debug(f"{self.__class__.__name__}: on_sidebar_new not implemented.")
        
    def on_sidebar_edit(self) -> None:
        self.data.logger.debug(f"{self.__class__.__name__}: on_sidebar_edit not implemented.")

    def on_sidebar_add(self) -> None:
        self.data.logger.debug(f"{self.__class__.__name__}: on_sidebar_add not implemented.")
    
    def on_sidebar_update(self) -> None:
        self.data.logger.debug(f"{self.__class__.__name__}: on_sidebar_update not implemented.")

    def on_sidebar_remove(self) -> None:
        self.data.logger.debug(f"{self.__class__.__name__}: on_sidebar_remove not implemented.")

    def on_sidebar_search(self) -> None:
        self.data.logger.debug(f"{self.__class__.__name__}: on_sidebar_search not implemented.")

    def on_sidebar_import(self) -> None:
        self.data.logger.debug(f"{self.__class__.__name__}: on_sidebar_import not implemented.")

    def on_sidebar_export(self) -> None:
        self.data.logger.debug(f"{self.__class__.__name__}: on_sidebar_export not implemented.")

    def on_sidebar_help(self) -> None:
        self.data.logger.debug(f"{self.__class__.__name__}: on_sidebar_help not implemented.")