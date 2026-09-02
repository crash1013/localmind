from __future__ import annotations

import copy
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import tkinter.font as tkfont
from typing import Any

import customtkinter as ctk # type: ignore
from localmind.widgets.CTkGetText import CTkGetText
from localmind.widgets.CTkOpenChoice import CTkOpenChoice


class LlamaBenchSettingsDialog(ctk.CTkToplevel):
    """
    Dialog for editing llama-bench settings generated from HELP_SPEC.

    Expected input shape:

        HELP_SPEC = {
            "program": "llama-bench",
            "usage": "...",
            "sections": {
                "options": [
                    {
                        "aliases": ["-r", "--repetitions"],
                        "primary": "--repetitions",
                        "takes_value": True,
                        "value_hint": "<n>",
                        "choices": None,
                        "default": "5",
                        "description": "number of times..."
                    }
                ],
                "test_parameters": [...]
            },
            "notes": [...]
        }

    Return value:

        None if cancelled.

        Otherwise a dict of only non-default settings:

            {
                "--output": "json",
                "--n-gpu-layers": "999",
                "--flash-attn": "off"
            }

    For flags that do not take a value:

            {
                "--verbose": True,
                "--progress": True
            }
    """

    def __init__(
        self,
        parent,
        help_spec: dict[str, Any],
        font: ctk.CTkFont | tuple[str, int, str] | tuple[str, int] | tuple[str, int, str, str] 
        ,
        title: str | None = None,
        width: int = 1100,
        height: int = 650,
        current_options: dict[str, Any] | None = None
    ) -> None:
        super().__init__(parent)

        self.parent = parent
        self.help_spec = copy.deepcopy(help_spec)

        self.current_options: dict[str, Any] = copy.deepcopy(current_options or {})
        self.result: dict[str, Any] | None = None
        self.result_ready = False
        self.font = font

        self._item_to_entry: dict[str, dict[str, Any]] = {}

        program_name = self.help_spec.get("program", "llama-bench")
        self.title(title or f"{program_name} Settings")
        self.geometry(f"{width}x{height}")
        self.minsize(900, 500)

        self.transient(parent)

        self._initialize_values()
        self._build_widgets()
        self._populate_tree()

        self.center_on_parent(parent)

        self.protocol("WM_DELETE_WINDOW", self._on_cancel)
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    def center_on_parent(self, parent: ctk.CTk | ctk.CTkToplevel) -> None:
        self.update_idletasks()
        parent.update_idletasks()

        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        dialog_width = self.winfo_reqwidth()
        dialog_height = self.winfo_reqheight()

        position_x = round(
            parent_x + (parent_width - dialog_width) / 2
        )
        position_y = round(
            parent_y + (parent_height - dialog_height) / 2
        )

        # The :+d formatter produces +500 or -500 correctly.
        #s = f"{dialog_width}x{dialog_height}{position_x:+d}{position_y:+d}"
        s = f"{position_x:+d}{position_y:+d}"
        self.geometry(
            s
        )


    def _make_modal(self) -> None:
        try:
            self.update_idletasks()
            self.deiconify()
            self.lift()
            self.focus_force()
            self.grab_set()
            self.wait_window()
        except tk.TclError as exc:
            print(f"Could not make dialog modal: {exc}")

    # ------------------------------------------------------------------
    # Data setup
    # ------------------------------------------------------------------

    def _initialize_values_old(self) -> None:
        """
        Add a temporary 'value' field to each option.

        For takes_value=True:
            value starts as default.

        For takes_value=False:
            value starts as False, meaning the flag is not emitted.
        """

        sections = self.help_spec.get("sections", {})

        for entries in sections.values():
            for entry in entries:
                if entry.get("takes_value", False):
                    entry["value"] = entry.get("default")
                else:
                    entry["value"] = False

    def _initialize_values(self) -> None:
        for section_entries in self.help_spec.get("sections", {}).values():
            for entry in section_entries:
                primary = entry.get("primary")
                default = entry.get("default")

                if not primary:
                    continue

                if primary in self.current_options:
                    entry["value"] = self.current_options[primary]
                elif entry.get("takes_value"): # changed 2026-08-17
                    # entry["value"] = default if default is not None else ""
                    entry["value"] = default
                else:
                    entry["value"] = False

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------

    def get_tk_font(self, f: ctk.CTkFont | None = None) -> tkfont.Font:
        if f is None:
            if isinstance(self.font, ctk.CTkFont):
                family=self.font.cget('family')
                size=self.font.cget('size')
            elif isinstance(self.font, tuple):
                family = self.font[0]
                size = self.font[1]
            else:
                print("Invalid font passed to CTkAppView using default Helvetica")
                family="Helvetica"
                size=14
        else:
            family=f.cget('family')
            size=f.cget('size')

        listbox_font = tkfont.Font(family=family, size=size)
        return listbox_font

    def _build_widgets(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self)
        header.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 6))
        header.grid_columnconfigure(0, weight=1)

        usage = self.help_spec.get("usage", "")
        notes = self.help_spec.get("notes", [])

        title_text = self.help_spec.get("program", "llama-bench")

        if self.font is not None:
            self.title_label = ctk.CTkLabel(
                header,
                text=f"{title_text} command line settings",
                font=self.font # ctk.CTkFont(size=18, weight="bold"),
            )
        else:
            self.title_label = ctk.CTkLabel(
                header,
                text=f"{title_text} command line settings",
                font=ctk.CTkFont(size=18, weight="bold"),
            )
        self.title_label.grid(row=0, column=0, sticky="w", padx=10, pady=(8, 2))


        subtitle = usage
        if notes:
            subtitle += "    |    " + " ".join(notes)

        self.subtitle_label = ctk.CTkLabel(
            header,
            text=subtitle,
            anchor="w",
            justify="left",
            font=self.font if self.font is not None else ctk.CTkFont(size=12),
        )
        self.subtitle_label.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 8))

        body = ctk.CTkFrame(self)
        body.grid(row=1, column=0, sticky="nsew", padx=12, pady=6)
        body.grid_columnconfigure(0, weight=1)
        body.grid_rowconfigure(0, weight=1)

        style = ttk.Style()
        style.configure("Treeview", rowheight=26)

        if isinstance(self.font, ctk.CTkFont):
            f = self.get_tk_font(self.font)
        else:
            f = tkfont.Font(size=12)
        
        style.configure("Treeview", font=f)
        style.configure("Treeview.Heading", font=f)

        self.tree = ttk.Treeview(
            body,
            columns=("value", "default", "hint", "choices", "description"),
            show="tree headings",
            selectmode="browse",
        )

        self.tree.heading("#0", text="Option")
        self.tree.heading("value", text="Value")
        self.tree.heading("default", text="Default")
        self.tree.heading("hint", text="Hint")
        self.tree.heading("choices", text="Choices")
        self.tree.heading("description", text="Description")

        self.tree.column("#0", width=250, minwidth=180, anchor="w")
        self.tree.column("value", width=130, minwidth=90, anchor="w")
        self.tree.column("default", width=130, minwidth=90, anchor="w")
        self.tree.column("hint", width=150, minwidth=90, anchor="w")
        self.tree.column("choices", width=170, minwidth=100, anchor="w")
        self.tree.column("description", width=380, minwidth=180, anchor="w")

        yscroll = ttk.Scrollbar(body, orient="vertical", command=self.tree.yview)
        xscroll = ttk.Scrollbar(body, orient="horizontal", command=self.tree.xview)

        self.tree.configure(
            yscrollcommand=yscroll.set,
            xscrollcommand=xscroll.set,
        )

        self.tree.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")

        self.tree.bind("<Double-1>", self._on_double_click)
        self.tree.bind("<Return>", self._on_edit_selected)
        self.tree.bind("<space>", self._on_edit_selected)

        footer = ctk.CTkFrame(self)
        footer.grid(row=2, column=0, sticky="ew", padx=12, pady=(6, 12))
        footer.grid_columnconfigure(0, weight=1)

        self.changed_label = ctk.CTkLabel(footer, text="Changed settings: 0", font=self.font if self.font is not None else ctk.CTkFont(size=12) )
        self.changed_label.grid(row=0, column=0, sticky="w", padx=8, pady=8)

        self.reset_button = ctk.CTkButton(
            footer,
            text="Reset Selected",
            width=130,
            command=self._reset_selected,
            font=self.font if self.font is not None else ctk.CTkFont(size=12),
        )
        self.reset_button.grid(row=0, column=1, padx=6, pady=8)

        self.ok_button = ctk.CTkButton(
            footer,
            text="OK",
            width=100,
            command=self._on_ok,
            font=self.font if self.font is not None else ctk.CTkFont(size=12),
        )
        self.ok_button.grid(row=0, column=2, padx=6, pady=8)

        self.cancel_button = ctk.CTkButton(
            footer,
            text="Cancel",
            width=100,
            command=self._on_cancel,
            font=self.font if self.font is not None else ctk.CTkFont(size=12),
        )
        self.cancel_button.grid(row=0, column=3, padx=6, pady=8)

        self.tree.tag_configure("changed", background="#fff3cd")
        self.tree.tag_configure("flag", foreground="#0a58ca")

    def _update_changed_label(self) -> None:
        changed_settings: int = len(self.get_non_default_settings())
        message = f"Changed settings: {changed_settings}"
        self.changed_label.configure(text=message)
    # ------------------------------------------------------------------
    # Tree population
    # ------------------------------------------------------------------

    def _populate_tree(self) -> None:
        self.tree.delete(*self.tree.get_children())
        self._item_to_entry.clear()

        sections = self.help_spec.get("sections", {})

        for section_name, entries in sections.items():
            section_id = self.tree.insert(
                "",
                "end",
                text=section_name,
                values=("", "", "", "", ""),
                open=True,
            )

            for entry in entries:
                self._insert_entry(section_id, entry)

        self._update_changed_label()

    def _insert_entry(self, parent_id: str, entry: dict[str, Any]) -> None:
        aliases = entry.get("aliases", [])
        primary = entry.get("primary", "")
        takes_value = bool(entry.get("takes_value", False))
        value_hint = entry.get("value_hint") or ""
        choices = entry.get("choices")
        default = entry.get("default")

        description = entry.get("description", "")

        value = entry.get("value")

        option_text = ", ".join(aliases) if aliases else primary
        choices_text = ", ".join(choices) if choices else ""

        if takes_value:
            value_text = self._display_value(value)
            default_text = self._display_value(default)
            tags: tuple[str, ...] = ()
        else:
            value_text = "enabled" if value else ""
            default_text = ""
            tags = ("flag",)

        if self._is_changed(entry):
            tags = tuple(set(tags + ("changed",)))

        item_id = self.tree.insert(
            parent_id,
            "end",
            text=option_text,
            values=(
                value_text,
                default_text,
                value_hint,
                choices_text,
                description,
            ),
            tags=tags,
        )

        self._item_to_entry[item_id] = entry

    # ------------------------------------------------------------------
    # Editing
    # ------------------------------------------------------------------

    def _on_double_click(self, event: tk.Event) -> None:
        item_id = self.tree.identify_row(event.y)
        if not item_id:
            return

        if item_id in self._item_to_entry:
            self._edit_item(item_id)

    def _on_edit_selected(self, event: tk.Event | None = None) -> None:
        selected = self.tree.selection()
        if not selected:
            return

        item_id = selected[0]
        if item_id in self._item_to_entry:
            self._edit_item(item_id)

    def _edit_item(self, item_id: str) -> None:
        entry = self._item_to_entry[item_id]

        if not entry.get("takes_value", False):
            entry["value"] = not bool(entry.get("value", False))
            self._refresh_item(item_id, entry)
            self._update_changed_label()
            return

        choices = entry.get("choices")
        value_hint = entry.get("value_hint")
        if value_hint == '<filename>':
            initial_dir = Path(self.current_options.get("--model", ".")).parent
            filename =filedialog.askopenfilename(
                title="Select the model file",
                # initialdir=".",
                initialdir=initial_dir,
                filetypes=[
                    ("GGUF files", "*.gguf"),
                    ("Text files", "*.txt"),
                    ("All files", "*.*"),
                ]
            )
            if filename:
                entry["value"] = filename
                self._refresh_item(item_id, entry)
                self._update_changed_label()
        elif choices:
            self._open_choice_dialog(item_id, entry, choices)
        else:
            self._open_value_dialog(item_id, entry)

    def _open_value_dialog(self, item_id: str, entry: dict[str, Any]) -> None:
        primary = entry.get("primary", "")
        hint = entry.get("value_hint") or ""
        current = entry.get("value")

        prompt = f"{primary}"
        if hint:
            prompt += f" {hint}"

        # dialog = ctk.CTkInputDialog(
        #     text=f"{prompt}\n\nCurrent value: {current}",
        #     title="Edit benchmark option",
        #     font=self.font if self.font is not None else ctk.CTkFont(size=14)
        # )
        if primary != "--model":
            dialog = CTkGetText(
                parent=self,
                title="Edit benchmark option",
                message=f"{prompt}\n\nCurrent value: {current}",
                font=self.font if self.font is not None else ctk.CTkFont(size=14)
            )
        else:
            file_open_dlg = filedialog.askopenfilename(
                title="Select the model file",
                initialdir=Path(self.current_options.get("--model", ".")).parent,
                initialfile=Path(self.current_options.get("--model", ".")).name,
                filetypes=[
                    ("GGUF files", "*.gguf"),
                    ("All files", "*.*"),
                ]
            )
            if file_open_dlg:
                entry["value"] = file_open_dlg
                self._refresh_item(item_id, entry)
                self._update_changed_label()
            return

        # new_value = dialog.get_input()
        new_value = dialog.result

        if not new_value:
            return

        entry["value"] = new_value.strip()

        self._refresh_item(item_id, entry)
        self._update_changed_label()

    def _open_choice_dialog(self, item_id: str, entry: dict[str, Any], choices: list[str]) -> None:
        dialog = CTkOpenChoice(
            parent=self,
            item_id=item_id,
            entry=entry,
            choices=choices,
            font=self.font if self.font is not None else ctk.CTkFont(size=14)
        )
        if dialog.result:
            entry["value"] = dialog.result
            self._refresh_item(item_id, entry)
            self._update_changed_label()

    def _reset_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            return

        item_id = selected[0]
        entry = self._item_to_entry.get(item_id)
        if not entry:
            return

        if entry.get("takes_value", False):
            entry["value"] = entry.get("default")
        else:
            entry["value"] = False

        self._refresh_item(item_id, entry)
        self._update_changed_label()

    def _refresh_item(self, item_id: str, entry: dict[str, Any]) -> None:
        takes_value = bool(entry.get("takes_value", False))
        choices = entry.get("choices")
        value_hint = entry.get("value_hint") or ""

        if takes_value:
            value_text = self._display_value(entry.get("value"))
            default_text = self._display_value(entry.get("default"))
            tags: tuple[str, ...] = ()
        else:
            value_text = "enabled" if entry.get("value") else ""
            default_text = ""
            tags = ("flag",)

        if self._is_changed(entry):
            tags = tuple(set(tags + ("changed",)))

        self.tree.item(
            item_id,
            values=(
                value_text,
                default_text,
                value_hint,
                ", ".join(choices) if choices else "",
                entry.get("description", ""),
            ),
            tags=tags,
        )

    # ------------------------------------------------------------------
    # Result
    # ------------------------------------------------------------------

    def _on_ok_old(self) -> None:
        self.result = self.get_non_default_settings()
        self.result_ready = True
        self.destroy()

    def _on_ok(self) -> None:
        changed: dict[str, Any] = {}

        for section_entries in self.help_spec.get("sections", {}).values():
            for entry in section_entries:
                primary = entry.get("primary")
                if not primary:
                    continue

                value = entry.get("value")

                if entry.get("takes_value"):
                    default = entry.get("default")
                    if str(value) != str(default):
                        changed[primary] = value
                else:
                    if bool(value):
                        changed[primary] = True

        self.result = changed
        self.result_ready = True
        self.destroy()

    def _on_cancel(self) -> None:
        self.result = None
        self.result_ready = True
        self.destroy()

    def get_non_default_settings(self) -> dict[str, Any]:
        """
        Return only non-default settings.

        Uses primary option names:

            --output
            --n-gpu-layers
            --flash-attn

        Flags are returned as True only when enabled.
        """

        result: dict[str, Any] = {}

        sections = self.help_spec.get("sections", {})

        for entries in sections.values():
            for entry in entries:
                if not self._is_changed(entry):
                    continue

                primary = entry.get("primary")
                if not primary:
                    continue

                if entry.get("takes_value", False):
                    result[primary] = entry.get("value")
                else:
                    result[primary] = True

        return result

    def get_command_args(self) -> list[str]:
        """
        Return non-default settings as command-line arguments.

        Example:

            ["--output", "json", "--n-gpu-layers", "999", "--verbose"]
        """

        args: list[str] = []

        settings = self.get_non_default_settings()

        for option, value in settings.items():
            if value is True:
                args.append(option)
            else:
                args.extend([option, str(value)])

        return args

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _display_value(value: Any) -> str:
        if value is None:
            return ""

        return str(value)

    @staticmethod
    def _is_changed(entry: dict[str, Any]) -> bool:
        if entry.get("takes_value", False):
            return str(entry.get("value")) != str(entry.get("default"))

        return bool(entry.get("value", False))