# CTkAppWorkInstructions.py

import customtkinter as ctk # type: ignore

from localmind.widgets.ctk_markdown import CTkMarkdown


import tkinter as tk

import os
from pathlib import Path
from typing import List, Union, Tuple

from localmind.gui.CTkAppView import CTkAppView
from localmind.gui.CTkAppData import CTkAppData

class MarkdownViewerHistory_old:
    """  We keep the markdown text itself in the history"""
    def __init__(self) -> None:
        self.history: list[tuple[str, str]] = []      # Push path on forward navigation
        self.future: list[tuple[str, str]] = []       # Push path when going back
        self.current: tuple[str, str] | None = None

    def clear(self) -> None:
        self.history.clear()
        self.future.clear()
        self.current = None

    def visit(self, file_path: str, markdown_text: str):
        """Called when opening a new file directly or via a link."""
        normalized: tuple[str, str] = (str(Path(file_path).resolve()), markdown_text)
        if self.current and self.current != normalized:
            self.history.append(self.current)
            self.future.clear()  # Clear redo history on new branch navigation
        self.current = normalized

    def go_back(self) -> tuple[str,str] | None:
        if not self.history:
            return None
        if self.current is not None and isinstance(self.current, tuple):
            self.future.append(self.current)
            self.current = self.history.pop()
        return self.current

    def go_forward(self) -> tuple[str,str] | None:
        if not self.future:
            return None
        if self.current is not None and isinstance(self.current, tuple):
            self.history.append(self.current)
            self.current = self.future.pop()
        return self.current


HistoryItem = tuple[str, str, float]

class MarkdownViewerHistory:
    """Keep the Markdown text and scroll position in navigation history."""

    def __init__(self) -> None:
        self.history: list[HistoryItem] = []
        self.future: list[HistoryItem] = []
        self.current: HistoryItem | None = None

    def clear(self) -> None:
        self.history.clear()
        self.future.clear()
        self.current = None

    def save_current_position(self, scroll_position: float) -> None:
        """Update the scroll position stored for the current document."""

        if self.current is None:
            return

        file_path, markdown_text, _ = self.current
        self.current = (
            file_path,
            markdown_text,
            scroll_position,
        )

    def visit(
        self,
        file_path: str,
        markdown_text: str,
        scroll_position: float = 0.0,
    ) -> None:
        """Called when opening a new file directly or through a link."""

        normalized: HistoryItem = (
            str(Path(file_path).resolve()),
            markdown_text,
            scroll_position,
        )

        if self.current and self.current[:2] != normalized[:2]:
            self.history.append(self.current)
            self.future.clear()

        self.current = normalized

    def go_back(self) -> HistoryItem | None:
        if not self.history:
            return None

        if self.current is not None:
            self.future.append(self.current)
            self.current = self.history.pop()

        return self.current

    def go_forward(self) -> HistoryItem | None:
        if not self.future:
            return None

        if self.current is not None:
            self.history.append(self.current)
            self.current = self.future.pop()

        return self.current

class CTkAppWorkInstructions(CTkAppView):
    def __init__(self, parent: ctk.CTk, frame: ctk.CTkFrame, font: Union[ctk.CTkFont, Tuple[str, int, str]], data: CTkAppData) -> None:
        super().__init__(parent, frame, font, data)
        #self.home = os.path.dirname(os.path.abspath(__file__))
        self.home : Path = Path(__file__).resolve().parent
        self.text_box: CTkMarkdown
        self.history: MarkdownViewerHistory = MarkdownViewerHistory()
        self.markdown_text: str = ""
        self.filename: Path | None = self.data.last_instruction_file
        self.data.logger.debug(f"Last instruction file: {self.filename}")

        self.markdown_folder: Path | None = self.filename.parent if self.filename is not None else None
        self.cwd: Path = Path.cwd()
        self.initialize_widgets()
        # self.pdf_frame: CTkPDFViewerNavigate | None = None
        self.load_instruction_file()
 
    def load_instruction_file(self) -> None:
        """Load the instruction file specified by self.filename and display its content in the markdown viewer.
        If the file does not exist or is not specified, log an error and return.
        This function is called when a file is opened by the system or when the
        """
        # self.filename = self.data.last_instruction_file
        self.data.logger.debug(f"Loading instruction file: {self.filename}")

        if self.filename is None:
            self.data.logger.warning("No instruction file has been set.")
            return

        path = Path(self.filename).expanduser()

        if not path.exists():
            self.data.logger.error(f"Instruction file does not exist: {path}")
            return
        
        self.markdown_folder = path.parent
        os.chdir(self.markdown_folder)
        self.data.logger.debug(f"Loading instruction markdown: {path}")
        with open(path, 'r', encoding='utf-8') as f:
            self.markdown_text = f.read()  
        self.history.clear()
        self.history.visit(str(path), self.markdown_text) 
        self.text_box.set_markdown(self.markdown_text)
        os.chdir(self.cwd)
        self.update_buttons()

    def _display_history_item(
        self,
        item: HistoryItem | None,
    ) -> None:
        if item is None:
            return

        path_string, markdown_text, scroll_position = item
        path = Path(path_string).resolve()

        self.filename = path
        self.markdown_folder = path.parent
        self.markdown_text = markdown_text

        previous_cwd = Path.cwd()

        try:
            os.chdir(self.markdown_folder)
            self.text_box.set_markdown(markdown_text)
        finally:
            os.chdir(previous_cwd)

        # Let Tk finish inserting and laying out the Markdown before scrolling.
        self.text_box.after_idle(
            lambda position=scroll_position:
                self.text_box.yview_moveto(position)
        )

        self.update_buttons()

    def _display_history_item_old(
        self,
        item: tuple[str, str] | None,
    ) -> None:
        if item is None:
            return

        path_string, markdown_text = item
        path = Path(path_string).resolve()

        self.filename = path
        self.markdown_folder = path.parent
        self.markdown_text = markdown_text

        previous_cwd = Path.cwd()

        try:
            os.chdir(self.markdown_folder)
            self.text_box.set_markdown(markdown_text)
        finally:
            os.chdir(previous_cwd)

        self.update_buttons()

    def _save_current_scroll_position(self) -> None:
        """Save the current document's vertical scroll position."""

        if self.history.current is None:
            return

        if not self.text_box or not hasattr(self.text_box, 'yview') or self.text_box.yview() is None:
            return

        if not self.text_box or not hasattr(self.text_box, 'yview') or self.text_box.yview() is None:
            return  
        yyview = self.text_box.yview()    
        if isinstance(yyview, tuple) and len(yyview) >= 1:
            scroll_position = yyview[0]
            self.history.save_current_position(scroll_position)

    def navigation_callback(
        self,
        path: str,
    ) -> None:
        """Load a Markdown file selected through a local link."""

        if self.markdown_folder is None:
            return

        md_path = (self.markdown_folder / path).expanduser().resolve()

        if not md_path.is_file():
            self.data.logger.warning(
                f"Linked instruction file does not exist: {md_path}"
            )
            return

        try:
            markdown_text = md_path.read_text(encoding="utf-8")
        except OSError:
            self.data.logger.exception(
                f"Unable to read instruction markdown: {md_path}"
            )
            return

        # preserve the document we are leaving, including its scroll position
        self._save_current_scroll_position()

        # Store the new path with the new document text.
        self.history.visit(str(md_path), markdown_text, scroll_position=0.0)

        self._display_history_item(self.history.current)

    def _restore_history_item(
        self,
        item: tuple[str, str] | None,
    ) -> None:
        if item is None:
            return

        path_string, markdown_text = item
        path = Path(path_string)

        self.filename = path # str(path)
        self.markdown_folder = path.parent
        self.markdown_text = markdown_text

        self.text_box.set_markdown(markdown_text)
        self.update_buttons()

    def on_sidebar_first(self) -> None:
        """Move to the first document in navigation history."""

        if not self.history.history:
            return

        self.data.logger.debug(
            "Navigating to the first instruction in history."
        )

        while self.history.history:
            self.history.go_back()

        self._display_history_item(self.history.current)


    def on_sidebar_next(self) -> None:
        """Move forward through navigation history."""

        self.data.logger.debug(
            "Navigating to the next instruction in history."
        )

        self._save_current_scroll_position()
        self._display_history_item(self.history.go_forward())


    def on_sidebar_prior(self) -> None:
        """Move backward through navigation history."""

        self.data.logger.debug(
            "Navigating to the prior instruction in history."
        )

        self._save_current_scroll_position()
        self._display_history_item(self.history.go_back())


    def initialize_widgets(self) -> None:
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)

        self.message_label_frame = ctk.CTkFrame(self.frame, bg_color='transparent')
        self.message_label_frame.grid(row=0, column=0, padx=5, pady=(5,5), sticky='new')
        self.message_label_frame.grid_columnconfigure(0, weight=1)
        self.message_label_frame.grid_rowconfigure(0, weight=1)
        self.message_label = ctk.CTkLabel(self.message_label_frame, text="Instructions", font=self.font)
        self.message_label.grid(row=0, column=0, padx=5, pady=(5,5), sticky='ew')

       # Textbox Frame
        self.text_frame = ctk.CTkFrame(self.frame, bg_color='transparent')
        self.text_frame.grid(row=1, column=0, padx=5, pady=(5, 0), sticky='nsew')
        self.text_frame.grid_columnconfigure(0, weight=1)
        self.text_frame.grid_rowconfigure(0, weight=1)

        # self.text_box = ctk.CTkTextbox(self.text_frame, height=40, font=font)
        if isinstance(self.font, ctk.CTkFont):
            self.markdown_font = (self.font.cget('family'), self.font.cget('size'))
        else:
            self.markdown_font = (self.font[0], self.font[1])
        self.text_box = CTkMarkdown(self.text_frame, font=self.markdown_font, navigation_callback=self.navigation_callback)

        self.text_box.set_markdown(self.markdown_text)
        
        self.text_box.grid(row=0, column=0, padx=5, pady=(5,0), sticky='nsew')

        self.next_button: ctk.CTkButton | None = self.data.get_button('next')
        self.prior_button: ctk.CTkButton | None = self.data.get_button('prior')
        self.first_button: ctk.CTkButton | None = self.data.get_button('first')

        self.update_buttons()


    def update_buttons(self) -> None:
        if self.next_button is not None:
            self.next_button.configure(state='normal' if self.history.future else 'disabled')
            self.data.logger.debug(f"Next button state: {'normal' if self.history.future else 'disabled'}")
        if self.prior_button is not None:
            self.prior_button.configure(state='normal' if self.history.history else 'disabled')
            self.data.logger.debug(f"Prior button state: {'normal' if self.history.history else 'disabled'}")
        if self.first_button is not None:
            self.first_button.configure(state='normal' if self.history.history else 'disabled')
            self.data.logger.debug(f"First button state: {'normal' if self.history.history else 'disabled'}")

    def open_file(self, open_filename: str):
        self.data.logger.debug(f"Opening instruction file: {open_filename}")
        path = Path(open_filename).expanduser()

        if not path.exists():
            self.data.logger.error(f"Instruction file does not exist: {path}")
            return

        self.filename = path
        self.data.last_instruction_file = str(self.filename)
        self.load_instruction_file()
        
    def on_visible(self) -> None:
        """ change the text of the buttons we use to reflect the current view"""
        self.set_button_names({
            "import": "Open",
            "first": "Home",
            "next": "Next",
            "prior": "Back"
        })

        self.update_buttons()

    def on_close_tab(self) -> None:
        pass

    def sb_button_list(self) -> List[str]: 
        """Return a list of button names that this view uses in the sidebar."""
        return [ 'import', 'first', 'next', 'prior' ]

    def on_sidebar_import(self):
        self.filename = Path(ctk.filedialog.askopenfilename())
        self.open_file(str(self.filename))
        #pass

    @property 
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        if not isinstance(value, CTkAppData):
            raise TypeError("Data type error, expecting CTkAppData")
        self._data = value
 

    def on_sidebar_last(self) -> None:
        """ 
            Activate the on_sidebar_end function in the active view
        """
        pass

    def on_sidebar_new(self):
        """ 
            Activate the on_sidebar_new function in the active view
        """
        pass

    
    def on_sidebar_edit(self):
        """ 
            Activate the on_sidebar_edit function in the active view
        """
        pass

    
    def on_sidebar_add(self):
        """ 
            Activate the on_sidebar_add function in the active view
        """
        pass

    
    def on_sidebar_update(self):
        """ 
            Activate the on_sidebar_update function in the active view
        """
        pass

    
    def on_sidebar_remove(self):
        """ 
            Activate the on_sidebar_remove function in the active view
        """
        pass
