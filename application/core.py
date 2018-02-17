"""Application wrapper for async2rewrite."""
import async2rewrite
import tkinter as tk
from tkinter import messagebox, filedialog
from pathlib import Path
import webbrowser
from pygments import lex
from pygments.lexers.python import Python3Lexer


def get_window_info(window, *, main_menu=False, custom_wh=None):
    """Fetches the center of the screen (according to x and y)."""
    w = 850
    h = 350
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    if main_menu:
        return '{}x{}+{}+{}'.format(w, h, int(x), int(y))
    if custom_wh:
        return '{}x{}+{}+{}'.format(custom_wh[0], custom_wh[1], int(x), int(y))
    return '+{}+{}'.format(int(x), int(y))


class Application(tk.Tk):
    """Base of the application."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initial window features
        self.geometry(get_window_info(self, main_menu=True))
        self.iconbitmap('a2r.ico')

        # Wrapper for frames
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

        # Basic declarations
        self.parent = parent
        self.controller = controller

        # Label
        a2r_img = tk.PhotoImage(file='../logo.png')
        label = tk.Label(self, image=a2r_img)
        label.image = a2r_img
        label.grid(row=1, column=1, sticky="we")

        # Menu buttons

        snippet = tk.Button(self, text="Convert Snippet", command=lambda: Snippet(self.parent))
        snippet.grid(row=2, column=1, sticky="we")

        file = tk.Button(self, text="Convert File", command=self.file)
        file.grid(row=3, column=1, sticky="we")

        notices = tk.Button(self, text="Credits", command=lambda: Notices(self.parent))
        notices.grid(row=4, column=1, sticky="we")

        # Configure grid geometry
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def file(self):
        """Converts a file from async to rewrite."""
        name = filedialog.askopenfilename(initialdir=".", title="Select a file",
                                          filetypes=(("Python Files", "*.py"),))  # Asks for original file
        save = filedialog.asksaveasfilename(initialdir=".", title="Save file as",
                                            filetypes=(("Python Files", "*.py"),))  # Asks where to save the file

        try:
            file_result = async2rewrite.from_file(name)  # Converts code from original file to rewrite
            with open(save, 'w') as f:
                f.write(file_result.replace('\t', '    '))
        except Exception as e:

            # Check if it's to do with file/directory not being found
            if 'No such file or directory' in str(e):
                messagebox.showerror('File Not Found', 'You did not choose a file to convert/save the conversion.')
            else:
                messagebox.showerror(type(e).__name__, str(e).replace('<unknown>', Path(name).name))
        else:
            save = Path(save).parent

            # Copy save url to clipboard
            self.controller.clipboard_clear()
            self.controller.clipboard_append(save)
            self.controller.update()

            messagebox.showinfo('Success!', 'The conversion was successful. Your converted file is in "{}"'.format(save)
                                            + '(Copied to clipboard).')


class Notices(tk.Toplevel):
    """Shows relevant notices."""

    GITHUB = 'https://github.com/TheTrain2000/async2rewrite'

    def __init__(self, master):
        super().__init__(master)

        # Initialize window features
        self.title("Credits")
        self.geometry(get_window_info(master))
        self.iconbitmap('a2r.ico')

        # Make list of phrases for notice
        notice = ["async2rewrite does not complete 100% of the necessary conversions.\n",
                  "It is a tool designed to minimize the amount of tedious work required.\n",
                  "async2rewrite will warn upon changes that it cannot make itself.\n",
                  "Make sure to read the migration documentation for rewrite when using this tool.\n\n",
                  "Library made by: TheTrain2000 (Tyler) with the aid of nitros12 (Pantsu).\n",
                  "Logo idea by: ReinaSakuraba.\n",
                  "Application by: NCPlayz (Nadir)."]

        # Show the notice on the Toplevel
        credit_lbl = tk.Label(self, text=' '.join(notice))
        credit_lbl.pack()

        # Menu buttons

        github = tk.Button(self, text='Open Github', command=lambda: webbrowser.open(self.GITHUB))
        github.pack()

        close = tk.Button(self, text='Close', command=self.destroy)
        close.pack()


class Snippet(tk.Toplevel):
    """Conversion of snippet of codes."""

    def __init__(self, master):
        super().__init__(master)

        # Initialize window features
        self.title("Convert a Snippet")
        self.geometry(get_window_info(master, custom_wh=[752, 440]))
        self.iconbitmap('a2r.ico')

        # Custom text with syntax highlighting
        self.input_text = SyntaxText(self)
        self.input_text.grid(sticky="we")

        # Menu buttons

        self.convert_btn = tk.Button(self, text="Convert to Rewrite", command=self.convert)
        self.convert_btn.grid(row=1, column=1, sticky="we")

        self.close_btn = tk.Button(self, text="Close", command=self.destroy)
        self.close_btn.grid(row=2, column=1, sticky="we")

    def convert(self):
        """Converts the input text to rewrite."""
        try:
            conversion = async2rewrite.from_text(self.input_text.get(1.0, tk.END).replace('\t', '    '))
        except Exception as e:
            if e:
                text = "\n\n#-- {}: \n# {}".format(type(e).__name__,
                                                   str(e).replace('<unknown>', '<async2rewrite converter>'))
                self.input_text.insert(tk.END, text)
        else:
            self.input_text.insert(tk.END, "\n\n#-- Rewrite Conversion:\n\n{}".format(conversion))
            self.input_text.highlight()


class SyntaxText(tk.Text):
    """Custom Text with syntax highlighting."""
    def __init__(self, master):
        super().__init__(master)

        # Configure tags for syntax highlighting
        self.tag_configure("Token.Comment.Single", foreground="red")
        self.tag_configure("Token.Keyword", foreground="orange")
        self.tag_configure("Token.Keyword.Constant", foreground="orange")
        self.tag_configure("Token.Keyword.Namespace", foreground="orange")
        self.tag_configure("Token.Literal.String.Affix", foreground="green")
        self.tag_configure("Token.Literal.String.Double", foreground="green")
        self.tag_configure("Token.Literal.String.Doc", foreground="green")
        self.tag_configure("Token.Literal.String.Single", foreground="green")
        self.tag_configure("Token.Name.Builtin", foreground="purple")
        self.tag_configure("Token.Name.Class", foreground="blue")
        self.tag_configure("Token.Name.Exception", foreground="purple")
        self.tag_configure("Token.Name.Function", foreground="blue")
        self.tag_configure("Token.Operator.Word", foreground="green")

        # Override events
        self.bind('<Tab>', self.replace_tabs)
        self.bind('<KeyRelease>', self.highlight)

    def highlight(self, event=None):
        """Does syntax highlighting."""
        data = self.get("1.0", "end-1c")
        if data != '':
            # Add tags
            self.mark_set("range_start", "1.0")

            # Run lexer for syntax highlighter
            for token, content in lex(data, Python3Lexer()):
                self.mark_set("range_end", "range_start + {}c".format(len(content)))
                self.tag_add(str(token), "range_start", "range_end")
                self.mark_set("range_start", "range_end")
            del event
        else:
            return

    def replace_tabs(self, event=None):
        """Replace tabs with spaces."""
        self.insert(tk.INSERT, "    ")
        del event
        return 'break'


if __name__ == '__main__':
    Application().mainloop()
