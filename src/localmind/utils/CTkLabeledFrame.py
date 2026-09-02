import customtkinter as ctk # type: ignore

from typing import List
from localmind.gui.CTkAppView import FontSpec


def labeled_frame(
    parent: ctk.CTkScrollableFrame | ctk.CTkFrame | ctk.CTkToplevel,
    label: str,
    parent_row: int,
    parent_column: int,
    columns: int,
    columnspan: int = 1,
    column_weight: List[int] = [],
    row0_weight: int = 1,
    make_scrollable: bool = False,
    font: FontSpec | None = None,
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

    if font is None:
        font = ctk.CTkFont(size=18)
    ctk_label = ctk.CTkLabel(frame_outer, text=label, font=font)
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
