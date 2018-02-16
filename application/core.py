"""Application wrapper for async2rewrite."""
import async2rewrite
import tkinter as tk
from tkinter import messagebox, filedialog
from pathlib import Path
import webbrowser


def get_window_info(window, *, main_menu=False):
    """Fetches the center of the screen (according to x and y)."""
    w = 250
    h = 100
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    if main_menu:
        return '{}x{}+{}+{}'.format(w, h, int(x), int(y))
    return '+{}+{}'.format(int(x), int(y))


class Application(tk.Tk):
    """Base of the application."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry(get_window_info(self, main_menu=True))
        container = tk.Frame(self)
        container.pack()
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (MainMenu,):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")
        self.title("async2rewrite")

    def show_frame(self, page_name):
        """Show a frame for the given page name."""
        frame = self.frames[page_name]
        frame.tkraise()


class MainMenu(tk.Frame):
    """Main menu of the application."""
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.parent = parent
        self.controller = controller

        snippet = tk.Button(self, text="Convert Snippet", command=lambda: Snippet(self.parent))
        snippet.grid(row=1, column=1, sticky="we")
        file = tk.Button(self, text="Convert File", command=self.file)
        file.grid(row=2, column=1, sticky="we")
        notices = tk.Button(self, text="Credits", command=lambda: Notices(self.parent))
        notices.grid(row=3, column=1, sticky="we")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def file(self):
        """Converts a file from async to rewrite."""
        name = filedialog.askopenfilename(initialdir=".", title="Select a file",
                                          filetypes=(("Python Files", "*.py"),))  # asks for original file
        save = filedialog.asksaveasfilename(initialdir=".", title="Save file as",
                                            filetypes=(("Python Files", "*.py"),))  # asks where to save the file

        try:
            file_result = async2rewrite.from_file(name)  # converts code from original file to rewrite
            with open(save, 'w') as f:
                f.write(file_result.replace('\t', '    '))
        except Exception as e:
            if 'No such file or directory' in str(e):
                messagebox.showerror('File Not Found', 'You did not choose a file to convert/save the conversion.')
            else:
                messagebox.showerror(type(e).__name__, str(e).replace('<unknown>', Path(name).name))
        else:
            save = Path(save).parent
            self.controller.clipboard_clear()
            self.controller.clipboard_append(save)
            self.controller.update()
            messagebox.showinfo('Success!', f'The conversion was successful. Your converted file is in "{save}" '
                                            f'(Copied to clipboard).')


class Notices(tk.Toplevel):
    """Shows relevant notices."""
    def __init__(self, master):
        super().__init__(master)

        self._master = master
        self.title("Credits")
        self.geometry(get_window_info(master))

        notice = ["async2rewrite does not complete 100% of the necessary conversions.\n",
                  "It is a tool designed to minimize the amount of tedious work required.\n",
                  "async2rewrite will warn upon changes that it cannot make itself.\n",
                  "Make sure to read the migration documentation for rewrite when using this tool.\n\n",
                  "Library made by: TheTrain2000 (Tyler) with the aid of nitros12 (Pantsu).\n",
                  "Logo idea by: ReinaSakuraba.\n",
                  "Application by: NCPlayz (Nadir)."]

        credit_lbl = tk.Label(self, text=' '.join(notice))
        credit_lbl.pack()

        github = tk.Button(self, text='Open Github', command=lambda: webbrowser.open('https://github.com/TheTrain2000/'
                                                                                     'async2rewrite'))
        github.pack()
        close = tk.Button(self, text='Close', command=self.destroy)
        close.pack()


class Snippet(tk.Toplevel):
    """Conversion of snippet of codes."""
    def __init__(self, master):
        super().__init__(master)
        self._master = master
        self.title("Convert a Snippet")
        self.geometry(get_window_info(master))

        self.input_text = tk.Text(self)
        self.input_text.grid(sticky="we")
        self.input_text.bind('<Tab>', self.replace_tabs)
        # TODO: syntax highlighting

        self.convert_btn = tk.Button(self, text="Convert to Rewrite", command=self.convert)
        self.convert_btn.grid(row=1, column=1, )
        self.convert_btn = tk.Button(self, text="Close", command=self.destroy)
        self.convert_btn.grid(row=2, column=1)

    def convert(self):
        """Converts the input text to rewrite."""
        try:
            conversion = async2rewrite.from_text(self.input_text.get(1.0, tk.END).replace('\t', '    '))
        except Exception as e:
            if e:
                text = f"\n\n# {type(e).__name__}: \n# {str(e).replace('<unknown>', '<async2rewrite converter>')}"
                self.input_text.insert(tk.END, text)
        else:
            self.input_text.insert(tk.END, f"\n\n# Conversion\n\n{conversion}")

    def replace_tabs(self, event=None):
        self.input_text.insert(tk.INSERT, "    ")
        del event
        return 'break'


if __name__ == '__main__':
    Application().mainloop()
